"""
Modelo de vehículos para el sistema de autolavado.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base


class Vehiculo(Base):
    """Modelo de la tabla vehiculos."""

    __tablename__ = "tbb_vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(20))
    color = Column(String(30))
    numero = Column(String(30))
    modelo = Column(String(40))
    id_cliente = Column(Integer, ForeignKey("tbc_clientes.id"))
