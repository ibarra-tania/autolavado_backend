'''Establece la conexión con el servidor de Base de Datos'''
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Usar variable de entorno o cadena por defecto
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:12345@localhost:3306/autolavadodb")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ FUNCIÓN IMPORTANTE: Dependencia para FastAPI
def get_db():
    """Dependencia para obtener la sesión de BD en cada petición"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()