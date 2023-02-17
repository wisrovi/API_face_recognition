import os
import sys
from datetime import datetime


def FormatearFecha(fecha):
    formato = "%m/%d/%y %H:%M:%S"
    fecha = fecha.strftime("%x %X")
    fecha = datetime.strptime(fecha, formato)
    return fecha


def get_folder_execution(atras: bool = False, verbose: bool = False):
    # https://www.codegrepper.com/code-examples/python/python+pyinstaller+get+path+of+executable
    application_path = None
    pyinstaller = False
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
        if verbose:
            print("pyinstaller")
        pyinstaller = True
    elif __file__:
        application_path = os.path.dirname(os.path.abspath(__file__))
        if verbose:
            print("python")

    if application_path is None:
        raise Exception("No se pudo obtener el directorio de ejecucion")

    if not pyinstaller and atras:
        application_path = os.sep.join(application_path.split(os.sep)[:-1])

    return application_path


# leer argumentos de la linea de comandos
def get_args():
    args = {}
    for arg in sys.argv:
        if "=" in arg:
            key, value = arg.split("=")
            args[key] = value
    return args
