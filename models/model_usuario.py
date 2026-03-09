'''Esta clase permite generar el modelo para los usuarios'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.orm import relationship
# pylint: disable=import-error
from config.db import Base

# pylint: disable=too-few-public-methods
class Usuario(Base):
    '''Clase para especificar tabla usuarios'''
    __tablename__ = "tbb_usuarios"
    Id = Column(Integer, primary_key=True, index=True)
    rol_Id = Column(Integer, ForeignKey("tbc_roles.Id"))
    nombre = Column(String(60))
    primer_apellido = Column(String(60))
    segundo_apellido = Column(String(60))
    direccion = Column(String(200))
    correo_electronico = Column(String(100))
    numero_telefono = Column(String(20))
    contrasena = Column(String(512))
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)
    
    rols = relationship("Rol", back_populates="usuarios")
    vehiculos = relationship("Vehiculo", back_populates="usuarios")
    servicios_cajero = relationship("UsuarioVehiculoServicio", foreign_keys="UsuarioVehiculoServicio.cajero_Id", back_populates="cajero")
    servicios_operativo = relationship("UsuarioVehiculoServicio", foreign_keys="UsuarioVehiculoServicio.operativo_Id", back_populates="operativo")
