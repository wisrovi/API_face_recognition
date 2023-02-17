"""
---------------------------------------
| LAYER 0
| library: face_recognition
| version: 1.3.0
| this library is used for convert image to vector
| and compare vectors for to identify person and verify
| if the person exists in the database (list of vectors)
---------------------------------------
"""

import face_recognition
import numpy as np


class FaceRecognition:
    vector: np.ndarray

    def __init__(self, image_path: str = None, max_distance: float = 0.6):
        self.points = None
        self.face_locations = None
        self.max_distance = max_distance
        self.image = None
        self.image_path = image_path
        self.setup()

    def read_image(self):
        self.image = face_recognition.load_image_file(self.image_path)

    def coordinates_of_face(self):
        self.face_locations = face_recognition.face_locations(self.image)

    def coordinates_of_landmarks(self):
        self.points = face_recognition.face_landmarks(self.image)

    def get_face_code(self):
        self.vector = face_recognition.face_encodings(self.image)[0]

    def setup(self) -> np.ndarray:
        if self.image_path:
            self.read_image()
            self.coordinates_of_face()
            if self.face_locations:
                self.coordinates_of_landmarks()
                self.get_face_code()

    def compare(
        self,
        all_face_vectors: list[np.ndarray],
        all_names_of_vectors: list[str],
    ):
        result_compare = face_recognition.compare_faces(
            all_face_vectors, self.vector, self.max_distance
        )
        if len(result_compare) > 0:
            position_positive = np.argmin(result_compare)
            if result_compare[position_positive]:
                return all_names_of_vectors[position_positive]
