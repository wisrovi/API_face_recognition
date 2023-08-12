from apis.face_recogniion.serializers import UserInDB
import jwt
from apis.face_recogniion.config import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    SECRET_KEY,
)


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return access_token


def is_allowed_file(filename):
    """
    Check if the provided filename has an allowed extension.
    """
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


def is_allowed_mime_type(content_type):
    """
    Check if the provided MIME type is allowed.
    """
    return content_type in ALLOWED_MIME_TYPES
