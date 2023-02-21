from shared.FaceRecognition.Face_recognition import Face_recognition
from shared.FaceRecognition.Facecode_AES import Facecode_AES
from shared.Image import Image
from tasks import TasksFacecode

image = Image()

tasks_facecode = TasksFacecode()


class TestFaceCodeAES:
    def test_facerecognition(self):
        robert_1 = Face_recognition("/app/test/resources/robert_1.jpg")
        robert_1 = {"first_name": "Robert", "vector": robert_1.vector}

        all_vectors = [robert_1["vector"]]
        all_names = [robert_1["first_name"]]

        robert_2 = Face_recognition("/app/test/resources/robert_2.jpg")
        result = robert_2.compare(all_vectors, all_names)
        assert result == robert_1["first_name"]
        assert robert_2.vector.any()

    def test_facecode(self):
        face_code = Facecode_AES(max_distance=0.9)

        face_code.path = "/app/test/resources/robert_1.jpg"
        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pillow(self):
        face_code = Facecode_AES(max_distance=0.9)

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/robert_1.jpg"
        )
        face_code.path = buffer_image

        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pillow_buffer(self):
        face_code = Facecode_AES(max_distance=0.9)

        # find fingerprint or image and put in buffer on face_code.path
        buffer_image_know = image.put_image_in_buffer(
            "/app/test/resources/robert_1.jpg"
        )
        face_code.path = buffer_image_know

        # create a database with all fingerprints and names of people
        person_know = {
            "first_name": "Robert",
            "fingerprint": face_code.fingerprint,
        }
        all_vectors = [person_know["fingerprint"]]
        all_names = [person_know["first_name"]]

        # find fingerprint or unknown image and put in buffer on face_code.path
        buffer_image_unknown = image.put_image_in_buffer(
            "/app/test/resources/robert_2.jpg"
        )
        face_code.path = buffer_image_unknown

        # compare the unknown fingerprint with the database
        result = face_code.compare_fingerprints(all_vectors, all_names)

        assert face_code.vector.any()
        assert result == person_know["first_name"]
        assert face_code.fingerprint != person_know["fingerprint"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_using_celery(self):
        tasks_facecode.change_max_distance.delay(0.8)
        max_distamce = tasks_facecode.get_max_distance.delay().get()
        assert max_distamce == 0.8

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/robert_1.jpg"
        )
        fingerprint = tasks_facecode.buffer_to_vector(buffer_image)
        assert isinstance(fingerprint, str)

        person_know = {"first_name": "Robert", "vector": fingerprint}

        all_vectors = [person_know["vector"]]
        all_names = [person_know["first_name"]]

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/robert_2.jpg"
        )
        fingerprint = tasks_facecode.buffer_to_vector(buffer_image)

        tasks_facecode.change_max_distance.delay(0.85)
        return
        result = tasks_facecode.compare_vectors.delay(
            fingerprint, all_vectors, all_names
        ).get()
        assert result == person_know["first_name"]
