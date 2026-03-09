"""test_base_datos.py"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN - SQLite para pruebas (sin necesitar MySQL)
# ─────────────────────────────────────────────────────────────────────────────
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_autolavado.db")

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import models.model_rol
import models.model_usuario
import models.model_servicio
import models.model_vehiculos
import models.model_usuario_vehiculo_servicio
from config.db import Base

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    """Sesión de BD que hace rollback al finalizar cada test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


# ─────────────────────────────────────────────────────────────────────────────
# TEST BD - ROL
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_rol_en_bd(db):
    """Insertar un rol directamente en BD y verificar su persistencia"""
    rol = models.model_rol.Rol(
        nombre_rol="Admin_BD",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)

    assert rol.Id is not None
    assert rol.nombre_rol == "Admin_BD"
    assert rol.estado is True


def test_leer_rol_de_bd(db):
    """Insertar y luego consultar rol por nombre"""
    rol = models.model_rol.Rol(
        nombre_rol="Operativo_BD",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(rol)
    db.commit()

    encontrado = db.query(models.model_rol.Rol).filter(
        models.model_rol.Rol.nombre_rol == "Operativo_BD"
    ).first()
    assert encontrado is not None
    assert encontrado.nombre_rol == "Operativo_BD"


# ─────────────────────────────────────────────────────────────────────────────
# TEST BD - USUARIO
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_usuario_en_bd(db):
    """Insertar usuario y verificar que se guardó correctamente"""
    rol = models.model_rol.Rol(
        nombre_rol="Cajero_BD",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(rol)
    db.commit()

    usuario = models.model_usuario.Usuario(
        rol_Id=rol.Id,
        nombre="Juan",
        primer_apellido="Perez",
        segundo_apellido="Lopez",
        direccion="Calle 5",
        correo_electronico="juan.bd@test.com",
        numero_telefono="4444444444",
        contrasena="hash_seguro_123",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    assert usuario.Id is not None
    assert usuario.correo_electronico == "juan.bd@test.com"
    assert usuario.contrasena == "hash_seguro_123"


def test_actualizar_usuario_en_bd(db):
    """Actualizar nombre de usuario y verificar cambio"""
    rol = models.model_rol.Rol(
        nombre_rol="RolUpdate",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(rol)
    db.commit()

    usuario = models.model_usuario.Usuario(
        rol_Id=rol.Id,
        nombre="Original",
        primer_apellido="Apellido",
        segundo_apellido="Seg",
        direccion="Dir 1",
        correo_electronico="original.bd@test.com",
        numero_telefono="1234567890",
        contrasena="hash",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(usuario)
    db.commit()

    usuario.nombre = "Actualizado"
    db.commit()
    db.refresh(usuario)

    assert usuario.nombre == "Actualizado"


def test_eliminar_usuario_en_bd(db):
    """Eliminar usuario y verificar que no existe"""
    rol = models.model_rol.Rol(
        nombre_rol="RolDelete",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(rol)
    db.commit()

    usuario = models.model_usuario.Usuario(
        rol_Id=rol.Id,
        nombre="Eliminar",
        primer_apellido="Test",
        segundo_apellido="BD",
        direccion="Dir",
        correo_electronico="eliminar.bd@test.com",
        numero_telefono="0000000001",
        contrasena="hash",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(usuario)
    db.commit()
    uid = usuario.Id

    db.delete(usuario)
    db.commit()

    resultado = db.query(models.model_usuario.Usuario).filter(
        models.model_usuario.Usuario.Id == uid
    ).first()
    assert resultado is None


# ─────────────────────────────────────────────────────────────────────────────
# TEST BD - SERVICIO
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_servicio_en_bd(db):
    """Insertar servicio y verificar campos numéricos"""
    servicio = models.model_servicio.Servicio(
        nombre="Lavado Express BD",
        descripcion="Rapido y eficiente",
        costo=80.0,
        duracion_minutos=20,
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(servicio)
    db.commit()
    db.refresh(servicio)

    assert servicio.Id is not None
    assert servicio.costo == 80.0
    assert servicio.duracion_minutos == 20


# ─────────────────────────────────────────────────────────────────────────────
# TEST BD - VEHICULO
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_vehiculo_en_bd(db):
    """Insertar vehículo y verificar placa única"""
    vehiculo = models.model_vehiculos.Vehiculo(
        usuario_Id=1,
        placas="BD-TEST-02",
        marca="Toyota",
        modelo="Yaris",
        anio=2019,
        color="Plata",
        tipo="Sedan",
        numero_serie="TOY2019BD2",
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(vehiculo)
    db.commit()
    db.refresh(vehiculo)

    assert vehiculo.Id is not None
    assert vehiculo.placas == "BD-TEST-02"


# ─────────────────────────────────────────────────────────────────────────────
# TEST BD - USUARIO VEHICULO SERVICIO
# ─────────────────────────────────────────────────────────────────────────────

def test_crear_uvs_en_bd(db):
    """Insertar registro UsuarioVehiculoServicio y verificar Enum de estatus"""
    uvs = models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio(
        vehiculo_Id=1,
        cajero_Id=1,
        operativo_Id=1,
        servicio_Id=1,
        fecha=date(2026, 3, 1),
        hora=time(10, 0, 0),
        descuento=0,
        estatus=models.model_usuario_vehiculo_servicio.EstatusSolicitud.PROGRAMADA,
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(uvs)
    db.commit()
    db.refresh(uvs)

    assert uvs.Id is not None
    assert uvs.estatus == models.model_usuario_vehiculo_servicio.EstatusSolicitud.PROGRAMADA


def test_cambiar_estatus_uvs_en_bd(db):
    """Cambiar estatus de Programada → Finalizada"""
    uvs = models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio(
        vehiculo_Id=1,
        cajero_Id=1,
        operativo_Id=1,
        servicio_Id=1,
        fecha=date(2026, 3, 2),
        hora=time(11, 0, 0),
        descuento=5,
        estatus=models.model_usuario_vehiculo_servicio.EstatusSolicitud.PROGRAMADA,
        estado=True,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )
    db.add(uvs)
    db.commit()

    uvs.estatus = models.model_usuario_vehiculo_servicio.EstatusSolicitud.FINALIZADA
    db.commit()
    db.refresh(uvs)

    assert uvs.estatus == models.model_usuario_vehiculo_servicio.EstatusSolicitud.FINALIZADA


# ─────────────────────────────────────────────────────────────────────────────
# TEST BD - CONEXIÓN
# ─────────────────────────────────────────────────────────────────────────────

def test_conexion_bd():
    """Verificar que la BD responde a una consulta básica"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1