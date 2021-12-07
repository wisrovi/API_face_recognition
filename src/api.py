import datetime
import os
import secrets
from typing import List
from utils.utils import descargar_archivos, guardar_imagen
from fastapi import FastAPI, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from config.config import MaxFaceDistanceInVector_forRecognition
from libraries.AES_FaceRecognition import AES_FaceRecognition
from setup import about, About
from database.Dto.Input import RolUsuario, TipoDocumento, EmailStr
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from main import DATABASE
from database.modelos.ObjectForm import Vector, Usuario, RelacionPersonaVector, Persona, Log, Licencia

aes_fr = AES_FaceRecognition()
app = FastAPI()
security = HTTPBasic()

DATA = DATABASE.copy()


# pedir un usuario y password obligatorios para ver la base de datos
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    credenciales_maestras = DATA.get("users")[0].__dict__
    usuario_maestro = credenciales_maestras.get("user")  # string
    password_maestro = credenciales_maestras.get("pwd")  # string
    # print(credenciales_maestras)

    # https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
    correct_username = secrets.compare_digest(credentials.username, usuario_maestro)
    correct_password = secrets.compare_digest(credentials.password, password_maestro)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/about", response_model=About)
async def read_about():
    return about


@app.get("/database/all")
async def read_current_user(username: str = Depends(get_current_username)):
    DATA_RTA = dict()
    for key, value in DATA.items():
        DATA_RTA[key] = [d.__dict__ for d in value]
    return DATA_RTA


@app.get("/{licencia}/plan")
def ver_plan(licencia: str):
    plan = dict()

    licencia_encontrada = None
    for license in DATA.get("licencias"):
        licencia_guardada = license.__dict__
        if licencia_guardada.get("licencia") == licencia:
            licencia_encontrada = licencia_guardada

    if licencia_encontrada is None:
        return {"Error": "Esta licencia no existe"}

    ids_persona_asociadas = list()
    for usuarios in DATA.get("users"):
        if usuarios.__dict__.get("id_usuario_padre") == licencia_encontrada.get("id_usuario") or \
                usuarios.__dict__.get("id") == licencia_encontrada.get("id_usuario"):
            ids_persona_asociadas.append(usuarios.__dict__.get("id"))

    cantidad_hijos_asociados = len(ids_persona_asociadas) - 1

    conteo_bytes_usados = 0
    for log_uso in DATA.get("log"):
        este_log = log_uso.__dict__
        if este_log.get("id_usuario") in ids_persona_asociadas:
            conteo_bytes_usados += este_log.get("bytes_usados")

    cantidad_rostros_vectorizados = 0
    for vector in DATA.get("vector"):
        if vector.__dict__.get("id_usuario") in ids_persona_asociadas:
            cantidad_rostros_vectorizados += 1

    plan['licencia'] = licencia
    plan['fechas'] = dict(Registro=licencia_encontrada.get("fecha_registro"),
                          Expira=licencia_encontrada.get("fecha_vencimiento"))
    plan['bytes'] = dict(Usados=conteo_bytes_usados, Total=licencia_encontrada.get("plan_bytes"))
    plan['hijos'] = dict(Usados=cantidad_hijos_asociados,
                         Total=licencia_encontrada.get("cantidad_hijos_que_puede_tener"))
    plan['rostros_para_reconocimiento'] = dict(Usados=cantidad_rostros_vectorizados, Total=licencia_encontrada.get(
        "cantidad_maxima_rostros_permitidos_tabla_vector"))

    return plan


