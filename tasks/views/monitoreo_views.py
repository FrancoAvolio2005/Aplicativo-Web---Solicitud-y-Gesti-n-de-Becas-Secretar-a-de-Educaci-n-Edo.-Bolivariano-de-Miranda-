# tasks/vistas/monitoreo_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse

from ..models import Solicitud 

# ====================
# Funciones auxiliares
# ====================

def is_admin_or_analyst(user):
    """
    Verifica si el usuario es un superusuario o un analista exterior.
    """
    if user.is_authenticated:
        return user.is_superuser or (hasattr(user, 'profile') and user.profile.is_analista_exterior)
    return False

# ==============================================================================
# Vistas de Monitoreo
# ==============================================================================

@login_required
@user_passes_test(is_admin_or_analyst, login_url='/') # Protegemos el acceso
def ver_actividad_view(request):
    """
    Muestra la lista de usuarios solicitantes para que el administrador pueda ver su actividad.
    """
    # Filtramos a los usuarios que NO son superusuarios y NO son analistas exteriores.
    normal_users = User.objects.filter(is_superuser=False, profile__is_analista_exterior=False)

    context = {
        'normal_users': normal_users
    }
    return render(request, 'ver_actividad.html', context)

@login_required
@user_passes_test(is_admin_or_analyst, login_url='/') # Protegemos el acceso
def get_user_activity(request, user_id):
    """
    Retorna los datos de actividad de un usuario específico en formato JSON (usado por AJAX).
    """
    try:
        user_to_check = get_object_or_404(User, id=user_id)
        
        # Obtenemos los datos del perfil si existe.
        profile = getattr(user_to_check, 'profile', None)
        
        user_data = {
            'username': user_to_check.username,
            'email': user_to_check.email,
            'date_joined': user_to_check.date_joined.isoformat() if user_to_check.date_joined else 'N/A',
            'last_login': user_to_check.last_login.isoformat() if user_to_check.last_login else 'N/A',
            
            # Usamos el perfil si existe; de lo contrario, 'N/A'
            'nombre_completo': profile.nombre_completo if profile else 'N/A',
            'apellido_completo': profile.apellido_completo if profile else 'N/A',
            'edad': profile.edad if profile else 'N/A',
            'genero': profile.genero if profile else 'N/A',
            'numero_telefono': profile.numero_telefono if profile else 'N/A',
            'cedula_identidad': profile.cedula_identidad if profile else 'N/A',
        }
        
        # Obtenemos las solicitudes del usuario
        solicitudes = Solicitud.objects.filter(user=user_to_check).order_by('-fecha_creacion')
        solicitudes_data = []
        for sol in solicitudes:
            solicitudes_data.append({
                'id_solicitud': sol.id_solicitud,
                'fecha_creacion': sol.fecha_creacion.isoformat() if sol.fecha_creacion else 'N/A',
                'estatus_beca': sol.estatus_beca.nombre if sol.estatus_beca else 'N/A',
                'beca': sol.beca.nombre if sol.beca else 'N/A',
            })
            
        response_data = {
            'user': user_data,
            'solicitudes': solicitudes_data,
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        # Registramos el error y retornamos una respuesta de error
        print(f"Error en get_user_activity: {e}")
        return JsonResponse({'error': 'Error al cargar la actividad. Por favor, inténtelo de nuevo.'}, status=500)