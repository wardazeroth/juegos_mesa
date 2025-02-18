from django.db import models
from django.contrib.auth.models import User
import requests

# Create your models here.

class UserProfile(models.Model):
    roles =(('jugador', 'Jugador'), ('anfitrion', 'Anfitrión'), ('admin', 'Admin'))
    user = models.OneToOneField(User, related_name = 'usuario', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length= 45)
    alias = models.CharField(max_length=45)
    puntos = models.IntegerField(null=True, blank=True)
    deuda = models.IntegerField(null=True, blank=True)
    rol = models.CharField(max_length=255, choices=roles, default = 'anfitrion')
    avatar = models.ImageField(null=True, upload_to='juegos/')
    
    def get_extra_attributes(self):
        """Devuelve atributos extra basados en el rol del usuario"""
        if self.rol == 'jugador':
            return {'puntos': self.puntos, 'deuda': self.deuda}
        else:
            return {'nombre': self.nombre, 'apellido': self.apellido}

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
    
class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique= True)
    descripcion = models.TextField()
    minimo_jugadores = models.IntegerField()
    maximo_jugadores = models.IntegerField()
    logo = models.ImageField(blank=True, null=True, upload_to='juegos/')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nombre'], name='unique_nombre')
        ]
    
    def __str__(self):
        return f'{self.nombre}'
    
class JuegoImagen(models.Model):
    juego= models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)
    
    def __str__(self):
        return f"Imagen de {self.juego.nombre}"
    
class Resultado(models.Model):
    puntos_ganador = models.IntegerField()
    jugador = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name='resultados')
    def save(self, *args, **kwargs):
        """Sobreescribir el método save para asegurarse de que solo se puede agregar un jugador con rol 'jugador'"""
        if self.jugador.rol != 'jugador':
            raise ValueError("El usuario debe tener el rol 'jugador'")
        super().save(*args, **kwargs)
        
class Local(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank= True, null=True)
    def __str__(self):
        return f'{self.nombre}'
    
    def guardar_coordenadas(self, *args, **kwargs):
        if not self.latitud or not self.longitud:
            self.obtener_coordenadas()
        super().save(*args, **kwargs)
    
    def obtener_coordenadas(self):
        url = f'https://nominatim.openstreetmap.org/search?q={self.ubicacion}&format=json'
        headers = {"User-Agent": "MiApp/1.0 (guardaajavier@gmail.com)"} 
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                    data = response.json()
                    print(f"Datos obtenidos de la API: {data}") 
            if data:
                print(f"Coordenadas encontradas: {data[0]['lat']}, {data[0]['lon']}")
                self.latitud = float(data[0]['lat'])
                self.longitud = float(data[0]['lon'])
            else:
                print("No se encontraron coordenadas para esta dirección.")
        except requests.exceptions.RequestException as e:
            print(f"Error en la API: {e}")
            
    def calcular_ruta(self, user, perfil= 'driving'):
        lat1 = self.latitud
        lon1 = self.longitud
        
        
        url= f'http://router.project-osrm.org/route/v1/{perfil}/{lat1}, {lon1}; {lat2}, {lon2}?overview=false'
        response = requests.get(url)
        data = response.json()
        return data

class LocalImagen(models.Model):
    local= models.ForeignKey(Local, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)
    
    def __str__(self):
        return f"Imagen de {self.local.nombre}"

class Partida(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='partidas')
    juego= models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='partidas')
    resultado= models.ForeignKey(Resultado, on_delete=models.RESTRICT, related_name='partidas', null =True, blank=True)
    
class PartidaJugador(models.Model):
    partida= models.ForeignKey(Partida, on_delete=models.CASCADE, related_name= 'jugadores_partida')
    jugador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partidas_jugador')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['partida', 'jugador'], name='unique_partida_jugador')
        ]
    # def save(self, *args, **kwargs):
    #     """Sobreescribir el método save para asegurarse de que solo se puede agregar un jugador con rol 'jugador'"""
    #     if self.jugador.rol != 'jugador':
    #         raise ValueError("El usuario debe tener el rol 'jugador'")
    #     super().save(*args, **kwargs)



    