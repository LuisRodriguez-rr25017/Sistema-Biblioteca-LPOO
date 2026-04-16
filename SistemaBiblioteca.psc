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

// =============================================
// REGISTRO DE LIBROS Y AUTORES
// =============================================
SubProceso ModuloLibros(libros Por Referencia, autores Por Referencia, estadoLibro Por Referencia, totalLibros Por Referencia)
    
    Definir opcion Como Entero
    Definir tituloBuscar Como Cadena
    Definir encontrado Como Logico
    
    Repetir
        Limpiar Pantalla
        Escribir "========================================"
        Escribir "       REGISTRO DE LIBROS Y AUTORES"
        Escribir "========================================"
        Escribir "1. Registrar nuevo libro y autor"
        Escribir "2. Mostrar todos los libros registrados"
        Escribir "3. Buscar libro por título"
        Escribir "4. Volver al Menú Principal"
        Escribir "========================================"
        Escribir "Ingrese una opción (1-4): "
        Leer opcion
        
        Segun opcion Hacer
            1:  // Registrar nuevo libro
                Si totalLibros >= 100 Entonces
                    Escribir "ERROR: Se ha alcanzado el límite máximo de 100 libros."
                    Esperar Tecla
                Sino
                    Limpiar Pantalla
                    Escribir "=== REGISTRAR NUEVO LIBRO ==="
                    
                    totalLibros <- totalLibros + 1
                    
                    Escribir "Ingrese el título del libro: "
                    Leer libros[totalLibros]
                    
                    Escribir "Ingrese el nombre del autor: "
                    Leer autores[totalLibros]
                    
                    estadoLibro[totalLibros] <- "Disponible" // Estado inicial
                    
                    Escribir ""
                    Escribir "¡Libro registrado exitosamente!"
                    Escribir "Título: ", libros[totalLibros]
                    Escribir "Autor: ", autores[totalLibros]
                    Escribir "Estado: ", estadoLibro[totalLibros]
                    Esperar Tecla
                FinSi
                
            2:  // Mostrar todos los libros
                Limpiar Pantalla
                Escribir "=== LISTADO DE LIBROS REGISTRADOS ==="
                Escribir ""
                
                Si totalLibros = 0 Entonces
                    Escribir "Aún no hay libros registrados."
                Sino
                    Para i <- 1 Hasta totalLibros Hacer
                        Escribir i, ". ", libros[i]
                        Escribir "   Autor: ", autores[i]
                        Escribir "   Estado: ", estadoLibro[i]
                        Escribir "   -----------------------------------"
                    FinPara
                FinSi
                
                Escribir ""
                Escribir "Presione una tecla para continuar..."
                Esperar Tecla
                
            3:  // Buscar libro por título
                Limpiar Pantalla
                Escribir "=== BUSCAR LIBRO POR TÍTULO ==="
                Escribir "Ingrese el título del libro a buscar: "
                Leer tituloBuscar
                
                encontrado <- Falso
                
                Para i <- 1 Hasta totalLibros Hacer
                    Si libros[i] = tituloBuscar Entonces
                        Escribir ""
                        Escribir "¡Libro encontrado!"
                        Escribir "Título: ", libros[i]
                        Escribir "Autor: ", autores[i]
                        Escribir "Estado: ", estadoLibro[i]
                        encontrado <- Verdadero
                        Esperar Tecla
                        i <- totalLibros + 1   // Forzar salida del bucle
                    FinSi
                FinPara
                
                Si encontrado = Falso Entonces
                    Escribir "No se encontró ningún libro con el título: ", tituloBuscar
                    Esperar Tecla
                FinSi
                
            4:
                Escribir "Volviendo al Menú Principal..."
                Esperar Tecla
                Limpiar Pantalla
                
            De Otro Modo:
                Escribir "Opción inválida. Por favor ingrese una opción entre 1 y 4."
                Esperar Tecla
        FinSegun
        
    Hasta Que opcion = 4
    
FinSubProceso
