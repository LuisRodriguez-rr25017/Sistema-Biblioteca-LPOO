const BASE = "http://127.0.0.1:8000/api";

// ── Libros ──────────────────────────────────
export const getLibros = () =>
  fetch(`${BASE}/libros`).then((r) => r.json());

export const buscarLibros = (q) =>
  fetch(`${BASE}/libros/buscar?q=${encodeURIComponent(q)}`).then((r) => r.json());

export const crearLibro = (datos) =>
  fetch(`${BASE}/libros`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  }).then((r) => r.json());

export const eliminarLibro = (id) =>
  fetch(`${BASE}/libros/${id}`, { method: "DELETE" }).then((r) => r.json());

export const actualizarLibro = (id, datos) =>
  fetch(`${BASE}/libros/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  }).then((r) => r.json());

// ── Socios ───────────────────────────────────
export const getSocios = () =>
  fetch(`${BASE}/socios`).then((r) => r.json());

export const crearSocio = (datos) =>
  fetch(`${BASE}/socios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  }).then((r) => r.json());

export const eliminarSocio = (id) =>
  fetch(`${BASE}/socios/${id}`, { method: "DELETE" }).then((r) => r.json());

export const getSociosConMulta = () =>
  fetch(`${BASE}/socios/multas`).then((r) => r.json());

export const pagarMulta = (id, datos) =>
  fetch(`${BASE}/socios/${id}/pagar-multa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  }).then((r) => r.json());

// ── Préstamos ────────────────────────────────
export const getPrestamosActivos = () =>
  fetch(`${BASE}/prestamos/activos`).then((r) => r.json());

export const registrarPrestamo = (datos) =>
  fetch(`${BASE}/prestamos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  }).then((r) => r.json());

export const registrarDevolucion = (id, datos) =>
  fetch(`${BASE}/prestamos/${id}/devolver`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  }).then((r) => r.json());
