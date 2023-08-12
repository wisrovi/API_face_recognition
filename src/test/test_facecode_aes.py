import os
from shared.FaceRecognition.Facecode_AES import Facecode_AES
from shared.Image import Image

import pickle

image = Image()

# save using pickle
face_code = Facecode_AES(max_distance=0.9)
os.makedirs("/models/face_recognion", exist_ok=True)
with open("/models/face_recognion/face_code.pkl", "wb") as f:
    pickle.dump(face_code, f)


class TestFaceCodeAES:
    def test_facecode_pillow_and_path(self):
        # load using pickle
        with open("/models/face_recognion/face_code.pkl", "rb") as f:
            face_code = pickle.load(f)
        face_code.distance = 0.9

        buffer_image = image.read_image_using_pillow("test/resources/u/robert_1.jpg")
        face_code.path = buffer_image

        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}

        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result[0] == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_pillow_and_pillow(self):
        # load using pickle
        with open("/models/face_recognion/face_code.pkl", "rb") as f:
            face_code = pickle.load(f)
        face_code.distance = 0.9

        # find fingerprint or image and put in buffer on face_code.path
        buffer_image_know = image.read_image_using_pillow(
            "test/resources/u/robert_1.jpg"
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
        buffer_image_unknown = image.read_image_using_pillow(
            "test/resources/robert_2.jpg"
        )
        face_code.path = buffer_image_unknown

        # compare the unknown fingerprint with the database
        result = face_code.compare_fingerprints(all_vectors, all_names)

        assert face_code.vector.any()
        assert result[0] == person_know["first_name"]
        assert face_code.fingerprint != person_know["fingerprint"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_opencv_and_opencv(self):
        # load image using opencv and put in buffer
        face_code.path = image.read_image_using_opencv("test/resources/u/robert_1.jpg")

        # create a database with all fingerprints and names of people
        person_know = {
            "first_name": "Robert",
            "fingerprint": face_code.fingerprint,
        }
        all_vectors = [person_know["fingerprint"]]
        all_names = [person_know["first_name"]]

        # load image using opencv and put in buffer
        face_code.path = image.read_image_using_opencv("test/resources/robert_2.jpg")

        # compare the unknown fingerprint with the database
        result = face_code.compare_fingerprints(all_vectors, all_names)

        assert face_code.vector.any()
        assert result[0] == person_know["first_name"]
        assert face_code.fingerprint != person_know["fingerprint"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_basic(self):
        # load using pickle
        with open("/models/face_recognion/face_code.pkl", "rb") as f:
            face_code = pickle.load(f)
        face_code.distance = 0.9

        face_code.path = "test/resources/u/robert_1.jpg"

        person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}
        all_vectors = [person_1["vector"]]
        all_names = [person_1["first_name"]]

        face_code.path = "test/resources/robert_2.jpg"
        result = face_code.compare_fingerprints(all_vectors, all_names)
        assert face_code.vector.any()
        assert result[0] == person_1["first_name"]
        assert face_code.fingerprint != person_1["vector"]
        assert isinstance(face_code.fingerprint, str)

    def test_facecode_using_stateMachine(self):
        pass
