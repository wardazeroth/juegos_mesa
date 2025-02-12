from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from juegos.forms import PartidaModelForm, JuegoModelForm, LocalModelForm, JuegoImagenForm, JuegoImagenMultipleForm, UserProfileForm
from django.views import View
from juegos.models import UserProfile, Partida, PartidaJugador, JuegoImagen, Juego
from datetime import timedelta, date, datetime

# Create your views here.

@login_required
def inicio(req):
    partidas = Partida.objects.all()
    week_day = get_weeks_days()
    
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
        'week_day': week_day
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
        return render(req, 'nuevo_locaL.html', context)
    
    def post(self, req):
        form= LocalModelForm(req.POST)
        form.save()
        messages.success(req, 'Local agregado')
        return redirect('/')
    
def partidas(req):
    datos = req.GET
    partidas_dispo= Partida.objects.all()
    
    context = {
        'partidas_dispo': partidas_dispo
    }
    return render(req, 'ver_partidas_reservadas.html', context)

class InscripcionView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, req, id):
        partida = Partida.objects.get(id=id)
        partida_jugador = PartidaJugador.objects.raw('select * from juegos_partidajugador where partida_id = %s', [id])
        context = {
            'partida': partida,
            'partida_jugador' : partida_jugador
        }
        return render (req, 'inscripcion.html', context)
    
    def post(self, req, id):
        partida = Partida.objects.get(id=id)
        suma = 0
        partida_jugador = PartidaJugador.objects.raw('select * from juegos_partidajugador where partida_id = %s', [id])
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
        
