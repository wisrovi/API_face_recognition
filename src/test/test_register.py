from libraries.DatabaseVectorPerson import DatabaseVectorPerson
from libraries.FaceRecognition import FaceRecognition
from config.config import BASE_DIR

database = DatabaseVectorPerson( KEY_AES="QUESO", base_dir=BASE_DIR )

fr = FaceRecognition(allVectorsFromPeople=database.getAllVectorsFromPeople(),
                     allNamesFromPeople=database.getAllNamesFromPeople())
fr.SetMaxFaceDistanceInVector(0.45)

rutaImagen = "demo.jpg"
fr.ReadImage(pathImage=rutaImagen)
fr.ExtractVectorOfImage()

person = fr.SearchPerson()

if person is not None:
    print("La persona es: ", person, " en: ", rutaImagen)
else:
    nameSave = len(database.getAllVectorsFromPeople())
    vectorThatPerson = fr.GetVector()

    database.AddPersonToVector(vectorThatPerson, nameSave)
    database.Update()

    fr.SetAllVectorsFromPeople(database.getAllVectorsFromPeople())
    fr.SetAllNamesFromPeople(database.getAllNamesFromPeople())

    print("Persona registrada correctamente")