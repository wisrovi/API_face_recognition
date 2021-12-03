from libraries.DatabaseVectorPerson import DatabaseVectorPerson
from config.config import BASE_DIR
database = DatabaseVectorPerson( KEY_AES="QUESO", base_dir=BASE_DIR )
total = len(database.getAllVectorsFromPeople())
print("Numero personas registradas", len(database.getAllVectorsFromPeople()), "-", len(database.getAllNamesFromPeople()))
