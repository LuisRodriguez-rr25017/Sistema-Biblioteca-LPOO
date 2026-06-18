"""
API REST del Sistema de Biblioteca — FastAPI.
Expone las funciones CRUD de modulo_libros y modulo_prestamos como endpoints HTTP.
Los mismos módulos alimentan también el menú CLI (menu_principal.py).
"""

from typing import List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import modulo_libros
import modulo_prestamos
from db_config import verificar_conexion
from schemas import (
    LibroCreate,
    LibroUpdate,
    LibroResponse,
    SocioCreate,
    SocioUpdate,
    SocioResponse,
    PrestamoCreate,
    DevolucionRequest,
    PagoMultaRequest,
    MensajeResponse,
    PrestamoActivoResponse,
)

app = FastAPI(
    title="Sistema de Biblioteca API",
    description="API REST para gestión de libros, socios y préstamos (Supabase)",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────

@app.get("/")
def raiz():
    return {
        "mensaje": "Sistema de Biblioteca API",
        "docs": "/docs",
        "estado_db": "conectado" if verificar_conexion() else "sin conexion",
    }


@app.get("/health")
def health():
    if not verificar_conexion():
        raise HTTPException(status_code=503, detail="Sin conexion a Supabase")
    return {"status": "ok"}


# ─────────────────────────────────────────────
# Endpoints — Libros
# ─────────────────────────────────────────────

@app.get("/api/libros", response_model=List[LibroResponse])
def api_listar_libros():
    return modulo_libros.listar_libros()


@app.get("/api/libros/buscar", response_model=List[LibroResponse])
def api_buscar_libros(q: str = Query(..., min_length=1)):
    return modulo_libros.buscar_libros_por_titulo(q)


@app.get("/api/libros/{libro_id}", response_model=LibroResponse)
def api_obtener_libro(libro_id: int):
    libro = modulo_libros.obtener_libro(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@app.post("/api/libros", response_model=LibroResponse, status_code=201)
def api_crear_libro(datos: LibroCreate):
    return modulo_libros.crear_libro(datos.titulo, datos.autor, datos.portada_url)


@app.put("/api/libros/{libro_id}", response_model=LibroResponse)
def api_actualizar_libro(libro_id: int, datos: LibroUpdate):
    if not modulo_libros.obtener_libro(libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not modulo_libros.actualizar_libro(libro_id, datos.titulo, datos.autor, datos.portada_url):
        raise HTTPException(status_code=400, detail="No se pudo actualizar el libro")
    return modulo_libros.obtener_libro(libro_id)


@app.delete("/api/libros/{libro_id}", response_model=MensajeResponse)
def api_eliminar_libro(libro_id: int):
    exito, mensaje = modulo_libros.eliminar_libro(libro_id)
    if not exito:
        raise HTTPException(status_code=400, detail=mensaje)
    return MensajeResponse(exito=True, mensaje=mensaje)


# ─────────────────────────────────────────────
# Endpoints — Socios
# ─────────────────────────────────────────────

@app.get("/api/socios", response_model=List[SocioResponse])
def api_listar_socios():
    return modulo_prestamos.listar_socios()


@app.get("/api/socios/multas", response_model=List[SocioResponse])
def api_socios_con_multa():
    return modulo_prestamos.listar_socios_con_multa()


@app.get("/api/socios/{socio_id}", response_model=SocioResponse)
def api_obtener_socio(socio_id: int):
    socio = modulo_prestamos.obtener_socio(socio_id)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio


@app.post("/api/socios", response_model=SocioResponse, status_code=201)
def api_crear_socio(datos: SocioCreate):
    nuevo_id = modulo_prestamos.crear_socio(datos.nombre, datos.telefono, datos.email)
    return modulo_prestamos.obtener_socio(nuevo_id)


@app.put("/api/socios/{socio_id}", response_model=SocioResponse)
def api_actualizar_socio(socio_id: int, datos: SocioUpdate):
    if not modulo_prestamos.obtener_socio(socio_id):
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    if not modulo_prestamos.actualizar_socio(socio_id, datos.nombre, datos.telefono, datos.email):
        raise HTTPException(status_code=400, detail="No se pudo actualizar el socio")
    return modulo_prestamos.obtener_socio(socio_id)


@app.delete("/api/socios/{socio_id}", response_model=MensajeResponse)
def api_eliminar_socio(socio_id: int):
    exito, mensaje = modulo_prestamos.eliminar_socio(socio_id)
    if not exito:
        raise HTTPException(status_code=400, detail=mensaje)
    return MensajeResponse(exito=True, mensaje=mensaje)


@app.post("/api/socios/{socio_id}/pagar-multa", response_model=MensajeResponse)
def api_pagar_multa(socio_id: int, datos: PagoMultaRequest):
    exito, mensaje = modulo_prestamos.pagar_multa(
        socio_id, datos.monto, pago_total=datos.pago_total
    )
    if not exito:
        raise HTTPException(status_code=400, detail=mensaje)
    return MensajeResponse(exito=True, mensaje=mensaje)


# ─────────────────────────────────────────────
# Endpoints — Préstamos
# ─────────────────────────────────────────────

@app.get("/api/prestamos/activos", response_model=List[PrestamoActivoResponse])
def api_prestamos_activos():
    return modulo_prestamos.listar_prestamos_activos()


@app.post("/api/prestamos", response_model=MensajeResponse, status_code=201)
def api_registrar_prestamo(datos: PrestamoCreate):
    exito, mensaje, fecha = modulo_prestamos.registrar_prestamo(
        datos.socio_id, datos.libro_id
    )
    if not exito:
        raise HTTPException(status_code=400, detail=mensaje)
    return MensajeResponse(
        exito=True,
        mensaje=f"Prestamo registrado: {mensaje} (fecha: {fecha})",
    )


@app.put("/api/prestamos/{prestamo_id}/devolver", response_model=MensajeResponse)
def api_registrar_devolucion(prestamo_id: int, datos: DevolucionRequest):
    exito, mensaje = modulo_prestamos.registrar_devolucion(
        prestamo_id,
        datos.a_tiempo,
        datos.dias_atraso,
        datos.pagar_multa_ahora,
    )
    if not exito:
        raise HTTPException(status_code=400, detail=mensaje)
    return MensajeResponse(exito=True, mensaje=mensaje)