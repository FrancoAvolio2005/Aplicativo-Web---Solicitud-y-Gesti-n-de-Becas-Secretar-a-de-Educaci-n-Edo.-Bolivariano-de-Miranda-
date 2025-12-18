# tasks/forms/analista_form.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Clase AnalistaForm: Formulario de Registro para usuarios Analistas/Internos.
class AnalistaForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super(AnalistaForm, self).__init__(*args, **kwargs)
 
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control' 
        self.fields['password2'].widget.attrs['class'] = 'form-control'