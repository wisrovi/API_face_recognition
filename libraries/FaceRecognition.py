import face_recognition
import numpy as np


class FaceRecognition(object):
    hayImagen = False
    hayVector = False
    MaxFaceDistanceInVector = 0.6

    def __init__(self, allVectorsFromPeople: list, allNamesFromPeople: list):
        self.vector = None
        self.result_search_bool = None
        self.result_search_int_distance = None
        self.allVectorsFromPeople = allVectorsFromPeople
        self.allNamesFromPeople = allNamesFromPeople

    def SetAllNamesFromPeople(self, allNamesFromPeople: list):
        self.allNamesFromPeople = allNamesFromPeople

    def SetAllVectorsFromPeople(self, allVectorsFromPeople: list):
        self.allVectorsFromPeople = allVectorsFromPeople

    def SetMaxFaceDistanceInVector(self, MaxFaceDistanceInVector):
        self.MaxFaceDistanceInVector = MaxFaceDistanceInVector

    def ReadImage(self, pathImage):
        self.image = face_recognition.load_image_file(pathImage)
        self.hayImagen = True
        return self.image

    def CalculeFaceUbication(self, pathImage=None):
        if pathImage is not None:
            self.hayImagen = False
            self.ReadImage(pathImage)

        if self.hayImagen:
            self.coordenadasRostro = face_recognition.face_locations(self.image)
            return self.coordenadasRostro
        else:
            return None

    def CoordenadasPuntosFaciales(self, pathImage=None):
        if pathImage is not None:
            self.hayImagen = False
            self.ReadImage(pathImage)

        if self.hayImagen:
            self.puntos_faciales = face_recognition.face_landmarks(self.image)
            return self.puntos_faciales
        else:
            return None

    def GetVector(self):
        return self.vector

    def ExtractVectorOfImage(self, pathImage=None):
        if pathImage is not None:
            self.hayImagen = False
            self.ReadImage(pathImage)

        if self.hayImagen:
            self.vector = face_recognition.face_encodings(self.image)[0]
            self.hayVector = True
            return self.vector
        else:
            return None

    def SearchPerson(self, pathImage=None, MaxFaceDistanceInVector=None):
        if pathImage is not None:
            self.hayImagen = False
            self.ReadImage(pathImage)

        if self.hayImagen:
            if not self.hayVector:
                self.ExtractVectorOfImage()

            if self.hayVector:
                if MaxFaceDistanceInVector is not None:
                    self.MaxFaceDistanceInVector = MaxFaceDistanceInVector
                self.result_search_bool = face_recognition.compare_faces(self.allVectorsFromPeople,
                                                                         self.vector,
                                                                         self.MaxFaceDistanceInVector)
                self.result_search_int_distance = face_recognition.face_distance(self.allVectorsFromPeople, self.vector)

                if len(self.result_search_int_distance) > 0:
                    best_match_index = np.argmin(self.result_search_int_distance)

                    name = None
                    print(best_match_index, self.result_search_bool, self.result_search_int_distance)
                    if self.result_search_bool[best_match_index]:
                        name = self.allNamesFromPeople[best_match_index]

                    nombre = None
                    options = []
                    for id_search in range(len(self.result_search_bool)):
                        if self.result_search_bool[id_search]:
                            options.append(id_search)

                    if best_match_index in options:
                        nombre = self.allNamesFromPeople[best_match_index]
                    #
                    # if True in self.result_search_bool:
                    #     indice = self.result_search_bool.index(True)
                    #     nombre = self.allNamesFromPeople[indice]

                    if name is not None and nombre is not None and name == nombre:
                        return name
                    else:
                        return None

    def GetVectorSearch(self):
        return self.result_search_int_distance
