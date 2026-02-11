"""
Modelo de roles de usuarios para el sistema de autolavado.
"""

from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base


class Rol(Base):
    """Modelo de la tabla de roles."""

    __tablename__ = "tbc_roles"

    id = Column(Integer, primary_key=True, index=True)
    nombreRol = Column(String(60))
    estatus = Column(Boolean)
    fecha_creacion = Column(DateTime)
    fecha_modificacion = Column(DateTime)
