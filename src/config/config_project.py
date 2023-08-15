import os


HOST = os.environ.get("PMA_HOST", "mariaDB")+":"+os.environ.get("PMA_PORT", "3306")
USER = os.environ.get("MYSQL_USER", "fingerprint_FC_db")
PASSWORD = os.environ.get("MYSQL_PASSWORD", "secret_fingerprint_password")
DATABASE = os.environ.get("MYSQL_DATABASE", "fingerprintdb")
USE_SQLITE = bool(os.environ.get("DEBUG", False))


# Face recognition
PATH_FR = "face_code.pkl"
CONFIDENCE = float(os.environ.get("CONFIDENCE_THRESHOLD", 0.6))


# Error messages fastapi
ERROR_404_ITEM_NOT_FOUND = "The item was not found."
ERROR_533_BAD_FINGERPRINT = (533, "The fingerprint is not valid.")
