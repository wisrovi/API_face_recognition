import mysql.connector
from config.config import DATABASE_CONECTION
from mysql.connector import errorcode


class Dao:
    def insertar(self, comando):
        try:
            with mysql.connector.connect(**DATABASE_CONECTION) as mydb:
                # print(mydb)
                with mydb.cursor() as cursor:
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

    def leerTodo(self, comando):
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
