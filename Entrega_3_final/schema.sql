-- 1. Creamos la tabla de socios
CREATE TABLE socios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    multa_actual NUMERIC(10,2) DEFAULT 0
);

-- 2. Creamos la tabla de libros con el enlace para la imagen
CREATE TABLE libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    portada_url TEXT,
    disponible BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Creamos la tabla relacional de préstamos
CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    libro_id INTEGER REFERENCES libros(id),
    socio_id INTEGER REFERENCES socios(id),
    fecha_prestamo DATE DEFAULT CURRENT_DATE,
    devuelto BOOLEAN DEFAULT FALSE,
    fecha_devolucion DATE,
    fecha_limite DATE,
    multa_generada NUMERIC(10,2) DEFAULT 0
);