Algoritmo SistemaBiblioteca
    
    Dimension libros[100], autores[100], estadoLibro[100]
    Definir totalLibros Como Entero
    totalLibros <- 0
    
    Dimension socios[100], librosPrestados[100], multas[100]
    Definir totalSocios Como Entero
    totalSocios <- 0
    
    Definir opcion Como Entero
    
    Repetir
        Escribir "=== SISTEMA DE BIBLIOTECA ==="
        Escribir "1. Módulo de Libros y Autores"
        Escribir "2. Módulo de Préstamos y Socios"
        Escribir "3. Salir"
        Escribir "Seleccione una opción: "
        Leer opcion
        
        Segun opcion Hacer
            1:
                ModuloLibros(libros, autores, estadoLibro, totalLibros)
            2:
                ModuloPrestamos(libros, estadoLibro, totalLibros, socios, librosPrestados, multas, totalSocios)
            3:
                Escribir "Saliendo del sistema..."
            De Otro Modo:
                Escribir "Opción inválida. Intente de nuevo."
        FinSegun
    Hasta Que opcion = 3
FinAlgoritmo