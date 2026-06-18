"""
Módulo 1: Registro de Libros y Autores.
Capa de negocio CRUD sobre la tabla 'libros' en Supabase (schema.sql).
Consumido por el menú CLI y por los endpoints FastAPI en main.py.
"""

from db_config import supabase


def _estado_texto(disponible):
    """Convierte el campo booleano 'disponible' a texto legible para el usuario."""
    return "Disponible" if disponible else "Prestado"


# ─────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────
def crear_libro(titulo, autor, portada_url=None):
    """Inserta un libro en Supabase. Por defecto queda disponible."""
    datos = {
        "titulo": titulo,
        "autor": autor,
        "portada_url": portada_url,
        "disponible": True,
    }
    respuesta = supabase.table("libros").insert(datos).execute()
    return respuesta.data[0]


# ─────────────────────────────────────────────
# READ
# ─────────────────────────────────────────────
def listar_libros():
    """Devuelve todos los libros registrados."""
    respuesta = (
        supabase.table("libros")
        .select("id, titulo, autor, portada_url, disponible")
        .order("id")
        .execute()
    )
    return respuesta.data


def buscar_libros_por_titulo(titulo_buscar):
    """Búsqueda flexible por título (ilike %titulo%)."""
    respuesta = (
        supabase.table("libros")
        .select("id, titulo, autor, portada_url, disponible")
        .ilike("titulo", f"%{titulo_buscar}%")
        .execute()
    )
    return respuesta.data


