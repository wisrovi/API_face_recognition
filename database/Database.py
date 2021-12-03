BASEDATOS = "AES_FaceRecognition"


class Base:
    @staticmethod
    def read_all(tabla: str):
        return f"SELECT * FROM {tabla}"

    @staticmethod
    def insertar(tabla: str, campos: str, valores: str):
        return f"INSERT INTO {tabla} ({campos}) VALUES('{valores}')"


class Vector:
    base = Base()

    def INSERT(self, value: str):
        return self.base.insertar(BASEDATOS + ".Vector", "vector_aes", value)

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".Vector")


class Licencia:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".Licencia")


class Login:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".Login")


class Persona:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".Persona")


class RelacionPersonaVector:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".RelacionPersonaVector")


class RolUsuario:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".RolUsuario")


class Usuario:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".Usuario")


class TipoDocumento:
    base = Base()

    def READALL(self):
        return self.base.read_all(BASEDATOS + ".TipoDocumento")


class Database:
    vector = Vector()
    licencia = Licencia()
    login = Login()
    persona = Persona()
    relacionPersonaVector = RelacionPersonaVector()
    rolUsuario = RolUsuario()
    usuario = Usuario()
    tipoDocumento = TipoDocumento()


if __name__ == '__main__':
    data = Database()
    print(data.vector.INSERT("ABCDE"))
    print(data.tipoDocumento.READALL())
