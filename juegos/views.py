from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from juegos.forms import PartidaModelForm, JuegoModelForm, LocalModelForm, JuegoImagenForm, JuegoImagenMultipleForm, UserProfileForm, PostModelForm, ComentarioModelForm
from django.views import View
from juegos.models import UserProfile, Partida, PartidaJugador, JuegoImagen, Juego, Local, LocalImagen, Resultado, Post, Comentario, Categoria, Like
from datetime import timedelta, date, datetime
from django.db.models import Q

# Create your views here.


def inicio(req):
    partidas = Partida.objects.all()
    week_day = get_weeks_days()
    hoy = date.today()
    ahora = datetime.now().time()
    ahora_mas_una = (datetime.combine(datetime.today(), ahora) + timedelta(hours=1)).time()


    
    partida_lunes = Partida.objects.filter(fecha = week_day[0]).order_by('hora')
    partida_martes = Partida.objects.filter(fecha = week_day[1]).order_by('hora')
    partida_miercoles = Partida.objects.filter(fecha = week_day[2]).order_by('hora')
    partida_jueves = Partida.objects.filter(fecha = week_day[3]).order_by('hora')
    partida_viernes = Partida.objects.filter(fecha = week_day[4]).order_by('hora')
    partida_sabado = Partida.objects.filter(fecha = week_day[5]).order_by('hora')
    partida_domingo = Partida.objects.filter(fecha = week_day[6]).order_by('hora')
    
    context = {
        'partidas': partidas,
        'partida_lunes': partida_lunes,
        'partida_martes': partida_martes,
        'partida_miercoles': partida_miercoles,
        'partida_jueves': partida_jueves,
        'partida_viernes': partida_viernes,
        'partida_sabado': partida_sabado,
        'partida_domingo': partida_domingo,
        'week_day': week_day,
        'hoy': hoy,
        'ahora_mas_una': ahora
        
    }
    return render(req, 'index.html', context)

def get_weeks_days():
    today = date.today()
    days = []
    weekday = today.weekday()
    first_date = today - timedelta(days = weekday)
    for i in range(7):
        days.append(first_date + timedelta(days=i))

    return days


def userprofile (req):
    return render (req, 'userprofile.html')

def change_password (req): 
    #1. Recibo los datos del formulario
    password = req.POST['password']
    pass_repeat = req.POST['pass_repeat']
    if password != pass_repeat:
        messages.error(req, 'Las contraseñas no coinciden')
        return
    else:
    #3. Actualizamos la contraseña
        req.user.set_password(password)
        req.user.save()
        #4. Le avisamos al usuario que el cambio fue exitoso
        messages.success(req, 'Contraseña actualizada')
    return redirect('/accounts/userprofile')

@login_required
def edit_user(req):

    #1.obtengo el usuario actual
    
    current_user = req.user
    username = current_user.username
    
    #2. Modifico los atributos del user
    user = User.objects.get(username=username)
    email = req.POST['email']
    first_name = req.POST['first_name']
    last_name = req.POST['last_name']
    alias = req.POST['alias']
    rol = req.POST['rol']
    avatar = req.FILES.get('avatar')

    user = current_user
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    
    try: 
        profile = UserProfile.objects.get(user=user)
        profile.nombre = first_name
        profile.apellido = last_name
        profile.alias = alias
        profile.rol = rol
        if avatar:
            profile.avatar = avatar
        profile.save()
        
    except:
        UserProfile.objects.create(
            user = user,
            nombre = first_name,
            apellido = last_name,
            alias = alias,
            rol = rol,
            avatar = avatar
        )
    messages.success(req, '¡Ha actualizado sus datos con éxito!')
    return redirect('/')

