import pickle
import os
from libraries.CriptVectorPerson import CriptVectorPerson


class DatabaseVectorPerson(object):
    FILE_ARRAY_VECTORS = "ARRAYS_PERSON.txt"
    FILE_NAMES = "NAMES.txt"

    base_datos_vectores_caracteristicas = []
    base_datos_vector_nombres = []

    hayCambios = False

    def __init__(self, KEY_AES, base_dir=None):
        self.crypto_aes = CriptVectorPerson(KEY_AES)
        self._Read()
        if base_dir is None:
            base_dir = ""
        self.base_dir = base_dir
        # print(base_dir)

    def _Read(self):
        try:
            path = os.path.join(self.base_dir, self.FILE_NAMES)
            print(path)
            with open(path, "rb") as fp:  # Unpickling
                b = pickle.load(fp)
                self.base_datos_vector_nombres = b
        except:
            self.base_datos_vector_nombres = []

        try:
            path = os.path.join(self.base_dir, self.FILE_ARRAY_VECTORS)
            print(path)
            with open(path, "rb") as fp:  # Unpickling
                b = pickle.load(fp)
                c = []
                for vector in b:
                    size = len(vector)
                    c.append(self.crypto_aes.StringToVector(vector))
                self.base_datos_vectores_caracteristicas = c
        except:
            self.base_datos_vectores_caracteristicas = []

    def getAllVectorsFromPeople(self):
        return self.base_datos_vectores_caracteristicas

    def getAllNamesFromPeople(self):
        return self.base_datos_vector_nombres

    def AddPersonToVector(self, vector, name):
        self.base_datos_vector_nombres.append(name)
        self.base_datos_vectores_caracteristicas.append(vector)
        self.hayCambios = True

    def Update(self):
        if self.hayCambios:
            path = os.path.join(self.base_dir, self.FILE_NAMES)
            print(path)
            with open(path, "wb") as fp:  # Pickling
                pickle.dump(self.base_datos_vector_nombres, fp)

            c = []
            for vector in self.base_datos_vectores_caracteristicas:
                vector_encript = self.crypto_aes.VectorToString(vector)
                c.append(vector_encript)

            path = os.path.join(self.base_dir, self.FILE_ARRAY_VECTORS)
            print(path)
            with open(path, "wb") as fp:  # Pickling
                pickle.dump(c, fp)
        return self.hayCambios
