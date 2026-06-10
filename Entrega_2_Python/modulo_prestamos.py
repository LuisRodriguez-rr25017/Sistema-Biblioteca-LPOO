import sqlite3
import os


def obtener_conexion():
    ruta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biblioteca.db')
    return sqlite3.connect(ruta_db)


# =============================================
# MODULO 2: PRESTAMOS Y SOCIOS
# =============================================
def menu_prestamos():

    opcion = 0

    while opcion != 6:
        print("\n========================================")
        print("       MODULO DE PRESTAMOS Y SOCIOS")
        print("========================================")
        print("1. Registrar Socio")
        print("2. Registrar Prestamo")
        print("3. Registrar Devolucion")
        print("4. Ver estado de Socios")
        print("5. Ver Socios con Multas pendientes")
        print("6. Volver al Menu Principal")
        print("========================================")

        try:
            opcion = int(input("Ingrese una opcion (1-6): "))

            match opcion:

                # =====================================
                # OPCION 1: REGISTRAR SOCIO
                # =====================================
                case 1:
                    nombre = input("Nombre completo del socio: ").strip()

                    if nombre == "":
                        print("Error: El nombre no puede estar vacio.")
                    else:
                        conexion = obtener_conexion()
                        cursor = conexion.cursor()

                        cursor.execute(
                            "INSERT INTO socios (nombre, multas) VALUES (?, ?)",
                            (nombre, 0.0)
                        )

                        conexion.commit()
                        conexion.close()

                        print("\nSocio registrado exitosamente!")
                        print(f"Nombre: {nombre}")
                        print("Libro en prestamo: ninguno")
                        print("Multa pendiente: $0")

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 2: REGISTRAR PRESTAMO
                # =====================================
                case 2:
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute("SELECT COUNT(*) FROM socios")
                    total_socios = cursor.fetchone()[0]

                    cursor.execute("SELECT COUNT(*) FROM libros")
                    total_libros = cursor.fetchone()[0]

                    if total_socios == 0:
                        print("No hay socios registrados. Registre un socio primero.")
                        conexion.close()
                        input("\nPresione ENTER para continuar...")

                    elif total_libros == 0:
                        print("No hay libros registrados en el sistema.")
                        conexion.close()
                        input("\nPresione ENTER para continuar...")

                    else:
                        cursor.execute("SELECT id, nombre, multas FROM socios")
                        socios = cursor.fetchall()

                        print("\n--- Socios registrados ---")
                        for s in socios:
                            cursor.execute(
                                "SELECT titulo FROM libros WHERE prestado_por = ?", (s[0],)
                            )
                            libro_actual = cursor.fetchone()
                            libro_str = libro_actual[0] if libro_actual else "ninguno"
                            print(f"{s[0]}. {s[1]}")
                            print(f"   Libro actual  : {libro_str}")
                            print(f"   Multa pendiente: ${s[2]:.2f}")

                        try:
                            idx_socio = int(input("\nSeleccione el numero del socio: "))

                            cursor.execute("SELECT id, nombre, multas FROM socios WHERE id = ?", (idx_socio,))
                            socio = cursor.fetchone()

                            if not socio:
                                print("Numero de socio invalido.")
                            else:
                                cursor.execute(
                                    "SELECT titulo FROM libros WHERE prestado_por = ?", (socio[0],)
                                )
                                libro_prestado = cursor.fetchone()

                                if libro_prestado:
                                    print(f"\nERROR: {socio[1]} ya tiene prestado el libro:")
                                    print(f"       {libro_prestado[0]}")
                                    print("Debe devolverlo antes de solicitar otro.")

                                elif socio[2] > 0:
                                    print(f"\nERROR: {socio[1]} tiene multa pendiente de ${socio[2]:.2f}")
                                    print("Debe pagar la multa antes de realizar un prestamo.")

                                else:
                                    cursor.execute(
                                        "SELECT id, titulo FROM libros WHERE estado = 'Disponible'"
                                    )
                                    libros_disponibles = cursor.fetchall()

                                    if not libros_disponibles:
                                        print("No hay libros disponibles en este momento.")
                                    else:
                                        print("\n--- Libros disponibles ---")
                                        for l in libros_disponibles:
                                            print(f"{l[0]}. {l[1]}  [Disponible]")

                                        try:
                                            idx_libro = int(input("\nSeleccione el numero del libro: "))

                                            cursor.execute(
                                                "SELECT id, titulo, estado FROM libros WHERE id = ?", (idx_libro,)
                                            )
                                            libro = cursor.fetchone()

                                            if not libro:
                                                print("Numero de libro invalido.")
                                            elif libro[2] != "Disponible":
                                                print("Ese libro no esta disponible actualmente.")
                                            else:
                                                cursor.execute(
                                                    "UPDATE libros SET estado = 'Prestado', prestado_por = ? WHERE id = ?",
                                                    (socio[0], libro[0])
                                                )
                                                conexion.commit()

                                                print("\nPrestamo registrado exitosamente!")
                                                print(f"Socio : {socio[1]}")
                                                print(f"Libro : {libro[1]}")
                                                print("Plazo : 14 dias para devolver.")

                                        except ValueError:
                                            print("Error: Debe ingresar un numero valido.")

                        except ValueError:
                            print("Error: Debe ingresar un numero valido.")

                        conexion.close()

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 3: REGISTRAR DEVOLUCION
                # =====================================
                case 3:
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute("""
                        SELECT s.id, s.nombre, l.id, l.titulo
                        FROM socios s
                        JOIN libros l ON l.prestado_por = s.id
                    """)
                    prestamos_activos = cursor.fetchall()

                    print("\n=== REGISTRAR DEVOLUCION ===\n")

                    if not prestamos_activos:
                        print("Ningun socio tiene libros en prestamo actualmente.")
                        conexion.close()
                        input("\nPresione ENTER para continuar...")
                    else:
                        print("--- Socios con libro prestado ---")
                        for p in prestamos_activos:
                            print(f"{p[0]}. {p[1]}  ->  {p[3]}")

                        try:
                            idx_dev = int(input("\nSeleccione el numero del socio que devuelve: "))

                            prestamo = next((p for p in prestamos_activos if p[0] == idx_dev), None)

                            if not prestamo:
                                print("Ese socio no tiene ningun libro en prestamo o el numero es invalido.")
                            else:
                                print("\nEl socio devuelve dentro del plazo de 14 dias?")
                                print("1. Si (sin multa)")
                                print("2. No (se aplica multa de $2 por dia)")
                                a_tiempo = int(input("Seleccione: "))

                                cursor.execute(
                                    "UPDATE libros SET estado = 'Disponible', prestado_por = NULL WHERE id = ?",
                                    (prestamo[2],)
                                )

                                if a_tiempo == 2:
                                    try:
                                        dias_atraso = int(input("Cuantos dias de atraso tiene? "))
                                        multa_nueva = dias_atraso * 2

                                        cursor.execute(
                                            "UPDATE socios SET multas = multas + ? WHERE id = ?",
                                            (multa_nueva, prestamo[0])
                                        )

                                        cursor.execute("SELECT multas FROM socios WHERE id = ?", (prestamo[0],))
                                        multa_total = cursor.fetchone()[0]

                                        print(f"\nMulta aplicada   : ${multa_nueva}")
                                        print(f"Multa total socio: ${multa_total:.2f}")

                                        print("\nDesea registrar el pago de la multa ahora?")
                                        print("1. Si, pago en este momento")
                                        print("2. No, pagara despues")

                                        try:
                                            pago = int(input("Seleccione: "))
                                            if pago == 1:
                                                cursor.execute(
                                                    "UPDATE socios SET multas = 0 WHERE id = ?",
                                                    (prestamo[0],)
                                                )
                                                print("Multa pagada. El socio puede realizar nuevos prestamos.")
                                            else:
                                                print("Multa pendiente. El socio debera pagarla antes del proximo prestamo.")
                                        except ValueError:
                                            print("Error: Ingrese una opcion valida.")

                                    except ValueError:
                                        print("Error: Ingrese un numero valido de dias.")
                                else:
                                    print("Devolucion a tiempo. Sin multa.")

                                conexion.commit()
                                print("Libro devuelto y disponible nuevamente.")

                        except ValueError:
                            print("Error: Debe ingresar un numero valido.")

                        conexion.close()

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 4: VER ESTADO DE SOCIOS
                # =====================================
                case 4:
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute("SELECT id, nombre, multas FROM socios")
                    socios = cursor.fetchall()

                    print("\n=== ESTADO ACTUAL DE SOCIOS ===\n")

                    if not socios:
                        print("No hay socios registrados.")
                    else:
                        for s in socios:
                            cursor.execute(
                                "SELECT titulo FROM libros WHERE prestado_por = ?", (s[0],)
                            )
                            libro_actual = cursor.fetchone()
                            libro_str = libro_actual[0] if libro_actual else "ninguno"

                            print(f"{s[0]}. {s[1]}")
                            print(f"   Libro en prestamo : {libro_str}")
                            print(f"   Multa pendiente   : ${s[2]:.2f}")
                            print("   ---------------------------------")

                    conexion.close()
                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 5: VER MULTAS PENDIENTES
                # =====================================
                case 5:
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute("SELECT id, nombre, multas FROM socios WHERE multas > 0")
                    socios_multa = cursor.fetchall()

                    print("\n=== SOCIOS CON MULTAS PENDIENTES ===\n")

                    if not socios_multa:
                        print("No hay socios con multas pendientes.")
                    else:
                        for s in socios_multa:
                            cursor.execute(
                                "SELECT titulo FROM libros WHERE prestado_por = ?", (s[0],)
                            )
                            libro_actual = cursor.fetchone()
                            libro_str = libro_actual[0] if libro_actual else "ninguno"

                            print(f"Socio : {s[1]}")
                            print(f"Libro : {libro_str}")
                            print(f"Multa : ${s[2]:.2f}")
                            print("   ---------------------------------")

                    conexion.close()
                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 6: VOLVER AL MENU
                # =====================================
                case 6:
                    print("Volviendo al Menu Principal...")

                # =====================================
                # OPCION INVALIDA
                # =====================================
                case _:
                    print("Opcion invalida. Intente de nuevo.")
                    input("\nPresione ENTER para continuar...")

        except ValueError:
            print("Error: Debe ingresar un numero entero valido.")
            input("\nPresione ENTER para continuar...")