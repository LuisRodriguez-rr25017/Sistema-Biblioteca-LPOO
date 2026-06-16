import pytest
from db_config import supabase

def test_insertar_socio():
    # 1. Preparamos un dato falso
    nuevo_socio = {
        "nombre": "Socio de Prueba Unitario",
        "telefono": "0000-0000"
    }
    
    try:
        # 2. Insertamos el dato en la tabla 'socios' de Supabase
        respuesta = supabase.table("socios").insert(nuevo_socio).execute()
        
        # 3. Verificamos que la base de datos nos devuelva lo que guardó
        assert len(respuesta.data) > 0
        assert respuesta.data[0]["nombre"] == "Socio de Prueba Unitario"
        
        # 4. Limpiamos la base de datos borrando el registro de prueba usando su ID
        id_creado = respuesta.data[0]["id"]
        supabase.table("socios").delete().eq("id", id_creado).execute()
        
    except Exception as e:
        # Si algo falla (ej. sin internet o tabla no existe), lanzamos un error claro
        pytest.fail(f"La prueba de base de datos falló: {e}")