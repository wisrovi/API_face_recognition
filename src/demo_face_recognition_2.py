"""
Example of use of the face recognition module
"""

import os
import time
import pickle


# load using pickle
FACE_CODE = None
with open("/models/face_recognion/face_code.pkl", "rb") as f:
    FACE_CODE = pickle.load(f)


start_time = time.time()
if not os.path.exists("/test/face_recognition/u/database_face_code.pkl"):
    folder = "/app/test/resources/u"
    all_vectors = []
    all_names = []
    for path in os.listdir(folder):
        if path.find(".pkl") == -1:
            real_path = os.path.join(folder, path)
            name = path.split(".")[0]
            FACE_CODE.path = real_path
            all_vectors.append(FACE_CODE.fingerprint)
            all_names.append(name)
    with open("/test/face_recognition/u/database_face_code.pkl", "wb") as f:
        pickle.dump([all_vectors, all_names], f)
else:
    with open("/test/face_recognition/u/database_face_code.pkl", "rb") as f:
        all_vectors, all_names = pickle.load(f)
end_time = time.time()
print(f"total time for load dataset: {end_time - start_time}")

print("\n"*3)

start_time = time.time()
FACE_CODE.path = "/test/face_recognition/robert_2.jpg"
end_time = time.time()
print(f"total time for get fingerprint: {end_time - start_time}")

print("\n"*3)

start_time = time.time()
FACE_CODE.path = "/test/face_recognition/robert_2.jpg"
result = FACE_CODE.compare_fingerprints(all_vectors, all_names)
print(f"the new person is {result}")
end_time = time.time()
print(f"total time for looking for person: {end_time - start_time}")
