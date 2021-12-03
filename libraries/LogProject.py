import logging
from config.config import BASE_DIR, MESSAGES_LOG_VIEW
import os

logging.basicConfig(
    level=MESSAGES_LOG_VIEW,
    format='{'
           '"Type": "%(levelname)s", '
           '"Date": "%(asctime)s", '
           '"Details": {'
           '"PathName": "%(pathname)s", '
           '"File": "%(filename)s", '
           '"Function": "%(funcName)s", '
           '"Line": "%(lineno)s", '
           '"Module": "%(module)s", '
           '"Name": "%(name)s", '
           '"Thread_number": "%(thread)s", '
           '"Thread_name": "%(threadName)s", '
           '"Process_number": "%(process)s", '
           '"Process_name": "%(processName)s" '
           '}, '
           '"Message": "%(message)s"'
           '}',
    #datefmt='%H:%M:%S',
    filename=os.path.join(BASE_DIR, 'logProject.txt')  # Para almacenar los mensajes
)
