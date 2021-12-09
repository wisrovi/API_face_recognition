# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# probar en local
from database.modelos.ObjectForm import Vector, RolUsuario, Usuario, RelacionPersonaVector, Persona, Log, \
    Licencia, TipoDocumento

todos_tipo_documento = list()
todos_tipo_documento.append(TipoDocumento("CC", "Cedula ciudadania"))
todos_tipo_documento.append(TipoDocumento("RC", "Registro civil"))
todos_tipo_documento.append(TipoDocumento("CE", "Cedula extrangeria"))

todos_vectores = list()

todas_personas = list()
todas_personas.append(Persona(
    nombre="william", nombre_2="steve",
    apellido="rodriguez", apellido_2="villamizar",
    tipo_doc=todos_tipo_documento[0].__dict__.get("id"), num_doc="1098685961"
))

todos_rol_usuario = list()
todos_rol_usuario.append(RolUsuario("SUPER", "ERASE, UPDATE, REGISTRAR AND READ"))
todos_rol_usuario.append(RolUsuario("ADMIN", "UPDATE, REGISTRAR AND READ"))
todos_rol_usuario.append(RolUsuario("ADVANCE", "REGISTRAR AND READ"))
todos_rol_usuario.append(RolUsuario("BASIC", "READ"))

todas_relaciones_persona_vector = list()

todos_usuarios = list()
todos_usuarios.append(Usuario(
    persona=todas_personas[0].__dict__.get("id"),
    user="wisrovi", pwd="rodriguez",
    rol=todos_rol_usuario[0].__dict__.get("id"),
    email="wisrovi.rodriguez@gmail.com",
    padre="root"
))

todas_licencias = list()
todas_licencias.append(Licencia(
    id_usuario_propietario_licencia=todos_usuarios[0].__dict__.get("id"),
    dias_vencimiento=3650, registros_rostros=500, bytes=5e10, numero_hijos=5e10
))

# print("[ROOT-licence]:", todas_licencias[0].__dict__)
# print("[ROOT-user]:", todos_usuarios[0].__dict__)

todos_log = list()

DATABASE = {
    "tipo_doc": todos_tipo_documento,
    "vector": todos_vectores,
    "person": todas_personas,
    "person_vector": todas_relaciones_persona_vector,
    "users": todos_usuarios,
    "rol": todos_rol_usuario,
    "licencias": todas_licencias,
    "log": todos_log
}


# import uvicorn


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print([d.__dict__ for d in todos_rol_usuario])
    print([d.__dict__ for d in todos_tipo_documento])
    # uvicorn.run("app.api:app", host="0.0.0.0", port=5050, reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
