import logging
from pathlib import Path

MESSAGES_LOG_VIEW = logging.DEBUG


key_AES = "www.wisrovi.com"
MaxFaceDistanceInVector_forRecognition = 0.45 # 0.4
FrecuenciaActualizarBaseDatosRostros = 600 # segundos

BASE_DIR = str(Path(__file__).resolve().parent.parent) + "/database"

DATABASE_CONECTION = {
  'user': 'root',
  'password': '12345678',
  'host': 'localhost', #'127.0.0.1',
  'database': 'AES_FaceRecognition',
  'raise_on_warnings': True
}