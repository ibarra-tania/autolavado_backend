from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, crud.crud_vehiculo, schemas.schema_vehiculo, models.model_vehiculos, models.model_usuario
from typing import List
from config.security import get_current_user


vehiculo = APIRouter()

models.model_vehiculos.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@vehiculo.get("/vehiculo/", response_model=List[schemas.schema_vehiculo.Vehiculo], tags=["Vehiculos"])
async def read_vehiculo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    return crud.crud_vehiculo.get_vehiculo(db=db, skip=skip, limit=limit)


@vehiculo.post("/vehiculo/", response_model=schemas.schema_vehiculo.Vehiculo, tags=["Vehiculos"])
def create_vehiculo(
    vehiculo: schemas.schema_vehiculo.VehiculoCreate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_vehiculo = crud.crud_vehiculo.get_vehiculo_by_nombre(db, placas=vehiculo.placas)
    if db_vehiculo:
        raise HTTPException(status_code=400, detail="Vehiculo existente intenta nuevamente")
    return crud.crud_vehiculo.create_vehiculo(db=db, vehiculo=vehiculo)


@vehiculo.put("/vehiculo/{id}", response_model=schemas.schema_vehiculo.Vehiculo, tags=["Vehiculos"])
async def update_vehiculo(
    id: int,
    vehiculo: schemas.schema_vehiculo.VehiculoUpdate,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_vehiculo = crud.crud_vehiculo.update_vehiculo(db=db, id=id, vehiculo=vehiculo)
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculos no existe, no actualizado")
    return db_vehiculo


@vehiculo.delete("/vehiculo/{id}", response_model=schemas.schema_vehiculo.Vehiculo, tags=["Vehiculos"])
async def delete_vehiculo(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_vehiculo = crud.crud_vehiculo.delete_vehiculo(db=db, id=id)
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="El vehiculo no existe, no se pudo eliminar")
    return db_vehiculo