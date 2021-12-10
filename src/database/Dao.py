import datetime

import mysql.connector
from config.config import DATABASE_CONECTION
from mysql.connector import errorcode
from database.Database import BASEDATOS, Database
from libraries.GeneradorLicenseAndToken import GeneradorLicenseAndToken

generator = GeneradorLicenseAndToken()


class Dao:

    def __init__(self):
        self.crear_basedatos(Database.base.create_database(BASEDATOS))

        self.crear_tabla(Database.vector.BUILD())

        self.crear_tabla(Database.relacionPersonaVector.BUILD())

        if self.crear_tabla(Database.tipoDocumento.BUILD()):
            self.insertar(Database.tipoDocumento.INSERT("CC", "Cedula"))
            self.insertar(Database.tipoDocumento.INSERT("RC", "Registro Civil"))
            self.insertar(Database.tipoDocumento.INSERT("CE", "Cedula Extranjeria"))
            print("Tipos Documento creados")

        if self.crear_tabla(Database.rolUsuario.BUILD()):
            self.insertar(Database.rolUsuario.INSERT("SUPER", "ERASE, UPDATE, REGISTRAR AND READ"))
            self.insertar(Database.rolUsuario.INSERT("ADMIN", "UPDATE, REGISTRAR AND READ"))
            self.insertar(Database.rolUsuario.INSERT("AVANCED", "REGISTRAR AND READ"))
            self.insertar(Database.rolUsuario.INSERT("BASIC", "READ"))
            print("Roles creados")

        if self.crear_tabla(Database.persona.BUILD()):
            self.insertar(Database.persona.INSERT(
                "William", "Steve", "Rodriguez", "Villamizar",
                1, 1098685961))
            print("Persona creada")

        if self.crear_tabla(Database.usuario.BUILD()):
            self.insertar(Database.usuario.INSERT(
                1,
                "wisrovi", "rodriguez",
                "wisrovi.rodriguez@gmail.com",
                1, 1))
            print("Usuario creado")

        if self.crear_tabla(Database.licencia.BUILD()):
            self.insertar(Database.licencia.INSERT(
                licencia=generator.CrearLicencia(3650)[1],
                id_usuario=1,
                cantidad_maxima_rostros=5e9,
                plan_bytes=5e9,
                cantidad_hijos=5e9,
                id_usuario_owner=1,
                fechaVencimiento=datetime.datetime.now() + datetime.timedelta(days=3650)
            ))
            print("Licencia Root creada")

        self.crear_tabla(Database.log.BUILD())

        self.crear_vista(Database.vistas.BuildSummary())

    @staticmethod
    def ejecutar_comando_sin_respuesta(comando):
        try:
            with mysql.connector.connect(**DATABASE_CONECTION) as mydb:
                # print(mydb)
                with mydb.cursor() as cursor:
                    # cursor.execute(Base().create_database(BASEDATOS))
                    # mydb.commit()
                    cursor.execute(comando)
                    mydb.commit()
                    return True

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return False

    @staticmethod
    def ejecutar_comando_con_respuesta(comando):
        try:
            with mysql.connector.connect(**DATABASE_CONECTION) as mydb:
                # print(mydb)
                with mydb.cursor() as cursor:
                    cursor.execute(comando)
                    result = cursor.fetchall()
                    return result

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None

    def leerTodo(self, comando):
        return self.ejecutar_comando_con_respuesta(comando)

    def insertar(self, comando):
        return self.ejecutar_comando_sin_respuesta(comando)

    def crear_tabla(self, comando):
        return self.ejecutar_comando_sin_respuesta(comando)

    def crear_basedatos(self, comando):
        return self.ejecutar_comando_sin_respuesta(comando)

    def crear_vista(self, comando):
        return self.ejecutar_comando_sin_respuesta(comando)
