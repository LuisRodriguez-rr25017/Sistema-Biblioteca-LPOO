import { useState } from "react";
import Navbar from "./components/Navbar";
import Catalogo from "./pages/Catalogo";
import Prestamos from "./pages/Prestamos";
import Socios from "./pages/Socios";
import Multas from "./pages/Multas";

function App() {
  const [pagina, setPagina] = useState("catalogo");

  const renderPagina = () => {
    switch (pagina) {
      case "catalogo":  return <Catalogo />;
      case "prestamos": return <Prestamos />;
      case "socios":    return <Socios />;
      case "multas":    return <Multas />;
      default:          return <Catalogo />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar pagina={pagina} setPagina={setPagina} />
      <main>{renderPagina()}</main>
    </div>
  );
}

export default App;
