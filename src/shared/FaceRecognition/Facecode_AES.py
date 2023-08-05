"""
---------------------------------------
| LAYER 1
| library: facecode_aes
| version: 1.0.0
| this library is used for convert vector to string (with AES)
| and convert string to vector (with AES)
| and use LAYER 0 (face_recognition)
---------------------------------------
"""

from .CriptVectorPerson import CriptVectorPerson
from .Face_recognition import Face_recognition


class Facecode_AES(Face_recognition):
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

    @fingerprint.setter
    def fingerprint(self, vector: str):
        self.vector = self.cript.StringToVector(vector)

    def compare_fingerprints(
        self, all_face_vectors: list[str], all_names_of_vectors: list[str]
    ):
        all_vectors = [self.cript.StringToVector(i) for i in all_face_vectors]
        result_compare = self.compare(all_vectors, all_names_of_vectors)
        return result_compare
