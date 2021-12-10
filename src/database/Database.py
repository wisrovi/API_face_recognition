import datetime

from config.config import BASEDATOS


class Base:
    @staticmethod
    def read_all(basedatos: str, tabla: str):
        return f"SELECT * FROM {basedatos}.{tabla}"

    @staticmethod
    def insertar(tabla: str, campos: str, valores: str):
        return f"INSERT INTO {tabla} ({campos}) VALUES({valores})"

    @staticmethod
    def create_database(name):
        return "CREATE DATABASE " + name

    @staticmethod
    def create_campos_finales():
        return """, fechaRegistro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    fechaModifica DATETIME ON UPDATE CURRENT_TIMESTAMP"""

    @staticmethod
    def create_campos_iniciales():
        return """id INT AUTO_INCREMENT PRIMARY KEY,"""


class Vector:
    base = Base()
    name_table = "Vector"

    def INSERT(self, value: str):
        return self.base.insertar(BASEDATOS + "." + self.name_table, "vector_aes", value)

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    vector VARCHAR(10000) NOT NULL,
                    imagen VARCHAR(50) NOT NULL,
                    id_usuario_owner INT NOT NULL {self.base.create_campos_finales()}
                )"""


class Licencia:
    base = Base()
    name_table = "Licencia"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, licencia: str, id_usuario: int,
               cantidad_maxima_rostros,
               plan_bytes, cantidad_hijos,
               id_usuario_owner: int, fechaVencimiento: datetime.datetime):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  """licencia, id_usuario, 
                                  cantidad_maxima_rostros, plan_bytes,
                                  cantidad_hijos, id_usuario_owner, fechaVencimiento""",
                                  "'" + licencia + "'," +
                                  " " + str(id_usuario) + "," +
                                  " " + str(int(cantidad_maxima_rostros)) + "," +
                                  " " + str(int(plan_bytes)) + "," +
                                  " " + str(int(cantidad_hijos)) + "," +
                                  " " + str(id_usuario_owner) + " ," +
                                  " '" + str(fechaVencimiento) + "' "
                                  )

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    licencia VARCHAR(200) NOT NULL,
                    id_usuario INT NOT NULL,
                    cantidad_maxima_rostros NUMERIC NOT NULL,
                    plan_bytes NUMERIC NOT NULL,
                    cantidad_hijos NUMERIC NOT NULL,
                    id_usuario_owner INT NOT NULL 
                    {self.base.create_campos_finales()},
                    fechaVencimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""


class Login:
    base = Base()
    name_table = "Login"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)


class Persona:
    base = Base()
    name_table = "Persona"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, primer_nombre: str, segundo_nombre: str,
               primer_apellido: str, segundo_apellido: str,
               id_tipo_documento: int, numero_documento: int):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  """primer_nombre, segundo_nombre, 
                                  primer_apellido, segundo_apellido,
                                  id_tipo_documento, numero_documento""",
                                  "'" + primer_nombre + "'," +
                                  "'" + segundo_nombre + "'," +
                                  "'" + primer_apellido + "'," +
                                  "'" + segundo_apellido + "'," +
                                  " " + str(id_tipo_documento) + " ," +
                                  " " + str(numero_documento) + " "
                                  )

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    primer_nombre VARCHAR(50) NOT NULL,
                    segundo_nombre VARCHAR(50) NOT NULL,
                    primer_apellido VARCHAR(50) NOT NULL,
                    segundo_apellido VARCHAR(50) NOT NULL,
                    id_tipo_documento INT NOT NULL,
                    numero_documento INT NOT NULL
                    {self.base.create_campos_finales()}
                )"""


