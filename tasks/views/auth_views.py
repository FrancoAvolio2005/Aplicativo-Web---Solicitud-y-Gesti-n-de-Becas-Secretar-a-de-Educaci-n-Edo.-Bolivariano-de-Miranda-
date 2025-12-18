# tasks/vistas/auth_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date

from ..forms.user_register_form import UserRegisterForm
from ..forms.profile_form import ProfileForm
from ..forms.analista_form import AnalistaForm
from ..forms.superuser_form import SuperuserForm 

from ..models import Profile

def is_admin_or_analyst(user):
    """
    Verifica si el usuario es un superusuario o un analista exterior.
    """
    if user.is_authenticated:
        return user.is_superuser or (hasattr(user, 'profile') and user.profile.is_analista_exterior)
    return False

@login_required(login_url='iniciar_sesion')
@user_passes_test(is_admin_or_analyst, login_url='/') 
def admin_home(request):
    """
    Permite el registro de nuevos analistas y superusuarios.
    """
    analista_form = AnalistaForm()
    superuser_form = SuperuserForm()

    if request.method == 'POST':
        if 'analista_register' in request.POST:
            analista_form = AnalistaForm(request.POST)
            if analista_form.is_valid():
                try:
                    with transaction.atomic():
                        new_analista = analista_form.save()
                        profile = new_analista.profile
                        profile.cedula_identidad = f'Analista-CDCE-{new_analista.id}'
                        profile.is_analista_exterior = True
                        profile.save()
                    messages.success(request, 'El analista ha sido registrado y marcado como analista exterior exitosamente.')
                    return redirect('admin_home')
                except Exception as e:
                    messages.error(request, f'Ocurrió un error al registrar el analista: {e}')
            else:
                messages.error(request, 'Por favor, corrige los errores del formulario de registro de analistas.')

        # Nueva lógica para el registro de superusuarios
        elif 'superuser_register' in request.POST:
            superuser_form = SuperuserForm(request.POST)
            if superuser_form.is_valid():
                username = superuser_form.cleaned_data['username']
                password = superuser_form.cleaned_data['password2']

                try:
                    with transaction.atomic():
                        User.objects.create_superuser(username=username, password=password)

                    messages.success(request, f'El superusuario {username} ha sido registrado exitosamente.')
                    return redirect('admin_home')
                except Exception as e:
                    messages.error(request, f'Ocurrió un error al registrar el superusuario: {e}')
            else:
                messages.error(request, 'Por favor, corrige los errores del formulario de registro de superusuario.')
    
    context = {
        'analista_form': analista_form,
        'superuser_form': superuser_form,
    }
    return render(request, 'admin_home.html', context)

def signup(request):
    """
    Maneja el registro de nuevos usuarios (solicitantes de becas),
    calculando la edad a partir de la fecha de nacimiento.
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                # 1. Guardar el usuario (User)
                user = user_form.save()
                
                # 2. Obtener el perfil relacionado
                profile = user.profile
                
                # 3. Obtener la fecha de nacimiento del formulario limpio
                fecha_nacimiento = profile_form.cleaned_data.get('fecha_nacimiento')
                
                # 4. Calcular la edad a partir de la fecha de nacimiento
                edad_calculada = None
                if fecha_nacimiento:
                    hoy = date.today()
                    # Lógica para calcular la edad exacta:
                    # Resta el año actual menos el año de nacimiento,
                    # y resta 1 si el cumpleaños aún no ha pasado este año.
                    edad_calculada = hoy.year - fecha_nacimiento.year - (
                        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
                    )
                
                # 5. Asignar los datos al perfil, incluyendo la EDAD CALCULADA
                profile.nombre_completo = profile_form.cleaned_data['nombre_completo']
                profile.apellido_completo = profile_form.cleaned_data['apellido_completo']
                profile.edad = edad_calculada # ¡Aquí se asigna la edad calculada!
                profile.genero = profile_form.cleaned_data.get('genero')
                profile.cedula_identidad = profile_form.cleaned_data['cedula_identidad']
                profile.fecha_nacimiento = fecha_nacimiento
                profile.numero_telefono = profile_form.cleaned_data.get('numero_telefono')
                
                # 6. Guardar el perfil
                profile.save()

                # 7. Iniciar sesión y redirigir
                login(request, user)
                messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
                return redirect('home')
            
            except IntegrityError:
                messages.error(request, 'El nombre de usuario o la cédula de identidad ya existen. Por favor, elige otros.')
                return render(request, 'signup.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'error': messages.get_messages(request)
                })
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return render(request, 'signup.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'error': messages.get_messages(request)
            })
    else:
        print('Enviando formulario de registro')
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
        return render(request, 'signup.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'error': messages.get_messages(request)
        })

def iniciar_sesion(request):
    """
    Maneja la autenticación y el login de usuarios.
    """
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html', {
            'form': AuthenticationForm(),
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'iniciar_sesion.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario o Contraseña es incorrecto'
            })
        else:
            login(request, user)
            
            if user.is_superuser:
                return redirect('admin_home')
            
            elif hasattr(user, 'profile') and user.profile.is_analista_exterior:
                return redirect('admin_home')
            else:
                return redirect('home')

@login_required
def cerrar_sesion(request):
    """
    Cierra la sesión del usuario.
    """
    logout(request)
    return redirect('home')