import numpy as np
import keras.utils as image
from keras_vggface.vggface import VGGFace
from keras_vggface import utils


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
    