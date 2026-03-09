'''Esta clase permite generar el modelo para los productos del autolavado'''
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from config.db import Base

# pylint: disable=too-few-public-methods
class Producto(Base):
    '''Clase para especificar tabla de productos'''
    __tablename__ = "tbc_productos"
    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String(255))
    categoria = Column(String(60))       # Ej: Shampoo, Cera, Ambientador, Herramienta
    marca = Column(String(60))
    unidad_medida = Column(String(30))   # Ej: litro, pieza, kg, ml
    precio_unitario = Column(Float)
    stock = Column(Integer)
    stock_minimo = Column(Integer)       # Alerta cuando el stock baja de este nivel
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)