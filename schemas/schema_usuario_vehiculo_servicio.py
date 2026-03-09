'''
Docstring for schemas.schema_usuario_vehiculo_servicios
'''
from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict, field_validator

class UsuarioVehiculoServicioBase(BaseModel):
    '''Clase para modelar los campos de tabla usuario_vehiculo_servicios'''
    vehiculo_Id: int
    cajero_Id: int
    operativo_Id: int
    servicio_Id: int
    fecha: date
    hora: time
    descuento: int
    estatus: str
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime

    @field_validator("hora", mode="before")
    @classmethod
    def limpiar_zona_horaria(cls, value):
        if isinstance(value, str):
            if value.endswith("Z"):
                value = value.replace("Z", "")
            if "+" in value:
                value = value.split("+")[0]
        return value

# pylint: disable=too-few-public-methods, unnecessary-pass
class UsuarioVehiculoServicioCreate(UsuarioVehiculoServicioBase):
    '''Clase para crear basado en la tabla usuario_vehiculo_servicios'''
    pass

class UsuarioVehiculoServicioUpdate(UsuarioVehiculoServicioBase):
    '''Clase para actualizar basado en la tabla usuario_vehiculo_servicios'''
    pass

class UsuarioVehiculoServicio(UsuarioVehiculoServicioBase):
    '''Clase para realizar operaciones por ID en tabla usuario_vehiculo_servicios'''
    Id: int

    # ✅ CORRECCIÓN: Pydantic v2 - reemplazar class Config con model_config
    model_config = ConfigDict(from_attributes=True)