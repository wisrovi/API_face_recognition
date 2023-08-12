from typing import Union
import numpy as np

from shared.tf_compare_faces.Match import Match
from shared.tf_compare_faces.KerasFace import KerasFace


class MatchFace(Match, KerasFace):
    def __init__(
        self,
        euclidean_umbral: float = 100,
        cosine_umbral: float = 0.4,
    ):
        super().__init__(euclidean_umbral, cosine_umbral)

    def compare(
        self,
        img1: Union[str, np.ndarray],
        img2: Union[str, np.ndarray],
    ) -> tuple:
        """
        Compare two images.

        :param img1: Image 1
        :type img1: Union[str, np.ndarray]
        :param img2: Image 2
        :type img2: Union[str, np.ndarray]
        :return: Tuple with euclidean and cosine distances
        """

        if isinstance(img1, str):
            self.image = img1
            emb1 = self.embedding
        else:
            emb1 = img1

        if isinstance(img2, str):
            self.image = img2
            emb2 = self.embedding
        else:
            emb2 = img2

        dist_euclidean = self.findEuclideanDistance(emb2, emb1)
        dist_cosine = self.findCosineDistance(emb2[0], emb1[0])

        return dist_euclidean, dist_cosine
