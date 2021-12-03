from libraries.FaceRecognition import FaceRecognition
from libraries.CriptVectorPerson import CriptVectorPerson
from config.config import key_AES, MaxFaceDistanceInVector_forRecognition

crypto = CriptVectorPerson(key_AES)
fr = FaceRecognition(allVectorsFromPeople=[],
                     allNamesFromPeople=[])
fr.SetMaxFaceDistanceInVector(MaxFaceDistanceInVector_forRecognition)


class AES_FaceRecognition:
    def ImageToStr(self, path):
        fr.ReadImage(pathImage=path)
        fr.ExtractVectorOfImage()
        vectorThatPerson = fr.GetVector()

        vector_persona_str = crypto.VectorToString(vectorThatPerson)
        return vector_persona_str

    def StrToVector(self, vector_persona_str):
        vector = crypto.StringToVector(vector_persona_str)
        return vector


