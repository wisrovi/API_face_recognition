from io import BytesIO

from app.shared.FaceRecognition.FaceRecognition import FaceRecognition
from app.shared.FaceRecognition.Facecode_AES import Facecode_AES
from app.shared.Image import Image


class TestFaceCodeAES:
    def test_facerecognition(self):
        robert_1 = FaceRecognition("/app/test/resources/robert_1.jpg")
        robert_1 = {"name": "Robert", "vector": robert_1.vector}

        all_vectors = [robert_1["vector"]]
        all_names = [robert_1["name"]]

        robert_2 = FaceRecognition("/app/test/resources/robert_2.jpg")
        result = robert_2.compare(all_vectors, all_names)
        assert result == robert_1["name"]
        assert robert_2.vector.any()

    def test_facecode(self):
        face_code = Facecode_AES(max_distance=0.9)

        face_code.path = "/app/test/resources/robert_1.jpg"
        buffer = BytesIO()
        person_1 = {"name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result == person_1["name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pillow(self):
        face_code = Facecode_AES(max_distance=0.9)
        image = Image()

        buffer_image = image.put_image_in_buffer("/app/test/resources/robert_1.jpg")
        face_code.path = buffer_image

        person_1 = {"name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result == person_1["name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_using_celery(self):
        pass
        assert True
