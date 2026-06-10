import Conexion_db
import modulo_libros
import modulo_prestamos

def menu_principal():
    Conexion_db.crear_tablas()
    
    opcion = 0
    while opcion != 3:
        print("\n========================================")
        print("        SISTEMA DE BIBLIOTECA (SQL)")
        print("========================================")
        print("1. Módulo de Libros y Autores")
        print("2. Módulo de Préstamos y Socios")
        print("3. Salir")
        print("========================================")
        
        try:
            opcion = int(input("Seleccione una opción: "))
            
            if opcion == 1:
                modulo_libros.menu_libros()
            elif opcion == 2:
                modulo_prestamos.menu_prestamos()
            elif opcion == 3:
                print("Cerrando el sistema... ¡Hasta luego!")
            else:
                print("Opción inválida. Por favor, elija un número del 1 al 3.")
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    menu_principal()