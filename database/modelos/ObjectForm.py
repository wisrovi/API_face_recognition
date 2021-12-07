import datetime
from dateutil.relativedelta import relativedelta
import uuid as UUID
from libraries.GeneradorLicenseAndToken import GeneradorLicenseAndToken

generator = GeneradorLicenseAndToken()

"""
        Tablas
"""


class Vector:
    id = str()
    vector = str()
    name_image = str()
    id_usuario = str()
    fecha_registro = datetime.datetime.now()

    def __init__(self, vector_str, nombre_imagen, persona):
        self.id = str(UUID.uuid4())
        self.vector = vector_str
        self.name_image = nombre_imagen
        self.id_usuario = persona
        self.fecha_registro = datetime.datetime.now()


class TipoDocumento:
    id = str()
    tipo_documento = str()
    descripcion = str()
    fecha_registro = datetime.datetime.now()

    def __init__(self, tipo_doc, desc):
        self.id = str(UUID.uuid4())
        self.tipo_documento = tipo_doc
        self.descripcion = desc
        self.fecha_registro = datetime.datetime.now()


class RolUsuario:
    id = str()
    rol_usuario = str()
    descripcion = str()
    fecha_registro = datetime.datetime.now()

    def __init__(self, rol, desc):
        self.id = str(UUID.uuid4())
        self.rol_usuario = rol
        self.descripcion = desc
        self.fecha_registro = datetime.datetime.now()


class Persona:
    id = str()
    primer_nombre = str()
    segundo_nombre = str()
    primer_apellido = str()
    segundo_apellido = str()
    id_tipo_documento = str()
    numero_documento = int()
    fecha_registro = datetime.datetime.now()

    def __init__(self, nombre, nombre_2, apellido, apellido_2, tipo_doc, num_doc):
        self.id = str(UUID.uuid4())
        self.primer_nombre = nombre
        self.segundo_nombre = nombre_2
        self.primer_apellido = apellido
        self.segundo_apellido = apellido_2
        self.id_tipo_documento = tipo_doc
        self.numero_documento = num_doc
        self.fecha_registro = datetime.datetime.now()


class RelacionPersonaVector:
    id = str()
    id_persona = str()
    id_vector = str()
    id_persona_registra = str()
    fecha_registro = datetime.datetime.now()

    def __init__(self, persona, vector, registra):
        self.id = str(UUID.uuid4())
        self.id_persona = persona
        self.id_vector = vector
        self.id_persona_registra = registra
        self.fecha_registro = datetime.datetime.now()


class Usuario:
    id = str()
    id_persona = str()
    user = str()
    pwd = str()
    email = str()
    id_usuario_padre = str()
    id_rol = str()
    fecha_registro = datetime.datetime.now()

    def __init__(self, persona, user, pwd, email, rol, padre):
        self.id = str(UUID.uuid4())
        self.id_persona = persona
        self.user = user
        self.pwd = pwd
        self.email = email
        self.id_rol = rol
        self.id_usuario_padre = padre
        self.fecha_registro = datetime.datetime.now()


class Licencia:
    id = str()
    id_usuario = str()
    licencia = str()
    cantidad_maxima_rostros_permitidos_tabla_vector = int()
    plan_bytes = int()
    cantidad_hijos_que_puede_tener = int()
    fecha_registro = datetime.datetime.now()
    fecha_vencimiento = datetime.datetime.now()

    def __init__(self, id_usuario_propietario_licencia,
                 dias_vencimiento=30, bytes=30000000,
                 registros_rostros=10, numero_hijos=0):
        self.id = str(UUID.uuid4())

        self.id_usuario = id_usuario_propietario_licencia

        self.licencia = generator.CrearLicencia(dias_vencimiento)[1]

        self.cantidad_maxima_rostros_permitidos_tabla_vector = registros_rostros
        self.plan_bytes = bytes
        self.cantidad_hijos_que_puede_tener = numero_hijos
        self.fecha_registro = datetime.datetime.now()
        self.fecha_vencimiento = self.fecha_registro + datetime.timedelta(days=dias_vencimiento)


class Log:
    id = str()
    id_usuario = str()
    bytes_usados = int()
    nombre_archivo = str()
    fecha_registro = datetime.datetime.now()

    def __init__(self, usuario, bytes_used, name_file):
        self.id = str(UUID.uuid4())
        self.id_usuario = usuario
        self.bytes_usados = bytes_used
        self.nombre_archivo = name_file
        self.fecha_registro = datetime.datetime.now()
