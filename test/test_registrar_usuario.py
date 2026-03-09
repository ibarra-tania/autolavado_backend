"""test_registrar_usuario.py"""

import pytest


def test_crear_usuario_exitoso(client):
    """POST /usuario/ - Crear usuario con datos válidos"""
    payload = {
        "rol_Id": 1,
        "nombre": "RegistroTest",
        "primer_apellido": "Test",
        "segundo_apellido": "Test",
        "direccion": "tes",
        "correo_electronico": "registro_test@test.com",
        "numero_telefono": "0000000000",
        "contrasena": "test1234",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }

    response = client.post("/usuario/", json=payload)

    assert response.status_code in (200, 201)

    data = response.json()
    assert data["correo_electronico"] == payload["correo_electronico"]
    assert data["nombre"] == "RegistroTest"

    # seguridad: contraseña no debe aparecer en la respuesta
    assert "contrasena" not in data


def test_crear_usuario_datos_invalidos(client):
    """POST /usuario/ - Datos con tipos incorrectos deben retornar 422"""
    payload_invalido = {
        "rol_Id": "no-es-un-numero",
        "nombre": "Error"
    }

    response = client.post("/usuario/", json=payload_invalido)

    assert response.status_code == 422