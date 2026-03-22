import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from .models import ChatMessage   

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        path = self.scope['path']
        if 'general' in path:
            self.room_group_name = 'global'
        elif 'partida' in path:
            id = self.scope['url_route']['kwargs']['partida_id']
            self.room_group_name = f'partida_{id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        #Aceptar la conexión del Websocket
        await self.accept()
        
        if self.scope["user"].is_authenticated:
            cache_key = f"online_user_{self.scope['user'].id}"
            from asgiref.sync import sync_to_async
            await sync_to_async(cache.set)(cache_key, True, 300)
        
        await self.enviar_conteo_usuarios()
        
    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            cache_key = f"online_user_{user.id}"
            from asgiref.sync import sync_to_async
            await sync_to_async(cache.delete)(cache_key)
            
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        await self.enviar_conteo_usuarios()
        
    #Recibe el mensaje desde el navegador (Front)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]
        
        utc_now = timezone.now()
        hora_local = timezone.localtime(utc_now)
        ahora = hora_local.strftime('%d/%m %H:%M')
        
        #Guardar mensaje en bd relacional
        if user.is_authenticated:
            await self.save_message(user, message, self.room_group_name, ahora)
            username = user.username
        else:
            username = 'Anónimo'
        
        #Enviar el mensaje al grupo en redis
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': username,
                'datetime': ahora
            }
        )
        
    @database_sync_to_async
    def save_message(self, user, message, room, ahora):
        return ChatMessage.objects.create(
            user=user,
            content=message,
            room_name=room,
            timestamp= ahora
        )
        
    #REcibe el mensaje desde Redis y lo mada al navegador
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        
        #Mandar el mensaje al webscoket del cliente
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'datetime': event['datetime']
        }))
        
    async def enviar_conteo_usuarios(self):
        from asgiref.sync import sync_to_async
        conteo = await sync_to_async(lambda: len(cache.keys("online_user_*"))) ()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_count_update',
                'count': conteo
            }
        )
        
    async def user_count_update(self, event):
        count = event['count']
        await self.send(text_data=json.dumps({
            'type': 'user_count',
            'count': count
        }))