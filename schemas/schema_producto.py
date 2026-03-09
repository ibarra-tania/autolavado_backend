'''
Docstring for schemas.schema_producto
'''
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProductoBase(BaseModel):
    '''Clase para modelar los campos de tabla Productos'''
    nombre: str
    descripcion: str
    categoria: str
    marca: str
    unidad_medida: str
    precio_unitario: float
    stock: int
    stock_minimo: int
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime

# pylint: disable=too-few-public-methods, unnecessary-pass
class ProductoCreate(ProductoBase):
    '''Clase para crear un Producto'''
    pass

class ProductoUpdate(ProductoBase):
    '''Clase para actualizar un Producto'''
    pass

class Producto(ProductoBase):
    '''Clase para realizar operaciones por ID en tabla Productos'''
    Id: int

    model_config = ConfigDict(from_attributes=True)