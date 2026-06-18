"""
Punto de entrada CLI del Sistema de Biblioteca — Entrega 3.
Orquesta los módulos de libros y préstamos conectados a Supabase.

Para la API REST, ejecutar en paralelo:
py -m uvicorn main:app --reload
"""

import modulo_libros
import modulo_prestamos
from db_config import verificar_conexion


def menu_principal():
    print("\nConectando a Supabase...")

    if not verificar_conexion():
        print(
            "ERROR: No se pudo conectar a Supabase.\n"
            "Verifique que el archivo .env tenga SUPABASE_URL y SUPABASE_KEY,\n"
            "y que las tablas esten creadas (schema.sql)."
        )
        return

    print("Conexion exitosa.\n")

    opcion = 0
    while opcion != 3:
        print("\n========================================")
        print("  SISTEMA DE BIBLIOTECA (Supabase + CLI)")
        print("========================================")
        print("1. Modulo de Libros y Autores")
        print("2. Modulo de Prestamos y Socios")
        print("3. Salir")
        print("========================================")

        try:
            opcion = int(input("Seleccione una opcion: "))

            if opcion == 1:
                modulo_libros.menu_libros()
            elif opcion == 2:
                modulo_prestamos.menu_prestamos()
            elif opcion == 3:
                print("Cerrando el sistema... ¡Hasta luego!")
            else:
                print("Opcion invalida. Por favor, elija un numero del 1 al 3.")

        except ValueError:
            print("Error: Por favor, ingrese un numero entero valido.")


if __name__ == "__main__":
    menu_principal()