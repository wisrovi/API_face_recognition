# Database

HOST = ("mariaDB",)
USER = ("fingerprint_FC_db",)
PASSWORD = ("secret_fingerprint_password",)
DATABASE = ("fingerprintdb",)
USE_SQLITE = (True,)


# Face recognition
PATH_FR = "face_code.pkl"
CONFIDENCE = 0.9


# Error messages fastapi
ERROR_404_ITEM_NOT_FOUND = "The item was not found."
ERROR_533_BAD_FINGERPRINT = (533, "The fingerprint is not valid.")
