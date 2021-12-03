import os
from typing import List
from fastapi import File, UploadFile


def descargar_archivos(files: List[UploadFile] = File(...)):
    try:
        os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        print(e)

    list_received = list()
    for image in files:
        file_name = os.getcwd() + "/images/" + image.filename.replace(" ", "-")

        received = dict()
        received['filename'] = image.filename.replace(" ", "-")
        received['path'] = file_name
        with open(file_name, 'wb+') as f:
            f.write(image.file.read())
            f.close()

        list_received.append(received)
    return list_received


from database.Dao import Dao
from database.Database import Database
database_comando = Database()
conexion_basedatos = Dao()
def leerTodosVectores():
    contenido_tabla_vector = conexion_basedatos.leerTodo(database_comando.vector.READALL())
