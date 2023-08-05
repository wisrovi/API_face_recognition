import os, time
import pickle

from shared.tf_compare_faces.KerasFace import KerasFace
from shared.tf_compare_faces.MatchFace import MatchFace

import warnings
warnings.filterwarnings("ignore")


start_time = time.time()
if not os.path.exists("/app/test/resources/u/database_face_tf.pkl"):
    folder = "/app/test/resources/u"
    all_vectors = []
    all_names = []
    for path in sorted(os.listdir(folder))[::-1]:
        if path.find(".pkl") == -1:
            real_path = os.path.join(folder, path)
            name = path.split(".")[0]

            emb1 = KerasFace(real_path).embedding

            all_vectors.append(emb1)
            all_names.append(name)
    with open("/app/test/resources/u/database_face_tf.pkl", "wb") as f:
        pickle.dump([all_vectors, all_names], f)
else:
    with open("/app/test/resources/u/database_face_tf.pkl", "rb") as f:
        all_vectors, all_names = pickle.load(f)
end_time = time.time()
print(f"total time for load dataset: {end_time - start_time}")

print("\n"*3)

match_face = MatchFace(euclidean_umbral=100, cosine_umbral=0.4)

start_time = time.time()
emb2 = KerasFace("/app/test/resources/robert_2.jpg").embedding
for i, emb1 in enumerate(all_vectors):
    d = match_face.compare(emb1, emb2)
    if d[0][1] and d[1][1]:
        print(f"the new person is {all_names[i]} ({i})")
        break
end_time = time.time()
print(f"total time for load dataset: {end_time - start_time}")
