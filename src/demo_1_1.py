import os, time
import pickle


# load using pickle
face_code = None
with open("/app/face_code.pkl", "rb") as f:
    face_code = pickle.load(f)


start_time = time.time()
if not os.path.exists("/app/test/resources/u/database_face_code.pkl"):
    folder = "/app/test/resources/u"
    all_vectors = []
    all_names = []
    for path in os.listdir(folder):
        if path.find(".pkl") == -1:
            real_path = os.path.join(folder, path)
            name = path.split(".")[0]
            face_code.path = real_path
            all_vectors.append(face_code.fingerprint)
            all_names.append(name)
    with open("/app/test/resources/u/database_face_code.pkl", "wb") as f:
        pickle.dump([all_vectors, all_names], f)
else:
    with open("/app/test/resources/u/database_face_code.pkl", "rb") as f:
        all_vectors, all_names = pickle.load(f)
end_time = time.time()
print(f"total time for load dataset: {end_time - start_time}")

print("\n"*3)

start_time = time.time()
face_code.path = "/app/test/resources/robert_2.jpg"
end_time = time.time()
print(f"total time for get fingerprint: {end_time - start_time}")

print("\n"*3)

start_time = time.time()
face_code.path = "/app/test/resources/robert_2.jpg"
result = face_code.compare_fingerprints(all_vectors, all_names)
print(f"the new person is {result}")
end_time = time.time()
print(f"total time for looking for person: {end_time - start_time}")

