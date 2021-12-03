from database.Dao import Dao
from database.Database import Database

database_comando = Database()
conexion_basedatos = Dao()
# dao.insertar(data.vector.INSERT("ABCDEF"))
print(conexion_basedatos.leerTodo(database_comando.vector.READALL()))
