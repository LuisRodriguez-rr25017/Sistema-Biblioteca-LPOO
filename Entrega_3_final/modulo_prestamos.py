"""
Módulo 2: Préstamos y Socios.
Capa de negocio CRUD sobre las tablas 'socios' y 'prestamos' en Supabase.
Consumido por el menú CLI y por los endpoints FastAPI en main.py.
"""

from datetime import date, timedelta
from db_config import supabase

PLAZO_DIAS = 14
MULTA_POR_DIA = 2.0


def _float(valor):
    """Normaliza valores numéricos que Supabase puede devolver como str o Decimal."""
    return float(valor) if valor is not None else 0.0


def _mapear_libro_activo(fila):
    """Aplana la respuesta anidada de Supabase para el menú CLI."""
    libro = fila.get("libros") or {}
    return {
        "titulo": libro.get("titulo", "Desconocido"),
        "fecha_prestamo": fila["fecha_prestamo"],
        "fecha_limite": fila.get("fecha_limite"),
    }


def _mapear_prestamo_activo(fila):
    """Aplana préstamos activos con datos de socio y libro."""
    socio = fila.get("socios") or {}
    libro = fila.get("libros") or {}
    return {
        "id": fila["id"],
        "socio_id": fila["socio_id"],
        "nombre": socio.get("nombre", "Desconocido"),
        "libro_id": fila["libro_id"],
        "titulo": libro.get("titulo", "Desconocido"),
        "fecha_prestamo": fila["fecha_prestamo"],
        "fecha_limite": fila.get("fecha_limite"),
    }


# ─────────────────────────────────────────────
# CRUD SOCIOS
# ─────────────────────────────────────────────

def crear_socio(nombre, telefono=None, email=None):
    """CREATE — Registra un nuevo socio."""
    datos = {
        "nombre": nombre,
        "telefono": telefono,
        "email": email,
        "multa_actual": 0.0,
    }
    respuesta = supabase.table("socios").insert(datos).execute()
    return respuesta.data[0]["id"]


def listar_socios():
    """READ — Obtiene todos los socios."""
    respuesta = (
        supabase.table("socios")
        .select("id, nombre, telefono, email, multa_actual")
        .order("id")
        .execute()
    )
    return respuesta.data


