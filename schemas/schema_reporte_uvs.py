'''
Schema de respuesta para el reporte detallado de UsuarioVehiculoServicio con JOIN.
Solo se usa como modelo de salida (response_model), no requiere Create/Update.
'''
from datetime import date, time
from pydantic import BaseModel, ConfigDict


class ReporteUVSPorFecha(BaseModel):
    '''Resultado del GET con JOIN para mostrar detalle de servicio por fecha'''

    # Cajero (rol_Id == 2)
    cajero_nombre_completo: str

    # Operativo (rol_Id == 3)
    operativo_nombre_completo: str

    # Servicio
    nombre_servicio: str
    costo_servicio: float
    descripcion_servicio: str

    # Vehículo
    placas: str
    marca: str
    modelo: str
    color: str

    # Registro
    fecha: date
    hora: time
    descuento: int          # porcentaje de descuento
    costo_total: float      # costo_servicio - (costo_servicio * descuento / 100)
    estatus: str

    model_config = ConfigDict(from_attributes=True)