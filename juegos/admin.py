from django.contrib import admin
from juegos.models import UserProfile, Juego, Resultado, Partida, PartidaJugador, Post, Comentario

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    pass

class JuegoAdmin(admin.ModelAdmin):
    pass

class ResultadoAdmin(admin.ModelAdmin):
    pass

class PartidaAdmin(admin.ModelAdmin):
    pass

class PartidaJugadorAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class ComentarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Juego, JuegoAdmin)
admin.site.register(Resultado, ResultadoAdmin)
admin.site.register(PartidaJugador, PartidaJugadorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario, ComentarioAdmin)