def obtener_socio(socio_id):
    """READ — Obtiene un socio por ID."""
    respuesta = (
        supabase.table("socios")
        .select("id, nombre, telefono, email, multa_actual")
        .eq("id", socio_id)
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None


def actualizar_socio(socio_id, nombre, telefono=None, email=None):
    """UPDATE — Modifica los datos de un socio."""
    datos = {"nombre": nombre, "telefono": telefono, "email": email}
    respuesta = (
        supabase.table("socios")
        .update(datos)
        .eq("id", socio_id)
        .execute()
    )
    return len(respuesta.data) > 0


def eliminar_socio(socio_id):
    """
    DELETE — Elimina un socio sin préstamos activos ni multas.
    Retorna (exito: bool, mensaje: str).
    """
    socio = obtener_socio(socio_id)
    if not socio:
        return False, "No se encontro el socio con ese ID."

    if _float(socio["multa_actual"]) > 0:
        return False, "No se puede eliminar: el socio tiene multa pendiente."

    activos = (
        supabase.table("prestamos")
        .select("id")
        .eq("socio_id", socio_id)
        .eq("devuelto", False)
        .execute()
    )
    if activos.data:
        return False, "No se puede eliminar: el socio tiene prestamos activos."

    supabase.table("socios").delete().eq("id", socio_id).execute()
    return True, "Socio eliminado exitosamente."


def listar_socios_con_multa():
    """READ — Socios con multa_actual > 0."""
    respuesta = (
        supabase.table("socios")
        .select("id, nombre, multa_actual")
        .gt("multa_actual", 0)
        .execute()
    )
    return respuesta.data


def obtener_libros_activos_socio(socio_id):
    """READ — Préstamos no devueltos de un socio."""
    respuesta = (
        supabase.table("prestamos")
        .select("fecha_prestamo, fecha_limite, libros(titulo)")
        .eq("socio_id", socio_id)
        .eq("devuelto", False)
        .execute()
    )
    return [_mapear_libro_activo(f) for f in respuesta.data]


# ─────────────────────────────────────────────
# CRUD PRÉSTAMOS
# ─────────────────────────────────────────────

def contar_registros():
    """Cuenta socios y libros antes de registrar un préstamo."""
    socios = supabase.table("socios").select("id", count="exact").execute()
    libros = supabase.table("libros").select("id", count="exact").execute()
    return socios.count or 0, libros.count or 0


def listar_libros_disponibles():
    """READ — Libros con disponible = TRUE."""
    respuesta = (
        supabase.table("libros")
        .select("id, titulo, autor")
        .eq("disponible", True)
        .execute()
    )
    return respuesta.data


def registrar_prestamo(socio_id, libro_id):
    """
    CREATE — Registra un préstamo y marca el libro como no disponible.
    Retorna (exito: bool, mensaje: str, fecha_prestamo: str).
    """
    socio = obtener_socio(socio_id)
    if not socio:
        return False, "Numero de socio invalido.", None

    multa = _float(socio["multa_actual"])
    if multa > 0:
        return (
            False,
            f"ERROR: {socio['nombre']} tiene multa pendiente de ${multa:.2f}. "
            "Debe pagar la multa antes de realizar un nuevo prestamo.",
            None,
        )

    resp_libro = (
        supabase.table("libros")
        .select("id, titulo, disponible")
        .eq("id", libro_id)
        .execute()
    )
    if not resp_libro.data:
        return False, "Numero de libro invalido.", None

    libro = resp_libro.data[0]
    if not libro["disponible"]:
        return False, "Ese libro no esta disponible actualmente.", None

    fecha_hoy = date.today()
    fecha_limite = fecha_hoy + timedelta(days=PLAZO_DIAS)
    fecha_str = fecha_hoy.isoformat()
    limite_str = fecha_limite.isoformat()

    supabase.table("prestamos").insert({
        "socio_id": socio_id,
        "libro_id": libro_id,
        "fecha_prestamo": fecha_str,
        "devuelto": False,
        "fecha_limite": limite_str,
    }).execute()

    supabase.table("libros").update({"disponible": False}).eq("id", libro_id).execute()

    return True, libro["titulo"], fecha_str


def listar_prestamos_activos():
    """READ — Préstamos con devuelto = FALSE, incluyendo socio y libro."""
    respuesta = (
        supabase.table("prestamos")
        .select(
            "id, socio_id, libro_id, fecha_prestamo, fecha_limite, "
            "socios(nombre), libros(titulo)"
        )
        .eq("devuelto", False)
        .order("fecha_prestamo")
        .execute()
    )
    return [_mapear_prestamo_activo(f) for f in respuesta.data]


def registrar_devolucion(prestamo_id, a_tiempo, dias_atraso=0, pagar_multa_ahora=False):
    """
    UPDATE — Cierra un préstamo, libera el libro y aplica multa si corresponde.
    Retorna (exito: bool, mensaje: str).
    """
    respuesta = (
        supabase.table("prestamos")
        .select(
            "id, socio_id, libro_id, fecha_prestamo, fecha_limite, "
            "socios(nombre), libros(titulo)"
        )
        .eq("id", prestamo_id)
        .eq("devuelto", False)
        .execute()
    )

    if not respuesta.data:
        return False, "Numero de prestamo invalido o ya fue devuelto."

    prestamo = _mapear_prestamo_activo(respuesta.data[0])
    fecha_hoy = date.today().isoformat()
    multa_nueva = 0.0

    if not a_tiempo:
        if dias_atraso <= 0:
            return False, "Los dias de atraso deben ser mayores a 0."
        multa_nueva = dias_atraso * MULTA_POR_DIA

    supabase.table("prestamos").update({
        "devuelto": True,
        "fecha_devolucion": fecha_hoy,
        "multa_generada": multa_nueva,
    }).eq("id", prestamo_id).execute()

    supabase.table("libros").update({"disponible": True}).eq("id", prestamo["libro_id"]).execute()

    if multa_nueva > 0:
        socio = obtener_socio(prestamo["socio_id"])
        multa_total = _float(socio["multa_actual"]) + multa_nueva

        if pagar_multa_ahora:
            supabase.table("socios").update({"multa_actual": 0}).eq("id", prestamo["socio_id"]).execute()
            mensaje_multa = f"Multa de ${multa_nueva:.2f} pagada en este momento."
        else:
            supabase.table("socios").update({"multa_actual": multa_total}).eq("id", prestamo["socio_id"]).execute()
            mensaje_multa = (
                f"Multa aplicada: ${multa_nueva:.2f}. "
                f"Multa total del socio: ${multa_total:.2f}. Pendiente de pago."
            )
    else:
        mensaje_multa = "Devolucion a tiempo. Sin multa."

    return True, (
        f"Libro '{prestamo['titulo']}' devuelto y disponible nuevamente. {mensaje_multa}"
    )


def pagar_multa(socio_id, monto, pago_total=False):
    """
    UPDATE — Registra pago total o parcial de la multa del socio.
    Retorna (exito: bool, mensaje: str).
    """
    respuesta = (
        supabase.table("socios")
        .select("id, nombre, multa_actual")
        .eq("id", socio_id)
        .gt("multa_actual", 0)
        .execute()
    )

    if not respuesta.data:
        return False, "Numero invalido o ese socio no tiene multa pendiente."

    socio = respuesta.data[0]
    multa_actual = _float(socio["multa_actual"])

    if pago_total:
        supabase.table("socios").update({"multa_actual": 0}).eq("id", socio_id).execute()
        mensaje = (
            f"Multa de ${multa_actual:.2f} pagada completamente. "
            f"{socio['nombre']} puede realizar nuevos prestamos."
        )
    else:
        if monto <= 0:
            return False, "El monto debe ser mayor a $0."
        if monto > multa_actual:
            return (
                False,
                f"El monto (${monto:.2f}) supera la multa (${multa_actual:.2f}). "
                "Use pago total para saldar la deuda completa.",
            )

        nueva_multa = multa_actual - monto
        supabase.table("socios").update({"multa_actual": nueva_multa}).eq("id", socio_id).execute()
        mensaje = f"Pago parcial registrado: ${monto:.2f}. Multa restante: ${nueva_multa:.2f}."
        if nueva_multa == 0:
            mensaje += f" {socio['nombre']} puede realizar nuevos prestamos."

    return True, mensaje


# ─────────────────────────────────────────────
# MENÚ INTERACTIVO (CLI)
# ─────────────────────────────────────────────
def menu_prestamos():
    opcion = 0

    while opcion != 9:
        print("\n========================================")
        print("       MODULO DE PRESTAMOS Y SOCIOS")
        print("========================================")
        print("1. Registrar Socio")
        print("2. Registrar Prestamo")
        print("3. Registrar Devolucion")
        print("4. Ver estado de Socios")
        print("5. Ver Socios con Multas pendientes")
        print("6. Pagar Multa de un Socio")
        print("7. Actualizar datos de Socio")
        print("8. Eliminar Socio")
        print("9. Volver al Menu Principal")
        print("========================================")

        try:
            opcion = int(input("Ingrese una opcion (1-9): "))

            match opcion:

                case 1:
                    nombre = input("Nombre completo del socio: ").strip()
                    telefono = input("Telefono (opcional): ").strip() or None
                    email = input("Email (opcional): ").strip() or None

                    if nombre == "":
                        print("Error: El nombre no puede estar vacio.")
                    else:
                        nuevo_id = crear_socio(nombre, telefono, email)
                        print("\nSocio registrado exitosamente!")
                        print(f"ID     : {nuevo_id}")
                        print(f"Nombre : {nombre}")
                        if telefono:
                            print(f"Telefono: {telefono}")
                        if email:
                            print(f"Email  : {email}")
                        print("Libros en prestamo: ninguno")
                        print("Multa pendiente: $0.00")

                    input("\nPresione ENTER para continuar...")

                case 2:
                    total_socios, total_libros = contar_registros()

                    if total_socios == 0:
                        print("No hay socios registrados. Registre un socio primero.")
                        input("\nPresione ENTER para continuar...")
                        continue

                    if total_libros == 0:
                        print("No hay libros registrados en el sistema.")
                        input("\nPresione ENTER para continuar...")
                        continue

                    socios = listar_socios()
                    print("\n--- Socios registrados ---")
                    for s in socios:
                        libros_activos = obtener_libros_activos_socio(s["id"])
                        libros_str = (
                            ", ".join(
                                f"{lb['titulo']} (desde {lb['fecha_prestamo']})"
                                for lb in libros_activos
                            )
                            if libros_activos
                            else "ninguno"
                        )
                        print(f"{s['id']}. {s['nombre']}")
                        print(f"   Libros en prestamo : {libros_str}")
                        print(f"   Multa pendiente    : ${_float(s['multa_actual']):.2f}")

                    try:
                        idx_socio = int(input("\nSeleccione el numero del socio: "))
                        libros_disponibles = listar_libros_disponibles()

                        if not libros_disponibles:
                            print("No hay libros disponibles en este momento.")
                        else:
                            print("\n--- Libros disponibles ---")
                            for lb in libros_disponibles:
                                print(f"{lb['id']}. {lb['titulo']}  |  Autor: {lb['autor']}")

                            idx_libro = int(input("\nSeleccione el numero del libro: "))
                            exito, resultado, fecha = registrar_prestamo(idx_socio, idx_libro)

                            if exito:
                                socio = obtener_socio(idx_socio)
                                print("\nPrestamo registrado exitosamente!")
                                print(f"Socio          : {socio['nombre']}")
                                print(f"Libro          : {resultado}")
                                print(f"Fecha prestamo : {fecha}")
                                print(
                                    f"Fecha limite   : "
                                    f"{(date.fromisoformat(fecha) + timedelta(days=PLAZO_DIAS)).isoformat()}"
                                )
                                print(f"Plazo          : {PLAZO_DIAS} dias para devolver.")
                            else:
                                print(f"\n{resultado}")

                    except ValueError:
                        print("Error: Debe ingresar un numero valido.")

                    input("\nPresione ENTER para continuar...")

                case 3:
                    prestamos_activos = listar_prestamos_activos()
                    print("\n=== REGISTRAR DEVOLUCION ===\n")

                    if not prestamos_activos:
                        print("Ningun socio tiene libros en prestamo actualmente.")
                        input("\nPresione ENTER para continuar...")
                        continue

                    print("--- Prestamos activos ---")
                    for p in prestamos_activos:
                        print(
                            f"Prestamo #{p['id']}  |  Socio: {p['nombre']}  ->  "
                            f"Libro: {p['titulo']}  |  Desde: {p['fecha_prestamo']}  "
                            f"|  Limite: {p['fecha_limite']}"
                        )

                    try:
                        idx_prestamo = int(input("\nIngrese el numero del Prestamo a devolver (#): "))
                        prestamo = next(
                            (p for p in prestamos_activos if p["id"] == idx_prestamo), None
                        )

                        if not prestamo:
                            print("Numero de prestamo invalido o ya fue devuelto.")
                        else:
                            print(f"\nDevolucion del libro: '{prestamo['titulo']}'")
                            print(
                                f"Socio: {prestamo['nombre']}  |  "
                                f"Fecha prestamo: {prestamo['fecha_prestamo']}  |  "
                                f"Fecha limite: {prestamo['fecha_limite']}"
                            )
                            print(f"\nEl socio devuelve dentro del plazo de {PLAZO_DIAS} dias?")
                            print("1. Si (sin multa)")
                            print(f"2. No (se aplica multa de ${MULTA_POR_DIA:.0f} por dia de atraso)")
                            a_tiempo_opcion = int(input("Seleccione: "))

                            a_tiempo = a_tiempo_opcion == 1
                            dias_atraso = 0
                            pagar_ahora = False

                            if not a_tiempo:
                                dias_atraso = int(input("Cuantos dias de atraso tiene? "))
                                print("\nDesea registrar el pago de la multa ahora?")
                                print("1. Si, pago en este momento")
                                print("2. No, pagara despues")
                                pago = int(input("Seleccione: "))
                                pagar_ahora = pago == 1

                            exito, mensaje = registrar_devolucion(
                                idx_prestamo, a_tiempo, dias_atraso, pagar_ahora
                            )
                            print(f"\n{mensaje}" if exito else f"\nError: {mensaje}")

                    except ValueError:
                        print("Error: Debe ingresar un numero valido.")

                    input("\nPresione ENTER para continuar...")

                case 4:
                    socios = listar_socios()
                    print("\n=== ESTADO ACTUAL DE SOCIOS ===\n")

                    if not socios:
                        print("No hay socios registrados.")
                    else:
                        for s in socios:
                            libros_activos = obtener_libros_activos_socio(s["id"])
                            print(f"{s['id']}. {s['nombre']}")
                            if s.get("telefono"):
                                print(f"   Telefono: {s['telefono']}")
                            if s.get("email"):
                                print(f"   Email   : {s['email']}")
                            if libros_activos:
                                print(f"   Libros en prestamo ({len(libros_activos)}):")
                                for lb in libros_activos:
                                    print(
                                        f"     - {lb['titulo']}  "
                                        f"(desde {lb['fecha_prestamo']}, limite {lb['fecha_limite']})"
                                    )
                            else:
                                print("   Libros en prestamo : ninguno")
                            print(f"   Multa pendiente    : ${_float(s['multa_actual']):.2f}")
                            print("   ---------------------------------")

                    input("\nPresione ENTER para continuar...")

                case 5:
                    socios_multa = listar_socios_con_multa()
                    print("\n=== SOCIOS CON MULTAS PENDIENTES ===\n")

                    if not socios_multa:
                        print("No hay socios con multas pendientes.")
                    else:
                        for s in socios_multa:
                            libros_activos = obtener_libros_activos_socio(s["id"])
                            libros_str = (
                                ", ".join(lb["titulo"] for lb in libros_activos)
                                if libros_activos
                                else "ninguno"
                            )
                            print(f"Socio : {s['nombre']}")
                            print(f"Libros en prestamo: {libros_str}")
                            print(f"Multa : ${_float(s['multa_actual']):.2f}")
                            print("   ---------------------------------")

                    input("\nPresione ENTER para continuar...")

                case 6:
                    socios_multa = listar_socios_con_multa()
                    print("\n=== PAGO DE MULTAS ===\n")

                    if not socios_multa:
                        print("No hay socios con multas pendientes.")
                        input("\nPresione ENTER para continuar...")
                        continue

                    print("--- Socios con multa pendiente ---")
                    for s in socios_multa:
                        print(f"{s['id']}. {s['nombre']}  |  Multa: ${_float(s['multa_actual']):.2f}")

                    try:
                        idx_socio = int(input("\nSeleccione el numero del socio que va a pagar: "))
                        socio = next((s for s in socios_multa if s["id"] == idx_socio), None)

                        if not socio:
                            print("Numero invalido o ese socio no tiene multa pendiente.")
                        else:
                            multa = _float(socio["multa_actual"])
                            print(f"\nSocio      : {socio['nombre']}")
                            print(f"Multa total: ${multa:.2f}")
                            print("\nTipo de pago:")
                            print("1. Pago total (salda toda la multa)")
                            print("2. Pago parcial")

                            tipo_pago = int(input("Seleccione: "))

                            if tipo_pago == 1:
                                exito, mensaje = pagar_multa(idx_socio, 0, pago_total=True)
                            elif tipo_pago == 2:
                                monto = float(input(f"Ingrese el monto a pagar (max ${multa:.2f}): $"))
                                exito, mensaje = pagar_multa(idx_socio, monto, pago_total=False)
                            else:
                                print("Opcion invalida.")
                                exito = False
                                mensaje = ""

                            if exito:
                                print(f"\n{mensaje}")

                    except ValueError:
                        print("Error: Ingrese un valor numerico valido.")

                    input("\nPresione ENTER para continuar...")

                case 7:
                    try:
                        socio_id = int(input("Ingrese el ID del socio a actualizar: "))
                        socio = obtener_socio(socio_id)

                        if not socio:
                            print("No se encontro el socio con ese ID.")
                        else:
                            print(f"\nDatos actuales: {socio['nombre']}")
                            nombre = input("Nuevo nombre (ENTER para mantener): ").strip()
                            telefono = input("Nuevo telefono (ENTER para mantener): ").strip()
                            email = input("Nuevo email (ENTER para mantener): ").strip()

                            nuevo_nombre = nombre if nombre else socio["nombre"]
                            nuevo_telefono = telefono if telefono else socio.get("telefono")
                            nuevo_email = email if email else socio.get("email")

                            if actualizar_socio(socio_id, nuevo_nombre, nuevo_telefono, nuevo_email):
                                print("\nSocio actualizado exitosamente!")
                            else:
                                print("No se pudo actualizar el socio.")

                    except ValueError:
                        print("Error: Debe ingresar un ID numerico valido.")

                    input("\nPresione ENTER para continuar...")

                case 8:
                    try:
                        socio_id = int(input("Ingrese el ID del socio a eliminar: "))
                        confirmar = input(
                            f"¿Confirma eliminar el socio #{socio_id}? (s/n): "
                        ).strip().lower()

                        if confirmar == "s":
                            exito, mensaje = eliminar_socio(socio_id)
                            print(f"\n{mensaje}")
                        else:
                            print("Operacion cancelada.")

                    except ValueError:
                        print("Error: Debe ingresar un ID numerico valido.")

                    input("\nPresione ENTER para continuar...")

                case 9:
                    print("Volviendo al Menu Principal...")

                case _:
                    print("Opcion invalida. Intente de nuevo.")
                    input("\nPresione ENTER para continuar...")

        except ValueError:
            print("Error: Debe ingresar un numero entero valido.")
            input("\nPresione ENTER para continuar...")
        except Exception as e:
            print(f"Error de conexion con Supabase: {e}")
            input("\nPresione ENTER para continuar...")