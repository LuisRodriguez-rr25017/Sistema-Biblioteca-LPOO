// =============================================
// SISTEMA DE BIBLIOTECA - ARCHIVO COMPLETO
// Módulo 1: Libros y Autores
// Módulo 2: Préstamos y Socios
// =============================================

Algoritmo SistemaBiblioteca
    
    // --- Arreglos compartidos Módulo 1 ---
    Dimension libros[100], autores[100], estadoLibro[100]
    Definir totalLibros Como Entero
    totalLibros <- 0
    
    // --- Arreglos compartidos Módulo 2 ---
    Dimension socios[100], librosPrestados[100]
    Dimension multas[100]
    Definir totalSocios Como Entero
    totalSocios <- 0
    
    Definir opcion Como Entero
    
    Repetir
        Limpiar Pantalla
        Escribir "========================================"
        Escribir "       SISTEMA DE BIBLIOTECA"
        Escribir "========================================"
        Escribir "1. Modulo de Libros y Autores"
        Escribir "2. Modulo de Prestamos y Socios"
        Escribir "3. Salir"
        Escribir "========================================"
        Escribir "Seleccione una opcion: "
        Leer opcion
        
        Segun opcion Hacer
            1:
                ModuloLibros(libros, autores, estadoLibro, totalLibros)
            2:
                ModuloPrestamos(libros, estadoLibro, totalLibros, socios, librosPrestados, multas, totalSocios)
            3:
                Escribir "Saliendo del sistema. Hasta luego."
            De Otro Modo:
                Escribir "Opcion invalida. Intente de nuevo."
                Esperar Tecla
        FinSegun
        
    Hasta Que opcion = 3
	
FinAlgoritmo

// =============================================
// MODULO 1: REGISTRO DE LIBROS Y AUTORES
// =============================================
SubProceso ModuloLibros(libros Por Referencia, autores Por Referencia, estadoLibro Por Referencia, totalLibros Por Referencia)
    
    Definir opcion Como Entero
    Definir tituloBuscar Como Cadena
    Definir encontrado Como Logico
    Definir i Como Entero
    
    Repetir
        Limpiar Pantalla
        Escribir "========================================"
        Escribir "       REGISTRO DE LIBROS Y AUTORES"
        Escribir "========================================"
        Escribir "1. Registrar nuevo libro y autor"
        Escribir "2. Mostrar todos los libros registrados"
        Escribir "3. Buscar libro por titulo"
        Escribir "4. Volver al Menu Principal"
        Escribir "========================================"
        Escribir "Ingrese una opcion (1-4): "
        Leer opcion
        
        Segun opcion Hacer
            1:
                Si totalLibros >= 100 Entonces
                    Escribir "ERROR: Se ha alcanzado el limite maximo de 100 libros."
                    Esperar Tecla
                Sino
                    Limpiar Pantalla
                    Escribir "=== REGISTRAR NUEVO LIBRO ==="
                    totalLibros <- totalLibros + 1
                    Escribir "Ingrese el titulo del libro: "
                    Leer libros[totalLibros]
                    Escribir "Ingrese el nombre del autor: "
                    Leer autores[totalLibros]
                    estadoLibro[totalLibros] <- "Disponible"
                    Escribir ""
                    Escribir "Libro registrado exitosamente!"
                    Escribir "Titulo: ", libros[totalLibros]
                    Escribir "Autor: ", autores[totalLibros]
                    Escribir "Estado: ", estadoLibro[totalLibros]
                    Esperar Tecla
                FinSi
                
            2:
                Limpiar Pantalla
                Escribir "=== LISTADO DE LIBROS REGISTRADOS ==="
                Escribir ""
                Si totalLibros = 0 Entonces
                    Escribir "Aun no hay libros registrados."
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
                
            3:
                Limpiar Pantalla
				Escribir "=== BUSCAR LIBRO POR TITULO ==="
                Escribir "Ingrese el titulo del libro a buscar: "
                Leer tituloBuscar
                encontrado <- Falso
                
                Para i <- 1 Hasta totalLibros Hacer
                    Si libros[i] = tituloBuscar Entonces
                        Escribir ""
                        Escribir "Libro encontrado!"
                        Escribir "Titulo: ", libros[i]
                        Escribir "Autor: ", autores[i]
                        Escribir "Estado: ", estadoLibro[i]
                        encontrado <- Verdadero
                        Esperar Tecla
                    FinSi
                FinPara
                
                Si encontrado = Falso Entonces
                    Escribir "No se encontro ningun libro con el titulo: ", tituloBuscar
                    Esperar Tecla
                FinSi
                
            4:
                Escribir "Volviendo al Menu Principal..."
                Esperar Tecla
                Limpiar Pantalla
                
            De Otro Modo:
                Escribir "Opcion invalida. Por favor ingrese una opcion entre 1 y 4."
                Esperar Tecla
        FinSegun
        
    Hasta Que opcion = 4
    
FinSubProceso

