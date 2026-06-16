import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar las variables del archivo secreto .env
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Crear el "puente" de conexión hacia la base de datos
supabase: Client = create_client(url, key)