def historial(req):
    current_user = req.user
    user_id = current_user.id
    partida_jugador = PartidaJugador.objects.filter(jugador_id=user_id)
    today = date.today()
    ahora = datetime.now().time()

    partidas = Partida.objects.filter(
        Q(fecha = today, hora__gt = ahora) | Q(fecha__gt = today),
        jugadores_partida__jugador_id = user_id
    )
    
    partidas_anteriores = Partida.objects.filter(
        Q(fecha = today, hora__lt = ahora) | Q(fecha__lt = today),
        jugadores_partida__jugador_id = user_id
    ).order_by('-fecha')
    
    partidas_anteriores_todas = Partida.objects.filter(
        Q(fecha = today, hora__lt = ahora) | Q(fecha__lt = today)
    ).order_by('-fecha')
    
    print(today)

    context = {
        'partida_jugador': partida_jugador,
        'partidas': partidas,
        'partidas_anteriores': partidas_anteriores,
        'partidas_anteriores_todas': partidas_anteriores_todas
    }
    
    return render(req, 'historial.html', context)

def detalles_historial(req, id):
    detalles_partida = Partida.objects.get(id=id)
    detalles_partida_jugador = PartidaJugador.objects.filter(partida_id = id).order_by('-puntaje')
    
    context = {
        'detalles_partida': detalles_partida,
        'detalles_partida_jugador': detalles_partida_jugador
    }
    
    return render(req, 'detalles_historial.html', context)

def ver_games(req):
    juegos = Juego.objects.all()
    context = {
        'juegos': juegos
    }
    
    return render(req, 'ver_juegos.html', context)

def detalleJuego(req, id):
    juego = Juego.objects.get(id=id)
    context = {
        'juego': juego
    }
    return render (req, 'detalle.html', context)

def edit_game(req, id):
    if req.method == 'GET':
        juego = Juego.objects.get(id=id)
        context = {
            'juego': juego
        }
        return render(req, 'editar_juego.html', context)
    else:
        juego_id = id
        juego = Juego.objects.get(id=juego_id)
        descripcion = req.POST['descripcion']
        minimo_jugadores = req.POST['minimo_jugadores']
        maximo_jugadores = req.POST['maximo_jugadores']
        imagenes = req.FILES.getlist('imagenes', None)
        logo = req.FILES.get('logo', None)
        juego.descripcion= descripcion
        juego.minimo_jugadores = minimo_jugadores
        juego.maximo_jugadores = maximo_jugadores
        juego.logo = logo
        nuevas_img = [JuegoImagen.objects.create(juego=juego, imagen=img) for img in imagenes]
        juego.imagenes.add(*nuevas_img)
        # Juego.objects.filter(id=juego_id).update(descripcion, minimo_jugadores, maximo_jugadores, imagenes)
        juego.save()
        messages.success(req, 'Juego editado con éxito')
        return redirect('/') 
    
def eliminar_game(req, id):
    
    Juego.objects.get(id=id).delete()
    messages.success(req, '¡Juego eliminado!')
    return redirect('/juegos/ver_juegos')

class RegistroView(View):

    def get(self, req):
        return render(req, 'registration/registro.html')
    
    def post(self, req):
        # 1. Recuperamos los datos del formulario
        username = req.POST['username']
        email = req.POST['email']
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        password = req.POST['password']
        pass_repeat = req.POST['pass_repeat']
    #     pass_repeat = req.POST['pass_repeat']
        # 2. Validamos que contraseñas concidan
        if password != pass_repeat:
            messages.error(req, 'Contraseñas no coinciden')
            return redirect('/accounts/registro')
            # 3. Creamos al usuario
        User.objects.create_user(username=username, email=email, first_name = first_name, last_name=last_name, password=password)
        # 5. Feedback y redirigimos
        messages.success(req, 'Usuario creado')
        return redirect('/') 
    
class NuevoJuegoView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, req):
        form = JuegoModelForm()
        imagen_form = JuegoImagenForm()
        context = {
            'form': form,
            'imagen_form': imagen_form
        }
        return render(req, 'nuevo_juego.html', context)
    
    def post(self, req):
        form = JuegoModelForm(req.POST, req.FILES)
        imagen_form = JuegoImagenMultipleForm(req.POST, req.FILES)
        try:
            if form.is_valid() and imagen_form.is_valid():
                juego = form.save()
                for img in req.FILES.getlist('imagen'):
                    JuegoImagen.objects.create(juego=juego, imagen = img)
                messages.success(req, 'Juego Creado')
        except IntegrityError:
            messages.warning(req, "Este juego ya está registrado!")
        
        return redirect('/')
        
