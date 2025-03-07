from django.contrib import admin
from django.urls import include, path
from juegos.views import inicio, userprofile, change_password, edit_user, RegistroView, NuevaPartidaView, NuevoJuegoView, NuevoLocalView, partidas, InscripcionView, desinscripcion, ver_games, detalleJuego, edit_game, eliminar_game, ver_locales, edit_local, eliminar_local, detalleLocal, historial, detalles_partida, detalles_historial, ResultadosView, CrearPostView, foro, detalle_post
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', inicio, name ='inicio'),
    path('nueva_jornada', NuevaPartidaView.as_view(), name ='nueva_jornada'),
    path('juegos/nuevo_juego', NuevoJuegoView.as_view(), name = 'nuevo_juego'),
    path('locales/nuevo_local', NuevoLocalView.as_view(), name= 'nuevo_local'),
    path('locales/ver_locales', ver_locales, name= 'ver_locales'),
    path('locales/<int:id>/', detalleLocal, name='detalle_local'),
    path('locales/editar_local/<int:id>/', edit_local, name='editar_local'),
    path('locales/eliminar_local/<int:id>/', eliminar_local, name='eliminar_local'),
    path('partidas', partidas, name='ver_partidas_reservadas'),
    path('partidas/<int:id>/detalles/', detalles_partida, name= 'detalles_partida'),
    path('partidas/<id>/inscribir/', InscripcionView.as_view(), name= 'inscribir'),
    path('partidas/<id>/desinscribir', desinscripcion, name='desinscribir'),
    path('partidas/<int:id>/editar_resultados', ResultadosView.as_view(), name= 'editar_resultados'),
    path('juegos/ver_juegos', ver_games, name= 'ver_juegos'),
    path('juegos/editar_juego/<int:id>/', edit_game, name='editar_juego'),
    path('juegos/eliminar_juego/<int:id>/', eliminar_game, name='eliminar_juego'),
    path('juegos/<int:id>/', detalleJuego, name='detalle_juego'),
    path('accounts/userprofile', userprofile, name = 'userprofile'),
    path('accounts/historial', historial, name= 'historial'),
    path('accounts/historial/<id>/detalles', detalles_historial, name='detalles_historial'),
    path('accounts/change-pass', change_password, name='change-password'),
    path('foro', foro, name='foro'),
    path('foro/nuevo_post', CrearPostView.as_view(), name= 'crear_post'),
    path('foro/<int:id>/detalle_post', detalle_post, name= 'detalle_post'),
    path('edit-user/', edit_user, name= 'edit_user'),
    path('accounts/registro', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name= 'login_url'),
    path('logout/', LogoutView.as_view(next_page= 'login_url'), name= 'logout')   
]

