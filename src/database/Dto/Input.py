from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class TipoDocumento(str, Enum):
    cedula_ciudadania = "CC"
    registro_civil = "RC"
    cedula_extrangeria = "CE"


class RolUsuario(str, Enum):
    super = "SUPER"
    admin = "ADMIN"
    advance = "ADVANCE"
    basic = "BASIC"


class RegisterUser(BaseModel):
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_apellido: str
    tipo_documento: TipoDocumento
    numero_documento: int
    email: EmailStr
    rol: RolUsuario

    user: str
    password: str

