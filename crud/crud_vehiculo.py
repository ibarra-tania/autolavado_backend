import models.model_vehiculos
import schemas.schema_vehiculo
from sqlalchemy.orm import Session
import models, schemas

def get_vehiculo(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.model_vehiculos.Vehiculo).offset(skip).limit(limit).all()

def get_vehiculo_by_nombre(db: Session, placas: str):
    return db.query(models.model_vehiculos.Vehiculo).filter(models.model_vehiculos.Vehiculo.placas == placas).first()

def create_vehiculo(db:Session, vehiculo: schemas.schema_vehiculo.VehiculoCreate):
    db_vehiculo = models.model_vehiculos.Vehiculo(
        usuario_Id = vehiculo.usuario_Id,
        placas = vehiculo.placas,
        marca = vehiculo.marca,
        modelo = vehiculo.modelo,
        anio = vehiculo.anio,
        color = vehiculo.color,
        tipo = vehiculo.tipo,
        numero_serie = vehiculo.numero_serie,
        estado = vehiculo.estado,
        fecha_registro = vehiculo.fecha_registro,
        fecha_actualizacion = vehiculo.fecha_actualizacion
    )
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def update_vehiculo(db:Session, id: int, vehiculo: schemas.schema_vehiculo.VehiculoUpdate):
    
    db_vehiculo = db.query(models.model_vehiculos.Vehiculo).filter(models.model_vehiculos.Vehiculo.Id == id).first()
    if db_vehiculo:
        for var, value in vars(vehiculo).items():
            setattr(db_vehiculo, var, value) if value else None
        db.add(db_vehiculo)
        db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def delete_vehiculo(db: Session, id: int):
    db_vehiculo = db.query(models.model_vehiculos.Vehiculo).filter(models.model_vehiculos.Vehiculo.Id == id).first()
    if db_vehiculo:
        db.delete(db_vehiculo)
        db.commit()
    return db_vehiculo