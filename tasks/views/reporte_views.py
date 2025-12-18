from django.http import HttpResponse
from django.db.models import Count, Q, ExpressionWrapper, fields
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, date
import datetime
import openpyxl 

from ..models import Solicitud, Profile, Becas, Plantel, EstatusBeca 
from django.contrib.auth.models import User  

from ..utils.export_excel import get_exporter 

# ==============================================================================
# FUNCIONES HELPER (Maneja la respuesta HTTP para todos los reportes)
# ==============================================================================

def _export_excel_response(workbook, filename_base):
    """Crea la respuesta HTTP de Excel a partir de un workbook de openpyxl."""
    now = datetime.datetime.now()
    filename = f"{filename_base}_{now.strftime('%d-%m-%Y')}.xlsx"

    # Configura la respuesta HTTP para descargar un archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Guarda el workbook en el objeto de respuesta
    workbook.save(response)
    return response

# ==============================================================================
# VISTAS DE EXPORTACIÓN (Usan el Patrón Estrategia)
# ==============================================================================

def export_profiles_to_excel(request):
    """Exporta los perfiles de los solicitantes usando la Estrategia Profiles."""
    # 1. Obtiene el Contexto con la Estrategia específica.
    # 2. Ejecuta la exportación y obtiene el Workbook.
    workbook = get_exporter('profiles').execute_export()
    # 3. Envía el Workbook al Helper para generar la respuesta HTTP.
    return _export_excel_response(workbook, "reporte_solicitantes")

def export_becas_to_excel(request):
    """Exporta el catálogo de becas usando la Estrategia Becas."""
    workbook = get_exporter('becas').execute_export()
    return _export_excel_response(workbook, "reporte_becas")

def export_planteles_to_excel(request):
    """Exporta el catálogo de planteles usando la Estrategia Planteles."""
    workbook = get_exporter('planteles').execute_export()
    return _export_excel_response(workbook, "reporte_planteles")

def export_solicitudes_to_excel(request):
    """Exporta el reporte completo de solicitudes usando la Estrategia Solicitudes."""
    workbook = get_exporter('solicitudes').execute_export()
    return _export_excel_response(workbook, "reporte_solicitudes")

# ==============================================================================
# VISTA DE GRÁFICOS (Se mantiene aquí, ya que renderiza HTML/JSON)
# ==============================================================================

