# tasks/forms/profile_form.py
from django import forms
from django.core.exceptions import ValidationError 
import re 

from ..models import Profile

# Clase ProfileForm: Formulario para capturar los datos personales del solicitante.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nombre_completo', 'apellido_completo', 'genero', 
            'cedula_identidad', 'fecha_nacimiento', 'numero_telefono'
        ]
        
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre', 'required': 'required'}),
            'apellido_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu apellido', 'required': 'required'}),
            'genero': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'cedula_identidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu cédula de identidad', 'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'numero_telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu número telefónico', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].label = "Nombre Completo"
        self.fields['apellido_completo'].label = "Apellido Completo"
        self.fields['genero'].label = "Sexo"
        self.fields['cedula_identidad'].label = "Cédula de Identidad (Máx. 8 dígitos)"
        self.fields['fecha_nacimiento'].label = "Fecha de Nacimiento"
        self.fields['numero_telefono'].label = "Número de Teléfono (Máx. 11 dígitos)"


    # --- 1. VALIDACIÓN PARA NOMBRE (Solo Letras y Espacios) ---
    def _validate_only_letters(self, field_name, label):
        """Método helper para validar que un campo solo contenga letras y espacios."""
        value = self.cleaned_data.get(field_name)
        
        if value:
            if not re.match(r'^[a-zA-Z\sñÑáéíóúÁÉÍÓÚ]+$', value):
                raise ValidationError(
                    f"El campo '{label}' solo puede contener letras y espacios, no se permiten números ni caracteres especiales."
                )
        return value

    def clean_nombre_completo(self):
        return self._validate_only_letters('nombre_completo', self.fields['nombre_completo'].label)

    def clean_apellido_completo(self):
        return self._validate_only_letters('apellido_completo', self.fields['apellido_completo'].label)


    # --- 2. VALIDACIÓN PARA CÉDULA (Máximo 8 Dígitos) ---
    def clean_cedula_identidad(self):
        cedula = self.cleaned_data.get('cedula_identidad')
        
        if cedula is not None:
            cedula_str = str(cedula) 
        
            if len(cedula_str) > 8:
                raise ValidationError(
                    "La Cédula de Identidad no puede tener más de 8 dígitos."
                )
        
        return cedula


    # --- 3. VALIDACIÓN PARA NÚMERO DE TELÉFONO (Máximo 11 Dígitos) ---
    def clean_numero_telefono(self):
        telefono = self.cleaned_data.get('numero_telefono')
        
        if telefono is not None:
            telefono_str = str(telefono) 
            
            if len(telefono_str) > 11:
                raise ValidationError(
                    "El Número de Teléfono no puede tener más de 11 dígitos."
                )

        return telefono