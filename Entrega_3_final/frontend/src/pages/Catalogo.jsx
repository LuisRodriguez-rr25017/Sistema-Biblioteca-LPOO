import { useState, useEffect } from "react";
import { getLibros, buscarLibros, crearLibro, eliminarLibro, actualizarLibro } from "../api";
import Modal from "../components/Modal";


const colores = [
  "bg-blue-600", "bg-violet-600", "bg-emerald-600",
  "bg-orange-500", "bg-rose-600", "bg-teal-600", "bg-indigo-600",
];

const colorLibro = (titulo) => colores[titulo.charCodeAt(0) % colores.length];

export default function Catalogo() {
  const [libros, setLibros] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [cargando, setCargando] = useState(true);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [mensaje, setMensaje] = useState(null);
  const [form, setForm] = useState({ titulo: "", autor: "", portada_url: "" });
  const [guardando, setGuardando] = useState(false);
  const [modalEditar, setModalEditar] = useState(false);
  const [libroEditando, setLibroEditando] = useState(null);
  const [formEditar, setFormEditar] = useState({ titulo: "", autor: "", portada_url: "" });

  const cargarLibros = async () => {
    setCargando(true);
    try {
      const data = await getLibros();
      setLibros(Array.isArray(data) ? data : []);
    } catch {
      mostrarMensaje("No se pudo conectar con el servidor.", "error");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarLibros();
  }, []);

  const mostrarMensaje = (texto, tipo = "ok") => {
    setMensaje({ texto, tipo });
    setTimeout(() => setMensaje(null), 3500);
  };

  const handleBuscar = async (e) => {
    const valor = e.target.value;
    setBusqueda(valor);
    if (valor.trim() === "") {
      cargarLibros();
    } else {
      try {
        const data = await buscarLibros(valor);
        setLibros(Array.isArray(data) ? data : []);
      } catch {
        mostrarMensaje("Error al buscar libros.", "error");
      }
    }
  };

  const handleCrear = async (e) => {
    e.preventDefault();
    if (!form.titulo.trim() || !form.autor.trim()) {
      mostrarMensaje("Título y autor son obligatorios.", "error");
      return;
    }
    setGuardando(true);
    try {
      const datos = {
        titulo: form.titulo.trim(),
        autor: form.autor.trim(),
        portada_url: form.portada_url.trim() || null,
      };
      await crearLibro(datos);
      setModalAbierto(false);
      setForm({ titulo: "", autor: "", portada_url: "" });
      mostrarMensaje("Libro registrado exitosamente.");
      cargarLibros();
    } catch {
      mostrarMensaje("Error al registrar el libro.", "error");
    } finally {
      setGuardando(false);
    }
  };
  const abrirEditar = (libro) => {
    setLibroEditando(libro);
    setFormEditar({
      titulo: libro.titulo,
      autor: libro.autor,
      portada_url: libro.portada_url || "",
    });
    setModalEditar(true);
  };

  const handleEditar = async (e) => {
    e.preventDefault();
    if (!formEditar.titulo.trim() || !formEditar.autor.trim()) {
      mostrarMensaje("Título y autor son obligatorios.", "error");
      return;
    }
    setGuardando(true);
    try {
      const res = await actualizarLibro(libroEditando.id, {
        titulo: formEditar.titulo.trim(),
        autor: formEditar.autor.trim(),
        portada_url: formEditar.portada_url.trim() || null,
      });
      if (res.id) {
        mostrarMensaje("Libro actualizado exitosamente.");
        setModalEditar(false);
        cargarLibros();
      } else {
        mostrarMensaje(res.detail || "No se pudo actualizar.", "error");
      }
    } catch {
      mostrarMensaje("Error al actualizar el libro.", "error");
    } finally {
      setGuardando(false);
    }
  };
  const handleEliminar = async (libro) => {
    if (!window.confirm(`¿Eliminar "${libro.titulo}"?`)) return;
    try {
      const res = await eliminarLibro(libro.id);
      if (res.exito) {
        mostrarMensaje("Libro eliminado.");
        cargarLibros();
      } else {
        mostrarMensaje(res.detail || "No se pudo eliminar.", "error");
      }
    } catch {
      mostrarMensaje("Error al eliminar.", "error");
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Encabezado */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Catálogo de Libros</h1>
          <p className="text-slate-500 text-sm mt-1">{libros.length} libro(s) encontrado(s)</p>
        </div>
        <button
          onClick={() => setModalAbierto(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors"
        >
          + Nuevo libro
        </button>
      </div>

      {/* Buscador */}
      <div className="relative mb-6">
        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🔍</span>
        <input
          type="text"
          placeholder="Buscar por título..."
          value={busqueda}
          onChange={handleBuscar}
          className="w-full pl-10 pr-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm"
        />
      </div>

      {/* Toast */}
      {mensaje && (
        <div
          className={`mb-4 px-4 py-3 rounded-xl text-sm font-medium ${
            mensaje.tipo === "error"
              ? "bg-red-50 text-red-700 border border-red-200"
              : "bg-green-50 text-green-700 border border-green-200"
          }`}
        >
          {mensaje.texto}
        </div>
      )}

      {/* Grid de libros */}
      {cargando ? (
        <div className="text-center py-20 text-slate-400">Cargando libros...</div>
      ) : libros.length === 0 ? (
        <div className="text-center py-20 text-slate-400">
          <p className="text-4xl mb-3">📭</p>
          <p>No hay libros registrados todavía.</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
          {libros.map((libro) => (
            <div
              key={libro.id}
              className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-shadow flex flex-col"
            >
             {libro.portada_url ? (
                <img
                  src={libro.portada_url}
                  alt={libro.titulo}
                  className="w-full h-44 object-cover bg-slate-100"
                  onError={(e) => {
                    e.target.style.display = "none";
                    e.target.nextSibling.style.display = "flex";
                  }}
                />
              ) : null}
              <div
                className={`w-full h-44 ${colorLibro(libro.titulo)} flex items-center justify-center p-3`}
                style={{ display: libro.portada_url ? "none" : "flex" }}
              >
                <p className="text-white text-center text-sm font-bold leading-tight line-clamp-4">
                  {libro.titulo}
                </p>
              </div>
              <div className="p-3 flex flex-col flex-1">
                <p className="font-semibold text-slate-800 text-sm leading-tight line-clamp-2">
                  {libro.titulo}
                </p>
                <p className="text-slate-500 text-xs mt-1 mb-2">{libro.autor}</p>
                <div className="mt-auto flex items-center justify-between">
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      libro.disponible
                        ? "bg-green-100 text-green-700"
                        : "bg-red-100 text-red-600"
                    }`}
                  >
                    {libro.disponible ? "Disponible" : "Prestado"}
                  </span>
                 <div className="flex gap-2">
                  <button
                    onClick={() => abrirEditar(libro)}
                    className="opacity-40 hover:opacity-100 transition-opacity"
                    title="Editar"
                  >
                    <img src="/iconos/icons8-editar.svg" alt="editar" className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleEliminar(libro)}
                    className="opacity-40 hover:opacity-100 transition-opacity"
                    title="Eliminar"
                  >
                    <img src="/iconos/icons8-eliminar.svg" alt="eliminar" className="w-4 h-4" />
                  </button>
                </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal nuevo libro */}
      {modalAbierto && (
        <Modal titulo="Registrar nuevo libro" onCerrar={() => setModalAbierto(false)}>
          <form onSubmit={handleCrear} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Título <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={form.titulo}
                onChange={(e) => setForm({ ...form, titulo: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ej: Cien años de soledad"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Autor <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={form.autor}
                onChange={(e) => setForm({ ...form, autor: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ej: Gabriel García Márquez"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                URL de portada <span className="text-slate-400 font-normal">(opcional)</span>
              </label>
              <input
                type="text"
                value={form.portada_url}
                onChange={(e) => setForm({ ...form, portada_url: e.target.value })}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="https://..."
              />
            </div>
            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => setModalAbierto(false)}
                className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={guardando}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-60"
              >
                {guardando ? "Guardando..." : "Registrar"}
              </button>
            </div>
          </form>
        </Modal>
      )}

      {modalEditar && libroEditando && (
  <Modal titulo="Editar libro" onCerrar={() => setModalEditar(false)}>
    <form onSubmit={handleEditar} className="flex flex-col gap-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">
          Título <span className="text-red-500">*</span>
        </label>
        <input type="text" value={formEditar.titulo}
          onChange={(e) => setFormEditar({ ...formEditar, titulo: e.target.value })}
          className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">
          Autor <span className="text-red-500">*</span>
        </label>
        <input type="text" value={formEditar.autor}
          onChange={(e) => setFormEditar({ ...formEditar, autor: e.target.value })}
          className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">
          URL de portada <span className="text-slate-400 font-normal">(opcional)</span>
        </label>
        <input type="text" value={formEditar.portada_url}
          onChange={(e) => setFormEditar({ ...formEditar, portada_url: e.target.value })}
          className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="https://..."
        />
      </div>
          {formEditar.portada_url && (
        <img src={formEditar.portada_url} alt="preview"
          className="w-24 h-32 object-cover rounded-lg border border-slate-200 mx-auto"
          onError={(e) => { e.target.style.display = "none"; }}
        />
      )}
      <div className="flex gap-3 pt-2">
        <button type="button" onClick={() => setModalEditar(false)}
          className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-sm hover:bg-slate-50 transition-colors">
          Cancelar
        </button>
        <button type="submit" disabled={guardando}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-60">
          {guardando ? "Guardando..." : "Guardar cambios"}
        </button>
      </div>
    </form>
  </Modal>
)}
    </div>
  );
}