def obtener_libro(libro_id):
    """Obtiene un libro por su ID. Retorna None si no existe."""
    respuesta = (
        supabase.table("libros")
        .select("id, titulo, autor, portada_url, disponible")
        .eq("id", libro_id)
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None


# ─────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────
def actualizar_libro(libro_id, titulo, autor, portada_url=None):
    """Actualiza título, autor y portada de un libro existente."""
    datos = {"titulo": titulo, "autor": autor, "portada_url": portada_url}
    respuesta = (
        supabase.table("libros")
        .update(datos)
        .eq("id", libro_id)
        .execute()
    )
    return len(respuesta.data) > 0


# ─────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────
def eliminar_libro(libro_id):
    """
    Elimina un libro si no tiene préstamos activos (devuelto = FALSE).
    Retorna (exito: bool, mensaje: str).
    """
    activos = (
        supabase.table("prestamos")
        .select("id")
        .eq("libro_id", libro_id)
        .eq("devuelto", False)
        .execute()
    )

    if activos.data:
        return False, "No se puede eliminar: el libro tiene préstamos activos."

    # Borrar historial de préstamos devueltos antes del libro (clave foránea)
    supabase.table("prestamos").delete().eq("libro_id", libro_id).execute()

    respuesta = supabase.table("libros").delete().eq("id", libro_id).execute()

    if respuesta.data:
        return True, "Libro eliminado exitosamente."
    return False, "No se encontró el libro con ese ID."


# ─────────────────────────────────────────────
# MENÚ INTERACTIVO (CLI)
# ─────────────────────────────────────────────
def menu_libros():
    opcion = 0

    while opcion != 6:
        print("\n========================================")
        print("       REGISTRO DE LIBROS Y AUTORES")
        print("========================================")
        print("1. Registrar nuevo libro y autor")
        print("2. Mostrar todos los libros registrados")
        print("3. Buscar libro por titulo")
        print("4. Actualizar libro existente")
        print("5. Eliminar libro")
        print("6. Volver al Menu Principal")
        print("========================================")

        try:
            opcion = int(input("Ingrese una opcion (1-6): "))

            match opcion:

                case 1:
                    titulo = input("Ingrese el titulo del libro: ").strip()
                    autor = input("Ingrese el nombre del autor: ").strip()
                    portada = input("URL de portada (opcional, ENTER para omitir): ").strip()

                    if titulo == "" or autor == "":
                        print("Error: El titulo y el autor no pueden estar vacios.")
                    else:
                        portada_url = portada if portada else None
                        libro = crear_libro(titulo, autor, portada_url)

                        print("\nLibro registrado exitosamente!")
                        print(f"ID     : {libro['id']}")
                        print(f"Titulo : {titulo}")
                        print(f"Autor  : {autor}")
                        if portada_url:
                            print(f"Portada: {portada_url}")
                        print("Estado : Disponible")

                    input("\nPresione ENTER para continuar...")

                case 2:
                    libros = listar_libros()
                    print("\n=== LISTADO DE LIBROS REGISTRADOS ===\n")

                    if not libros:
                        print("Aun no hay libros registrados.")
                    else:
                        for libro in libros:
                            print(f"{libro['id']}. {libro['titulo']}")
                            print(f"   Autor  : {libro['autor']}")
                            print(f"   Estado : {_estado_texto(libro['disponible'])}")
                            if libro.get("portada_url"):
                                print(f"   Portada: {libro['portada_url']}")
                            print("   -----------------------------------")

                    input("\nPresione ENTER para continuar...")

                case 3:
                    titulo_buscar = input("Ingrese el titulo del libro a buscar: ").strip()
                    resultados = buscar_libros_por_titulo(titulo_buscar)

                    if resultados:
                        print(f"\nSe encontraron {len(resultados)} resultado(s):")
                        for libro in resultados:
                            print(f"\nID     : {libro['id']}")
                            print(f"Titulo : {libro['titulo']}")
                            print(f"Autor  : {libro['autor']}")
                            print(f"Estado : {_estado_texto(libro['disponible'])}")
                            print("   -----------------------------------")
                    else:
                        print(f"\nNo se encontro ningun libro con el titulo: '{titulo_buscar}'")

                    input("\nPresione ENTER para continuar...")

                case 4:
                    try:
                        libro_id = int(input("Ingrese el ID del libro a actualizar: "))
                        libro = obtener_libro(libro_id)

                        if not libro:
                            print("No se encontro un libro con ese ID.")
                        else:
                            print(f"\nDatos actuales: '{libro['titulo']}' — {libro['autor']}")
                            titulo = input("Nuevo titulo (ENTER para mantener): ").strip()
                            autor = input("Nuevo autor (ENTER para mantener): ").strip()
                            portada = input("Nueva URL portada (ENTER para mantener): ").strip()

                            nuevo_titulo = titulo if titulo else libro["titulo"]
                            nuevo_autor = autor if autor else libro["autor"]
                            nueva_portada = portada if portada else libro.get("portada_url")

                            if actualizar_libro(libro_id, nuevo_titulo, nuevo_autor, nueva_portada):
                                print("\nLibro actualizado exitosamente!")
                            else:
                                print("No se pudo actualizar el libro.")

                    except ValueError:
                        print("Error: Debe ingresar un ID numerico valido.")

                    input("\nPresione ENTER para continuar...")

                case 5:
                    try:
                        libro_id = int(input("Ingrese el ID del libro a eliminar: "))
                        confirmar = input(
                            f"¿Confirma eliminar el libro #{libro_id}? (s/n): "
                        ).strip().lower()

                        if confirmar == "s":
                            exito, mensaje = eliminar_libro(libro_id)
                            print(f"\n{mensaje}")
                        else:
                            print("Operacion cancelada.")

                    except ValueError:
                        print("Error: Debe ingresar un ID numerico valido.")

                    input("\nPresione ENTER para continuar...")

                case 6:
                    print("Volviendo al Menu Principal...")

                case _:
                    print("Opcion invalida. Por favor ingrese una opcion entre 1 y 6.")
                    input("\nPresione ENTER para continuar...")

        except ValueError:
            print("Error: Debe ingresar un numero entero valido.")
            input("\nPresione ENTER para continuar...")
        except Exception as e:
            print(f"Error de conexion con Supabase: {e}")
            input("\nPresione ENTER para continuar...")