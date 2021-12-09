from pydantic import BaseModel, EmailStr
from typing import List
from typing import Optional


class About(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    packages: Optional[List[str]] = None
    url: Optional[str] = None
    license: Optional[str] = None
    author: Optional[str] = None
    author_email: Optional[str] = None
    description: Optional[str] = None
    tipo: Optional[str] = None


about = About()
about.name = 'API_face_recognition'
about.version = '1.0.1'
about.packages = [
    'cmake',
    'dlib',
    'face-recognition',
    'email-validator',
    'mysql-connector-python',
    'Pillow',
    'pycrypto',
    'pycryptodome',
    'python-dateutil',
    'python-multipart',
    'uvicorn',
    'wrapt',
    'fastapi',
    'pydantic']
about.url = 'https://github.com/wisrovi/API_face_recognition'
about.license = 'MIT'
about.author = 'wisrovi'
about.author_email = 'wisrovi.rodriguez@gmail.com'
about.description = 'Api reconocimiento facial'
about.tipo = "Demo, todo dato se perdera cuando se reinicie el sistema"
