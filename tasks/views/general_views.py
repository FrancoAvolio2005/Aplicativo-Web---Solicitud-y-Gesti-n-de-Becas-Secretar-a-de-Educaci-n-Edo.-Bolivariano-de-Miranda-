# tasks/vistas/general_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    """Maneja la página de inicio."""
    return render(request, 'home.html', {'user':request.user})

def becas(request):
    """Maneja la página de información de becas."""
    return render(request, 'becas.html')

def info(request):
    """Maneja la página de información general."""
    return render(request, 'info.html')

@login_required
def admin_dashboard(request):
    """Maneja el dashboard de administración/analista (como vista de bienvenida)."""
    return render(request, 'admin_dashboard.html')