import logging
from pathlib import Path

MESSAGES_LOG_VIEW = logging.DEBUG

key_AES = "www.wisrovi.com"
MaxFaceDistanceInVector_forRecognition = 0.45  # 0.4
FrecuenciaActualizarBaseDatosRostros = 600  # segundos

BASE_DIR = str(Path(__file__).resolve().parent.parent) + "/database"


BASEDATOS = "AES_FaceRecognition"
DATABASE_CONECTION = {
    'user': 'root',
    'password': '12345678',
    'host': 'localhost',  # '127.0.0.1',
    'database': BASEDATOS,
    'raise_on_warnings': True
}

URL_HOST_API = "http://localhost:5050"

gmail_user = 'wisrovi.rodriguez@gmail.com'
gmail_password = 'ywmxtmeaxpgdjbhr'
host = 'smtp.gmail.com'
puerto = 465