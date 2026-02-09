"""
Modelo de clientes para el sistema de autolavado.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.db import Base


class Cliente(Base):
    """Modelo de la tabla clientes."""

    __tablename__ = "tbc_clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    papellido = Column(String(60))
    sapellido = Column(String(60))
    direccion = Column(String(120))
    telefono = Column(String(15))
    correo = Column(String(80))
    estatus = Column(Boolean)
    fecha_creacion = Column(DateTime)
    fecha_modificacion = Column(DateTime)
