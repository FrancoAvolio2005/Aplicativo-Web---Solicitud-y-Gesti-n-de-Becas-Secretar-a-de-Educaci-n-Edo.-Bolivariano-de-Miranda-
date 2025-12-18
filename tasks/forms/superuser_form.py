# tasks/forms/superuser_form.py
from django.contrib.auth.forms import UserCreationForm

# Clase SuperuserForm: Formulario para la creación de Superusuarios o usuarios CDCE.
class SuperuserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilo a todos los campos visibles.
        for field in self.visible_fields():
            field.field.widget.attrs.update({'class': 'form-control'})