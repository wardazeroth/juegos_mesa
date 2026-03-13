from django import forms
from django.forms import ModelForm
from juegos.models import Partida, Juego, Local, PartidaJugador, JuegoImagen, UserProfile, Resultado, User, Post, Comentario, ComentarioImagen, PostImagen
from datetime import date, time, datetime, timedelta

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

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
        
class JuegoImagenMultipleForm(forms.ModelForm):
    imagen = forms.ImageField(
        widget=MultiFileInput(attrs={'multiple': True})
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
                    'class': 'form-control textarea-post'
                }
            ),
            
            'contenido': forms.Textarea(
                attrs={
                    'class': 'form-control textarea-post',
                    'rows': 6,
                    'placeholder': 'Escribe el contenido de tu post aquí...',
                }
            ),
            
            'categoria': forms.Select(
                attrs={
                    'class': 'form-select',
                    'style': 'background-color: #454e75; color: #FFFFFF'
                }
            ),
    }
        
class ComentarioModelForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['mensaje']
        
        widgets= {
            
        'mensaje': forms.Textarea(
            attrs={
                'class': 'form-control textarea-com',
                'rows': 6,
                'placeholder': 'Escribe el contenido de tu comentario aquí...'
                
            }
        ),     
        
        'imagenes': forms.Select(
            attrs={
                'class': 'form-select', 
                'id': 'imagenes',
            }
        )
    }
        
        def clean_post_cita(self):
            post_cita = self.cleaned_data.get('post_cita')
            if post_cita == '':
                post_cita = None
            return post_cita
        
        def clean_comentario_cita(self):
            comentario_cita = self.cleaned_data.get('comentario_cita')
            if comentario_cita == '':
                comentario_cita =  None
            return comentario_cita

class ComentarioImagenForm(ModelForm):
    class Meta:
        model = ComentarioImagen
        fields = ['imagen']
        
        widgets = {
        'imagen': forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'imagen'
            }
        )
    }
        

        