# tasks/urls.py

from django.urls import path

from .views import general_views
from .views import auth_views
from .views import user_solicitud_views
from .views import admin_solicitud_views
from .views import reporte_views
from .views import monitoreo_views

# ----------------------------------------------------------------------
# Definición de patrones de URL (URLconf) 
urlpatterns = [
    # 1. Vistas Generales (general_views.py)
    path('info/', general_views.info, name='info'),
    path('admin_dashboard/', general_views.admin_dashboard, name='admin_dashboard'),
    path('', general_views.home, name='home'),
    path('becas/', general_views.becas, name='becas'),

    # 2. Autenticación (auth_views.py)
    path('admin_home/', auth_views.admin_home, name='admin_home'),
    path('signup/', auth_views.signup, name='signup'),
    path('logout/', auth_views.cerrar_sesion, name='cerrar_sesion'),
    path('iniciar_sesion/', auth_views.iniciar_sesion, name='iniciar_sesion'),

    # 3. Solicitudes de Usuario (user_solicitud_views.py)
    path('tasks/', user_solicitud_views.tasks, name='tasks'),
    path('tasks_completed/', user_solicitud_views.tasks_completed, name='tasks_completed'),
    path('tasks/create', user_solicitud_views.create_tasks, name='create_tasks'),
    path('tasks/<int:task_id>/', user_solicitud_views.tasks_details, name='tasks_detail'),
    path('tasks/<int:task_id>/complete', user_solicitud_views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', user_solicitud_views.delete_task, name='delete_task'),
    path('solicitudes_user/<int:solicitud_id>/', user_solicitud_views.solic_details_user, name='solic_details_user'),

    # 4. Solicitudes de Admin/Analista (admin_solicitud_views.py)
    path('asig_beca/', admin_solicitud_views.asig_beca, name='asig_beca'),
    path('ver_asig_beca/', admin_solicitud_views.ver_asig_beca, name='ver_asig_beca'),
    path('solic_pendiente/', admin_solicitud_views.solic_pendiente, name='solic_pendiente'),
    path('solic_aprobadas/', admin_solicitud_views.solic_aprobadas, name='solic_aprobadas'),
    path('solic_rechazadas/', admin_solicitud_views.solic_rechazadas, name='solic_rechazadas'),
    path('solicitudes/<int:solicitud_id>/', admin_solicitud_views.solic_details, name='solic_details'),
    path('asig_beca_estado/<int:solicitud_id>/', admin_solicitud_views.asig_beca_estado, name='asig_beca_estado'),
    path('solicitudes/<int:solicitud_id>/<str:accion>/', admin_solicitud_views.gestionar_solicitud, name='gestionar_solicitud'),

    # 5. Reportes y Gráficos (reporte_views.py)
    path('graf_beca/', reporte_views.graf_beca, name='estadísticas'),
    path('reporte/perfiles/excel/', reporte_views.export_profiles_to_excel, name='export_profiles_excel'),
    path('reporte/becas/excel/', reporte_views.export_becas_to_excel, name='export_becas_excel'),
    path('reporte/planteles/excel/', reporte_views.export_planteles_to_excel, name='export_planteles_excel'),
    path('reporte/solicitudes/excel', reporte_views.export_solicitudes_to_excel, name='export_solicitudes_excel'),

    # 6. Monitoreo (monitoreo_views.py)
    path('ver_actividad/', monitoreo_views.ver_actividad_view, name='ver_actividad'),
    path('get_user_activity/<int:user_id>/', monitoreo_views.get_user_activity, name='get_user_activity'),
]