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

from typing import List
import face_recognition
import numpy as np


class Face_recognition:
    """
    This class is used for convert image to vector
    """
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

    def setup(self) -> None:
        """
        setup the image and get the vector of the image
        """
        if self.image_path:
            self.read_image()
            self.coordinates_of_face()
            if self.face_locations:
                self.coordinates_of_landmarks()
                self.get_face_code()

    def compare(self,
                all_face_vectors: List[np.ndarray],
                all_names_of_vectors: List[str],
                summary: bool = False) -> List[str]:
        """
        Compare the vector of the image with the vectors of the database

        @type all_face_vectors: list[np.ndarray]
        @param all_face_vectors: list of vectors of the database

        @type all_names_of_vectors: list[str]
        @param all_names_of_vectors: list of names of the database

        @type summary: bool
        @param summary: if True, return a list of booleans,
        else return a list of names

        @rtype: list[str]
        @returns: list of names
        """

        result_compare = face_recognition.compare_faces(
            all_face_vectors, self.vector, self.max_distance
        )

        if summary:
            return result_compare

        if len(result_compare) > 0:
            # opcion 1
            result = [all_names_of_vectors[i]
                      for i in range(len(result_compare)) if result_compare[i]]

            # opcion 2
            # position_positive = np.argmin(result_compare)
            # if result_compare[position_positive]:
            #     return all_names_of_vectors[position_positive]
            return result

        return []
