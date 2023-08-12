import numpy as np


class Match:
    def __init__(
        self,
        euclidean_umbral: float = 100,
        cosine_umbral: float = 0.4,
    ):
        self.euclidean_umbral = euclidean_umbral
        self.cosine_umbral = cosine_umbral

    def findEuclideanDistance(
        self,
        source_representation: np.ndarray,
        test_representation: np.ndarray,
    ) -> (float, bool):
        """
        Euclidean distance is the "ordinary" straight-line distance between
        two points in Euclidean space.
        With this distance, Euclidean space becomes a metric space.
        The associated norm is called the Euclidean norm.
        Euclidean distance between points p and q is the length of the line
        segment connecting them.
        In Cartesian coordinates, if p = (p1, p2,..., pn)
        and q = (q1, q2,..., qn)
        are two points in Euclidean n-space,
        then the distance (d) from p to q, or from q to p is given
        by the Pythagorean formula:
        d(p,q) = d(q,p) = sqrt((q1-p1)^2 + (q2-p2)^2 + ... + (qn-pn)^2)

        :param source_representation: source representation
        :param test_representation: test representation
        :return: euclidean distance
        """

        euclidean_distance = source_representation - test_representation
        euclidean_distance = np.sum(
            np.multiply(euclidean_distance, euclidean_distance),
        )
        euclidean_distance = np.sqrt(euclidean_distance)
        is_same = euclidean_distance < self.euclidean_umbral

        return euclidean_distance, is_same

    def findCosineDistance(
        self,
        source_representation: np.ndarray,
        test_representation: np.ndarray,
    ) -> (float, bool):
        """
        Cosine distance is a measure of similarity between two non-zero vectors
        of an inner product space that measures the cosine of the angle
        between them.
        The cosine of 0° is 1, and it is less than 1 for any other angle.
        It is thus a judgment of orientation and not magnitude:
        two vectors with the same orientation have a cosine similarity of 1,
        two vectors at 90° have a similarity of 0,
        and two vectors diametrically opposed have a similarity of -1,
        independent of their magnitude.
        Cosine distance is thus an angular distance metric and is
        not symmetric.

        :param source_representation: source representation
        :param test_representation: test representation
        :return: cosine distance
        """

        a = np.matmul(np.transpose(source_representation), test_representation)
        b = np.sum(np.multiply(source_representation, source_representation))
        c = np.sum(np.multiply(test_representation, test_representation))

        cosice_distance = 1 - (a / (np.sqrt(b) * np.sqrt(c)))
        is_same = cosice_distance < self.cosine_umbral

        return cosice_distance, is_same
