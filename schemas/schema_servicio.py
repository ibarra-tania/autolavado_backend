"""
Esquemas Pydantic para Servicio.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class ServicioBase(BaseModel):
    """
    Esquema base de Servicio.
    """
    nombre: str
    descripcion: Optional[str]
    costo: float
    estatus: bool
    id_user: int


class ServicioCreate(ServicioBase):
    """
    Esquema para crear servicio.
    """


class ServicioUpdate(ServicioBase):
    """
    Esquema para actualizar servicio.
    """


class ServicioResponse(ServicioBase):
    """
    Esquema de respuesta de servicio.
    """
    se_id: int
    fecha_registro: datetime
    fecha_modificacion: Optional[datetime]

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True