@app.post("/{licencia_autoriza}/register/userlogin")
async def register_user_login(licencia_autoriza: str,
                              foto_persona: UploadFile = File(...),
                              primer_nombre: str = Form(...),
                              segundo_nombre: str = Form(...),
                              primer_apellido: str = Form(...),
                              segundo_apellido: str = Form(...),
                              tipo_documento: TipoDocumento = Form(...),
                              numero_documento: int = Form(...),

                              email: EmailStr = Form(...),
                              rol: RolUsuario = Form(...),

                              usuario: str = Form(...),
                              password: str = Form(...)
                              ):
    global DATA
    es_hijo = None
    id_usuario_registra = None
    conteo = 0
    for licencia in DATA.get("licencias"):
        if licencia.__dict__.get("licencia") == licencia_autoriza:
            id_usuario_registra = licencia.__dict__.get("id_usuario")
            limite_hijos = licencia.__dict__.get("cantidad_hijos_que_puede_tener")

            fecha_vencimiento = licencia.__dict__.get("fecha_vencimiento")
            hoy = datetime.datetime.now()
            if fecha_vencimiento < hoy:
                return {"Error": "Esta licencia ya expiro"}

            conteo_hijos_ya_registrados = 0
            for usuarios in DATA.get("users"):
                if usuarios.__dict__.get("id_usuario_padre") == id_usuario_registra:
                    conteo_hijos_ya_registrados += 1

            if conteo == 0:
                es_hijo = False
            else:
                es_hijo = True

            if conteo_hijos_ya_registrados >= limite_hijos:
                return {"Error": f"Esta licencia no permite tener mas hijos asignados, el limite es {limite_hijos}"}

            break
        conteo += 1

    if id_usuario_registra is None:
        return {"Error": "Esta licencia no esta autorizada o no es valida"}

    received = guardar_imagen(foto_persona)
    nombre_archivo = received.get("path")
    str_person = aes_fr.ImageToStr(nombre_archivo)
    os.remove(nombre_archivo)

    for rol_sel in DATA.get("rol"):
        if rol_sel.__dict__.get("rol_usuario") == rol.__dict__.get('_value_'):
            rol = rol_sel
            break

    for tipo_doc in DATA.get("tipo_doc"):
        if tipo_doc.__dict__.get("tipo_documento") == tipo_documento.__dict__.get('_value_'):
            tipo_documento = tipo_doc
            break

    new_person = Persona(nombre=primer_nombre, nombre_2=segundo_nombre,
                         apellido=primer_apellido, apellido_2=segundo_apellido,
                         tipo_doc=tipo_documento.__dict__.get("id"), num_doc=numero_documento
                         )
    new_user = Usuario(persona=new_person.__dict__.get("id"),
                       user=usuario, pwd=password, email=email, rol=rol.__dict__.get("id"),
                       padre=id_usuario_registra
                       )

    new_vector = Vector(vector_str=str_person,
                        persona=new_user.__dict__.get("id"),
                        nombre_imagen=foto_persona.filename)

    new_relation = RelacionPersonaVector(persona=new_person.id,
                                         vector=new_vector.id,
                                         registra=id_usuario_registra)

    if not es_hijo:
        licencia = Licencia(id_usuario_propietario_licencia=new_user.__dict__.get("id"), numero_hijos=1)
        DATA.get("licencias").append(licencia)

    DATA.get("vector").append(new_vector)
    DATA.get("person_vector").append(new_relation)
    DATA.get("users").append(new_user)
    DATA.get("person").append(new_person)

    return {
        "vector": new_vector.__dict__.get("vector"),
        "person": new_person.__dict__,
        "user": new_user.__dict__.get("user"),
        "file": nombre_archivo,
        "note": f"Al correo {email} fue enviado el codigo de licencia para el uso de la API"
    }


