import models.model_rol
import schemas.schema_rol
from sqlalchemy.orm import Session
import models, schemas

def get_rol(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.model_rol.Rol).offset(skip).limit(limit).all()

def get_rol_by_nombre(db: Session, nombre_rol: str):
    return db.query(models.model_rol.Rol).filter(models.model_rol.Rol.nombre_rol == nombre_rol).first()

def create_rol(db:Session, rol: schemas.schema_rol.RolCreate):
    db_rol = models.model_rol.Rol(
        nombre_rol = rol.nombre_rol,
        estado = rol.estado,
        fecha_registro = rol.fecha_registro,
        fecha_actualizacion = rol.fecha_actualizacion
    )
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def update_rol(db:Session, id: int, rol: schemas.schema_rol.RolUpdate):
    
    db_rol = db.query(models.model_rol.Rol).filter(models.model_rol.Rol.Id == id).first()
    if db_rol:
        for var, value in vars(rol).items():
            setattr(db_rol, var, value) if value else None
        db.add(db_rol)
        db.commit()
    db.refresh(db_rol)
    return db_rol

def delete_rol(db: Session, id: int):
    db_rol = db.query(models.model_rol.Rol).filter(models.model_rol.Rol.Id == id).first()
    if db_rol:
        db.delete(db_rol)
        db.commit()
    return db_rol
