from django import forms
from django.forms import ModelForm
from juegos.models import Partida, Juego, Local, PartidaJugador
from datetime import date, time, datetime, timedelta

# @staticmethod
# def generar_opciones_horas():
#     return [
#         ('15:00', '15:00 PM'),
#         ('16:00', '16:00 PM'),
#         ('17:00', '17:00 PM'),
#         ('18:00', '18:00 PM'),
#         ('19:00', '19:00 PM'),
#         ('20:00', '20:00 PM'),
#         ('21:00', '21:00 PM'),
#     ]
        
class PartidaModelForm(ModelForm):
    hora_inicio = time(9,0)
    hora_fin = time(21, 0)
    
    class Meta:
        model = Partida
        fields = ['fecha', 'hora', 'local', 'juego']
        
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': date.today().isoformat()  # Establece la fecha mínima como la de hoy
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'min': '15:00',
                    'max': '21:00',
                }),
            # 'hora': forms.Select(choices=generar_opciones_horas())
            # ,
            'local': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'juego': forms.Select(
                attrs={
                    'class': 'forms-select'
                }
            )
        }
        

        
class JuegoModelForm(ModelForm):
    class Meta:
        model= Juego
        fields = ['nombre', 'descripcion', 'minimo_jugadores', 'maximo_jugadores']
        
        widgets= {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'minimo_jugadores': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'maximo_jugadores': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class LocalModelForm(ModelForm):
    class Meta:
        model= Local
        fields = ['nombre', 'ubicacion']
        
        widgets= {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'ubicacion': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

