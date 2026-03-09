from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.crud_rol, config.db, schemas.schema_rol, models.model_rol, models.model_usuario
from typing import List
from config.security import get_current_user


rol = APIRouter()

models.model_rol.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@rol.get("/rol/", response_model=List[schemas.schema_rol.Rol], tags=["Rols"])
async def read_rols(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    return crud.crud_rol.get_rol(db=db, skip=skip, limit=limit)


@rol.post("/rol/", response_model=schemas.schema_rol.Rol, tags=["Rols"])
def create_rol(
    rol: schemas.schema_rol.RolCreate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_rol = crud.crud_rol.get_rol_by_nombre(db, nombre_rol=rol.nombre_rol)
    if db_rol:
        raise HTTPException(status_code=400, detail="Rol existente intenta nuevamente")
    return crud.crud_rol.create_rol(db=db, rol=rol)


@rol.put("/rol/{id}", response_model=schemas.schema_rol.Rol, tags=["Rols"])
async def update_rol(
    id: int,
    rol: schemas.schema_rol.RolUpdate,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_rol = crud.crud_rol.update_rol(db=db, id=id, rol=rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no existe, no actualizado")
    return db_rol


@rol.delete("/rol/{id}", response_model=schemas.schema_rol.Rol, tags=["Rols"])
async def delete_rol(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒
):
    db_rol = crud.crud_rol.delete_rol(db=db, id=id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="El Rol no existe, no se pudo eliminar")
    return db_rol