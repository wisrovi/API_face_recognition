from io import BytesIO
import cv2
from PIL import Image as PilImage


class Image:
    def read_image_using_pillow(self, path: str):
        input_image = PilImage.open(path)
        buffer = BytesIO()
        input_image.save(buffer, format="jpeg")
        buffer.seek(0)
        return buffer

    def read_image_using_opencv(self, path: str):
        input_image = cv2.imread(path)
        _, buffer = cv2.imencode('.jpg', input_image)
        buffer = BytesIO(buffer)
        return buffer
