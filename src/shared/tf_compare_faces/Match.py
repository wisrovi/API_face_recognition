import numpy as np


class Match:
    def __init__(self, euclidean_umbral: float = 100, cosine_umbral: float = 0.4):
        self.euclidean_umbral = euclidean_umbral
        self.cosine_umbral = cosine_umbral
        
    def findEuclideanDistance(self, source_representation, test_representation):
        euclidean_distance = source_representation - test_representation
        euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
        euclidean_distance = np.sqrt(euclidean_distance)
        is_same = euclidean_distance < self.euclidean_umbral
        return euclidean_distance, is_same
    
    def findCosineDistance(self, source_representation, test_representation):
        a = np.matmul(np.transpose(source_representation), test_representation)
        b = np.sum(np.multiply(source_representation, source_representation))
        c = np.sum(np.multiply(test_representation, test_representation))
        cosice_distance = 1 - (a / (np.sqrt(b) * np.sqrt(c)))
        is_same = cosice_distance < self.cosine_umbral
        return cosice_distance, is_same
        