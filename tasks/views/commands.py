# tasks/views/commands.py

from django.db import transaction
from django.contrib import messages
from ..models import Solicitud, EstatusBeca 
# Usamos '...' porque las vistas están en views/, y models está un nivel arriba.

# -----------------------------------------------------------
# 1. Interfaz del Comando
# -----------------------------------------------------------
class SolicitudCommand:
    """Clase base (Interfaz) para todos los comandos de solicitud."""
    def execute(self, request, solicitud):
        raise NotImplementedError("Subclase debe implementar el método execute()")

    def get_estatus(self, nombre_estatus):
        """Helper para obtener el objeto EstatusBeca, o lanzar un error claro."""
        try:
            return EstatusBeca.objects.get(nombre=nombre_estatus)
        except EstatusBeca.DoesNotExist:
            raise Exception(f'Error: El EstatusBeca "{nombre_estatus}" no está definido en la BD.')

# -----------------------------------------------------------
# 2. Comandos Concretos (La lógica de cada if/elif)
# -----------------------------------------------------------

class AprobarSolicitudCommand(SolicitudCommand):
    """Implementa la lógica de la acción 'aprobar'."""
    def execute(self, request, solicitud):
        solicitud.estatus_beca = self.get_estatus('Aprobada')
        solicitud.motivo_rechazo = None
        solicitud.save()
        messages.success(request, f'La solicitud #{solicitud.id_solicitud} ha sido Aprobada. 👍')


class RechazarSolicitudCommand(SolicitudCommand):
    """Implementa la lógica de la acción 'rechazar', incluyendo la validación POST."""
    def execute(self, request, solicitud):
        if request.method != 'POST':
            # Solo se captura si falta el POST. Si falta el motivo, se maneja abajo.
            messages.error(request, 'Acción de rechazo no válida (requiere datos POST).')
            # Devolvemos None si no hay datos POST válidos para que la vista lo maneje
            return 

        motivo_select = request.POST.get('motivo_select')
        motivo_texto = request.POST.get('motivo_texto', '').strip()

        if not motivo_select:
            # Si faltan los datos necesarios, lanzamos una excepción para detener la transacción
            raise ValueError('Debe seleccionar un Motivo de Rechazo para continuar. ⚠️')
        
        motivo_completo = f"Motivo Principal: {motivo_select}"
        if motivo_texto:
            motivo_completo += f" | Detalles Adicionales: {motivo_texto}"

        solicitud.estatus_beca = self.get_estatus('Rechazada')
        solicitud.motivo_rechazo = motivo_completo
        solicitud.save()
        messages.info(request, f'La solicitud #{solicitud.id_solicitud} ha sido Rechazada. 🚫')


class AsignarSolicitudCommand(SolicitudCommand):
    """Implementa la lógica de la acción 'asignar'."""
    def execute(self, request, solicitud):
        solicitud.estatus_beca = self.get_estatus('Asignada')
        solicitud.save()
        messages.success(request, f'La solicitud #{solicitud.id_solicitud} ha sido Asignada. 🏅')


# -----------------------------------------------------------
# 3. Mapa de Comandos (El Invoker)
# -----------------------------------------------------------
# Este diccionario reemplaza la cadena de if/elif
COMMAND_MAP = {
    'aprobar': AprobarSolicitudCommand(),
    'rechazar': RechazarSolicitudCommand(),
    'asignar': AsignarSolicitudCommand(),
}