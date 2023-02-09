from app.shared.FaceRecognition.Facecode_AES import Facecode_AES
from tasks import app

face_code = Facecode_AES(max_distance=0.9)


@app.task
def change_max_distance(max_distance: float):
    face_code.max_distance = max_distance
    return face_code.max_distance


def ok_facecode():
    print("ok_facecode")
