from shared.FaceRecognition.Face_recognition import Face_recognition
from shared.FaceRecognition.Facecode_AES import Facecode_AES
from shared.Image import Image

import pickle

image = Image()


class TestFaceCodeAES:
    def test_facerecognition(self):
        robert_1 = Face_recognition("/app/test/resources/u/robert_1.jpg")
        robert_1 = {"first_name": "Robert", "vector": robert_1.vector}

        all_vectors = [robert_1["vector"]]
        all_names = [robert_1["first_name"]]

        robert_2 = Face_recognition("/app/test/resources/robert_2.jpg")
        result = robert_2.compare(all_vectors, all_names)
        assert result[0] == robert_1["first_name"]
        assert robert_2.vector.any()

    def test_facecode(self):
        face_code = Facecode_AES(max_distance=0.9)

        face_code.path = "/app/test/resources/u/robert_1.jpg"
        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result[0] == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pillow(self):
        face_code = Facecode_AES(max_distance=0.9)

        buffer_image = image.put_image_in_buffer(
            "/app/test/resources/u/robert_1.jpg"
        )
        face_code.path = buffer_image

        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result[0] == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pillow_buffer(self):
        face_code = Facecode_AES(max_distance=0.9)

        # find fingerprint or image and put in buffer on face_code.path
        buffer_image_know = image.put_image_in_buffer(
            "/app/test/resources/u/robert_1.jpg"
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
        assert result[0] == person_know["first_name"]
        assert face_code.fingerprint != person_know["fingerprint"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pickle(self):
        face_code = Facecode_AES(max_distance=0.6)

        # save using pickle
        with open("/app/face_code.pkl", "wb") as f:
            pickle.dump(face_code, f)

        # load using pickle
        with open("/app/face_code.pkl", "rb") as f:
            face_code = pickle.load(f)        
        face_code.distance = 0.9

        face_code.path = "/app/test/resources/u/robert_1.jpg"

        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}
        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "/app/test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result[0] == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)