import sqlite3
import os

def crear_tablas():
    ruta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biblioteca.db')
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            estado TEXT DEFAULT 'Disponible')''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            libros_prestados INTEGER DEFAULT 0,
            multas REAL DEFAULT 0.0)''')
            
    cursor.execute("SELECT COUNT(*) FROM socios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO socios (nombre) VALUES ('Socio de Prueba')")
        
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()