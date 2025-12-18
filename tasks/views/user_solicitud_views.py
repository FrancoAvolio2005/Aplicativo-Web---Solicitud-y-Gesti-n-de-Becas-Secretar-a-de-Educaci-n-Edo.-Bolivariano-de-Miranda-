# tasks/vistas/user_solicitud_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date

# Importaciones relativas
from ..models import Task, Solicitud
from ..forms.solicitud_form import SolicitudForm

@login_required
def tasks(request):
    """Muestra todas las solicitudes/tareas del usuario."""
    solic_pend = Solicitud.objects.filter(user=request.user).order_by('-fecha_creacion')
    return render(request, 'tasks.html',{'solic_pend': solic_pend})

@login_required
def tasks_completed(request):
    """Muestra tareas completadas (si usas el modelo Task)."""
    tasks = Task.objects.filter(user=request.user, datacompleted__isnull=False).order_by('-datacompleted')
    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
def create_tasks(request):
    """
    Permite al usuario crear una nueva solicitud/tarea, 
    calculando automáticamente la edad del becario.
    """
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {
            'form': SolicitudForm()
        })
    else:
        # Usa request.POST y request.FILES ya que tienes archivos adjuntos
        form = SolicitudForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Usa commit=False para poder modificar la instancia antes de guardarla
            new_tasks = form.save(commit=False)
            
            # --- Lógica de Cálculo de Edad ---
            fecha_nacimiento = new_tasks.fecha_nacimiento_becario
            edad_calculada = None
            
            if fecha_nacimiento:
                hoy = date.today()
                # Cálculo de edad: (Año actual - Año nacimiento) - (Restar 1 si no ha cumplido años)
                edad_calculada = hoy.year - fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
                )
            # Asignar la edad calculada a la instancia del modelo (Solicitud)
            # **Asegúrate de que tu modelo Solicitud tenga el campo 'edad_becario'**
            new_tasks.edad_becario = edad_calculada
            # -----------------------------------
            
            # Asignar el usuario que crea la solicitud/tarea
            new_tasks.user = request.user
            
            # Ahora sí, guardar la instancia completamente
            try:
                new_tasks.save()
                return redirect('tasks') # Redirigir a la lista de tareas/solicitudes
            except Exception as e:
                # Manejo genérico de errores al guardar
                return render(request, 'create_tasks.html', {
                    'form': form,
                    'error': f'Ocurrió un error al guardar la solicitud: {e}'
                })
        else:
            # Si el formulario no es válido, renderizar con errores
            return render(request, 'create_tasks.html', {
                'form': form,
                'error': 'No se envió correctamente la solicitud. Por favor, revisa los datos y los archivos adjuntos.'
            })

@login_required
def tasks_details(request, task_id):
    """
    Maneja la vista de detalles y edición de una tarea (asumiendo que task es el modelo Solicitud).
    """
    if request.method == 'GET':
        tasks = get_object_or_404(Task, pk=task_id, user=request.user)
        form = SolicitudForm(instance=tasks)
        return render(request, 'task_details.html', {'tasks': tasks, 'form': form})
    else:
        try:
            tasks = get_object_or_404(Task, pk=task_id, user=request.user)
            form = SolicitudForm(request.POST, instance=tasks)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_details.html', {'tasks': tasks, 'form': form, 'error': 'Error actualizando'})

@login_required
def complete_task(request, task_id):
    """Marca una tarea como completada."""
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datacompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    """Elimina una tarea."""
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def solic_details_user(request, solicitud_id):
    """Muestra detalles de una solicitud para el usuario solicitante."""
    solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id, user=request.user)
    context = {
        'solicitud': solicitud
    }
    return render(request, 'solic_details_user.html', context)