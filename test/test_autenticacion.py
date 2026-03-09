"""test_autenticacion.py"""

import pytest
from fastapi.testclient import TestClient


# ─────────────────────────────────────────────────────────────────────────────
# TEST LOGIN
# ─────────────────────────────────────────────────────────────────────────────

def test_login_exitoso(client, test_user):
    """POST /login - Credenciales correctas deben retornar access_token"""
    response = client.post(
        "/login",
        data={
            "username": test_user["correo_electronico"],
            "password": test_user["contrasena"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "usuario" in data
    assert "id" in data["usuario"]
    assert "correo" in data["usuario"]


def test_login_contrasena_incorrecta(client, test_user):
    """POST /login - Contraseña incorrecta debe retornar 401"""
    response = client.post(
        "/login",
        data={
            "username": test_user["correo_electronico"],
            "password": "contrasena_mal"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_login_correo_no_registrado(client):
    """POST /login - Correo inexistente debe retornar 401"""
    response = client.post(
        "/login",
        data={"username": "noexiste_nunca@test.com", "password": "test1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# TEST AUTORIZACIÓN - TOKEN INVÁLIDO
# ─────────────────────────────────────────────────────────────────────────────

def test_acceso_con_token_invalido(client):
    """GET /usuario/ - Token inventado debe retornar 401"""
    response = client.get(
        "/usuario/",
        headers={"Authorization": "Bearer token.falso.invalido"},
    )
    assert response.status_code == 401


def test_acceso_sin_prefijo_bearer(client, token):
    """GET /usuario/ - Token sin prefijo Bearer debe retornar 401"""
    response = client.get(
        "/usuario/",
        headers={"Authorization": token},  # sin "Bearer "
    )
    assert response.status_code == 401


def test_acceso_sin_header_authorization(client):
    """GET /servicio/ - Sin header Authorization debe retornar 401"""
    response = client.get("/servicio/")
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# TEST RUTAS PROTEGIDAS CON TOKEN VÁLIDO
# ─────────────────────────────────────────────────────────────────────────────

def test_get_usuarios_con_token(client, token):
    """GET /usuario/ - Con token válido debe retornar 200 y lista"""
    response = client.get("/usuario/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_servicios_con_token(client, token):
    """GET /servicio/ - Con token válido debe retornar 200 y lista"""
    response = client.get("/servicio/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_vehiculos_con_token(client, token):
    """GET /vehiculo/ - Con token válido debe retornar 200 y lista"""
    response = client.get("/vehiculo/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_usuario_vehiculo_servicio_con_token(client, token):
    """GET /usuario_vehiculo_servicio/ - Con token válido debe retornar 200"""
    response = client.get(
        "/usuario_vehiculo_servicio/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ─────────────────────────────────────────────────────────────────────────────
# TEST CICLO - Crear recurso con token
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_servicio_con_token(client, token):
    """POST /servicio/ - Con token debe crear servicio exitosamente"""
    payload = {
        "nombre": "Lavado Premium Test Auth",
        "descripcion": "Lavado completo con cera",
        "costo": 250.0,
        "duracion_minutos": 60,
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }
    response = client.post(
        "/servicio/", json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["nombre"] == "Lavado Premium Test Auth"
    assert data["costo"] == 250.0


def test_crear_vehiculo_con_token(client, token):
    """POST /vehiculo/ - Con token debe crear vehículo exitosamente"""
    payload = {
        "usuario_Id": 1,
        "placas": "AUTH-001",
        "marca": "Nissan",
        "modelo": "Versa",
        "anio": 2023,
        "color": "Blanco",
        "tipo": "Sedan",
        "numero_serie": "NIS2023AUTH",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }
    response = client.post(
        "/vehiculo/", json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["placas"] == "AUTH-001"