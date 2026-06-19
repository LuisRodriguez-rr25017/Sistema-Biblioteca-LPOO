import { useState, useEffect } from "react";
import { getSocios, crearSocio, eliminarSocio } from "../api";
import Modal from "../components/Modal";

export default function Socios() {
  const [socios, setSocios] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [mensaje, setMensaje] = useState(null);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [form, setForm] = useState({ nombre: "", telefono: "", email: "" });
  const [guardando, setGuardando] = useState(false);

  const cargar = async () => {
    setCargando(true);
    try {
      const data = await getSocios();
      setSocios(Array.isArray(data) ? data : []);
    } catch {
      mostrarMensaje("Error al conectar con el servidor.", "error");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => { cargar(); }, []);

  const mostrarMensaje = (texto, tipo = "ok") => {
    setMensaje({ texto, tipo });
    setTimeout(() => setMensaje(null), 3500);
  };

  const handleCrear = async (e) => {
    e.preventDefault();
    if (!form.nombre.trim()) {
      mostrarMensaje("El nombre es obligatorio.", "error");
      return;
    }
    setGuardando(true);
    try {
      const res = await crearSocio({
        nombre: form.nombre.trim(),
        telefono: form.telefono.trim() || null,
        email: form.email.trim() || null,
      });
      if (res.id) {
        mostrarMensaje("Socio registrado exitosamente.");
        setModalAbierto(false);
        setForm({ nombre: "", telefono: "", email: "" });
        cargar();
      } else {
        mostrarMensaje(res.detail || "No se pudo registrar.", "error");
      }
    } catch {
      mostrarMensaje("Error al registrar el socio.", "error");
    } finally {
      setGuardando(false);
    }
  };

  const handleEliminar = async (socio) => {
    if (!window.confirm(`¿Eliminar a "${socio.nombre}"?`)) return;
    try {
      const res = await eliminarSocio(socio.id);
      if (res.exito) {
        mostrarMensaje("Socio eliminado.");
        cargar();
      } else {
        mostrarMensaje(res.detail || "No se pudo eliminar.", "error");
      }
    } catch {
      mostrarMensaje("Error al eliminar.", "error");
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Socios</h1>
          <p className="text-slate-500 text-sm mt-1">{socios.length} socio(s) registrado(s)</p>
        </div>
        <button
          onClick={() => setModalAbierto(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors"
        >
          + Nuevo socio
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
      ) : socios.length === 0 ? (
        <div className="text-center py-20 text-slate-400">
          <p>No hay socios registrados todavía.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {socios.map((s) => (
            <div key={s.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-4 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 font-bold flex items-center justify-center text-sm flex-shrink-0">
                  {s.nombre.charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="font-semibold text-slate-800">{s.nombre}</p>
                  <div className="flex gap-3 text-xs text-slate-400 mt-0.5">
                  {s.telefono && (
                    <span className="flex items-center gap-1">
                      <img src="/iconos/phone-icon.svg" alt="teléfono" className="w-3 h-3 opacity-60" />
                      {s.telefono}
                    </span>
                  )}
                  {s.email && (
                    <span className="flex items-center gap-1">
                      <img src="/iconos/email-icon.svg" alt="email" className="w-3 h-3 opacity-60" />
                      {s.email}
                    </span>
                  )}
                </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {s.multa_actual > 0 && (
                  <span className="bg-red-100 text-red-600 text-xs font-medium px-2 py-1 rounded-full">
                    Multa: ${parseFloat(s.multa_actual).toFixed(2)}
                  </span>
                )}
               <button
                onClick={() => handleEliminar(s)}
                className="opacity-40 hover:opacity-100 transition-opacity"
                title="Eliminar"
              >
                <img src="/iconos/icons8-eliminar.svg" alt="eliminar" className="w-4 h-4" />
              </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {modalAbierto && (
        <Modal titulo="Registrar nuevo socio" onCerrar={() => setModalAbierto(false)}>
          <form onSubmit={handleCrear} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Nombre completo <span className="text-red-500">*</span>
              </label>
              <input type="text" value={form.nombre}
                onChange={(e) => setForm({ ...form, nombre: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ej: Juan Pérez"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Teléfono <span className="text-slate-400 font-normal">(opcional)</span>
              </label>
              <input type="text" value={form.telefono}
                onChange={(e) => setForm({ ...form, telefono: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ej: 7555-1234"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Email <span className="text-slate-400 font-normal">(opcional)</span>
              </label>
              <input type="email" value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ej: juan@correo.com"
              />
            </div>
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={() => setModalAbierto(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" disabled={guardando}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-60">
                {guardando ? "Guardando..." : "Registrar"}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}
