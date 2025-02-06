from django.contrib import admin
from django.urls import include, path
from juegos.views import inicio, userprofile, change_password, edit_user, RegistroView, NuevaPartidaView, NuevoJuegoView, NuevoLocalView, partidas, InscripcionView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', inicio, name ='inicio'),
    path('nueva_jornada', NuevaPartidaView.as_view(), name ='nueva_jornada'),
    path('nuevo_juego', NuevoJuegoView.as_view(), name = 'nuevo_juego'),
    path('nuevo_local', NuevoLocalView.as_view(), name= 'nuevo_local'),
    path('partidas', partidas, name='ver_partidas_reservadas'),
    path('partidas/<id>/inscribir/', InscripcionView.as_view(), name= 'inscribir'),
    path('accounts/userprofile', userprofile, name = 'userprofile'),
    path('accounts/change-pass', change_password, name='change-password'),
    path('edit-user/', edit_user, name= 'edit_user'),
    path('accounts/registro', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name= 'login_url'),
    path('logout/', LogoutView.as_view(next_page= 'login_url'), name= 'logout')   
]