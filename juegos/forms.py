from django import forms
from django.forms import ModelForm
from juegos.models import Partida, Juego, Local, PartidaJugador, JuegoImagen, UserProfile, Resultado, User, Post, Comentario
from datetime import date, time, datetime, timedelta

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nombre', 'apellido', 'alias', 'rol', 'avatar']
        
        widgets= {
            
    'nombre': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),
    'apellido': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),
    'alias': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),
    'rol': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),
    'avatar': forms.ClearableFileInput(
        attrs= {
            'class': 'form-control'
        }
    )
}


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
                    'class': 'form-select'
                }
            )
        }
        

        
class JuegoModelForm(ModelForm):
    class Meta:
        model= Juego
        fields = ['nombre', 'descripcion', 'minimo_jugadores', 'maximo_jugadores', 'logo']
        
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
            ),
            'logo': forms.ClearableFileInput(
                attrs= {
                    'class': 'form-control'
                }
            )
        }
        
class JuegoImagenForm(ModelForm):
    class Meta:
        model = JuegoImagen
        fields = ['imagen']
        
class JuegoImagenMultipleForm(ModelForm):
    imagen = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        )
    )
    class Meta:
        model = JuegoImagen
        fields = ['imagen']

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
        
class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categoria']
        
        widgets= {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            
            'contenido': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            
            'categoria': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            )
                }
        
class ComentarioModelForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['mensaje']
        
        widgets= {
        'mensaje': forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )     
            }  
# class ResultadoModelForm(ModelForm):
#     class Meta:
#         model = Resultado
#         fields = ['ganador']
        
#     def __init__(self, *args, partida=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         if partida  :
#             self.fields['ganador'].queryset = User.objects.filter(jugadores_partida__partida = partida)
