import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class _LazySupabase:
    """Inicializa el cliente Supabase solo al primer uso (evita fallo al importar sin .env)."""

    _client: Client | None = None

    def _get_client(self) -> Client:
        if self._client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise RuntimeError(
                    "Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env"
                )
            self._client = create_client(url, key)
        return self._client

    def __getattr__(self, name):
        return getattr(self._get_client(), name)


supabase = _LazySupabase()


def verificar_conexion() -> bool:
    """Comprueba que el cliente Supabase responda y las tablas existan."""
    try:
        supabase.table("socios").select("id").limit(1).execute()
        return True
    except Exception:
        return False