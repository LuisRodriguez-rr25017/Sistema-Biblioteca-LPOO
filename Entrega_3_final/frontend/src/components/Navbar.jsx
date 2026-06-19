export default function Navbar({ pagina, setPagina }) {
  const links = [
    { id: "catalogo", label: "Catálogo" },
    { id: "prestamos", label: "Préstamos" },
    { id: "socios", label: "Socios" },
    { id: "multas", label: "Multas" },
  ];

  return (
    <nav className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between shadow-lg">
      <div className="flex items-center gap-2">
        <span className="font-bold text-lg tracking-wide">Sistema De Biblioteca</span>
      </div>
      <div className="flex gap-1">
        {links.map((l) => (
          <button
            key={l.id}
            onClick={() => setPagina(l.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              pagina === l.id
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-700"
            }`}
          >
            {l.label}
          </button>
        ))}
      </div>
    </nav>
  );
}
