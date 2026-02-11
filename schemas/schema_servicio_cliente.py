"""
Esquemas Pydantic para ServicioVehiculo.
"""

from datetime import datetime, time
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class ServicioVehiculoBase(BaseModel):
    """
    Esquema base de ServicioVehiculo.
    """
    au_id: int
    se_id: int
    us_id: int
    as_monto: float
    as_pagado: bool
    as_aprobado: bool


class ServicioVehiculoCreate(ServicioVehiculoBase):
    """
    Esquema para crear servicio de vehiculo.
    """


class ServicioVehiculoResponse(ServicioVehiculoBase):
    """
    Esquema de respuesta de servicio de vehiculo.
    """
    as_id: int
    as_fecha: datetime
    as_hora: time

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True