# tasks/forms/solicitud_form.py
from django import forms
from django.core.exceptions import ValidationError 
from ..models import Solicitud 
import os 
import re 

# Clase SolicitudForm: Formulario para la creación y manejo de las solicitudes de beca.
class SolicitudForm(forms.ModelForm):
    
    class Meta:
        model = Solicitud
        fields = [
            'nombre_becario', 'apellido_becario', 'cedula_becario',
            'fecha_nacimiento_becario', 'nacionalidad_becario', 'direccion_residencial_becario',
            'estado', 'parroquia', 'municipio', 'plantel', 'beca',
            'constancia_estudios', 'constancia_numero_cuenta', 'boletin', 'cedula',
            'banco', 'numero_de_cuenta', 'estatus_beca'
        ]
        
        widgets = {
            'nombre_becario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el nombre del estudiante', 'required': 'required'}),
            'apellido_becario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el apellido del estudiante', 'required': 'required'}),
            'cedula_becario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la cédula de identidad del estudiante (Máx 8)', 'required': 'required'}),
            'fecha_nacimiento_becario': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            
            'nacionalidad_becario': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'direccion_residencial_becario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la dirección de vivienda del estudiante', 'required': 'required'}),
            'estado': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'parroquia': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'municipio': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'plantel': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'beca': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            
            'constancia_estudios': forms.FileInput(attrs={'class': 'form-control', 'required': 'required', 'accept': '.jpg,.jpeg'}),
            'constancia_numero_cuenta': forms.FileInput(attrs={'class': 'form-control', 'required': 'required', 'accept': '.jpg,.jpeg'}),
            'boletin': forms.FileInput(attrs={'class': 'form-control', 'required': 'required', 'accept': '.jpg,.jpeg'}),
            'cedula': forms.FileInput(attrs={'class': 'form-control', 'required': 'required', 'accept': '.jpg,.jpeg'}),
            
            'banco': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'numero_de_cuenta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejm: 01020304050607080910 (20 dígitos)', 'required': 'required'}),
            
            'estatus_beca': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_becario'].label = "Nombre del Becario"
        self.fields['apellido_becario'].label = "Apellido del Becario"
        self.fields['cedula_becario'].label = "Cédula de Identidad del Becario (Máx. 8 dígitos)"
        self.fields['fecha_nacimiento_becario'].label = "Fecha de Nacimiento del Becario"
        self.fields['nacionalidad_becario'].label = "Nacionalidad"
        self.fields['direccion_residencial_becario'].label = "Dirección Residencial"
        self.fields['estado'].label = "Estado"
        self.fields['parroquia'].label = "Parroquia"
        self.fields['municipio'].label = "Municipio"
        self.fields['plantel'].label = "Institución Educativa"
        self.fields['beca'].label = "Beca a solicitar"
        self.fields['constancia_estudios'].label = "Constancia de Estudios (.jpg)"
        self.fields['boletin'].label = "Boletín (.jpg)"
        self.fields['cedula'].label = "Cédula de Identidad (.jpg)"
        self.fields['constancia_numero_cuenta'].label = "Constancia Número de Cuenta Bancaria (.jpg)"
        self.fields['banco'].label = "Banco"
        self.fields['numero_de_cuenta'].label = "Número de Cuenta Bancaria (20 dígitos)"

    def _validate_only_letters(self, field_name):
        value = self.cleaned_data.get(field_name)
        label = self.fields[field_name].label
        
        if value:
            if not re.match(r'^[a-zA-Z\sñÑáéíóúÁÉÍÓÚ]+$', value):
                raise ValidationError(
                    f"El campo '{label}' solo puede contener letras y espacios, no se permiten números ni caracteres especiales."
                )
        return value

    def clean_nombre_becario(self):
        return self._validate_only_letters('nombre_becario')

    def clean_apellido_becario(self):
        return self._validate_only_letters('apellido_becario')

    def clean_cedula_becario(self):
        cedula = self.cleaned_data.get('cedula_becario')
        
        if cedula is not None:
            cedula_str = str(cedula) 
            if len(cedula_str) > 8:
                raise ValidationError(
                    "La Cédula del Becario no puede tener más de 8 dígitos."
                )
        return cedula

    def clean_numero_de_cuenta(self):
        cuenta = self.cleaned_data.get('numero_de_cuenta')
        
        if cuenta is not None:
            cuenta_str = str(cuenta).replace(" ", "").replace("-", "") 
            
            if len(cuenta_str) != 20:
                raise ValidationError(
                    "El Número de Cuenta Bancaria debe ser exactamente de 20 dígitos."
                )
        return cuenta
    
    def _validate_jpg_file(self, field_name):
        file = self.cleaned_data.get(field_name)
        
        if not file:
            return file

        ext = os.path.splitext(file.name)[1].lower()
        
        if ext not in ['.jpg', '.jpeg']:
            raise ValidationError(
                f"El archivo para '{self.fields[field_name].label}' debe ser en formato JPG. No se permiten archivos {ext.upper()}."
            )
            
        return file
    
    def clean_constancia_estudios(self):
        return self._validate_jpg_file('constancia_estudios')

    def clean_constancia_numero_cuenta(self):
        return self._validate_jpg_file('constancia_numero_cuenta')
        
    def clean_boletin(self):
        return self._validate_jpg_file('boletin')

    def clean_cedula(self):
        return self._validate_jpg_file('cedula')

    def clean(self):
        cleaned_data = super().clean()

        file_fields = [
            'constancia_estudios', 
            'constancia_numero_cuenta', 
            'boletin', 
            'cedula'
        ]
        
        uploaded_file_names = set()
        
        for field_name in file_fields:
            file = cleaned_data.get(field_name)
            
            if file:
                file_name = file.name.lower()
                
                if file_name in uploaded_file_names:
                    label = self.fields[field_name].label

                    self.add_error(
                        field_name, 
                        f"El archivo para '{label}' tiene el mismo nombre ('{file.name}') que otro archivo subido. Por favor, renombre uno de los archivos."
                    )
                    
                else:
                    uploaded_file_names.add(file_name)
                    
        return cleaned_data