import numpy as np

from shared.FaceRecognition.AESCipher import AESCipher


class CriptVectorPerson(AESCipher):
    def __init__(self, key: str = "secret"):
        super().__init__(key)

    def VectorToString(self, vector_person):
        person_encoding_list = list(vector_person)
        person_encoding_string = str(person_encoding_list).strip("[]")

        person_encoding_string_encrip = self.encrypt(person_encoding_string)

        return person_encoding_string_encrip

    def StringToVector(self, person_encoding_string_encrip):
        person_encoding_string = self.decrypt(person_encoding_string_encrip)

        vectorString = list(person_encoding_string.split(","))
        vectorFloat = [float(i) for i in vectorString]
        vectorNumpy = np.asarray(vectorFloat)
        return vectorNumpy
