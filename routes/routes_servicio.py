from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, crud.crud_servicio, schemas.schema_servicio, models.model_servicio, models.model_usuario
from typing import List
from config.security import get_current_user


servicio = APIRouter()

models.model_servicio.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@servicio.get("/servicio/", response_model=List[schemas.schema_servicio.Servicio], tags=["Servicios"])
async def read_servicio(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    return crud.crud_servicio.get_servicio(db=db, skip=skip, limit=limit)


@servicio.post("/servicio/", response_model=schemas.schema_servicio.Servicio, tags=["Servicios"])
def create_servicio(
    servicio: schemas.schema_servicio.ServicioCreate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_servicio = crud.crud_servicio.get_servicio_by_nombre(db, nombre=servicio.nombre)
    if db_servicio:
        raise HTTPException(status_code=400, detail="Servicio existente intenta nuevamente")
    return crud.crud_servicio.create_servicio(db=db, servicio=servicio)


@servicio.put("/servicio/{id}", response_model=schemas.schema_servicio.Servicio, tags=["Servicios"])
async def update_servicio(
    id: int,
    servicio: schemas.schema_servicio.ServicioUpdate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_servicio = crud.crud_servicio.update_servicio(db=db, id=id, servicio=servicio)
    if db_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no existe, no actualizado")
    return db_servicio


@servicio.delete("/servicio/{id}", response_model=schemas.schema_servicio.Servicio, tags=["Servicios"])
async def delete_servicio(
    id: int,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_servicio = crud.crud_servicio.delete_servicio(db=db, id=id)
    if db_servicio is None:
        raise HTTPException(status_code=404, detail="El Servicio no existe, no se pudo eliminar")
    return db_servicio