@app.post("/{licencia}/register/personaRecognition")
async def register_user_login(licencia: str,
                              foto_persona: UploadFile = File(...),
                              primer_nombre: str = Form(...),
                              segundo_nombre: str = Form(...),
                              primer_apellido: str = Form(...),
                              segundo_apellido: str = Form(...),
                              tipo_documento: TipoDocumento = Form(...),
                              numero_documento: int = Form(...),
                              ):
    global DATA
    id_usuario_registra = None
    conteo = 0
    for licencia_obj in DATA.get("licencias"):
        if licencia_obj.__dict__.get("licencia") == licencia:
            id_usuario_registra = licencia_obj.__dict__.get("id_usuario")

            fecha_vencimiento = licencia_obj.__dict__.get("fecha_vencimiento")
            hoy = datetime.datetime.now()
            if fecha_vencimiento < hoy:
                return {"Error": "Esta licencia ya expiro"}

            cantidad_maxima_rostros_permitidos_tabla_vector = licencia_obj.__dict__.get(
                "cantidad_maxima_rostros_permitidos_tabla_vector")
            cantidad_rostros_vectorizados = 0
            for vector in DATA.get("vector"):
                if vector.__dict__.get("id_usuario") in [id_usuario_registra]:
                    cantidad_rostros_vectorizados += 1
            if cantidad_rostros_vectorizados >= cantidad_maxima_rostros_permitidos_tabla_vector:
                return {
                    "Error": f"Esta licencia no permite tener mas rostros vectorizados, el limite es {cantidad_maxima_rostros_permitidos_tabla_vector}."}
            break
        conteo += 1

    if id_usuario_registra is None:
        return {"Error": "Esta licencia no esta autorizada o no es valida"}

    received = guardar_imagen(foto_persona)
    nombre_archivo = received.get("path")
    str_person = aes_fr.ImageToStr(nombre_archivo)
    os.remove(nombre_archivo)

    for tipo_doc in DATA.get("tipo_doc"):
        if tipo_doc.__dict__.get("tipo_documento") == tipo_documento.__dict__.get('_value_'):
            tipo_documento = tipo_doc
            break

    new_person = Persona(nombre=primer_nombre, nombre_2=segundo_nombre,
                         apellido=primer_apellido, apellido_2=segundo_apellido,
                         tipo_doc=tipo_documento.__dict__.get("id"), num_doc=numero_documento
                         )

    new_vector = Vector(vector_str=str_person,
                        persona=id_usuario_registra,
                        nombre_imagen=foto_persona.filename)

    new_relation = RelacionPersonaVector(persona=new_person.id,
                                         vector=new_vector.id,
                                         registra=id_usuario_registra)

    DATA.get("vector").append(new_vector)
    DATA.get("person_vector").append(new_relation)
    DATA.get("person").append(new_person)

    return {
        "vector": new_vector.__dict__.get("vector"),
        "person": new_person.__dict__,
        "file": nombre_archivo
    }


@app.post("/{licencia}/identify/")
async def identify_person(
        licencia: str,
        files: List[UploadFile] = File(...)):
    licencia_encontrada = None
    for license in DATA.get("licencias"):
        licencia_guardada = license.__dict__
        if licencia_guardada.get("licencia") == licencia:
            licencia_encontrada = licencia_guardada
    if licencia_encontrada is None:
        return {"Error": "Esta licencia no existe"}
    ids_persona_asociadas = list()
    for usuarios in DATA.get("users"):
        if usuarios.__dict__.get("id_usuario_padre") == licencia_encontrada.get("id_usuario") or \
                usuarios.__dict__.get("id") == licencia_encontrada.get("id_usuario"):
            ids_persona_asociadas.append(usuarios.__dict__.get("id"))

    conteo_bytes_usados = 0
    for log_uso in DATA.get("log"):
        este_log = log_uso.__dict__
        if este_log.get("id_usuario") in ids_persona_asociadas:
            conteo_bytes_usados += este_log.get("bytes_usados")
    if conteo_bytes_usados > licencia_encontrada.get("plan_bytes"):
        return {"Error": "Ya se ha consumido el limite de bytes disponibles para esta licencia"}

    ids_vectores_conocidos = list()
    vectores_personas_conocidas = list()
    nombres_personas_conocidas = list()
    for vector in DATA.get("vector"):
        if vector.__dict__.get("id_usuario") in ids_persona_asociadas:
            vector_str = vector.__dict__.get("vector")
            id_vector = vector.__dict__.get("id")
            vector_matrix = aes_fr.StrToVector(vector_str)
            ids_vectores_conocidos.append(id_vector)
            vectores_personas_conocidas.append(vector_matrix)

    for vector in DATA.get("person_vector"):
        if vector.__dict__.get("id_vector") in ids_vectores_conocidos:
            nombres_personas_conocidas.append(vector.__dict__.get("id_persona"))

    # print(vectores_personas_conocidas, nombres_personas_conocidas)

    received = descargar_archivos(files=files)

    for value in received:
        rutaImagen = value['path']
        # str_person = aes_fr.ImageToStr(rutaImagen)
        # value['vector'] = str_person

        nombre_persona = aes_fr.Search(vectores_personas_conocidas, nombres_personas_conocidas, value['path'])
        os.remove(value['path'])

        value[
            'persona'] = f"La persona que aparece en la imagen no esta registrada, no hay ningun coincidencia con el factor de {MaxFaceDistanceInVector_forRecognition} de tolerancia."
        for person in DATA.get("person"):
            id_this_person = person.__dict__
            if id_this_person.get("id") == nombre_persona:
                value['persona'] = id_this_person

        new_log = Log(usuario=licencia_encontrada.get("id_usuario"),
                      name_file=dict(file=value['path'], name=nombre_persona),
                      bytes_used=value['bytes_size'])

        DATA.get("log").append(new_log)

        conteo_bytes_usados = 0
        for log_uso in DATA.get("log"):
            este_log = log_uso.__dict__
            if este_log.get("id_usuario") in ids_persona_asociadas:
                conteo_bytes_usados += este_log.get("bytes_usados")
        if conteo_bytes_usados > licencia_encontrada.get("plan_bytes"):
            break

    return received


