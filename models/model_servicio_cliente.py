"""
Modelo de servicios realizados a vehículos.
"""

from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from config.db import Base


class ServicioVehiculo(Base):
    """Modelo de la tabla detalle de servicios por vehículo."""

    __tablename__ = "tbd_servicios_vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    id_cajero = Column(Integer, ForeignKey("tbb_users.id"))
    id_lavador = Column(Integer, ForeignKey("tbb_users.id"))
    id_vehiculo = Column(Integer, ForeignKey("tbb_vehiculo.id"))
    id_servicio = Column(Integer, ForeignKey("tbc_servicios.id"))
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
