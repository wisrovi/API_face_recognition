import os
import requests
import pytest


def open_image(file_name):
    name = file_name.split(os.sep)[-1]
    return (name, open(file_name, "rb"), "image/jpeg")


if os.environ.get("DEBUG"):
    BASE_URL = "http://api:1722"
    FOLDER_IMAGES_TEST = "/app/test/resources/u/"
else:
    BASE_URL = "http://0.0.0.0:1722"
    FOLDER_IMAGES_TEST = "resources/u"

data_images = []
for file_name in sorted(
    [x for x in os.listdir(FOLDER_IMAGES_TEST) if x.endswith(".jpg")][:5]
):
    data_images.append(
        {
            "send": ("faces", open_image(f"{FOLDER_IMAGES_TEST}/{file_name}")),
            "fingerprint": "",
            "name": file_name.split(os.sep)[-1].split(".")[0],
            "id": -1,
        }
    )


# Fixture que se ejecutará antes y después de cada método de prueba
@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Código a ejecutar antes de cada método de prueba
    yield
    # Código a ejecutar después de cada método de prueba


# Fixture que se ejecutará antes de todos los métodos de prueba en la clase
@pytest.fixture(scope="class", autouse=True)
def class_setup_and_teardown(request):
    # Código a ejecutar antes de todos los métodos de prueba en la clase
    yield
    # Código a ejecutar después de todos los métodos de prueba en la clase
    if os.path.exists("/app/fingerprintdb.db"):
        os.remove("/app/fingerprintdb.db")


