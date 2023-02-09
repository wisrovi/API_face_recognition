from app.shared.FaceRecognition.CriptVectorPerson import CriptVectorPerson
from app.shared.FaceRecognition.FaceRecognition import FaceRecognition


class Facecode_AES(FaceRecognition):
    def __init__(
            self,
            image_path: str = None,
            max_distance: float = 0.6,
            secret_key_aes: str = "secret",
    ):
        super().__init__(image_path, max_distance)
        self.cript = CriptVectorPerson(secret_key_aes)

    @property
    def distance(self):
        return self.max_distance

    @distance.setter
    def distance(self, max_distance: float):
        self.max_distance = max_distance

    @property
    def path(self):
        return self.image_path

    @path.setter
    def path(self, image_path: str):
        self.image_path = image_path
        self.setup()

    @property
    def fingerprint(self):
        return self.cript.VectorToString(self.vector)

    def compare_fingerprints(
            self, all_face_vectors: list[str], all_names_of_vectors: list[str]
    ):
        all_vectors = [self.cript.StringToVector(i) for i in all_face_vectors]
        result_compare = self.compare(all_vectors, all_names_of_vectors)
        return result_compare
