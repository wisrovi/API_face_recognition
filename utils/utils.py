import os
from typing import List
from fastapi import File, UploadFile


def crear_carpeta_si_no_existe():
    try:
        os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        # print(e)
        pass


crear_carpeta_si_no_existe()


def guardar_imagen(image):
    file_name = os.getcwd() + "/images/" + image.filename.replace(" ", "-")

    received = dict()
    received['filename'] = image.filename.replace(" ", "-")
    received['path'] = file_name
    with open(file_name, 'wb+') as f:
        f.write(image.file.read())
        f.close()

    sizefile = os.stat(file_name).st_size
    received['bytes_size'] = sizefile
    return received


def descargar_archivos(files: List[UploadFile] = File(...)):
    crear_carpeta_si_no_existe()

    list_received = list()
    for image in files:
        received = guardar_imagen(image)
        list_received.append(received)
    return list_received


from database.Dao import Dao
from database.Database import Database

database_comando = Database()
conexion_basedatos = Dao()


def leerTodosVectores():
    contenido_tabla_vector = conexion_basedatos.leerTodo(database_comando.vector.READALL())
