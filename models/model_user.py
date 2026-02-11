"""
Modelo de usuarios para el sistema de autolavado.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base


class User(Base):
    """Modelo de la tabla de usuarios."""

    __tablename__ = "tbb_users"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("tbc_roles.id"))
    nombre = Column(String(60))
    papellido = Column(String(60))
    sapellido = Column(String(60))
    direccion = Column(String(200))
    correo = Column(String(80))    
    usuario = Column(String(60))
    contrasena = Column(String(60))
    telefono = Column(String(15))
    estatus = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_modificacion = Column(DateTime)

