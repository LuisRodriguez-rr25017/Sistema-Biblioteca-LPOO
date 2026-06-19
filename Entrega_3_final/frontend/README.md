# Sistema de Biblioteca — Entrega 3

Sistema web de gestión de biblioteca con backend en FastAPI, base de datos en Supabase y frontend en React + Tailwind CSS.

---

## Lo que necesitas instalar antes

- Python 3.10 o superior
- Node.js (cualquier versión reciente)

---

## Paso 1 — Bajar el proyecto

```bash
git clone https://github.com/LuisRodriguez-rr25017/Sistema-Biblioteca-LPOO.git
cd Sistema-Biblioteca-LPOO
```

---

## Paso 2 — Configurar el backend

Entra a la carpeta:
```bash
cd Entrega_3_final
```

Instala las dependencias de Python:
```bash
pip install fastapi uvicorn supabase python-dotenv
```

Crea un archivo llamado `.env` en esa misma carpeta con este contenido:


SUPABASE_URL=https://lhhyypagxirtfztjuhop.supabase.co

SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxoaHl5cGFneGlydGZ6dGp1aG9wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA4NzI1NjAsImV4cCI6MjA5NjQ0ODU2MH0.Vkvo3yLajzkWBUdlDoFP9tME9RfnKGVerIdY1n7dfH0



Arranca el backend:
```bash
py -m uvicorn main:app --reload
```

Debe aparecer: `Uvicorn running on http://127.0.0.1:8000`

---

## Paso 3 — Configurar el frontend

Abre **otra terminal** y entra a la carpeta del frontend:
```bash
cd Entrega_3_final/frontend
```

Instala las dependencias de React:
```bash
npm install
```

Arranca el frontend:
```bash
npm start
```

Se abre automáticamente en el navegador en `http://localhost:3000`

---

## Nota importante

Las dos terminales deben estar corriendo al mismo tiempo. Si cierras una el sistema deja de funcionar.