"""
Modelo de servicios para el sistema de autolavado.
"""

from sqlalchemy import Column, Integer, String, Float
from config.db import Base


class Servicio(Base):
    """Modelo de la tabla servicios."""

    __tablename__ = "tbc_servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    descripcion = Column(String(120))
    costo = Column(Float)
    estado = Column(Boolean)
    duracionMinutos = Column(Integer)
    id_user = Column(Integer, ForeignKey("tbb_users.id"))
