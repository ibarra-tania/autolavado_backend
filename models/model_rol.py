'''Esta clase permite generar el modelo para los tipos de roles'''
from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.orm import relationship
# pylint: disable=import-error
from config.db import Base

# pylint: disable=too-few-public-methods
class Rol(Base):
    '''Clase para especificar tabla roles de usuario'''
    __tablename__ = "tbc_roles"

    Id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(15))
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    usuarios = relationship("Usuario", back_populates="rols")
