import { useState, useEffect } from "react";
import {
  getPrestamosActivos,
  getLibros,
  getSocios,
  registrarPrestamo,
  registrarDevolucion,
} from "../api";
import Modal from "../components/Modal";

export default function Prestamos() {
  const [prestamos, setPrestamos] = useState([]);
  const [libros, setLibros] = useState([]);
  const [socios, setSocios] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [mensaje, setMensaje] = useState(null);

  const [modalPrestamo, setModalPrestamo] = useState(false);
  const [modalDevolucion, setModalDevolucion] = useState(false);
  const [prestamoSeleccionado, setPrestamoSeleccionado] = useState(null);

  const [formPrestamo, setFormPrestamo] = useState({ socio_id: "", libro_id: "" });
  const [formDevolucion, setFormDevolucion] = useState({
    a_tiempo: true,
    dias_atraso: 0,
    pagar_multa_ahora: false,
  });
  const [guardando, setGuardando] = useState(false);

  const cargar = async () => {
    setCargando(true);
    try {
      const [p, l, s] = await Promise.all([
        getPrestamosActivos(),
        getLibros(),
        getSocios(),
      ]);
      setPrestamos(Array.isArray(p) ? p : []);
      setLibros(Array.isArray(l) ? l.filter((lb) => lb.disponible) : []);
      setSocios(Array.isArray(s) ? s : []);
    } catch {
      mostrarMensaje("Error al conectar con el servidor.", "error");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => { cargar(); }, []);

  const mostrarMensaje = (texto, tipo = "ok") => {
    setMensaje({ texto, tipo });
    setTimeout(() => setMensaje(null), 4000);
  };

  const handlePrestamo = async (e) => {
    e.preventDefault();
    if (!formPrestamo.socio_id || !formPrestamo.libro_id) {
      mostrarMensaje("Selecciona un socio y un libro.", "error");
      return;
    }
    setGuardando(true);
    try {
      const res = await registrarPrestamo({
        socio_id: parseInt(formPrestamo.socio_id),
        libro_id: parseInt(formPrestamo.libro_id),
      });
      if (res.exito) {
        mostrarMensaje("Préstamo registrado exitosamente.");
        setModalPrestamo(false);
        setFormPrestamo({ socio_id: "", libro_id: "" });
        cargar();
      } else {
        mostrarMensaje(res.detail || "No se pudo registrar.", "error");
      }
    } catch {
      mostrarMensaje("Error al registrar el préstamo.", "error");
    } finally {
      setGuardando(false);
    }
  };

  const abrirDevolucion = (prestamo) => {
    setPrestamoSeleccionado(prestamo);
    setFormDevolucion({ a_tiempo: true, dias_atraso: 0, pagar_multa_ahora: false });
    setModalDevolucion(true);
  };

  const handleDevolucion = async (e) => {
    e.preventDefault();
    setGuardando(true);
    try {
      const res = await registrarDevolucion(prestamoSeleccionado.id, {
        a_tiempo: formDevolucion.a_tiempo,
        dias_atraso: formDevolucion.a_tiempo ? 0 : parseInt(formDevolucion.dias_atraso) || 0,
        pagar_multa_ahora: formDevolucion.pagar_multa_ahora,
      });
      if (res.exito) {
        mostrarMensaje(res.mensaje);
        setModalDevolucion(false);
        cargar();
      } else {
        mostrarMensaje(res.detail || "No se pudo registrar.", "error");
      }
    } catch {
      mostrarMensaje("Error al registrar la devolución.", "error");
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Préstamos activos</h1>
          <p className="text-slate-500 text-sm mt-1">{prestamos.length} préstamo(s) en curso</p>
        </div>
        <button
          onClick={() => setModalPrestamo(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors"
        >
          + Nuevo préstamo
        </button>
      </div>

      {mensaje && (
        <div className={`mb-4 px-4 py-3 rounded-xl text-sm font-medium ${
          mensaje.tipo === "error"
            ? "bg-red-50 text-red-700 border border-red-200"
            : "bg-green-50 text-green-700 border border-green-200"
        }`}>
          {mensaje.texto}
        </div>
      )}

      {cargando ? (
        <div className="text-center py-20 text-slate-400">Cargando...</div>
      ) : prestamos.length === 0 ? (
        <div className="text-center py-20 text-slate-400">
          <img src="/iconos/clipboard-check.svg" alt="sin préstamos" className="w-12 h-12 mx-auto mb-3 opacity-100" />
          <p>No hay préstamos activos en este momento.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {prestamos.map((p) => (
            <div key={p.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-4 flex items-center justify-between gap-4">
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-slate-800 truncate">{p.titulo}</p>
                <p className="text-slate-500 text-sm">{p.nombre}</p>
              </div>
              <div className="text-right text-xs text-slate-400 hidden sm:block">
                <p>Desde: <span className="text-slate-600">{p.fecha_prestamo}</span></p>
                {p.fecha_limite && (
                  <p>Límite: <span className="text-orange-500 font-medium">{p.fecha_limite}</span></p>
                )}
              </div>
              <button
                onClick={() => abrirDevolucion(p)}
                className="bg-slate-800 hover:bg-slate-700 text-white text-sm px-4 py-2 rounded-lg transition-colors whitespace-nowrap"
              >
                Registrar devolución
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Modal nuevo préstamo */}
      {modalPrestamo && (
        <Modal titulo="Registrar préstamo" onCerrar={() => setModalPrestamo(false)}>
          <form onSubmit={handlePrestamo} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Socio <span className="text-red-500">*</span>
              </label>
              <select
                value={formPrestamo.socio_id}
                onChange={(e) => setFormPrestamo({ ...formPrestamo, socio_id: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecciona un socio...</option>
                {socios.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.nombre} {s.multa_actual > 0 ? `⚠️ Multa: $${s.multa_actual}` : ""}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Libro disponible <span className="text-red-500">*</span>
              </label>
              <select
                value={formPrestamo.libro_id}
                onChange={(e) => setFormPrestamo({ ...formPrestamo, libro_id: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecciona un libro...</option>
                {libros.map((l) => (
                  <option key={l.id} value={l.id}>
                    {l.titulo} — {l.autor}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={() => setModalPrestamo(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" disabled={guardando}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-60">
                {guardando ? "Registrando..." : "Registrar"}
              </button>
            </div>
          </form>
        </Modal>
      )}

      {/* Modal devolución */}
      {modalDevolucion && prestamoSeleccionado && (
        <Modal titulo="Registrar devolución" onCerrar={() => setModalDevolucion(false)}>
          <div className="mb-4 bg-slate-50 rounded-xl p-3 text-sm">
            <p className="font-medium text-slate-700">{prestamoSeleccionado.titulo}</p>
            <p className="text-slate-500">Socio: {prestamoSeleccionado.nombre}</p>
            {prestamoSeleccionado.fecha_limite && (
              <p className="text-slate-500">Límite: {prestamoSeleccionado.fecha_limite}</p>
            )}
          </div>
          <form onSubmit={handleDevolucion} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                ¿Devuelve a tiempo?
              </label>
              <div className="flex gap-3">
                <button type="button"
                  onClick={() => setFormDevolucion({ ...formDevolucion, a_tiempo: true, dias_atraso: 0 })}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-colors ${
                    formDevolucion.a_tiempo
                      ? "bg-green-600 text-white border-green-600"
                      : "border-slate-200 text-slate-600 hover:bg-slate-50"
                  }`}>
                  Sí, a tiempo
                </button>
                <button type="button"
                  onClick={() => setFormDevolucion({ ...formDevolucion, a_tiempo: false })}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-colors ${
                    !formDevolucion.a_tiempo
                      ? "bg-red-500 text-white border-red-500"
                      : "border-slate-200 text-slate-600 hover:bg-slate-50"
                  }`}>
                  No, con atraso
                </button>
              </div>
            </div>

            {!formDevolucion.a_tiempo && (
              <>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Días de atraso
                  </label>
                  <input type="number" min="1"
                    value={formDevolucion.dias_atraso}
                    onChange={(e) => setFormDevolucion({ ...formDevolucion, dias_atraso: e.target.value })}
                    className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {formDevolucion.dias_atraso > 0 && (
                    <p className="text-orange-600 text-xs mt-1">
                      Multa a aplicar: ${(formDevolucion.dias_atraso * 2).toFixed(2)}
                    </p>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <input type="checkbox" id="pagar_ahora"
                    checked={formDevolucion.pagar_multa_ahora}
                    onChange={(e) => setFormDevolucion({ ...formDevolucion, pagar_multa_ahora: e.target.checked })}
                    className="w-4 h-4 accent-blue-600"
                  />
                  <label htmlFor="pagar_ahora" className="text-sm text-slate-700">
                    Pagar multa en este momento
                  </label>
                </div>
              </>
            )}

            <div className="flex gap-3 pt-2">
              <button type="button" onClick={() => setModalDevolucion(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" disabled={guardando}
                className="flex-1 bg-slate-800 hover:bg-slate-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-60">
                {guardando ? "Registrando..." : "Confirmar devolución"}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}