@app.get("/{licencia}/log")
async def read_log(
        licencia: str):
    licencia_encontrada = None
    for license in DATA.get("licencias"):
        licencia_guardada = license.__dict__
        if licencia_guardada.get("licencia") == licencia:
            licencia_encontrada = licencia_guardada
    if licencia_encontrada is None:
        return {"Error": "Esta licencia no existe"}
    ids_persona_asociadas = list()
    for usuarios in DATA.get("users"):
        if usuarios.__dict__.get("id_usuario_padre") == licencia_encontrada.get("id_usuario") or \
                usuarios.__dict__.get("id") == licencia_encontrada.get("id_usuario"):
            ids_persona_asociadas.append(usuarios.__dict__.get("id"))

    resumen_uso_log = list()
    for log_uso in DATA.get("log"):
        este_log = log_uso.__dict__
        if este_log.get("id_usuario") in ids_persona_asociadas:
            resumen_uso_log.append(este_log)
    return resumen_uso_log


@app.get("/{licencia}/vector")
async def read_log(
        licencia: str):
    licencia_encontrada = None
    for license in DATA.get("licencias"):
        licencia_guardada = license.__dict__
        if licencia_guardada.get("licencia") == licencia:
            licencia_encontrada = licencia_guardada
    if licencia_encontrada is None:
        return {"Error": "Esta licencia no existe"}
    ids_persona_asociadas = list()
    for usuarios in DATA.get("users"):
        if usuarios.__dict__.get("id_usuario_padre") == licencia_encontrada.get("id_usuario") or \
                usuarios.__dict__.get("id") == licencia_encontrada.get("id_usuario"):
            ids_persona_asociadas.append(usuarios.__dict__.get("id"))

    resumen_vectores = list()
    for vector_uso in DATA.get("vector"):
        este_vector = vector_uso.__dict__
        if este_vector.get("id_usuario") in ids_persona_asociadas:
            resumen_vectores.append(este_vector)
    return resumen_vectores


@app.get("/{licencia}/hijos")
async def read_log(
        licencia: str):
    licencia_encontrada = None
    for license in DATA.get("licencias"):
        licencia_guardada = license.__dict__
        if licencia_guardada.get("licencia") == licencia:
            licencia_encontrada = licencia_guardada
    if licencia_encontrada is None:
        return {"Error": "Esta licencia no existe"}
    ids_persona_asociadas = list()
    for usuarios in DATA.get("users"):
        if usuarios.__dict__.get("id_usuario_padre") == licencia_encontrada.get("id_usuario") or \
                usuarios.__dict__.get("id") == licencia_encontrada.get("id_usuario"):
            ids_persona_asociadas.append(usuarios.__dict__.get("id"))

    padres = list()
    hijos = list()
    id_root = DATA.get("users")[0].__dict__.get("id_persona")
    for usuarios in DATA.get("users"):
        if usuarios.__dict__.get("id_usuario_padre") in ids_persona_asociadas:
            hijos.append(usuarios.__dict__)
        elif usuarios.__dict__.get("id") in ids_persona_asociadas:
            padres.append(usuarios.__dict__)

    return dict(Padre=padres, Hijos=hijos)

# @app.get("/")
# async def main():
#    content = """
# <body>
# <form action="/identify/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#    """
#    return HTMLResponse(content=content)