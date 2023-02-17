from shared.FaceRecognition.FaceRecognition import FaceRecognition
from shared.FaceRecognition.Facecode_AES import Facecode_AES
from shared.Image import Image
from tasks import TasksFacecode

image = Image()

tasks_facecode = TasksFacecode()


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

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/robert_1.jpg"
        )
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

    """
    def test_facecode_using_celery(self):
        tasks_facecode.change_max_distance.delay(0.8)
        max_distamce = tasks_facecode.get_max_distance.delay().get()
        assert max_distamce == 0.8

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/robert_1.jpg"
        )
        fingerprint = tasks_facecode.buffer_to_vector(buffer_image)
        assert isinstance(fingerprint, str)

        person_know = {"name": "Robert", "vector": fingerprint}

        all_vectors = [person_know["vector"]]
        all_names = [person_know["name"]]

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/robert_2.jpg"
        )
        fingerprint = tasks_facecode.buffer_to_vector(buffer_image)

        tasks_facecode.change_max_distance.delay(0.85)
        return
        result = tasks_facecode.compare_vectors.delay(
            fingerprint, all_vectors, all_names
        ).get()
        assert result == person_know["name"]
    """
