Sistema de Biblioteca

Este es un proyecto desarrollado en Python para gestionar los procesos de una biblioteca. Incluye menú CLI, API REST con FastAPI y base de datos en Supabase.

Funcionalidades Principales
* Registro de libros y autores.
* Control de disponibilidad de ejemplares.
* Gestión de socios y préstamos.
* Control de límites de libros y verificación de multas por vencimiento.

Integrantes del Equipo
1. Luis Mario Rodriguez Ramirez - rr25017
2. Jose Aristides Palacios Rodriguez - PR19058
3. Michael Octavio Murillo Cabrera - mm23003

Estado del Proyecto
* [x]  Entrega 1: Demo en Pseudocódigo (PSeInt) y configuración inicial.
* [x] Entrega 2: Demo de avance de código.
* [x] Entrega 3: Funcionalidad completa y pruebas unitarias.

## Cómo ejecutar

En la carpeta `Entrega_3_final`, instale las dependencias con `py -m pip install -r requirements.txt`, configure el archivo `.env` con `SUPABASE_URL` y `SUPABASE_KEY`, ejecute `schema.sql` en Supabase e inicie la API con `py -m uvicorn main:app --reload`; en Postman importe `Sistema_Biblioteca_API.postman_collection.json` con `base_url = http://127.0.0.1:8000`, o use el menú CLI con `py menu_principal.py`.
