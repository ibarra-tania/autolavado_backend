import models.model_usuario_vehiculo_servicio
import schemas.schema_usuario_vehiculo_servicio
from sqlalchemy.orm import Session
import models, schemas

def get_usuario_vehiculo_servicio(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio).offset(skip).limit(limit).all()

def get_usuario_vehiculo_servicio_by_nombre(db: Session, fecha, hora):
    return db.query(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio).filter(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio.fecha == fecha,models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio.hora == hora ).first()

def create_usuario_vehiculo_servicio(db:Session, usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioCreate):
    db_usuario_vehiculo_servicio = models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio(
        vehiculo_Id = usuario_vehiculo_servicio.vehiculo_Id,
        cajero_Id = usuario_vehiculo_servicio.cajero_Id,
        operativo_Id = usuario_vehiculo_servicio.operativo_Id,
        servicio_Id = usuario_vehiculo_servicio.servicio_Id,
        fecha = usuario_vehiculo_servicio.fecha,
        hora = usuario_vehiculo_servicio.hora,
        descuento = usuario_vehiculo_servicio.descuento,
        estatus = usuario_vehiculo_servicio.estatus,
        estado = usuario_vehiculo_servicio.estado,
        fecha_registro = usuario_vehiculo_servicio.fecha_registro,
        fecha_actualizacion = usuario_vehiculo_servicio.fecha_actualizacion
    )
    db.add(db_usuario_vehiculo_servicio)
    db.commit()
    db.refresh(db_usuario_vehiculo_servicio)
    return db_usuario_vehiculo_servicio

def update_usuario_vehiculo_servicio(db:Session, id: int, usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioUpdate):
    
    db_usuario_vehiculo_servicio = db.query(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio).filter(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio.Id == id).first()
    if db_usuario_vehiculo_servicio:
        for var, value in vars(usuario_vehiculo_servicio).items():
            setattr(db_usuario_vehiculo_servicio, var, value) if value else None
        db.add(db_usuario_vehiculo_servicio)
        db.commit()
    db.refresh(db_usuario_vehiculo_servicio)
    return db_usuario_vehiculo_servicio

def delete_usuario_vehiculo_servicio(db: Session, id: int):
    db_usuario_vehiculo_servicio = db.query(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio).filter(models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio.Id == id).first()
    if db_usuario_vehiculo_servicio:
        db.delete(db_usuario_vehiculo_servicio)
        db.commit()
    return db_usuario_vehiculo_servicio