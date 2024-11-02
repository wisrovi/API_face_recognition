import os
import cv2
from pydantic import BaseModel, Field, ConfigDict
import requests
from io import BytesIO
from PIL import Image
from util.sqlite_dni import DatabaseHandler

server = os.environ.get("server", "localhost")

BASE_URL = f"http://{server}:1722"
faces_to_fingerprint_url = f"{BASE_URL}/faces_to_fingerprint"
faces_url = f"{BASE_URL}/faces_vs_database"

COMPANY = {
    "company": "eCaptureDtech",
    "group": "AIDIAGNOST",
}


def open_image_with_opencv(file_path=None, img=None):
    # Lee la imagen con OpenCV
    if img is None:
        img = cv2.imread(file_path)

    # Codifica la imagen como JPEG en memoria
    _, img_encoded = cv2.imencode(".jpg", img)
    # Convierte el resultado a un archivo en BytesIO
    img_bytes = BytesIO(img_encoded.tobytes())
    return img_bytes


def open_image_with_pillow(file_path):
    # Abre la imagen con Pillow
    img = Image.open(file_path)
    # Guarda la imagen en un archivo en memoria en formato JPEG
    img_bytes = BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)  # Restablece el puntero al inicio
    return img_bytes


class RegisterDB(BaseModel):
    file: BytesIO
    dni: str = Field("-", min_length=1, description="DNI de la persona")
    distance: int = Field(40, ge=0, le=100, description="Distancia para coincidencias")

    # Configuración para permitir tipos arbitrarios
    model_config = ConfigDict(arbitrary_types_allowed=True)


class FaceRecognitionControl:

    _person = None

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, user: RegisterDB):
        self._person = user

    def _prepare_company_data(
        self, save_db: bool = False, max_distance: float = None
    ) -> dict:
        data = COMPANY.copy()
        if save_db:
            data["save_db"] = True
        if max_distance is not None:
            data["max_distance"] = max_distance
        return data

    def _post_request(self, url: str, files: list, data: dict) -> requests.Response:
        try:
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise RuntimeError(f"Error al hacer la solicitud: {e}")

    def register(self):
        """Envía la imagen para registrar en la base de datos."""
        if not self._person.dni:
            raise ValueError("DNI es necesario para el registro.")

        company_data = self._prepare_company_data(save_db=True)
        files = [("faces", ("image.jpg", self._person.file, "image/jpeg"))]

        response = self._post_request(faces_to_fingerprint_url, files, company_data)

        datos = response.json()
        fingerprint = datos.get("fingerprint", [None])[0]
        id_ = datos.get("indices", [-1])[0]

        with DatabaseHandler() as db_handler:
            db_handler.insertar_registro(id_, fingerprint, self._person.dni)

        return id_, fingerprint

    def search(self):
        """Envía la imagen para buscar coincidencias en la base de datos."""
        distance = max(0, min(1 - (self._person.distance / 100), 1))
        company_data = self._prepare_company_data(max_distance=distance)

        files = [("images", ("image.jpg", self._person.file, "image/jpeg"))]
        response = self._post_request(faces_url, files, company_data)

        vector = response.json().get("matched_indices", [])
        matched_indices = [sorted(x) for x in vector]

        names = set()
        for id_ in matched_indices[0]:
            with DatabaseHandler() as db_handler:
                registro = db_handler.buscar_por_numero(id_)
                if registro and "dni" in registro:
                    names.add(registro["dni"])

        return str(names)