def graf_beca(request):
    """
    Genera los datos para los gráficos del dashboard (Solicitudes por Estatus, Fecha, Becas, etc.).
    """
    # Gráfico de Solicitudes por Estatus
    solicitudes_por_estatus = Solicitud.objects.values('estatus_beca__nombre').annotate(count=Count('id_solicitud'))
    labels_estatus = [item['estatus_beca__nombre'] for item in solicitudes_por_estatus if item['estatus_beca__nombre'] is not None]
    data_estatus = [item['count'] for item in solicitudes_por_estatus if item['estatus_beca__nombre'] is not None]

    # Gráfico de Solicitudes por Fecha (Últimos 30 días)
    today = timezone.localdate()
    dates_30_days_ago = today - timedelta(days=29)

    all_dates_in_range = [(dates_30_days_ago + timedelta(days=i)) for i in range(30)]
    labels_fecha = [d.strftime('%Y-%m-%d') for d in all_dates_in_range]

    solicitudes_por_fecha = Solicitud.objects.filter(
        fecha_creacion__date__gte=dates_30_days_ago
    ).values('fecha_creacion__date').annotate(count=Count('id_solicitud')).order_by('fecha_creacion__date')

    data_fecha_dict = {str(item['fecha_creacion__date']): item['count'] for item in solicitudes_por_fecha}
    data_fecha = [data_fecha_dict.get(date_str, 0) for date_str in labels_fecha]

    # Gráfico de Usuarios Registrados por Fecha (Últimos 30 días)
    usuarios_por_fecha = User.objects.filter(
        date_joined__date__gte=dates_30_days_ago
    ).values('date_joined__date').annotate(count=Count('id')).order_by('date_joined__date')

    data_usuarios_fecha_dict = {str(item['date_joined__date']): item['count'] for item in usuarios_por_fecha}
    data_usuarios_fecha = [data_usuarios_fecha_dict.get(date_str, 0) for date_str in labels_fecha]

    # Gráfico de Becas Más Solicitadas
    becas_mas_solicitadas_qs = Solicitud.objects.values('beca__nombre').annotate(
        total_solicitudes=Count('id_solicitud')
    ).order_by('-total_solicitudes')[:5]

    labels_becas_solicitadas = [item['beca__nombre'] for item in becas_mas_solicitadas_qs if item['beca__nombre'] is not None]
    data_becas_solicitadas = [item['total_solicitudes'] for item in becas_mas_solicitadas_qs if item['beca__nombre'] is not None]

    # Gráfico de Solicitudes por Municipio
    solicitudes_por_municipio = Solicitud.objects.values('municipio__nombre').annotate(count=Count('id_solicitud')).order_by('-count')[:10]
    labels_municipio = [item['municipio__nombre'] for item in solicitudes_por_municipio if item['municipio__nombre'] is not None]
    data_municipio = [item['count'] for item in solicitudes_por_municipio if item['municipio__nombre'] is not None]

    # Gráfico de Solicitudes por Parroquia
    solicitudes_por_parroquia = Solicitud.objects.values('parroquia__nombre').annotate(count=Count('id_solicitud')).order_by('-count')[:10]
    labels_parroquia = [item['parroquia__nombre'] for item in solicitudes_por_parroquia if item['parroquia__nombre'] is not None]
    data_parroquia = [item['count'] for item in solicitudes_por_parroquia if item['parroquia__nombre'] is not None]
    
    # LÓGICA: Solicitudes por GÉNERO
    solicitudes_por_genero = Solicitud.objects.values('user__profile__genero').annotate(
        count=Count('id_solicitud')
    ).filter(
        Q(user__profile__genero='M') | Q(user__profile__genero='F') 
    )

    labels_genero_raw = [item['user__profile__genero'] for item in solicitudes_por_genero]
    data_genero = [item['count'] for item in solicitudes_por_genero]
    
    labels_genero = []
    for raw_label in labels_genero_raw:
        if raw_label == 'M':
            labels_genero.append('Masculino')
        elif raw_label == 'F':
            labels_genero.append('Femenino')
        else:
            labels_genero.append('Otro/No especificado')
            
    # LÓGICA: Solicitudes por RANGO de EDAD
    today_date = date.today()
    
    age_field = ExpressionWrapper(
        (today_date.year - ExtractYear('user__profile__fecha_nacimiento')),
        output_field=fields.IntegerField()
    )
    
    rangos_edad_data = Solicitud.objects.annotate(age=age_field).aggregate(
        r18_24=Count('id_solicitud', filter=Q(age__gte=18, age__lte=24)),
        r25_34=Count('id_solicitud', filter=Q(age__gte=25, age__lte=34)),
        r35_mas=Count('id_solicitud', filter=Q(age__gte=35)),
        r_menor=Count('id_solicitud', filter=Q(age__lt=18, age__gte=0)) 
    )

    labels_edad = ['18-24 años', '25-34 años', '35+ años', 'Menor de 18']
    data_edad = [
        rangos_edad_data['r18_24'],
        rangos_edad_data['r25_34'],
        rangos_edad_data['r35_mas'],
        rangos_edad_data['r_menor']
    ]

    if data_edad[-1] == 0 and len(data_edad) > 1:
        labels_edad.pop()
        data_edad.pop()
    
    # Conteo de usuarios por tipo (Datos para tarjetas o resumen)
    total_usuarios = User.objects.count()
    analistas_bienestar = User.objects.filter(is_superuser=True).count()
    analistas_exterior = User.objects.filter(profile__is_analista_exterior=True).count()
    solicitantes = User.objects.filter(is_superuser=False).exclude(profile__is_analista_exterior=True).count()

    context = {
        'labels_estatus': labels_estatus,
        'data_estatus': data_estatus,
        'labels_fecha': labels_fecha,
        'data_fecha': data_fecha,
        'data_usuarios_fecha': data_usuarios_fecha,
        'labels_becas_solicitadas': labels_becas_solicitadas,
        'data_becas_solicitadas': data_becas_solicitadas,
        'labels_municipio': labels_municipio,
        'data_municipio': data_municipio,
        'labels_parroquia': labels_parroquia,
        'data_parroquia': data_parroquia,
        
        # DATOS DE GÉNERO Y EDAD
        'labels_genero': labels_genero,
        'data_genero': data_genero,
        'labels_edad': labels_edad,
        'data_edad': data_edad,
        
        # DATOS DE RESUMEN DE USUARIOS
        'total_usuarios': total_usuarios,
        'analistas_bienestar': analistas_bienestar,
        'analistas_exterior': analistas_exterior,
        'solicitantes': solicitantes,
    }
    return render(request, 'graf_becas.html', context)