"""test_integracion.py"""

import pytest


def auth(t):
    return {"Authorization": f"Bearer {t}"}


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRACIÓN - FLUJO COMPLETO USUARIO
# ─────────────────────────────────────────────────────────────────────────────

def test_flujo_registro_y_login(client):
    """Registro de usuario nuevo seguido de login exitoso"""
    correo = "flujo_integ_unico@test.com"
    reg = client.post("/usuario/", json={
        "rol_Id": 1,
        "nombre": "FlujoIntegracion",
        "primer_apellido": "Integracion",
        "segundo_apellido": "OK",
        "direccion": "Av. Flujo 10",
        "correo_electronico": correo,
        "numero_telefono": "3333333333",
        "contrasena": "flujo1234",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    })
    # Puede retornar 400 si el usuario ya existe de una ejecución anterior
    assert reg.status_code in (200, 201, 400)

    login = client.post(
        "/login",
        data={"username": correo, "password": "flujo1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_flujo_crud_servicio(client, token):
    """Crear → Leer → Actualizar → Eliminar un servicio"""
    crear = client.post("/servicio/", json={
        "nombre": "Servicio Integracion CRUD",
        "descripcion": "Para test de integracion",
        "costo": 150.0,
        "duracion_minutos": 45,
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert crear.status_code in (200, 201)
    servicio_id = crear.json()["Id"]

    lista = client.get("/servicio/", headers=auth(token))
    assert lista.status_code == 200
    assert servicio_id in [s["Id"] for s in lista.json()]

    actualizar = client.put(f"/servicio/{servicio_id}", json={
        "nombre": "Servicio Actualizado",
        "descripcion": "Descripcion actualizada",
        "costo": 180.0,
        "duracion_minutos": 50,
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert actualizar.status_code == 200
    assert actualizar.json()["costo"] == 180.0

    eliminar = client.delete(f"/servicio/{servicio_id}", headers=auth(token))
    assert eliminar.status_code == 200

    lista2 = client.get("/servicio/", headers=auth(token))
    assert servicio_id not in [s["Id"] for s in lista2.json()]


def test_flujo_crud_vehiculo(client, token):
    """Crear → Leer → Actualizar → Eliminar un vehículo"""
    crear = client.post("/vehiculo/", json={
        "usuario_Id": 1,
        "placas": "INTEG-VEH-01",
        "marca": "Chevrolet",
        "modelo": "Spark",
        "anio": 2020,
        "color": "Verde",
        "tipo": "Hatchback",
        "numero_serie": "CHEV2020INTEG",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert crear.status_code in (200, 201)
    vehiculo_id = crear.json()["Id"]

    lista = client.get("/vehiculo/", headers=auth(token))
    assert lista.status_code == 200

    actualizar = client.put(f"/vehiculo/{vehiculo_id}", json={
        "usuario_Id": 1,
        "placas": "INTEG-VEH-01",
        "marca": "Chevrolet",
        "modelo": "Spark GT",
        "anio": 2021,
        "color": "Verde Oscuro",
        "tipo": "Hatchback",
        "numero_serie": "CHEV2020INTEG",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert actualizar.status_code == 200
    assert actualizar.json()["modelo"] == "Spark GT"

    eliminar = client.delete(f"/vehiculo/{vehiculo_id}", headers=auth(token))
    assert eliminar.status_code == 200


def test_flujo_crud_usuario_vehiculo_servicio(client, token):
    """Crear → Leer → Actualizar estatus → Eliminar"""
    crear = client.post("/usuario_vehiculo_servicio/", json={
        "vehiculo_Id": 1,
        "cajero_Id": 1,
        "operativo_Id": 1,
        "servicio_Id": 1,
        "fecha": "2026-03-01",
        "hora": "09:00:00",
        "descuento": 10,
        "estatus": "Programada",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert crear.status_code in (200, 201)
    uvs_id = crear.json()["Id"]

    lista = client.get("/usuario_vehiculo_servicio/", headers=auth(token))
    assert lista.status_code == 200

    actualizar = client.put(f"/usuario_vehiculo_servicio/{uvs_id}", json={
        "vehiculo_Id": 1,
        "cajero_Id": 1,
        "operativo_Id": 1,
        "servicio_Id": 1,
        "fecha": "2026-03-01",
        "hora": "09:00:00",
        "descuento": 10,
        "estatus": "Proceso",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert actualizar.status_code == 200
    assert actualizar.json()["estatus"] == "Proceso"

    eliminar = client.delete(f"/usuario_vehiculo_servicio/{uvs_id}", headers=auth(token))
    assert eliminar.status_code == 200


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRACIÓN - Recursos no encontrados (404)
# ─────────────────────────────────────────────────────────────────────────────

def test_update_servicio_no_existente(client, token):
    """PUT /servicio/99999 - ID inexistente debe retornar 404"""
    response = client.put("/servicio/99999", json={
        "nombre": "No existe",
        "descripcion": "x",
        "costo": 10.0,
        "duracion_minutos": 10,
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z",
    }, headers=auth(token))
    assert response.status_code == 404


def test_delete_vehiculo_no_existente(client, token):
    """DELETE /vehiculo/99999 - ID inexistente debe retornar 404"""
    response = client.delete("/vehiculo/99999", headers=auth(token))
    assert response.status_code == 404


def test_delete_uvs_no_existente(client, token):
    """DELETE /usuario_vehiculo_servicio/99999 - ID inexistente debe retornar 404"""
    response = client.delete("/usuario_vehiculo_servicio/99999", headers=auth(token))
    assert response.status_code == 404