import json
import requests


class BuscarCoordenadas:
    def __init__(self, ubicacion: str):
        self.ubicacion = ubicacion
        self.data = self.obtenerCoordenadas()
        
    def obtenerCoordenadas(self):
        url = f'https://nominatim.openstreetmap.org/search?q={self.ubicacion}&format=json'
        headers = {"User-Agent": "MiApp/1.0 (guardaajavier@gmail.com)"} 
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    
punto_frick = BuscarCoordenadas('Arauco 585')
print(punto_frick.data[0]['lat'], punto_frick.data[0]['lon'])



# lugar = Local.objects.create(nombre='Cosas', ubicacion='Picarte 4000, Valdivia')
# print(lugar.latitud, lugar.longitud)