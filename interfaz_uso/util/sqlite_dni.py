import sqlite3


class DatabaseHandler:
    def __init__(self, db_name="database/dni_db.db"):
        self.db_name = db_name

    def __enter__(self):
        """Inicia la conexión al entrar en el contexto."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.crear_tabla()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cierra la conexión al salir del contexto."""
        if hasattr(self, "conn"):
            self.conn.close()

    def crear_tabla(self):
        """Crea la tabla si no existe."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mi_tabla (
                numero INTEGER PRIMARY KEY,
                texto TEXT,
                dni TEXT
            )
        """
        )
        self.conn.commit()

    def insertar_registro(self, numero, texto, dni):
        """Inserta un registro en la tabla."""
        try:
            self.cursor.execute(
                "INSERT INTO mi_tabla (numero, texto, dni) VALUES (?, ?, ?)",
                (numero, texto, dni),
            )
            self.conn.commit()
            print("Registro insertado exitosamente.")
        except sqlite3.IntegrityError:
            print("Error: El número ya existe en la base de datos.")

    def buscar_por_numero(self, numero):
        """Busca un registro en la tabla por el campo 'numero'."""
        self.cursor.execute("SELECT * FROM mi_tabla WHERE numero = ?", (numero,))
        resultado = self.cursor.fetchone()
        if resultado:
            return {"numero": resultado[0], "texto": resultado[1], "dni": resultado[2]}
        else:
            return None

    def buscar_por_dni(self, dni):
        """Busca registros en la tabla por el campo 'dni'."""
        self.cursor.execute("SELECT * FROM mi_tabla WHERE dni = ?", (dni,))
        resultados = self.cursor.fetchall()
        return [{"numero": r[0], "texto": r[1], "dni": r[2]} for r in resultados]


if __name__ == "__main__":
    # Uso de la clase con 'with' para manejar automáticamente la conexión
    with DatabaseHandler() as db_handler:
        # Insertar un registro
        db_handler.insertar_registro(2, "fingerprint", "12345678A")
        db_handler.insertar_registro(1, "fingerprint2", "12345678A")

        # Buscar por número
        registro = db_handler.buscar_por_numero(1)
        print("Resultado de búsqueda por número:", registro)

        # Buscar por DNI
        registros_dni = db_handler.buscar_por_dni("12345678A")
        print("Resultados de búsqueda por DNI:", registros_dni)
