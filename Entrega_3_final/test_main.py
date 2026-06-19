from fastapi.testclient import TestClient
from main import app  # Importamos tu API real

# Creamos un cliente falso que simula ser un navegador web
cliente = TestClient(app)

def test_api_encendida():
    # 1. El cliente falso intenta entrar a la ruta principal ("/")
    respuesta = cliente.get("/")
    
    # 2. Verificamos que el servidor responda con "200 OK" (Código de éxito en internet)
    assert respuesta.status_code == 200
    
    # 3. Extraemos el JSON de respuesta y verificamos que traiga el mensaje correcto
    datos = respuesta.json()
    assert "mensaje" in datos
    assert datos["mensaje"] == "Sistema de Biblioteca API"