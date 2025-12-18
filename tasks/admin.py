from django.contrib import admin
from .models import Task
from .models import Certificado
from .models import Becas
from .models import Solicitud
from .models import Plantel
from .models import Estado
from .models import Municipio
from .models import Parroquia
from .models import Banco
from .models import EstatusBeca
from .models import Profile
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
    
admin.site.register(Task, TaskAdmin,)
admin.site.register(Becas)
admin.site.register(Solicitud)
admin.site.register(Plantel)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Parroquia)
admin.site.register(Banco)
admin.site.register(EstatusBeca)
admin.site.register(Profile)
