import logging
from pathlib import Path
import os

from colorlog import ColoredFormatter

MESSAGES_LOG_VIEW = logging.DEBUG
BASE_DIR = str(Path(__file__).resolve().parent.parent) + "/logs/"
BASE_DIR = "/logs"
os.makedirs(BASE_DIR, exist_ok=True)

"""
        Configuracion del loggin
"""

# Configurar el nivel de registro global


class ErrorCriticalFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:

        return record.levelno == logging.ERROR or \
            record.levelno == logging.CRITICAL


class InfoWarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:

        return record.levelno == logging.INFO or \
                record.levelno == logging.WARNING


class DebugFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:

        return record.levelno == logging.DEBUG


class SecretFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:

        return "secreto" not in record.getMessage()


class CountFilter(logging.Filter):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.count = 0

    def filter(self, record: logging.LogRecord) -> bool:
        if self.message in record.getMessage():
            self.count += 1

            # return False
        return True


def logger_build(path: str = "", file_log: str = 'app.log') -> logging.Logger:
    formato = '> %(asctime)s - %(levelname)s - ' + \
        '[%(filename)s:%(lineno)d] - %(message)s'

    # Configurar el nivel de registro global
    logging.basicConfig(level=MESSAGES_LOG_VIEW,
                        format=formato,
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging_formatter = logging.Formatter(
        formato,
        datefmt='%Y-%m-%d %H:%M:%S')

    color_formatter = ColoredFormatter(
        formato,
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    )

    # Crear un manipulador para imprimir en la consola (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(MESSAGES_LOG_VIEW)
    console_handler.setFormatter(color_formatter)

    # Crear un manipulador para guardar en un archivo de registro
    file_handler = logging.FileHandler(
        os.path.join(path, file_log))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging_formatter)
    file_handler.addFilter(InfoWarningFilter())

    # Crear un manipulador para guardar en un archivo de registro
    file_error_handler = logging.FileHandler(
        os.path.join(path, file_log.split(".")[0]+"_error.log"))
    file_error_handler.setLevel(logging.DEBUG)
    file_error_handler.setFormatter(logging_formatter)
    file_error_handler.addFilter(ErrorCriticalFilter())

    # Crear un manipulador para guardar en un archivo de registro
    file_debug_handler = logging.FileHandler(
        os.path.join(path, file_log.split(".")[0]+"_debug.log"))
    file_debug_handler.setLevel(logging.DEBUG)
    file_debug_handler.setFormatter(logging_formatter)
    file_debug_handler.addFilter(DebugFilter())

    # Obtener el registrador raíz y agregar los manipuladores
    logger = logging.getLogger('face_recognition')
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(file_error_handler)
    logger.addHandler(file_debug_handler)

    return logger


def logger_custom(PROJECT_NAME: str) -> logging.Logger:
    contador_yolo = CountFilter('FR')
    logger = logger_build(BASE_DIR, f"{PROJECT_NAME}.log")
    logger.addFilter(contador_yolo)
    logger.addFilter(SecretFilter())

    return logger


if __name__ == "__main__":
    PROJECT_NAME = "face_recognition"
    logger = logger_custom(PROJECT_NAME)
    logger.debug('Esto es un mensaje de depuración')
    logger.info('Este es un mensaje de información')
    logger.warning('¡Cuidado! Esto es una advertencia')
    logger.error('Algo salió mal. Este es un mensaje de error')
    logger.critical('El acceso está prohibido')
