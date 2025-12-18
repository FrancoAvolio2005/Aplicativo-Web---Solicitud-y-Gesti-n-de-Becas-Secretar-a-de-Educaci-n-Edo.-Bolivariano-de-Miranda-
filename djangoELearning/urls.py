# djangoELearning/urls.py (CÓDIGO FINAL Y CORRECTO PARA EL PROYECTO PRINCIPAL)

# Importa el módulo de administración de Django.
from django.contrib import admin
# Importa las funciones path (para definir rutas URL) e include (para incluir rutas de otras apps).
from django.urls import path, include 
# Importa la configuración de Django (necesaria para manejar archivos de medios en desarrollo).
from django.conf import settings
# Importa la función static para servir archivos estáticos/media en desarrollo.
from django.conf.urls.static import static

# ----------------------------------------------------------------------
# Definición de patrones de URL (URLconf)
urlpatterns = [
    # Ruta de acceso al sitio de administración de Django.
    path('admin/', admin.site.urls),
    
    
    path('', include('tasks.urls')),
]

# ----------------------------------------------------------------------
# Manejo de Archivos de Medios (Media Files)
if settings.DEBUG:
    # Si la aplicación está en modo de depuración (DEBUG=True),
    # Añade un patrón de URL para servir archivos subidos por los usuarios (MEDIA_URL)
    # desde la ubicación física donde están almacenados (MEDIA_ROOT).
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)