import sqlite3
import os
 
 
def obtener_conexion():
    ruta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biblioteca.db')
    return sqlite3.connect(ruta_db)
 
 
def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
 
    # Tabla de socios
    cursor.execute('''CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            multas REAL DEFAULT 0.0)''')
 
    # Tabla de libros (sin prestado_por, eso ahora lo maneja la tabla prestamos)
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            estado TEXT DEFAULT 'Disponible')''')
 
    # Tabla de prestamos: permite multiples libros por socio y guarda la fecha
    cursor.execute('''CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER NOT NULL,
            libro_id INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (socio_id) REFERENCES socios(id),
            FOREIGN KEY (libro_id) REFERENCES libros(id))''')
 
    conexion.commit()
    conexion.close()
 
 
if __name__ == "__main__":
    crear_tablas()
 