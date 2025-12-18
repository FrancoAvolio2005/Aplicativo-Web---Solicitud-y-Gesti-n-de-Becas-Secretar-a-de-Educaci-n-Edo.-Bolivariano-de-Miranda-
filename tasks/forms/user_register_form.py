# tasks/forms/user_register_form.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 
import re 

# Clase UserRegisterForm: Formulario de Registro para Solicitantes.
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo Electrónico", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilos y placeholders a los campos para la UI.
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Crea tu nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa tú correo electrónico'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Crea una contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
        
    # MÉTODO DE VALIDACIÓN PERSONALIZADO PARA EL CAMPO 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # 1. Validación: No se permiten espacios en el correo
        if ' ' in email:
            raise ValidationError("El correo electrónico no puede contener espacios en blanco.")
        
        # 2. 🟢 VALIDACIÓN DE CARACTERES ARREGLADA 🟢
        # Este patrón ahora permite: letras, números, el símbolo '@', el punto (.) y el guion bajo (_)
        # Esto soluciona el problema de correos estándar que eran rechazados.
        if not re.match(r'^[a-zA-Z0-9@._]+$', email): 
            raise ValidationError(
                "El correo electrónico solo puede contener letras, números, los símbolos '@', punto (.), o guion bajo (_). No se permiten otros caracteres especiales."
            )
        
        # 3. Validación: Comprobar que contenga '@' (aunque EmailField y RegEx lo cubren)
        if '@' not in email:
            raise ValidationError("El correo electrónico no es válido.") 
            
        # 4. Definir y validar el dominio
        allowed_domains = ['gmail.com', 'hotmail.com']
        
        # Extraer el dominio (esto fallaría si hay dos '@', pero ya la RegEx previa lo previene)
        domain = email.split('@')[-1].lower()

        if domain not in allowed_domains:
            raise ValidationError(
                f"El dominio '{domain}' no está permitido. Solo se aceptan correos de Gmail o Hotmail."
            )
            
        return email # Retorna el valor limpio

    # MÉTODO DE VALIDACIÓN GENERAL (clean) para contraseñas
    def clean(self):
        cleaned_data = super().clean()
        password_fields = ['password2'] 

        for field_name in password_fields:
            password = cleaned_data.get(field_name)
            
            # Validación: No se permiten espacios en contraseñas
            if password and ' ' in password:
                self.add_error('password1', "La contraseña no puede contener espacios en blanco.")
                if field_name in cleaned_data:
                    # Elimina el campo limpio para forzar una nueva entrada
                    del cleaned_data[field_name] 
        
        return cleaned_data