import sqlite3
import os


def obtener_conexion():
    ruta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biblioteca.db')
    return sqlite3.connect(ruta_db)


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            estado TEXT DEFAULT 'Disponible',
            prestado_por INTEGER DEFAULT NULL,
            FOREIGN KEY (prestado_por) REFERENCES socios(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            multas REAL DEFAULT 0.0)''')

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()