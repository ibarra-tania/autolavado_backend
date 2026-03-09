import sys
import os
import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from config.db import Base, get_db

# ✅ Usar SQLite para pruebas, NO MySQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_autolavado.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Sobrescribe la dependencia get_db para usar BD de prueba SQLite"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# ✅ Aplicar la sobrescritura ANTES de que los tests corran
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crear tablas antes de las pruebas y eliminarlas después"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Sesión de BD para pruebas con rollback automático"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client():
    """Cliente de prueba reutilizable por módulo"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_user(client):
    """
    Crea un usuario de prueba con correo único y lo devuelve junto con sus credenciales.
    ✅ Corrección: usar uuid para evitar colisiones entre ejecuciones.
    """
    correo = f"test_{uuid.uuid4().hex[:8]}@test.com"
    user_data = {
        "rol_Id": 1,
        "nombre": "Test",
        "primer_apellido": "User",
        "segundo_apellido": "Prueba",
        "direccion": "Calle Test 123",
        "correo_electronico": correo,
        "numero_telefono": "1234567890",
        "contrasena": "test1234",
        "estado": True,
        "fecha_registro": "2026-02-25T14:34:23.167Z",
        "fecha_actualizacion": "2026-02-25T14:34:23.167Z"
    }

    response = client.post("/usuario/", json=user_data)
    assert response.status_code in (200, 201), f"Error creando usuario de prueba: {response.text}"
    return user_data


@pytest.fixture(scope="module")
def token(client, test_user):
    """Obtiene token JWT para el usuario de prueba"""
    response = client.post(
        "/login",
        data={
            "username": test_user["correo_electronico"],
            "password": test_user["contrasena"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Error obteniendo token: {response.text}"
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(token):
    """Headers con token de autorización listos para usar"""
    return {"Authorization": f"Bearer {token}"}