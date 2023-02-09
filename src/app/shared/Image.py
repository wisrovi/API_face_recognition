from io import BytesIO

from PIL import Image as PilImage


class Image:
    def put_image_in_buffer(self, path: str):
        input_image = PilImage.open(path)
        buffer = BytesIO()
        input_image.save(buffer, format="jpeg")
        buffer.seek(0)
        return buffer
