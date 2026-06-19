import { useState, useEffect } from "react";
import { getSociosConMulta, pagarMulta } from "../api";
import Modal from "../components/Modal";

export default function Multas() {
  const [socios, setSocios] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [mensaje, setMensaje] = useState(null);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [socioSeleccionado, setSocioSeleccionado] = useState(null);
  const [tipoPago, setTipoPago] = useState("total");
  const [monto, setMonto] = useState("");
  const [guardando, setGuardando] = useState(false);

  const cargar = async () => {
    setCargando(true);
    try {
      const data = await getSociosConMulta();
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
    setTimeout(() => setMensaje(null), 4000);
  };

  const abrirModal = (socio) => {
    setSocioSeleccionado(socio);
    setTipoPago("total");
    setMonto("");
    setModalAbierto(true);
  };

  const handlePago = async (e) => {
    e.preventDefault();
    setGuardando(true);
    try {
      const datos =
        tipoPago === "total"
          ? { monto: 0, pago_total: true }
          : { monto: parseFloat(monto) || 0, pago_total: false };

      const res = await pagarMulta(socioSeleccionado.id, datos);
      if (res.exito) {
        mostrarMensaje(res.mensaje);
        setModalAbierto(false);
        cargar();
      } else {
        mostrarMensaje(res.detail || "No se pudo procesar el pago.", "error");
      }
    } catch {
      mostrarMensaje("Error al procesar el pago.", "error");
    } finally {
      setGuardando(false);
    }
  };

  const totalMultas = socios.reduce(
    (acc, s) => acc + parseFloat(s.multa_actual || 0),
    0
  );

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Multas pendientes</h1>
        <p className="text-slate-500 text-sm mt-1">
          {socios.length} socio(s) con deuda pendiente
        </p>
      </div>

      {/* Resumen */}
      {socios.length > 0 && (
        <div className="bg-red-50 border border-red-100 rounded-2xl p-4 mb-6 flex items-center justify-between">
          <div>
            <p className="text-sm text-red-600 font-medium">Total a cobrar</p>
            <p className="text-2xl font-bold text-red-700">${totalMultas.toFixed(2)}</p>
          </div>
          <img src="/iconos/alert-triangle.svg" alt="alerta" className="w-8 h-8 opacity-100" />
        </div>
      )}

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
          <p>No hay socios con multas pendientes.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {socios.map((s) => (
            <div key={s.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-4 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-red-100 text-red-600 font-bold flex items-center justify-center text-sm flex-shrink-0">
                  {s.nombre.charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="font-semibold text-slate-800">{s.nombre}</p>
                  <p className="text-xs text-slate-400 mt-0.5">ID #{s.id}</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-red-600 font-bold text-lg">
                  ${parseFloat(s.multa_actual).toFixed(2)}
                </span>
                <button
                  onClick={() => abrirModal(s)}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg transition-colors"
                >
                  Registrar pago
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {modalAbierto && socioSeleccionado && (
        <Modal titulo="Registrar pago de multa" onCerrar={() => setModalAbierto(false)}>
          <div className="mb-4 bg-slate-50 rounded-xl p-3 text-sm">
            <p className="font-medium text-slate-700">{socioSeleccionado.nombre}</p>
            <p className="text-red-600 font-bold text-base mt-1">
              Multa total: ${parseFloat(socioSeleccionado.multa_actual).toFixed(2)}
            </p>
          </div>
          <form onSubmit={handlePago} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Tipo de pago
              </label>
              <div className="flex gap-3">
                <button type="button"
                  onClick={() => setTipoPago("total")}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-colors ${
                    tipoPago === "total"
                      ? "bg-blue-600 text-white border-blue-600"
                      : "border-slate-200 text-slate-600 hover:bg-slate-50"
                  }`}>
                  Pago total
                </button>
                <button type="button"
                  onClick={() => setTipoPago("parcial")}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-colors ${
                    tipoPago === "parcial"
                      ? "bg-blue-600 text-white border-blue-600"
                      : "border-slate-200 text-slate-600 hover:bg-slate-50"
                  }`}>
                  Pago parcial
                </button>
              </div>
            </div>

            {tipoPago === "parcial" && (
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Monto a pagar
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">$</span>
                  <input type="number" min="0.01" step="0.01"
                    max={parseFloat(socioSeleccionado.multa_actual)}
                    value={monto}
                    onChange={(e) => setMonto(e.target.value)}
                    className="w-full border border-slate-200 rounded-lg pl-7 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="0.00"
                  />
                </div>
                {monto && (
                  <p className="text-xs text-slate-400 mt-1">
                    Saldo restante: ${(parseFloat(socioSeleccionado.multa_actual) - parseFloat(monto || 0)).toFixed(2)}
                  </p>
                )}
              </div>
            )}

            <div className="flex gap-3 pt-2">
              <button type="button" onClick={() => setModalAbierto(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" disabled={guardando}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-60">
                {guardando ? "Procesando..." : "Confirmar pago"}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}
