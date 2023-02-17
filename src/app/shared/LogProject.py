import logging
from pathlib import Path

MESSAGES_LOG_VIEW = logging.DEBUG
BASE_DIR = str(Path(__file__).resolve().parent.parent) + "/database"

"""
        Configuracion del loggin
"""
import logging
from colorlog import ColoredFormatter

name_log = "logProject.txt"
formato = """
 > %(asctime)s - [%(levelname)s] 
|> [Function: %(funcName)s] 
|> [Line: %(lineno)d]
|> [Module: %(module)s]
|> [Process:%(process)d] - [%(threadName)s] 
|> %(message)s |"""
stream = logging.StreamHandler()
formatter = ColoredFormatter(
    formato.replace("|>", "%(log_color)s").replace("|", "%(reset)s |")[:-1]
)
stream.setFormatter(formatter)
logging.basicConfig(
    level=logging.DEBUG,
    format=formato,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(name_log), stream],
)
