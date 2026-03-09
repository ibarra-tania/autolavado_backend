"""test_endpoints.py"""

import uuid
import pytest

# ─────────────────────────────────────────────────────────────────────────────
# TEST ENDPOINTS - USUARIO (ruta pública)
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_usuario_exitoso(client):
    """POST /usuario/ - Crear usuario con datos válidos"""
    # ✅ CORRECCIÓN: uuid ya está importado arriba (faltaba en versión original)
    correo = f"test_{uuid.uuid4().hex[:8]}@test.com"
    payload = {
        "rol_Id": 1,
        "nombre": "Test",
        "primer_apellido": "Apellido",
        "segundo_apellido": "Segundo",
        "direccion": "Calle Falsa 123",
        "correo_electronico": correo,
        "numero_telefono": "0000000000",
        "contrasena": "test1234",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    response = client.post("/usuario/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["correo_electronico"] == correo
    assert data["nombre"] == "Test"
    # Seguridad: la contraseña no debe retornarse
    assert "contrasena" not in data


def test_crear_usuario_duplicado(client):
    """POST /usuario/ - Crear usuario con nombre ya registrado debe retornar 400"""
    # ✅ NOTA: La ruta /usuario/ comprueba duplicado por nombre, no por correo.
    #    Ambas llamadas usan el mismo nombre "Duplicado" para forzar el 400.
    correo_base = f"dup_{uuid.uuid4().hex[:6]}@test.com"
    payload = {
        "rol_Id": 1,
        "nombre": "NombreDuplicadoTest",
        "primer_apellido": "Test",
        "segundo_apellido": "Test",
        "direccion": "Calle 1",
        "correo_electronico": correo_base,
        "numero_telefono": "1111111111",
        "contrasena": "test1234",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    client.post("/usuario/", json=payload)   # primera vez
    # segunda vez con mismo nombre (diferente correo para que no falle por otro motivo)
    payload2 = dict(payload)
    payload2["correo_electronico"] = f"dup2_{uuid.uuid4().hex[:6]}@test.com"
    response = client.post("/usuario/", json=payload2)
    assert response.status_code == 400


def test_get_usuarios_sin_token(client):
    """GET /usuario/ - Sin token debe retornar 401"""
    response = client.get("/usuario/")
    assert response.status_code == 401


def test_put_usuario_sin_token(client):
    """PUT /usuario/{id} - Sin token debe retornar 401"""
    payload = {
        "rol_Id": 1, "nombre": "Modificado", "primer_apellido": "T",
        "segundo_apellido": "T", "direccion": "x", "correo_electronico": "x@x.com",
        "numero_telefono": "0", "contrasena": "x", "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    response = client.put("/usuario/1", json=payload)
    assert response.status_code == 401


def test_delete_usuario_sin_token(client):
    """DELETE /usuario/{id} - Sin token debe retornar 401"""
    response = client.delete("/usuario/1")
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# TEST ENDPOINTS - ROL
# ─────────────────────────────────────────────────────────────────────────────

def test_get_roles_sin_token(client):
    """GET /rol/ - Sin token debe retornar 401"""
    response = client.get("/rol/")
    assert response.status_code == 401


def test_crear_rol_sin_token(client):
    """POST /rol/ - Sin token debe retornar 401"""
    payload = {
        "nombre_rol": "RolSinToken",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    response = client.post("/rol/", json=payload)
    # ✅ NOTA: Si POST /rol/ no requiere token en tu app (está comentado),
    #    cambia este assert a: assert response.status_code in (200, 201, 401)
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# TEST ENDPOINTS - SERVICIO
# ─────────────────────────────────────────────────────────────────────────────

def test_get_servicios_sin_token(client):
    """GET /servicio/ - Sin token debe retornar 401"""
    response = client.get("/servicio/")
    assert response.status_code == 401


def test_crear_servicio_sin_token(client):
    """POST /servicio/ - Sin token debe retornar 401"""
    payload = {
        "nombre": "Lavado Básico",
        "descripcion": "Lavado exterior básico",
        "costo": 100.0,
        "duracion_minutos": 30,
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    response = client.post("/servicio/", json=payload)
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# TEST ENDPOINTS - VEHICULO
# ─────────────────────────────────────────────────────────────────────────────

def test_get_vehiculos_sin_token(client):
    """GET /vehiculo/ - Sin token debe retornar 401"""
    response = client.get("/vehiculo/")
    assert response.status_code == 401


def test_crear_vehiculo_sin_token(client):
    """POST /vehiculo/ - Sin token debe retornar 401"""
    payload = {
        "usuario_Id": 1,
        "placas": "ABC-123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "anio": 2022,
        "color": "Rojo",
        "tipo": "Sedan",
        "numero_serie": "SER123456",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    response = client.post("/vehiculo/", json=payload)
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# TEST ENDPOINTS - USUARIO VEHICULO SERVICIO
# ─────────────────────────────────────────────────────────────────────────────

def test_get_usuario_vehiculo_servicio_sin_token(client):
    """GET /usuario_vehiculo_servicio/ - Sin token debe retornar 401"""
    response = client.get("/usuario_vehiculo_servicio/")
    assert response.status_code == 401


def test_crear_usuario_vehiculo_servicio_sin_token(client):
    """POST /usuario_vehiculo_servicio/ - Sin token debe retornar 401"""
    payload = {
        "vehiculo_Id": 1,
        "cajero_Id": 1,
        "operativo_Id": 2,
        "servicio_Id": 1,
        "fecha": "2026-02-25",
        "hora": "10:00:00",
        "descuento": 0,
        "estatus": "Programada",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }
    response = client.post("/usuario_vehiculo_servicio/", json=payload)
    assert response.status_code == 401