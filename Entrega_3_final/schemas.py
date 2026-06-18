"""
Modelos Pydantic para validar peticiones y respuestas de la API FastAPI.
"""

from typing import Optional
from pydantic import BaseModel, Field


# ── Libros ──────────────────────────────────────────────────

class LibroCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    autor: str = Field(..., min_length=1, max_length=100)
    portada_url: Optional[str] = None


class LibroUpdate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    autor: str = Field(..., min_length=1, max_length=100)
    portada_url: Optional[str] = None


class LibroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    portada_url: Optional[str] = None
    disponible: bool
    fecha_registro: Optional[str] = None


# ── Socios ──────────────────────────────────────────────────

class SocioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=150)


class SocioUpdate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=150)


class SocioResponse(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    multa_actual: float = 0.0


# ── Préstamos ───────────────────────────────────────────────

class PrestamoCreate(BaseModel):
    socio_id: int
    libro_id: int


class DevolucionRequest(BaseModel):
    a_tiempo: bool = True
    dias_atraso: int = 0
    pagar_multa_ahora: bool = False


class PagoMultaRequest(BaseModel):
    monto: float = 0.0
    pago_total: bool = False


class MensajeResponse(BaseModel):
    exito: bool
    mensaje: str


class PrestamoActivoResponse(BaseModel):
    id: int
    socio_id: int
    nombre: str
    libro_id: int
    titulo: str
    fecha_prestamo: str
    fecha_limite: Optional[str] = None