class NuevaPartidaView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    #El get carga el template
    def get(self, req):
        form = PartidaModelForm()
        context = {
            'form': form
        }
        return render(req, 'nueva_jornada.html', context)
    
    def post(self, req):
        form = PartidaModelForm(req.POST)
        form.save()
        messages.success(req, 'Partida Creada')
        return redirect('/')
    
def detalles_partida(req, id):
    partida = Partida.objects.get(id=id)
    partida_jugador = PartidaJugador.objects.filter(partida_id = id)
    
    context = {
        'partida': partida,
        'partida_jugador': partida_jugador
    }
    
    return render(req, 'detalles_partida.html', context)
    
    
class NuevoLocalView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    #El get carga el template
    def get(self, req):
        form = LocalModelForm()
        context = {
            'form': form
        }       
        return render(req, 'nuevo_local.html', context)
    
    def post(self, req):
        form= LocalModelForm(req.POST)
        if form.is_valid():
            local = form.save(commit=False)
            local.guardar_coordenadas()
            local.save()
        messages.success(req, 'Local agregado')
        return redirect('/')

def ver_locales(req):
    locales = Local.objects.all()
    context = {
        'locales': locales
    }
    
    return render(req, 'ver_locales.html', context)

def detalleLocal(req, id):
    local= Local.objects.get(id=id)
    context = {
        'local': local
    }
    return render (req, 'detalle_local.html', context)

def edit_local(req, id):
    if req.method == 'GET':
        local = Local.objects.get(id=id)
        context = {
            'local': local
        }
        return render(req, 'editar_local.html', context)
    else:
        local_id = id
        local = Local.objects.get(id=local_id)
        ubicacion = req.POST['ubicacion']
        imagenes = req.FILES.getlist('imagenes', None)
        
        local.ubicacion= ubicacion
        local.guardar_coordenadas()
        nuevas_img = [LocalImagen.objects.create(local=local, imagen=img) for img in imagenes]
        local.imagenes.add(*nuevas_img)
        local.save()

        messages.success(req, 'Juego editado con éxito')
        return redirect('/')
    
def eliminar_local(req, id):
    Local.objects.get(id=id).delete()
    messages.success(req, '¡Local eliminado!')
    return redirect('/locales/ver_locales')

    
def partidas(req):
    today = date.today()
    ahora = datetime.now().time()

    partidas_dispo = Partida.objects.filter(
        Q(fecha = today, hora__gt = ahora) | Q(fecha__gt = today)
    )
    
    partidas_anteriores = Partida.objects.filter(
        (Q(fecha = today, hora__lt = ahora) | Q(fecha__lt = today))
    ).order_by('fecha')
    
    context = {
        'partidas_dispo': partidas_dispo,
        'partidas_anteriores': partidas_anteriores
    }
    return render(req, 'ver_partidas_reservadas.html', context)

class InscripcionView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, req, id):
        partida = Partida.objects.get(id=id)
        partida_jugador = PartidaJugador.objects.filter(partida_id=id)
        local = Local.objects.filter(id=id)

        context = { 
            'partida': partida,
            'partida_jugador' : partida_jugador,
            'local': local
        }
        
        return render (req, 'inscripcion.html', context)
    
    def post(self, req, id):
        partida = Partida.objects.get(id=id)
        suma = 0
        partida_jugador = PartidaJugador.objects.filter(partida_id=id)
        for p in partida_jugador:
            print(p)
            suma +=1
        print(suma)
        jugador = req.user
        try:
            if suma < partida.juego.maximo_jugadores:
                PartidaJugador.objects.create(
                    partida = partida,
                    jugador = jugador
                )
                messages.success(req, '¡Se ha inscrito en la partida con éxito!')
                return redirect('/')
            else:
                messages.warning(req, 'No quedan cupos para esta partida')
                return redirect('/')
        except IntegrityError:
            messages.warning(req, "El usuario ya está registrado en esta partida.")
            return redirect('/partidas')
        
def desinscripcion (req, id):
    user_id = req.user.id
    partida_actual = Partida.objects.get(id=id)
    PartidaJugador.objects.get(partida_id= partida_actual, jugador_id = user_id).delete()
    messages.success(req, 'Se ha quitado de esta partida')
    return redirect('/')
    
