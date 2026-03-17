import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer


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
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    #Recibe el mensaje desde el navegador (Front)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"].get_username() if self.scope["user"].is_authenticated else "Anónimo"
        
        utc_now = timezone.now()
        hora_local = timezone.localtime(utc_now)
        ahora = hora_local.strftime('%d/%m %H:%M')
        
        #Enviar el mensaje al grupo en redis
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'datetime': ahora
            }
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
        