// =============================================
// MODULO 2: PRESTAMOS Y SOCIOS
// =============================================
SubProceso ModuloPrestamos(libros Por Referencia, estadoLibro Por Referencia, totalLibros Por Referencia, socios Por Referencia, librosPrestados Por Referencia, multas Por Referencia, totalSocios Por Referencia)
	
    Definir opcion Como Entero
    Definir i Como Entero
    Definir idxSocio, idxLibro, idxDev Como Entero
    Definir aTiempo, diasAtraso Como Entero
    Definir hayDisponibles, hayMultas Como Logico
	
    Repetir
        Limpiar Pantalla
        Escribir "========================================"
        Escribir "       MODULO DE PRESTAMOS Y SOCIOS"
        Escribir "========================================"
        Escribir "1. Registrar Socio"
        Escribir "2. Registrar Prestamo"
        Escribir "3. Registrar Devolucion"
        Escribir "4. Ver estado de Socios"
        Escribir "5. Ver Socios con Multas pendientes"
        Escribir "6. Volver al Menu Principal"
        Escribir "========================================"
        Escribir "Ingrese una opcion (1-6): "
        Leer opcion
		
        Segun opcion Hacer
			
				//  OPCION 1: Registrar Socio 
            1:
                Si totalSocios >= 100 Entonces
                    Escribir "ERROR: Limite maximo de socios alcanzado."
                    Esperar Tecla
                Sino
                    Limpiar Pantalla
                    Escribir " REGISTRAR SOCIO "
                    totalSocios <- totalSocios + 1
                    Escribir "Nombre completo del socio: "
                    Leer socios[totalSocios]
                    librosPrestados[totalSocios] <- "ninguno"
                    multas[totalSocios] <- 0
                    Escribir ""
                    Escribir "Socio registrado exitosamente!"
                    Escribir "Nombre: ", socios[totalSocios]
                    Escribir "Libro en prestamo: ninguno"
                    Escribir "Multa pendiente: $0"
                    Esperar Tecla
                FinSi
				
				//  OPCION 2: Registrar Prestamo 
            2:
                Limpiar Pantalla
                Escribir "=== REGISTRAR PRESTAMO ==="
                Escribir ""
				
                Si totalSocios = 0 Entonces
                    Escribir "No hay socios registrados. Registre un socio primero."
                    Esperar Tecla
                Sino
                    Si totalLibros = 0 Entonces
                        Escribir "No hay libros registrados en el sistema."
                        Esperar Tecla
                    Sino
                        // Mostrar socios disponibles
                        Escribir "--- Socios registrados ---"
                        Para i <- 1 Hasta totalSocios Hacer
                            Escribir i, ". ", socios[i]
                            Escribir "   Libro actual  : ", librosPrestados[i]
                            Escribir "   Multa pendiente: $", multas[i]
                        FinPara
                        Escribir ""
                        Escribir "Seleccione el numero del socio: "
                        Leer idxSocio
						
                        Si idxSocio < 1 O idxSocio > totalSocios Entonces
                            Escribir "Numero de socio invalido."
                            Esperar Tecla
                        Sino
                            // Verificar si el socio ya tiene un libro prestado
                            Si librosPrestados[idxSocio] <> "ninguno" Entonces
                                Escribir ""
                                Escribir "ERROR: ", socios[idxSocio], " ya tiene prestado el libro:"
                                Escribir "       ", librosPrestados[idxSocio]
                                Escribir "Debe devolverlo antes de solicitar otro."
                                Esperar Tecla
                            Sino
                                // Verificar si tiene multa pendiente
                                Si multas[idxSocio] > 0 Entonces
                                    Escribir ""
                                    Escribir "ERROR: ", socios[idxSocio], " tiene multa pendiente de $", multas[idxSocio]
                                    Escribir "Debe pagar la multa antes de realizar un prestamo."
                                    Esperar Tecla
                                Sino
                                    // Mostrar solo libros disponibles
                                    Escribir ""
                                    Escribir "--- Libros disponibles ---"
                                    hayDisponibles <- Falso
                                    Para i <- 1 Hasta totalLibros Hacer
                                        Si estadoLibro[i] = "Disponible" Entonces
                                            Escribir i, ". ", libros[i], "  [", estadoLibro[i], "]"
                                            hayDisponibles <- Verdadero
                                        FinSi
                                    FinPara
									
                                    Si hayDisponibles = Falso Entonces
                                        Escribir "No hay libros disponibles en este momento."
                                        Esperar Tecla
                                    Sino
                                        Escribir ""
                                        Escribir "Seleccione el numero del libro: "
                                        Leer idxLibro
										
                                        Si idxLibro < 1 O idxLibro > totalLibros Entonces
                                            Escribir "Numero de libro invalido."
                                            Esperar Tecla
                                        Sino
                                            Si estadoLibro[idxLibro] <> "Disponible" Entonces
                                                Escribir "Ese libro no esta disponible actualmente."
                                                Esperar Tecla
                                            Sino
                                                // REGISTRAR PRESTAMO
                                                estadoLibro[idxLibro]     <- "Prestado"
                                                librosPrestados[idxSocio] <- libros[idxLibro]
                                                Escribir ""
                                                Escribir "Prestamo registrado exitosamente!"
                                                Escribir "Socio : ", socios[idxSocio]
                                                Escribir "Libro : ", libros[idxLibro]
                                                Escribir "Plazo : 14 dias para devolver."
                                                Esperar Tecla
                                            FinSi
                                        FinSi
                                    FinSi
                                FinSi
                            FinSi
                        FinSi
                    FinSi
                FinSi
				
				// --- OPCION 3: Registrar Devolucion ---
            3:
                Limpiar Pantalla
                Escribir "=== REGISTRAR DEVOLUCION ==="
                Escribir ""
				
                Si totalSocios = 0 Entonces
                    Escribir "No hay socios registrados."
                    Esperar Tecla
                Sino
                    Escribir "--- Socios con libro prestado ---"
                    hayDisponibles <- Falso
                    Para i <- 1 Hasta totalSocios Hacer
                        Si librosPrestados[i] <> "ninguno" Entonces
                            Escribir i, ". ", socios[i], "  ->  ", librosPrestados[i]
                            hayDisponibles <- Verdadero
                        FinSi
                    FinPara
					
                    Si hayDisponibles = Falso Entonces
                        Escribir "Ningun socio tiene libros en prestamo actualmente."
                        Esperar Tecla
                    Sino
                        Escribir ""
                        Escribir "Seleccione el numero del socio que devuelve: "
                        Leer idxDev
						
                        Si idxDev < 1 O idxDev > totalSocios Entonces
                            Escribir "Numero de socio invalido."
                            Esperar Tecla
                        Sino
                            Si librosPrestados[idxDev] = "ninguno" Entonces
                                Escribir socios[idxDev], " no tiene ningun libro en prestamo."
                                Esperar Tecla
                            Sino
                                Escribir ""
                                Escribir "El socio devuelve dentro del plazo de 14 dias?"
                                Escribir "1. Si (sin multa)"
                                Escribir "2. No (se aplica multa de $2 por dia)"
                                Leer aTiempo
								
                                // Liberar el libro en el arreglo del Modulo 1
								i <- 1
								Mientras i <= totalLibros Hacer
									Si libros[i] = librosPrestados[idxDev] Entonces
										estadoLibro[i] <- "Disponible"
										i <- totalLibros + 1
									Sino
										i <- i + 1
									FinSi
								FinMientras
								
                                Si aTiempo = 2 Entonces
                                    Escribir "Cuantos dias de atraso tiene? "
                                    Leer diasAtraso
                                    multas[idxDev] <- multas[idxDev] + (diasAtraso * 2)
                                    Escribir ""
                                    Escribir "Multa aplicada   : $", diasAtraso * 2
                                    Escribir "Multa total socio: $", multas[idxDev]
                                Sino
                                    Escribir "Devolucion a tiempo. Sin multa."
                                FinSi
								
                                librosPrestados[idxDev] <- "ninguno"
                                Escribir "Libro devuelto y disponible nuevamente."
                                Esperar Tecla
                            FinSi
                        FinSi
                    FinSi
                FinSi
				
				// --- OPCION 4: Ver estado de Socios ---
            4:
                Limpiar Pantalla
                Escribir "=== ESTADO ACTUAL DE SOCIOS ==="
                Escribir ""
                Si totalSocios = 0 Entonces
                    Escribir "No hay socios registrados."
                Sino
                    Para i <- 1 Hasta totalSocios Hacer
                        Escribir i, ". ", socios[i]
                        Escribir "   Libro en prestamo : ", librosPrestados[i]
                        Escribir "   Multa pendiente   : $", multas[i]
                        Escribir "   ---------------------------------"
                    FinPara
                FinSi
                Escribir ""
                Esperar Tecla
				
				// --- OPCION 5: Ver multas pendientes ---
            5:
                Limpiar Pantalla
                Escribir "=== SOCIOS CON MULTAS PENDIENTES ==="
                Escribir ""
                hayMultas <- Falso
                Para i <- 1 Hasta totalSocios Hacer
                    Si multas[i] > 0 Entonces
                        Escribir "Socio : ", socios[i]
                        Escribir "Libro : ", librosPrestados[i]
                        Escribir "Multa : $", multas[i]
                        Escribir "   ---------------------------------"
                        hayMultas <- Verdadero
                    FinSi
                FinPara
                Si hayMultas = Falso Entonces
                    Escribir "No hay socios con multas pendientes."
                FinSi
                Escribir ""
                Esperar Tecla
				
            6:
                Escribir "Volviendo al Menu Principal..."
                Esperar Tecla
                Limpiar Pantalla
				
            De Otro Modo:
                Escribir "Opcion invalida. Intente de nuevo."
                Esperar Tecla
				
        FinSegun
		
    Hasta Que opcion = 6
	
FinSubProceso