class ResultadosView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, req, id):
        partida = Partida.objects.get(id=id)
        partida_jugador = PartidaJugador.objects.filter(partida_id = id)
        participantes = User.objects.filter(partidas_jugador__partida = id)
        
        context = {
            'partida': partida,
            'partida_jugador': partida_jugador,
            'participantes': participantes
        }
        return render (req, 'resultados.html', context)
    
    def post(self, req, id):
        partida = Partida.objects.get(id=id)
        partida_jugador = PartidaJugador.objects.filter(partida_id = id)
        
        for p in partida_jugador:
            puntaje_key = f'puntaje_{p.jugador.id}'
            ganador_key = f'ganador_{p.jugador.id}'
            nuevo_puntaje = req.POST.get(puntaje_key)
            ganador = req.POST.get(ganador_key)
            print(puntaje_key)
            if nuevo_puntaje is not None:
                p.puntaje = int(nuevo_puntaje)   
            elif partida.ganador is not None:
                partida.ganador =  ganador   
                partida.save()

            p.save()
        partida.guardar_ganador()
        
        messages.success(req, 'Puntaje actualizado')
        return redirect(f'/accounts/historial/{id}/detalles') 
    
def foro(req):
    posteos = Post.objects.all()
    for p in posteos:
        p.obtener_respuestas()
    context = {
        'posteos': posteos, 
    }
    return render(req, 'foro.html', context)

class CrearPostView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    #El get carga el template
    def get(self, req):
        form = PostModelForm()
        context = {
            'form': form
        }       
        return render(req, 'nuevo_post.html', context)
    
    def post(self, req):
        form= PostModelForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = req.user
            post.save()
        messages.success(req, 'Post publicado con éxito')
        return redirect('/foro')

def detalle_post(req, modelo, id):
    if req.method == 'GET':
        if modelo == 'Post':
            post = Post.objects.get(id=id)
            comentarios = Comentario.objects.filter(post=post)
            form = ComentarioModelForm()
            content_type = ContentType.objects.get(app_label= 'juegos', model = modelo)
            content_type_coment = ContentType.objects.get(app_label= 'juegos', model = 'Comentario')
            
            if req.user.is_authenticated:
                
                liked_post = Like.objects.filter(content_type = content_type, object_id=id, usuario=req.user).exists()
                liked_coments = {com.id : Like.objects.filter(content_type = content_type_coment, object_id = com.id, usuario= req.user).exists()
                for com in comentarios } 
                # liked = Like.objects.filter(object_id = id, usuario = req.user)
                context = {
                'post': post,
                'form': form,
                'comentarios': comentarios, 
                'liked_post': liked_post,
                'liked_coments': liked_coments
            }
            return render(req, 'detalle_post.html', context)
        else:
            post = Post.objects.get(comentarios__id= id)
            comentarios = Comentario.objects.filter(post=post)
            form = ComentarioModelForm()
            content_type = ContentType.objects.get(app_label= 'juegos', model = modelo)
            content_type_post = ContentType.objects.get(app_label= 'juegos', model = 'Post')

            if req.user.is_authenticated:
                
                liked_coments = { com.id: Like.objects.filter(content_type = content_type, object_id=com.id, usuario=req.user).exists() 
                    for com in comentarios
                    } 
                liked_post = Like.objects.filter(content_type=content_type_post, object_id = post.id ,usuario=req.user).exists()
                # liked = Like.objects.filter(object_id = id, usuario = req.user)
                context = {
                'post': post,
                'form': form,
                'comentarios': comentarios, 
                'liked_coments': liked_coments,
                'liked_post': liked_post
            }
            return render(req, 'detalle_post.html', context)
        
    else:
        if modelo == 'Post':
            form= ComentarioModelForm(req.POST)
            post = Post.objects.get(id=id)
        else:
            form= ComentarioModelForm(req.POST)
            post = Post.objects.get(comentarios__id= id)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = req.user
            comentario.save()
        
        messages.success(req, 'Respuesta publicada con éxito')
        return redirect(f'/foro/{modelo}/{id}/detalle_post')
    