class RelacionPersonaVector:
    base = Base()
    name_table = "RelacionPersonaVector"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, id_persona: int,
               id_vector: int,
               id_persona_registra: int):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  "id_persona, id_vector, id_persona_registra",
                                  "" + str(id_persona) + ","
                                  "" + str(id_vector) + "," +
                                  "" + str(id_persona_registra) + "")

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    id_persona INT NOT NULL,
                    id_vector INT NOT NULL,
                    id_persona_registra INT NOT NULL
                    {self.base.create_campos_finales()}
                )"""


class RolUsuario:
    base = Base()
    name_table = "RolUsuario"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, rol: str, descripcion: str):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  "rol_usuario, descripcion",
                                  "'" + rol + "',"
                                              "'" + descripcion + "'")

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    rol_usuario VARCHAR(30) NOT NULL,
                    descripcion VARCHAR(100)  NOT NULL
                    {self.base.create_campos_finales()}
                )"""


class Usuario:
    base = Base()
    name_table = "Usuario"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, id_persona: int,
               usuario: str, password_aes: str,
               email: str,
               id_usuario_padre: int, id_rol_usuario: int):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  """ id_persona, 
                                  usuario, password, 
                                  email, 
                                  id_usuario_padre, id_rol_usuario""",
                                  " " + str(id_persona) + "," +
                                  "'" + usuario + "'," +
                                  "'" + password_aes + "'," +
                                  "'" + email + "'," +
                                  "'" + str(id_usuario_padre) + "'," +
                                  " " + str(id_rol_usuario) + " ")

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    id_persona INT NOT NULL,
                    usuario VARCHAR(50) NOT NULL,
                    password VARCHAR(30)  NOT NULL,
                    email VARCHAR(50)  NOT NULL,
                    id_usuario_padre INT NOT NULL,
                    id_rol_usuario INT NOT NULL
                    {self.base.create_campos_finales()}
                )"""


class TipoDocumento:
    base = Base()
    name_table = "TipoDocumento"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, tipo_documento: str, descripcion: str):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  "tipo_documento, descripcion",
                                  "'" + tipo_documento + "',"
                                                         "'" + descripcion + "'")

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    tipo_documento VARCHAR(30) NOT NULL,
                    descripcion VARCHAR(30)  NOT NULL
                    {self.base.create_campos_finales()}
                )"""


class Log:
    base = Base()
    name_table = "Log"

    def READALL(self):
        return self.base.read_all(BASEDATOS, self.name_table)

    def INSERT(self, id_usuario: int,
               bytes_usados: int,
               nombre_archivo: str):
        return self.base.insertar(BASEDATOS + "." + self.name_table,
                                  "id_usuario, bytes_usados, nombre_archivo",
                                  "" + str(id_usuario) + ","
                                  "" + str(bytes_usados) + "," +
                                  "'" + nombre_archivo + "'")

    def BUILD(self):
        return f"""CREATE TABLE {self.name_table}(
                    {self.base.create_campos_iniciales()}
                    id_usuario INT NOT NULL,
                    bytes_usados INT NOT NULL,
                    nombre_archivo VARCHAR(30)  NOT NULL
                    {self.base.create_campos_finales()}
                )"""


class Vistas:

    @staticmethod
    def BuildSummary():
        return """CREATE VIEW Summary AS
                SELECT p.primer_nombre, p.segundo_nombre, p.primer_apellido, p.segundo_apellido, td.descripcion, p.numero_documento 
                , u.usuario, u.password, u.email, ru.rol_usuario, l.licencia 
                from Licencia l 
                INNER JOIN Usuario u ON u.id = l.id_usuario 
                INNER JOIN Persona p ON p.id = u.id_persona 
                INNER JOIN RolUsuario ru ON ru.id = u.id_rol_usuario 
                INNER JOIN TipoDocumento td ON td.id = p.id_tipo_documento """


class Database:
    base = Base()
    vector = Vector()
    licencia = Licencia()
    login = Login()
    persona = Persona()
    relacionPersonaVector = RelacionPersonaVector()
    rolUsuario = RolUsuario()
    usuario = Usuario()
    tipoDocumento = TipoDocumento()
    log = Log()
    vistas = Vistas()


if __name__ == '__main__':
    data = Database()
    print(data.vector.INSERT("ABCDE"))
    print(data.tipoDocumento.READALL())
