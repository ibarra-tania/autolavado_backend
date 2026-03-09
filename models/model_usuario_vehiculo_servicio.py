'''Esta clase permite generar el modelo para las ventas y asignaciones'''
from sqlalchemy import Column, Integer, Boolean, DateTime,Date,Time, ForeignKey,Enum
import enum
# pylint: disable=import-error
from config.db import Base
from sqlalchemy.orm import relationship

class EstatusSolicitud(str, enum.Enum):
    PROGRAMADA = "Programada"
    PROCESO = "Proceso"
    FINALIZADA = "Finalizado"
    CANCELADA = "Cancelada"

# pylint: disable=too-few-public-methods
class UsuarioVehiculoServicio(Base):
    '''Clase para especificar tabla usuarios, vehiculos, servicios'''
    __tablename__ = "tbd_usuario_vehiculo_servicios"
    Id = Column(Integer, primary_key=True, index=True)
    vehiculo_Id = Column(Integer, ForeignKey("tbb_vehiculos.Id"))
    cajero_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    operativo_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    servicio_Id = Column(Integer, ForeignKey("tbc_servicios.Id"))
    fecha = Column(Date)
    hora = Column(Time)
    descuento = Column(Integer)
    estatus = Column(Enum(EstatusSolicitud), nullable=False)
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    vehiculos = relationship("Vehiculo", back_populates="usuarios_vehiculos_servicios")
    servicios = relationship("Servicio", back_populates="usuarios_vehiculos_servicios")
    cajero = relationship("Usuario", foreign_keys=[cajero_Id], back_populates="servicios_cajero")
    operativo = relationship("Usuario",foreign_keys=[operativo_Id], back_populates="servicios_operativo")
    
