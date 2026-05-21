
import sqlite3
import os


def obtener_conexion():
    ruta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biblioteca.db')
    return sqlite3.connect(ruta_db)


# =============================================
# MODULO 1: REGISTRO DE LIBROS Y AUTORES
# =============================================
def menu_libros():

    opcion = 0

    while opcion != 4:
        print("\n========================================")
        print("       REGISTRO DE LIBROS Y AUTORES")
        print("========================================")
        print("1. Registrar nuevo libro y autor")
        print("2. Mostrar todos los libros registrados")
        print("3. Buscar libro por titulo")
        print("4. Volver al Menu Principal")
        print("========================================")

        try:
            opcion = int(input("Ingrese una opcion (1-4): "))

            match opcion:

                # =====================================
                # REGISTRAR LIBRO
                # =====================================
                case 1:
                    titulo = input("Ingrese el titulo del libro: ").strip()
                    autor = input("Ingrese el nombre del autor: ").strip()

                    if titulo == "" or autor == "":
                        print("Error: El titulo y el autor no pueden estar vacios.")
                    else:
                        conexion = obtener_conexion()
                        cursor = conexion.cursor()

                        cursor.execute(
                            "INSERT INTO libros (titulo, autor, estado) VALUES (?, ?, ?)",
                            (titulo, autor, "Disponible")
                        )

                        conexion.commit()
                        conexion.close()

                        print("\nLibro registrado exitosamente!")
                        print(f"Titulo: {titulo}")
                        print(f"Autor: {autor}")
                        print("Estado: Disponible")

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # MOSTRAR LIBROS
                # =====================================
                case 2:
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute("SELECT id, titulo, autor, estado FROM libros")
                    libros = cursor.fetchall()

                    conexion.close()

                    print("\n=== LISTADO DE LIBROS REGISTRADOS ===\n")

                    if len(libros) == 0:
                        print("Aun no hay libros registrados.")
                    else:
                        for libro in libros:
                            print(f"{libro[0]}. {libro[1]}")
                            print(f"   Autor: {libro[2]}")
                            print(f"   Estado: {libro[3]}")
                            print("   -----------------------------------")

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # BUSCAR LIBRO
                # =====================================
                case 3:
                    titulo_buscar = input("Ingrese el titulo del libro a buscar: ").strip()

                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute(
                        "SELECT titulo, autor, estado FROM libros WHERE titulo = ?",
                        (titulo_buscar,)
                    )

                    libro = cursor.fetchone()

                    conexion.close()

                    if libro:
                        print("\nLibro encontrado!")
                        print(f"Titulo: {libro[0]}")
                        print(f"Autor: {libro[1]}")
                        print(f"Estado: {libro[2]}")
                    else:
                        print(f"\nNo se encontro ningun libro con el titulo: {titulo_buscar}")

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # VOLVER AL MENU
                # =====================================
                case 4:
                    print("Volviendo al Menu Principal...")

                # =====================================
                # OPCION INVALIDA
                # =====================================
                case _:
                    print("Opcion invalida. Por favor ingrese una opcion entre 1 y 4.")
                    input("\nPresione ENTER para continuar...")

        except ValueError:
            print("Error: Debe ingresar un numero entero valido.")
            input("\nPresione ENTER para continuar...")