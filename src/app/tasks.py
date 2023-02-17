import os
from time import sleep

from celery import Celery

from shared.FaceRecognition.Facecode_AES import Facecode_AES

sleep(5)
# ----------------------------
# Celery
# ----------------------------

broker_url = os.environ.get("BROKER_RABBITMQ")
redis_url = os.environ.get("BROKER_REDIS")

if not broker_url:
    print("BROKER_RABBITMQ not found in env")
if not redis_url:
    print("BROKER_REDIS not found in env")

broker_url = "amqp://localhost" if not broker_url else broker_url
redis_url = "redis://localhost" if not redis_url else redis_url

app = Celery('tasks', broker=broker_url, backend=redis_url)
app.conf.update(
    result_expires=3600,
)


@app.task
def say_hello(name: str = "World"):
    # https://sqa-consulting.com/asynchronous-tasks-in-python-with-celery-rabbitmq-redis/
    return f"Hello {name}"


# ----------------------------
# Facecode
# ----------------------------


face_code = Facecode_AES(max_distance=0.9)


class TasksFacecode:
    @staticmethod
    @app.task
    def change_max_distance(max_distance: float):
        face_code.max_distance = max_distance
        return face_code.max_distance

    @staticmethod
    @app.task
    def get_max_distance():
        return face_code.max_distance

    @staticmethod
    def buffer_to_vector(buffer):
        face_code.path = buffer
        return face_code.fingerprint

    @staticmethod
    @app.task
    def compare_vectors(vector, vectors, names, organization_id=None):
        face_code.fingerprint = vector
        return face_code.compare_fingerprints(vectors, names)

# crear tarea para comparar un vector con una lista de vectores


# python -m celery multi start 10 -A tasks worker -l info -Q:1-3 --pool=solo
