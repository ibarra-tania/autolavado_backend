'''
Docstring for schemas.schema_vehiculos
'''
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class VehiculoBase(BaseModel):
    '''Clase para modelar los campos de tabla Vehiculos'''
    usuario_Id: int
    placas: str
    marca: str
    modelo: str
    anio: int
    color: str
    tipo: str
    numero_serie: str
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime

# pylint: disable=too-few-public-methods, unnecessary-pass
class VehiculoCreate(VehiculoBase):
    '''Clase para crear un Vehiculo basado en la tabla Vehiculos'''
    pass

class VehiculoUpdate(VehiculoBase):
    '''Clase para actualizar un Vehiculo basado en la tabla Vehiculos'''
    pass

class Vehiculo(VehiculoBase):
    '''Clase para realizar operaciones por ID en tabla Vehiculos'''
    Id: int

    # ✅ CORRECCIÓN: Pydantic v2 - reemplazar class Config con model_config
    model_config = ConfigDict(from_attributes=True)