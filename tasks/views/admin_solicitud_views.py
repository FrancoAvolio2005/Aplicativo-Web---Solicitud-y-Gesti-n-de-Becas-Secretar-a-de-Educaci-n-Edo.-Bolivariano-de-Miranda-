from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from ..models import Solicitud, EstatusBeca 
# Importa el mapa de comandos
from .commands import COMMAND_MAP 

# ----------------
# FUNCIONES HELPER 
# ----------------

def _get_solicitudes_by_estatus(request, estatus_nombre, template_name, context_key):
    """Función helper para obtener y renderizar listas de solicitudes por estatus."""
    solicitudes = []
    try:
        estatus = EstatusBeca.objects.get(nombre=estatus_nombre)
        solicitudes = Solicitud.objects.filter(estatus_beca=estatus).order_by('-fecha_creacion')
    except EstatusBeca.DoesNotExist:
        messages.warning(request, f"El estado '{estatus_nombre}' no está definido en la BD. Por favor, revíselo.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al cargar las solicitudes de {estatus_nombre}: {e}")

    context = {
        context_key: solicitudes
    }
    return render(request, template_name, context)

# ----------------------------------------------------------------------
# VISTAS DE LISTADO (USAN EL HELPER)
# ----------------------------------------------------------------------

def solic_pendiente(request):
    """Muestra las solicitudes con estatus 'En proceso'."""
    return _get_solicitudes_by_estatus(request, 'En proceso', 'solic_pendiente.html', 'solic_pend')

def solic_aprobadas(request):
    """Muestra las solicitudes con estatus 'Aprobada'."""
    return _get_solicitudes_by_estatus(request, 'Aprobada', 'solic_aprobadas.html', 'solic_aprobadas')

@login_required
def solic_rechazadas(request):
    """Muestra las solicitudes con estatus 'Rechazada'."""
    return _get_solicitudes_by_estatus(request, 'Rechazada', 'solic_rechazadas.html', 'solic_rechazadas')

def asig_beca(request):
    """Muestra las solicitudes aprobadas listas para asignación."""
    # Nota: Llama al mismo estatus 'Aprobada' que solic_aprobadas, pero usa un template diferente.
    return _get_solicitudes_by_estatus(request, 'Aprobada', 'asig_beca.html', 'solic_aprobadas')

def ver_asig_beca(request):
    """Muestra las solicitudes con estatus 'Asignada'."""
    return _get_solicitudes_by_estatus(request, 'Asignada', 'ver_asig_beca.html', 'solic_asig')

# ----------------------------------------------------------------------
# VISTAS DE DETALLE Y ACCIÓN
# ----------------------------------------------------------------------

@login_required
def solic_details(request, solicitud_id):
    """Muestra detalles de una solicitud para el administrador/analista."""
    solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)
    context = {
        'solicitud': solicitud
    }
    return render(request, 'solic_details.html', context)

@login_required
def asig_beca_estado(request, solicitud_id):
    """Vista de detalle para confirmar la asignación de beca por estado."""
    solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)
    context = {
        'solicitud': solicitud
    }
    return render(request, 'asig_beca_estado.html', context)

@login_required
def gestionar_solicitud(request, solicitud_id, accion):
    """
    Controla las acciones de Aprobación, Rechazo o Asignación de una solicitud
    utilizando el Patrón Comando. (Invoker)
    """
    solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)

    # 1. Busca el comando
    command = COMMAND_MAP.get(accion)

    if not command:
        messages.error(request, f'Acción "{accion}" no válida.')
    else:
        try:
            # 2. Ejecuta el comando dentro de una transacción para seguridad
            with transaction.atomic():
                command.execute(request, solicitud)
            
        except ValueError as ve:
            # Captura errores de validación del comando (ej. motivo de rechazo faltante)
            messages.error(request, str(ve))
        except Exception as e:
            # Captura errores de base de datos, estatus no definidos, etc.
            messages.error(request, f'Ocurrió un error al procesar la solicitud: {e} 🐛')

    # 3. Redirige al detalle de la solicitud
    return redirect('solic_details', solicitud_id=solicitud.id_solicitud)