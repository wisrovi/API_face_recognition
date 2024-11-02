import gradio as gr
from util.face_recognition_control import (
    FaceRecognitionControl,
    RegisterDB,
    open_image_with_opencv,
)
from wkafka.controller.wkafka import Wkafka, Consumer_data


kafka_instance = Wkafka(server="192.168.1.137:9092", name="video_show")
face_recognition = FaceRecognitionControl()


@kafka_instance.consumer(
    topic="face_recognition",
    value_type="image",
)
def process_message(data: Consumer_data):

    img_bytes = open_image_with_opencv(img=data.value)

    results = {}

    if "register" in data.header and "dni" in data.header:
        try:
            face_recognition.person = RegisterDB(
                file=img_bytes,
                dni=data.header.get("dni"),
            )
            id_, fingerprint = face_recognition.register()

            results["id"] = id_
        except RuntimeError as ve:
            results["error"] = f"Datos inválidos: {ve}"
        except Exception as e:
            results["error"] = f"Error al registrar: {str(e)}"
    else:
        try:
            face_recognition.person = RegisterDB(
                file=img_bytes,
                distance=int(data.header.get("distance")),
            )
            results = face_recognition.search()
            return results
        except RuntimeError as ve:
            results["error"] = f"Datos inválidos: {ve}"
        except Exception as e:
            results["error"] = f"Error al buscar: {str(e)}"

    if "respond_to" in data.header:
        with kafka_instance.producer() as kf_producer:
            kf_producer.send(
                topic=data.header.get("respond_to"),
                value=results,
                key="json",
                value_type="json",
                headers=data.header,
            )


if __name__ == "__main__":
    kafka_instance.run_consumers()
