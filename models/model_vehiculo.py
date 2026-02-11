"""
Modelo de vehículos para el sistema de autolavado.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time, DateTime
from config.db import Base


class Vehiculo(Base):
    """Modelo de la tabla vehiculos."""

    __tablename__ = "tbb_vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20))
    serie = Column(String(60))
    color = Column(String(30))
    tipo = Column(String(250))
    anio = Column(Integer)
    estatus = Column(Boolean)
    numero = Column(String(30))
    modelo = Column(String(40))
    id_usuario = Column(Integer, ForeignKey("tbb_users.id"))