def categorias(req):
    if req.method == 'GET':
        categorias = Categoria.objects.all()
        context = {
            'categorias': categorias
        }
        return render(req, 'foro_categorias.html', context)
    else:
        categoria_nombre = req.POST['nombre']
        Categoria.objects.create(nombre = categoria_nombre)
        messages.success(req, 'Categoria creada')
        return redirect('/foro/categorias')
        
def categorias_group(req, id):
    categoria = Categoria.objects.get(id=id)
    posteos = Post.objects.filter(categoria = categoria)

    context = {
        'posteos': posteos
    }   
    return render(req, 'categorias_grupo.html', context)

@login_required
def reaccionar(req, modelo, id):
    if not req.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)
    
    usuario = req.user
    content_type = ContentType.objects.get(app_label= 'juegos', model = modelo)
    print(content_type)
    
    model_class = content_type.model_class()
    objeto = model_class.objects.get(id = id)
    
    liked = Like.objects.filter(content_type = content_type, object_id=id, usuario=usuario).exists()
    
    if liked:
        Like.objects.filter(content_type= content_type, object_id=id, usuario=usuario).delete()
        liked = False
    else:

        Like.objects.create(content_type= content_type, object_id=id, usuario=usuario) 
        
        liked = True
        
    
    return JsonResponse({'liked':liked, 'total_likes': objeto.total_likes()})

def editar_post(req, modelo, id):
    if req.method == 'GET':
        post = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(post=post)
        form = ComentarioModelForm()
        content_type = ContentType.objects.get(app_label= 'juegos', model = modelo)
        content_type_coment = ContentType.objects.get(app_label= 'juegos', model = 'Comentario')
            
        if req.user.is_authenticated:
            
            liked_post = Like.objects.filter(content_type = content_type, object_id=id, usuario=req.user).exists()
            liked_coments = {com.id : Like.objects.filter(content_type = content_type_coment, object_id = com.id, usuario= req.user).exists()
            for com in comentarios } 
            # liked = Like.objects.filter(object_id = id, usuario = req.user)
            context = {
            'post': post,
            'form': form,
            'comentarios': comentarios, 
            'liked_post': liked_post,
            'liked_coments': liked_coments
            }
            return render(req, 'detalle_post.html', context)
    else:
        post = Post.objects.get(id=id)
        contenido = req.POST['contenido']
        post.contenido = contenido
        post.save()
        messages.success(req, 'Post editado con éxito')
        return redirect(f'/foro/{modelo}/{id}/detalle_post') 

def eliminar_post(req, id):
    Post.objects.get(id = id).delete()
    messages.success(req, 'Ha eliminado el post')
    return redirect('/foro')

def editar_comentario(req, modelo, id):
    if req.method == 'GET':
        post = Post.objects.get(comentarios__id= id)
        comentarios = Comentario.objects.filter(post=post)
        form = ComentarioModelForm()
        content_type = ContentType.objects.get(app_label= 'juegos', model = modelo)
        content_type_post = ContentType.objects.get(app_label= 'juegos', model = 'Post')
        
        if req.user.is_authenticated:
            
            liked_coments = { com.id: Like.objects.filter(content_type = content_type, object_id=com.id, usuario=req.user).exists() 
                for com in comentarios
                } 
            liked_post = Like.objects.filter(content_type=content_type_post, usuario=req.user).exists()
            # liked = Like.objects.filter(object_id = id, usuario = req.user)
            context = {
            'post': post,
            'form': form,
            'comentarios': comentarios, 
            'liked_coments': liked_coments,
            'liked_post': liked_post
        }
        return render(req, 'detalle_post.html', context)
        
    else:
        comentarios = Comentario.objects.get(id=id)
        mensaje = req.POST['mensaje']
        comentarios.mensaje = mensaje
        comentarios.save()
        messages.success(req, 'Comentario editado con éxito')
        return redirect(f'/foro/{modelo}/{id}/detalle_post') 

def eliminar_comentario(req, id):
    Comentario.objects.get(id = id).delete()
    messages.success(req, 'Ha eliminado el comentario')
    return redirect('/foro')
