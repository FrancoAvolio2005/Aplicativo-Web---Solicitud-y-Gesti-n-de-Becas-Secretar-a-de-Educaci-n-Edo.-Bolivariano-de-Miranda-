# Importa la funcionalidad de modelos de Django.
from django.db import models
# Importa el modelo de usuario por defecto de Django para relaciones.
from django.contrib.auth.models import User
# Importa utilidades de tiempo de Django.
from django.utils import timezone
# Importa la señal post_save, que se dispara después de guardar un objeto.
from django.db.models.signals import post_save
# Importa el decorador receiver para conectar funciones a señales.
from django.dispatch import receiver
# Create your models here.

# ----------------------------------------------------------------------
class Task(models.Model):
    title = models.CharField(max_length=200)
    descriptio = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datacompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '- by ' +self.user.username

class Certificado(models.Model):
    fecha = models.DateTimeField(null=True,blank=True)
    completo = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha + '- by ' +self.user.username

# Modelo Becas: Catálogo de las diferentes becas disponibles.
class Becas(models.Model):
    # Clave primaria autoincremental para la beca.
    id_beca = models.AutoField(primary_key=True, verbose_name="ID Beca")
    # Nombre de la beca.
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    # Descripción detallada de la beca.
    descripcion = models.TextField(verbose_name="Descripción")

    # Función __str__: Retorna el nombre de la beca para una representación legible.
    def __str__(self):
        return f"{self.nombre}"   #(ID: {self.id_beca}), esto se coloca al lado de {self.nombre} solamente para ver el ID de la beca, no tan necesario por ahora, se puede colocar si lo piden en la secretaría

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        # Nombre singular legible para el administrador de Django.
        verbose_name = "Beca"
        # Nombre plural legible para el administrador de Django.
        verbose_name_plural = "Becas"

# ----------------------------------------------------------------------
# Modelo Plantel: Catálogo de las instituciones educativas (planteles).
class Plantel(models.Model):
    
    # Opciones predefinidas para el campo estado_plantel.
    ESTADO_CHOICES = [
        ('Amazonas', 'Amazonas'), ('Anzoátegui', 'Anzoátegui'), ('Apure', 'Apure'),
        ('Aragua', 'Aragua'), ('Barinas', 'Barinas'), ('Bolívar', 'Bolívar'),
        ('Carabobo', 'Carabobo'), ('Cojedes', 'Cojedes'), ('Delta Amacuro', 'Delta Amacuro'),
        ('Falcón', 'Falcón'), ('Guárico', 'Guárico'), ('Lara', 'Lara'),
        ('Mérida', 'Mérida'), ('Miranda', 'Miranda'), ('Monagas', 'Monagas'),
        ('Nueva Esparta', 'Nueva Esparta'), ('Portuguesa', 'Portuguesa'), ('Sucre', 'Sucre'),
        ('Táchira', 'Táchira'), ('Trujillo', 'Trujillo'), ('Vargas', 'Vargas'),
        ('Yaracuy', 'Yaracuy'), ('Zulia', 'Zulia'), ('Distrito Capital', 'Distrito Capital'),
        ('Dependencias Federales', 'Dependencias Federales'),
    ]

    # Opciones predefinidas para el campo tipo_dependencia.
    DEPENDENCIA_CHOICES = [
        ('estadal', 'Estadal'), ('nacional', 'Nacional'), ('privada', 'Privada'),
        ('autonoma', 'Autónoma'), ('privada_mppe', 'Privada subvencionada por MPPE'),
        ('privada_oficial', 'Privada subvencionada por Oficial'),
    ]

    # Opciones predefinidas para el campo modalidad_principal.
    MODALIDAD_CHOICES = [
        ('jovenes', 'Jóvenes'), ('adultos', 'Adultos y adultas'),
        ('regular', 'Sistema Regular'), ('especial', 'Educación Especial'),
    ]

    # Opciones predefinidas para el campo estatus_plantel.
    ESTATUS_CHOICES = [
        ('activo', 'Activo'), ('inactivo', 'Inactivo'),
    ]

    # Nombre del plantel.
    nombre_plantel = models.CharField(max_length=255, verbose_name="Nombre del Plantel")
    # Estado donde se ubica el plantel, usando las opciones predefinidas.
    estado_plantel = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        verbose_name="Estado del Plantel"
    )
    # Municipio del plantel.
    municipio_plantel = models.CharField(max_length=100, verbose_name="Municipio del Plantel")
    # Código único del plantel.
    codigo_plantel = models.CharField(max_length=20, unique=True, verbose_name="Código del Plantel")
    # Tipo de dependencia (estatal, nacional, privada, etc.), usando opciones predefinidas.
    tipo_dependencia = models.CharField(
        max_length=20,
        choices=DEPENDENCIA_CHOICES,
        verbose_name="Tipo de Dependencia"
    )
    # Modalidad principal de educación que ofrece, usando opciones predefinidas.
    modalidad_principal = models.CharField(
        max_length=20,
        choices=MODALIDAD_CHOICES,
        verbose_name="Modalidad Principal"
    )
    # Estatus actual del plantel (activo o inactivo), por defecto 'activo'.
    estatus_plantel = models.CharField(
        max_length=10,
        choices=ESTATUS_CHOICES,
        default='activo',
        verbose_name="Estatus del Plantel"
    )

    # Función __str__: Retorna el nombre del plantel para una representación legible.
    def __str__(self):
        return self.nombre_plantel

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Plantel"
        verbose_name_plural = "Planteles"

