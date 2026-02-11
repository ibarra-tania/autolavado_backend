"""
Esquemas Pydantic para Cliente.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class ClienteBase(BaseModel):
    """
    Esquema base de Cliente.
    """
    nombre: str
    papellido: str
    sapellido: Optional[str]
    direccion: Optional[str]
    correo: Optional[str]
    telefono: Optional[str]
    estatus: bool


class ClienteCreate(ClienteBase):
    """
    Esquema para crear cliente.
    """
    cl_password: str


class ClienteUpdate(ClienteBase):
    """
    Esquema para actualizar cliente.
    """


class ClienteResponse(ClienteBase):
    """
    Esquema de respuesta de cliente.
    """
    cl_id: int
    cl_fecha_registro: datetime
    cl_fecha_modificacion: Optional[datetime]

    class Config:
        """
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        """
        orm_mode = True