"""
Esquemas Pydantic para Vehiculo.
"""

from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class VehiculoBase(BaseModel):
    """
    Esquema base de Vehiculo.
    """
    modelo: str
    matricula: str
    color: Optional[str]
    numero: Optional[str]
    id_cliente: int


class VehiculoCreate(VehiculoBase):
    """
    Esquema para crear vehiculo.
    """


class VehiculoUpdate(VehiculoBase):
    """
    Esquema para actualizar vehiculo.
    """


class VehiculoResponse(VehiculoBase):
    """
    Esquema de respuesta de vehiculo.
    """
    au_id: int

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True