# ----------------------------------------------------------------------
# Modelo Estado: Catálogo de estados geográficos.
class Estado(models.Model):
    # Nombre del estado, debe ser único.
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Estado")

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        # Ordena los resultados por el nombre del estado.
        ordering = ['nombre']

    # Función __str__: Retorna el nombre del estado.
    def __str__(self):
        return self.nombre

# ----------------------------------------------------------------------
# Modelo Municipio: Catálogo de municipios, dependientes de un Estado.
class Municipio(models.Model):
    # Nombre del municipio.
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Municipio")
    # Clave foránea que relaciona el municipio con un Estado.
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='municipios', verbose_name="Estado")

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        # Asegura que la combinación de nombre y estado sea única.
        unique_together = ('nombre', 'estado')
        # Ordena los resultados por el nombre del municipio.
        ordering = ['nombre']

    # Función __str__: Retorna el nombre del municipio y el nombre del estado al que pertenece.
    def __str__(self):
        return f"{self.nombre} ({self.estado.nombre})"

# ----------------------------------------------------------------------
# Modelo Parroquia: Catálogo de parroquias, dependientes de un Municipio.
class Parroquia(models.Model):
    # Nombre de la parroquia.
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Parroquia")
    # Clave foránea que relaciona la parroquia con un Municipio.
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='parroquias', verbose_name="Municipio")

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Parroquia"
        verbose_name_plural = "Parroquias"
        # Asegura que la combinación de nombre y municipio sea única.
        unique_together = ('nombre', 'municipio')
        # Ordena los resultados por el nombre de la parroquia.
        ordering = ['nombre']

    # Función __str__: Retorna el nombre de la parroquia, municipio y estado para una representación completa.
    def __str__(self):
        return f"{self.nombre} ({self.municipio.nombre}, {self.municipio.estado.nombre})"

# ----------------------------------------------------------------------
# Modelo Banco: Catálogo de entidades bancarias.
class Banco(models.Model):
    # Nombre del banco, debe ser único.
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Banco")
    # Código bancario, debe ser único y es opcional.
    codigo_bancario = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Código Bancario")

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"
        # Ordena los resultados por el nombre del banco.
        ordering = ['nombre']

    # Función __str__: Retorna el nombre del banco.
    def __str__(self):
        return self.nombre

# ----------------------------------------------------------------------
# Modelo EstatusBeca: Catálogo de posibles estatus para una solicitud de beca.
class EstatusBeca(models.Model):
    # Nombre del estatus (ej. 'En proceso', 'Aprobada', 'Rechazada'), debe ser único.
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Estatus")
    # Descripción detallada del estatus, es opcional.
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Estatus")

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Estatus de Beca"
        verbose_name_plural = "Estatus de Becas"
        # Ordena los resultados por el nombre del estatus.
        ordering = ['nombre']

    # Función __str__: Retorna el nombre del estatus.
    def __str__(self):
        return self.nombre

# ----------------------------------------------------------------------
# Función auxiliar para obtener o crear el estatus 'En proceso' por defecto.
def get_default_estatus_beca():
    # Busca el estatus 'En proceso', si no existe, lo crea.
    estatus_beca, created = EstatusBeca.objects.get_or_create(nombre='En proceso')
    # Retorna la instancia del estatus.
    return estatus_beca

