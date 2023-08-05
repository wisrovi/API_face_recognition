from shared.FaceRecognition.Facecode_AES import Facecode_AES
from shared.LogProject import logger_custom
import time
from PIL import Image as PilImage
from io import BytesIO
import cv2


# from shared.Image import Image
PROJECT_NAME = "face_recognition"
logger = logger_custom(PROJECT_NAME)

logger.debug("loading the database")

# create the database
face_code = Facecode_AES(max_distance=0.9)
face_code.path = "/app/test/resources/robert_1.jpg"
# logger.debug(face_code.fingerprint)
person_1 = {"first_name": "Robert", "vector": face_code.fingerprint}
all_vectors = [person_1["vector"]]
all_names = [person_1["first_name"]]
logger.debug("database loaded")


start_time = time.time()
# set a new person
face_code = Facecode_AES(max_distance=0.9)

# option 1: set the path of the image
#face_code.path = "/app/test/resources/robert_2.jpg"

# option 2: set the image in a buffer using PIL
#input_image = PilImage.open("/app/test/resources/robert_2.jpg")
#buffer = BytesIO()
#input_image.save(buffer, format="jpeg")
#buffer.seek(0)
#face_code.path = buffer

# option 3: set the image in a buffer using OpenCV
input_image = cv2.imread("/app/test/resources/robert_2.jpg")
_, buffer = cv2.imencode('.jpg', input_image)
buffer = BytesIO(buffer)
face_code.path = buffer

# logger.debug(face_code.fingerprint)

logger.debug("comparing the new person with the database")
# compare the new person with the database
result = face_code.compare_fingerprints(all_vectors, all_names)
logger.debug(f"the new person is {result} according to the database")

end_time = time.time()
logger.debug(f"total time: {end_time - start_time}")





input_image = PilImage.open("/app/test/resources/robert_2.jpg")
buffer = BytesIO()
input_image.save(buffer, format="jpeg")
buffer.seek(0)


print("\n"*3)


start_time = time.time()
face_code = Facecode_AES(max_distance=0.9)
face_code.path = buffer
end_time = time.time()
print(f"total time: {end_time - start_time}")


print("\n"*3)



start_time = time.time()
result = face_code.compare_fingerprints(all_vectors, all_names)
print(f"the new person is {result} according to the database")
end_time = time.time()
print(f"total time: {end_time - start_time}")