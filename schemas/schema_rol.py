"""
Schema para roles del sistema de autolavado.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RolBase(BaseModel):
    """Base schema para roles."""
    nombre: str
    estatus: bool
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None


class RolCreate(RolBase):
    """Schema para crear roles."""


class RolUpdate(RolBase):
    """Schema para actualizar roles."""


class Rol(RolBase):
    """Schema completo para roles."""
    id: int
    

    class Config:
        """Configuración de Pydantic."""
        orm_mode = True