# ----------------------------------------------------------------------
# Modelo Solicitud: Almacena la información principal de la solicitud de beca.
class Solicitud(models.Model):
    # Clave primaria autoincremental para la solicitud.
    id_solicitud = models.AutoField(primary_key=True, verbose_name="ID de la solicitud")
    # Claves foráneas a modelos geográficos (Estado, Parroquia, Municipio) y catálogos (Plantel, Becas, Banco).
    # Todas son opcionales y se enlazan al modelo Solicitud.
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Estado", null=True, blank=True)
    parroquia = models.ForeignKey(Parroquia, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Parroquia", null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Municipio", null=True, blank=True)
    plantel = models.ForeignKey(Plantel, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Plantel", null=True, blank=True)
    beca = models.ForeignKey(Becas, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Beca a solicitar", null=True, blank=True)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Banco", null=True, blank=True)
    # Clave foránea al estatus de la beca, usando la función get_default_estatus_beca como valor por defecto.
    estatus_beca = models.ForeignKey(EstatusBeca, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Estatus de la Beca", null=True, blank=True, default=get_default_estatus_beca)
    # Clave foránea al usuario que realiza la solicitud.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Usuario", null=True, blank=True)
    # Fecha de creación de la solicitud, se establece automáticamente al crearse.
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    # Campos de tipo ImageField para subir los documentos requeridos.
    constancia_estudios = models.ImageField(upload_to='constancias/', verbose_name="Constancia de Estudios (JPG)", null=True, blank=True)
    constancia_numero_cuenta = models.ImageField(upload_to='constancias/', verbose_name="Constancia de Número de Cuenta (JPG)", null=True, blank=True)
    boletin = models.ImageField(upload_to='boletines/', verbose_name="Boletín (JPG)", null=True, blank=True)
    cedula = models.ImageField(upload_to='cedulas/', verbose_name="Cédula de Identidad (JPG)", null=True, blank=True)
    # Número de cuenta bancaria del becario.
    numero_de_cuenta = models.CharField(max_length=50, verbose_name="Número de Cuenta Bancaria", null=True, blank=True)

    # Campos de información personal del becario (que podría ser diferente al usuario que aplica).
    nombre_becario = models.CharField(max_length=100, verbose_name="Nombre del Becario", null=True, blank=True)
    apellido_becario = models.CharField(max_length=100, verbose_name="Apellido del Becario", null=True, blank=True)
    edad_becario = models.IntegerField(verbose_name="Edad del Becario", null=True, blank=True)
    cedula_becario = models.CharField(max_length=20, verbose_name="Cédula del Becario", null=True, blank=True)
    fecha_nacimiento_becario = models.DateField(verbose_name="Fecha de Nacimiento del Becario", null=True, blank=True)
    
    # Opciones predefinidas para la nacionalidad del becario.
    NACIONALIDAD_CHOICES = [
        ('V', 'Venezolano'),
        ('E', 'Extranjero'),
    ]
    # Campo para la nacionalidad, usando las opciones predefinidas.
    nacionalidad_becario = models.CharField(
        max_length=1, 
        choices=NACIONALIDAD_CHOICES, 
        verbose_name="Nacionalidad del Becario", 
        null=True, 
        blank=True
    )
    
    # Teléfono y dirección residencial del becario.
    telefono_becario = models.CharField(max_length=15, verbose_name="Teléfono del Becario", null=True, blank=True)
    direccion_residencial_becario = models.CharField(max_length=255, verbose_name="Dirección Residencial del Becario", null=True, blank=True)
    motivo_rechazo = models.TextField(verbose_name="Motivo de Rechazo", null=True, blank=True)

    # Función __str__: Retorna una descripción de la solicitud (usuario y beca solicitada).
    def __str__(self):
        beca_nombre = self.beca.nombre if self.beca else "Desconocida"
        user_username = self.user.username if self.user else "Usuario Desconocido"
        return f"Solicitud de {user_username} para la beca {beca_nombre}"

    # Clase Meta: Configuración interna del modelo.
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

# ----------------------------------------------------------------------
# Modelo Profile: Extensión del modelo User de Django para almacenar datos adicionales del usuario.
class Profile(models.Model):
    # Relación uno a uno con el modelo User, es el núcleo del Profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Campos de datos personales adicionales.
    nombre_completo = models.CharField(max_length=100, help_text="Nombre(s) completo(s)")
    apellido_completo = models.CharField(max_length=100, help_text="Apellido(s) completo(s)")
    edad = models.IntegerField(null=True, blank=True, help_text="Edad del usuario")
    
    # Opciones predefinidas para el género.
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    # Campo de género, usando las opciones predefinidas.
    genero = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text="Género del usuario"
    )

    # Cédula de identidad, debe ser única y es opcional.
    cedula_identidad = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text="Número de Cédula de Identidad")
    # Fecha de nacimiento, opcional.
    fecha_nacimiento = models.DateField(null=True, blank=True, help_text="Fecha de nacimiento del usuario")
    # Número de teléfono, opcional.
    numero_telefono = models.CharField(max_length=15, blank=True, null=True, help_text="Número de teléfono de contacto")

    # Indicador booleano para identificar si el usuario es un "Analista Exterior CDCE".
    is_analista_exterior = models.BooleanField(default=False, verbose_name="Es Analista Exterior CDCE")

    # Función __str__: Retorna el perfil asociado al nombre de usuario.
    def __str__(self):
        return f'Perfil de {self.user.username}'

# ----------------------------------------------------------------------
# Función create_user_profile: Receptor de señal (Signal Receiver).
# Se conecta a la señal post_save del modelo User.
@receiver(post_save, sender=User)
# Se ejecuta CADA VEZ que se guarda un objeto User.
def create_user_profile(sender, instance, created, **kwargs):
    # Condición: Solo se ejecuta si el objeto User acaba de ser creado.
    if created:
        # Crea un nuevo objeto Profile y lo asocia al nuevo usuario.
        Profile.objects.create(user=instance)

# ----------------------------------------------------------------------
# Función save_user_profile: Receptor de señal (Signal Receiver).
# Se conecta a la señal post_save del modelo User.
@receiver(post_save, sender=User)
# Se ejecuta CADA VEZ que se guarda un objeto User.
def save_user_profile(sender, instance, **kwargs):
    # Condición: Verifica si la instancia de User tiene un objeto Profile asociado.
    if hasattr(instance, 'profile'):
        # Si tiene un Profile, lo guarda (actualizando los datos del perfil).
        instance.profile.save()