# Test class
class TestAPI:
    def test_faces_to_fingerprint(self):
        faces_to_fingerprint_url = f"{BASE_URL}/faces_to_fingerprint"
        faces_to_fingerprint_files = [s["send"] for s in data_images]
        faces_to_fingerprint_data = {
            "company": "HACENDADO",
            "group": "Naranja",
            "save_db": True,
        }

        # print("0. Hallar Huella Dactilar con Opción de Guardar:")
        response = requests.post(
            faces_to_fingerprint_url,
            files=faces_to_fingerprint_files,
            data=faces_to_fingerprint_data,
        )

        if response.status_code != 200:
            print(response)
            assert False

        for i, result in enumerate(response.json()["indices"]):
            data_images[i]["fingerprint"] = response.json()["fingerprint"][i]
            data_images[i]["id"] = response.json()["indices"][i]

        assert True

    def test_fingerprint_vs_database(self):
        fingerprint_data = [s["fingerprint"] for s in data_images]
        for i, fingerprint in enumerate(fingerprint_data):
            if len(fingerprint) == 0:
                print(f"Error: {data_images[i]['name']} no tiene huella dactilar")
                assert False

        # Ruta para comparar huellas dactilares con la base de datos
        fingerprint_url = f"{BASE_URL}/fingerprint_vs_database"
        fingerprint_data = {
            "fingerprints": fingerprint_data,
            "company": "HACENDADO",
            "group": "Naranja",
        }

        print("1. Comparación de Huellas Dactilares:")
        response = requests.post(fingerprint_url, data=fingerprint_data)
        matched_indices = response.json()["matched_indices"]
        matched_indices = [sorted(x) for x in matched_indices]

        assert len(matched_indices) == 5
        assert len(matched_indices[0]) == 3
        assert len(matched_indices[1]) == 4
        assert len(matched_indices[2]) == 3
        assert len(matched_indices[3]) == 4
        assert len(matched_indices[4]) == 1

        assert matched_indices[0] == [1, 2, 4]
        assert matched_indices[1] == [1, 2, 3, 4]
        assert matched_indices[2] == [2, 3, 4]
        assert matched_indices[3] == [1, 2, 3, 4]
        assert matched_indices[4] == [5]

    def test_faces_vs_database(self):
        # Ruta para comparar rostros con la base de datos
        faces_url = f"{BASE_URL}/faces_vs_database"
        faces_files = [
            ("images", open_image(f"{FOLDER_IMAGES_TEST}/robert_1.jpg")),
            ("images", open_image(f"{FOLDER_IMAGES_TEST}/robert_2.jpg")),
        ]
        faces_data = {
            "company": "HACENDADO",
            "group": "Naranja",
        }
        print("2. Comparación de Rostros:")
        response = requests.post(faces_url, files=faces_files, data=faces_data)

        matched_indices = response.json()["matched_indices"]
        matched_indices = [sorted(x) for x in matched_indices]

        assert len(matched_indices) == 2
        assert len(matched_indices[0]) == 3
        assert len(matched_indices[1]) == 3

        assert matched_indices[0] == [1, 2, 4]
        assert matched_indices[1] == [1, 2, 4]

    def test_face_vs_fingerprint(self):
        # Ruta para comparar rostro con huella dactilar
        face_fingerprint_url = f"{BASE_URL}/face_vs_fingerprint"
        face_fingerprint_files = [
            ("images", open_image(f"{FOLDER_IMAGES_TEST}/robert_1.jpg")),
            ("images", open_image(f"{FOLDER_IMAGES_TEST}/robert_2.jpg")),
        ]
        face_fingerprint_data = [s["fingerprint"] for s in data_images]
        face_fingerprint_data = {
            "fingerprints": face_fingerprint_data,
        }

        response = requests.post(
            face_fingerprint_url,
            files=face_fingerprint_files,
            data=face_fingerprint_data,
        )
        matched_indices = response.json()["matched_indices"]
        matched_indices = [sorted(x) for x in matched_indices]

        assert len(matched_indices) == 2
        assert len(matched_indices[0]) == 3
        assert len(matched_indices[1]) == 3

        assert matched_indices[0] == [0, 1, 3]
        assert matched_indices[1] == [0, 1, 3]

    def test_fingerprint_vs_fingerprint(self):
        # Ruta para comparar huella dactilar con huella dactilar
        fingerprint_fingerprint_url = f"{BASE_URL}/fingerprint_vs_fingerprint"
        fingerprint_fingerprint_data = {
            "fingerprint1": [s["fingerprint"] for s in data_images],
            "fingerprint2": [s["fingerprint"] for s in data_images],
        }
        print("4. Comparación de Huella Dactilar con Huella Dactilar:")
        response = requests.post(
            fingerprint_fingerprint_url, data=fingerprint_fingerprint_data
        )
        matched_indices = response.json()["matched_indices"]
        matched_indices = [sorted(x) for x in matched_indices]

        assert len(matched_indices) == 5
        assert len(matched_indices[0]) == 3
        assert len(matched_indices[1]) == 4
        assert len(matched_indices[2]) == 3
        assert len(matched_indices[3]) == 4
        assert len(matched_indices[4]) == 1

        assert matched_indices[0] == [0, 1, 3]
        assert matched_indices[1] == [0, 1, 2, 3]
        assert matched_indices[2] == [1, 2, 3]
        assert matched_indices[3] == [0, 1, 2, 3]
        assert matched_indices[4] == [4]

    def test_face_vs_face(self):
        # Ruta para comparar rostro con rostros
        face_face_url = f"{BASE_URL}/face_vs_face"

        face_face_files = [
            ("images1", open_image(f"{FOLDER_IMAGES_TEST}/robert_1.jpg")),
            ("images1", open_image(f"{FOLDER_IMAGES_TEST}/yann_lecun1.jpg")),
            ("images2", open_image(f"{FOLDER_IMAGES_TEST}/yann_lecun2.jpg")),
            ("images2", open_image(f"{FOLDER_IMAGES_TEST}/yann_lecun3.jpg")),
            ("images2", open_image(f"{FOLDER_IMAGES_TEST}/robert_2.jpg")),
            ("images2", open_image(f"{FOLDER_IMAGES_TEST}/yann_lecun4.jpg")),
        ]

        response = requests.post(face_face_url, files=face_face_files)
        matched_indices = response.json()["matched_indices"]
        matched_indices = [sorted(x) for x in matched_indices]

        assert len(matched_indices) == 2
        assert len(matched_indices[0]) == 1
        assert len(matched_indices[1]) == 3

        assert matched_indices[0] == [2]
        assert matched_indices[1] == [0, 1, 3]


if __name__ == "__main__":
    pytest.main([__file__])
