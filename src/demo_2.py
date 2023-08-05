

import numpy as np
import keras.utils as image
from keras_vggface.vggface import VGGFace
from keras_vggface import utils
from typing import Union
import time


vgg_features = VGGFace(include_top=False, input_shape=(224, 224, 3), pooling='avg') # pooling: None, avg or max


class KerasFace:
    _image = None
    _embedding = None

    def __init__(self, img: str = None):
        if img:
            self.image = img

    @property   
    def embedding(self) -> np.ndarray:
        return self._embedding

    @property
    def image(self) -> str:
        return self._image
    
    @image.setter
    def image(self, path: str):
        self._image = image.load_img(path, target_size=(224, 224))
        self._embedding = self._get_embedding(self._image)

    def _get_embedding(self, img):
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=1)
        emb = vgg_features.predict(x)
        return emb
    

class Match:
    def __init__(self, euclidean_umbral: float = 100, cosine_umbral: float = 0.4):
        self.euclidean_umbral = euclidean_umbral
        self.cosine_umbral = cosine_umbral
        self.vgg_features = VGGFace(include_top=False, 
                                    input_shape=(224, 224, 3), 
                                    pooling='avg')
        
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
        

class MatchFace(Match, KerasFace):

    def __init__(self, euclidean_umbral: float = 100, cosine_umbral: float = 0.4):
        super().__init__(euclidean_umbral, cosine_umbral)

    def compare(self, img1: Union[str, np.ndarray], img2: Union[str, np.ndarray]):
        if isinstance(img1, str):
            # print("img1 is str")
            self.image = img1
            emb1 = self.embedding
        else:
            # print("img1 is ndarray")
            emb1 = img1

        if isinstance(img2, str):
            # print("img2 is str")
            self.image = img2
            emb2 = self.embedding
        else:
            # print("img2 is ndarray")
            emb2 = img2

        dist_euclidean = self.findEuclideanDistance(emb2, emb1)
        dist_cosine = self.findCosineDistance(emb2[0], emb1[0])
        return dist_euclidean, dist_cosine


print("\n"*10)

match_face = MatchFace(euclidean_umbral=100, cosine_umbral=0.4)


start_time = time.time()
emb1 = KerasFace("/app/test/resources/u/robert_1.jpg").embedding
end_time = time.time()
print(f"total time: {end_time - start_time}")


print("\n"*3)


start_time = time.time()
emb1 = KerasFace("/app/test/resources/u/robert_1.jpg").embedding
end_time = time.time()
print(f"total time: {end_time - start_time}")


print("\n"*3)

start_time = time.time()
emb2 = KerasFace("/app/test/resources/robert_2.jpg").embedding
d = match_face.compare(emb1, emb2)
print(d)
end_time = time.time()
print(f"total time: {end_time - start_time}")


print("\n"*3)

start_time = time.time()
d = match_face.compare("/app/test/resources/u/robert_1.jpg", "/app/test/resources/robert_2.jpg")
end_time = time.time()
print(d)
print(f"total time: {end_time - start_time}")


print("\n"*3)



emb1 = KerasFace("/app/test/resources/u/robert_1.jpg").embedding
start_time = time.time()
d = match_face.compare(emb1, "/app/test/resources/robert_2.jpg")
end_time = time.time()
print(d)
print(f"total time: {end_time - start_time}")


print("\n"*3)




emb1 = KerasFace("/app/test/resources/u/robert_1.jpg").embedding
emb2 = KerasFace("/app/test/resources/robert_2.jpg").embedding
start_time = time.time()
d = match_face.compare(emb1, emb2)
print(d)
end_time = time.time()
print(f"total time: {end_time - start_time}")
