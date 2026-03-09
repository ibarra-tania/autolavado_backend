import models.model_servicio
import schemas.schema_servicio
from sqlalchemy.orm import Session
import models, schemas

def get_servicio(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.model_servicio.Servicio).offset(skip).limit(limit).all()

def get_servicio_by_nombre(db: Session, nombre: str):
    return db.query(models.model_servicio.Servicio).filter(models.model_servicio.Servicio.nombre == nombre).first()

def create_servicio(db:Session, servicio: schemas.schema_servicio.ServicioCreate):
    db_servicio = models.model_servicio.Servicio(
        nombre = servicio.nombre,
        descripcion = servicio.descripcion,
        costo = servicio.costo,
        duracion_minutos = servicio.duracion_minutos,
        estado = servicio.estado,
        fecha_registro = servicio.fecha_registro,
        fecha_actualizacion = servicio.fecha_actualizacion
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio

def update_servicio(db:Session, id: int, servicio: schemas.schema_servicio.ServicioUpdate):
    
    db_servicio = db.query(models.model_servicio.Servicio).filter(models.model_servicio.Servicio.Id == id).first()
    if db_servicio:
        for var, value in vars(servicio).items():
            setattr(db_servicio, var, value) if value else None
        db.add(db_servicio)
        db.commit()
    db.refresh(db_servicio)
    return db_servicio

def delete_servicio(db: Session, id: int):
    db_servicio = db.query(models.model_servicio.Servicio).filter(models.model_servicio.Servicio.Id == id).first()
    if db_servicio:
        db.delete(db_servicio)
        db.commit()
    return db_servicio