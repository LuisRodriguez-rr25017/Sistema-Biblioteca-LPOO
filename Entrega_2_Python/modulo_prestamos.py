from datetime import date
from Conexion_db import obtener_conexion


# =============================================
# MODULO 2: PRESTAMOS Y SOCIOS
# =============================================
def menu_prestamos():

    opcion = 0

    while opcion != 7:
        print("\n========================================")
        print("       MODULO DE PRESTAMOS Y SOCIOS")
        print("========================================")
        print("1. Registrar Socio")
        print("2. Registrar Prestamo")
        print("3. Registrar Devolucion")
        print("4. Ver estado de Socios")
        print("5. Ver Socios con Multas pendientes")
        print("6. Pagar Multa de un Socio")
        print("7. Volver al Menu Principal")
        print("========================================")

        try:
            opcion = int(input("Ingrese una opcion (1-7): "))

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
                        print("Libros en prestamo: ninguno")
                        print("Multa pendiente: $0.00")

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
                                """SELECT l.titulo, p.fecha_prestamo
                                   FROM prestamos p
                                   JOIN libros l ON l.id = p.libro_id
                                   WHERE p.socio_id = ? AND p.activo = 1""",
                                (s[0],)
                            )
                            libros_activos = cursor.fetchall()
                            libros_str = ", ".join(f"{lb[0]} (desde {lb[1]})" for lb in libros_activos) if libros_activos else "ninguno"
                            print(f"{s[0]}. {s[1]}")
                            print(f"   Libros en prestamo : {libros_str}")
                            print(f"   Multa pendiente    : ${s[2]:.2f}")

                        try:
                            idx_socio = int(input("\nSeleccione el numero del socio: "))

                            cursor.execute("SELECT id, nombre, multas FROM socios WHERE id = ?", (idx_socio,))
                            socio = cursor.fetchone()

                            if not socio:
                                print("Numero de socio invalido.")
                            elif socio[2] > 0:
                                print(f"\nERROR: {socio[1]} tiene multa pendiente de ${socio[2]:.2f}")
                                print("Debe pagar la multa antes de realizar un nuevo prestamo.")
                            else:
                                cursor.execute(
                                    "SELECT id, titulo, autor FROM libros WHERE estado = 'Disponible'"
                                )
                                libros_disponibles = cursor.fetchall()

                                if not libros_disponibles:
                                    print("No hay libros disponibles en este momento.")
                                else:
                                    print("\n--- Libros disponibles ---")
                                    for lb in libros_disponibles:
                                        print(f"{lb[0]}. {lb[1]}  |  Autor: {lb[2]}")

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
                                            fecha_hoy = date.today().strftime("%Y-%m-%d")

                                            cursor.execute(
                                                """INSERT INTO prestamos (socio_id, libro_id, fecha_prestamo, activo)
                                                   VALUES (?, ?, ?, 1)""",
                                                (socio[0], libro[0], fecha_hoy)
                                            )

                                            cursor.execute(
                                                "UPDATE libros SET estado = 'Prestado' WHERE id = ?",
                                                (libro[0],)
                                            )

                                            conexion.commit()

                                            print("\nPrestamo registrado exitosamente!")
                                            print(f"Socio          : {socio[1]}")
                                            print(f"Libro          : {libro[1]}")
                                            print(f"Fecha prestamo : {fecha_hoy}")
                                            print("Plazo          : 14 dias para devolver.")

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
                        SELECT p.id, s.id, s.nombre, l.id, l.titulo, p.fecha_prestamo
                        FROM prestamos p
                        JOIN socios s ON s.id = p.socio_id
                        JOIN libros l ON l.id = p.libro_id
                        WHERE p.activo = 1
                        ORDER BY s.nombre, p.fecha_prestamo
                    """)
                    prestamos_activos = cursor.fetchall()

                    print("\n=== REGISTRAR DEVOLUCION ===\n")

                    if not prestamos_activos:
                        print("Ningun socio tiene libros en prestamo actualmente.")
                        conexion.close()
                        input("\nPresione ENTER para continuar...")
                    else:
                        print("--- Prestamos activos ---")
                        for p in prestamos_activos:
                            print(f"Prestamo #{p[0]}  |  Socio: {p[2]}  ->  Libro: {p[4]}  |  Desde: {p[5]}")

                        try:
                            idx_prestamo = int(input("\nIngrese el numero del Prestamo a devolver (#): "))

                            prestamo = next((p for p in prestamos_activos if p[0] == idx_prestamo), None)

                            if not prestamo:
                                print("Numero de prestamo invalido o ya fue devuelto.")
                            else:
                                print(f"\nDevolucion del libro: '{prestamo[4]}'")
                                print(f"Socio: {prestamo[2]}  |  Fecha prestamo: {prestamo[5]}")
                                print("\nEl socio devuelve dentro del plazo de 14 dias?")
                                print("1. Si (sin multa)")
                                print("2. No (se aplica multa de $2 por dia de atraso)")
                                a_tiempo = int(input("Seleccione: "))

                                # Cerrar el prestamo
                                cursor.execute(
                                    "UPDATE prestamos SET activo = 0 WHERE id = ?",
                                    (prestamo[0],)
                                )

                                # Solo marcar disponible si no tiene otros prestamos activos
                                cursor.execute(
                                    "SELECT COUNT(*) FROM prestamos WHERE libro_id = ? AND activo = 1",
                                    (prestamo[3],)
                                )
                                otros = cursor.fetchone()[0]
                                if otros == 0:
                                    cursor.execute(
                                        "UPDATE libros SET estado = 'Disponible' WHERE id = ?",
                                        (prestamo[3],)
                                    )

                                if a_tiempo == 2:
                                    try:
                                        dias_atraso = int(input("Cuantos dias de atraso tiene? "))
                                        if dias_atraso <= 0:
                                            print("Los dias de atraso deben ser mayores a 0.")
                                        else:
                                            multa_nueva = dias_atraso * 2

                                            cursor.execute(
                                                "UPDATE socios SET multas = multas + ? WHERE id = ?",
                                                (multa_nueva, prestamo[1])
                                            )

                                            cursor.execute("SELECT multas FROM socios WHERE id = ?", (prestamo[1],))
                                            multa_total = cursor.fetchone()[0]

                                            print(f"\nMulta aplicada   : ${multa_nueva:.2f}")
                                            print(f"Multa total socio: ${multa_total:.2f}")
                                            print("\nDesea registrar el pago de la multa ahora?")
                                            print("1. Si, pago en este momento")
                                            print("2. No, pagara despues")

                                            try:
                                                pago = int(input("Seleccione: "))
                                                if pago == 1:
                                                    cursor.execute(
                                                        "UPDATE socios SET multas = 0 WHERE id = ?",
                                                        (prestamo[1],)
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
                                print(f"\nLibro '{prestamo[4]}' devuelto y disponible nuevamente.")

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
                                """SELECT l.titulo, p.fecha_prestamo
                                   FROM prestamos p
                                   JOIN libros l ON l.id = p.libro_id
                                   WHERE p.socio_id = ? AND p.activo = 1""",
                                (s[0],)
                            )
                            libros_activos = cursor.fetchall()

                            print(f"{s[0]}. {s[1]}")
                            if libros_activos:
                                print(f"   Libros en prestamo ({len(libros_activos)}):")
                                for lb in libros_activos:
                                    print(f"     - {lb[0]}  (desde {lb[1]})")
                            else:
                                print("   Libros en prestamo : ninguno")
                            print(f"   Multa pendiente    : ${s[2]:.2f}")
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
                                """SELECT l.titulo, p.fecha_prestamo
                                   FROM prestamos p
                                   JOIN libros l ON l.id = p.libro_id
                                   WHERE p.socio_id = ? AND p.activo = 1""",
                                (s[0],)
                            )
                            libros_activos = cursor.fetchall()
                            libros_str = ", ".join(lb[0] for lb in libros_activos) if libros_activos else "ninguno"

                            print(f"Socio : {s[1]}")
                            print(f"Libros en prestamo: {libros_str}")
                            print(f"Multa : ${s[2]:.2f}")
                            print("   ---------------------------------")

                    conexion.close()
                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 6: PAGAR MULTA
                # =====================================
                case 6:
                    conexion = obtener_conexion()
                    cursor = conexion.cursor()

                    cursor.execute("SELECT id, nombre, multas FROM socios WHERE multas > 0")
                    socios_multa = cursor.fetchall()

                    print("\n=== PAGO DE MULTAS ===\n")

                    if not socios_multa:
                        print("No hay socios con multas pendientes.")
                        conexion.close()
                        input("\nPresione ENTER para continuar...")
                    else:
                        print("--- Socios con multa pendiente ---")
                        for s in socios_multa:
                            print(f"{s[0]}. {s[1]}  |  Multa: ${s[2]:.2f}")

                        try:
                            idx_socio = int(input("\nSeleccione el numero del socio que va a pagar: "))

                            socio = next((s for s in socios_multa if s[0] == idx_socio), None)

                            if not socio:
                                print("Numero invalido o ese socio no tiene multa pendiente.")
                            else:
                                print(f"\nSocio      : {socio[1]}")
                                print(f"Multa total: ${socio[2]:.2f}")
                                print("\nTipo de pago:")
                                print("1. Pago total (salda toda la multa)")
                                print("2. Pago parcial")

                                tipo_pago = int(input("Seleccione: "))

                                if tipo_pago == 1:
                                    cursor.execute(
                                        "UPDATE socios SET multas = 0 WHERE id = ?",
                                        (socio[0],)
                                    )
                                    conexion.commit()
                                    print(f"\nMulta de ${socio[2]:.2f} pagada completamente.")
                                    print(f"{socio[1]} puede realizar nuevos prestamos.")

                                elif tipo_pago == 2:
                                    monto = float(input(f"Ingrese el monto a pagar (max ${socio[2]:.2f}): $"))

                                    if monto <= 0:
                                        print("El monto debe ser mayor a $0.")
                                    elif monto > socio[2]:
                                        print(f"El monto (${monto:.2f}) supera la multa (${socio[2]:.2f}).")
                                        print("Use pago total para saldar la deuda completa.")
                                    else:
                                        nueva_multa = socio[2] - monto
                                        cursor.execute(
                                            "UPDATE socios SET multas = ? WHERE id = ?",
                                            (nueva_multa, socio[0])
                                        )
                                        conexion.commit()
                                        print(f"\nPago parcial registrado: ${monto:.2f}")
                                        print(f"Multa restante: ${nueva_multa:.2f}")
                                        if nueva_multa > 0:
                                            print("El socio aun tiene multa pendiente.")
                                        else:
                                            print(f"{socio[1]} puede realizar nuevos prestamos.")
                                else:
                                    print("Opcion invalida.")

                        except ValueError:
                            print("Error: Ingrese un valor numerico valido.")

                        conexion.close()

                    input("\nPresione ENTER para continuar...")

                # =====================================
                # OPCION 7: VOLVER AL MENU
                # =====================================
                case 7:
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
