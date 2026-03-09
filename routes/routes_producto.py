'''Rutas CRUD para productos del autolavado — protegidas con JWT'''
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import config.db
import crud.crud_producto
import schemas.schema_producto
import models.model_producto
import models.model_usuario
from config.security import get_current_user

producto = APIRouter()

models.model_producto.Base.metadata.create_all(bind=config.db.engine)


def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── GET ──────────────────────────────────────────────────────────────────────
@producto.get(
    "/producto/",
    response_model=List[schemas.schema_producto.Producto],
    tags=["Productos"]
)
async def read_productos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user),  # 🔒
):
    return crud.crud_producto.get_producto(db=db, skip=skip, limit=limit)


# ─── POST ─────────────────────────────────────────────────────────────────────
@producto.post(
    "/producto/",
    response_model=schemas.schema_producto.Producto,
    tags=["Productos"]
)
def create_producto(
    producto: schemas.schema_producto.ProductoCreate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user),  # 🔒
):
    db_producto = crud.crud_producto.get_producto_by_nombre(db, nombre=producto.nombre)
    if db_producto:
        raise HTTPException(status_code=400, detail="Producto existente, intenta con otro nombre")
    return crud.crud_producto.create_producto(db=db, producto=producto)


# ─── PUT ──────────────────────────────────────────────────────────────────────
@producto.put(
    "/producto/{id}",
    response_model=schemas.schema_producto.Producto,
    tags=["Productos"]
)
async def update_producto(
    id: int,
    producto: schemas.schema_producto.ProductoUpdate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user),  # 🔒
):
    db_producto = crud.crud_producto.update_producto(db=db, id=id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no existe, no actualizado")
    return db_producto


# ─── DELETE ───────────────────────────────────────────────────────────────────
@producto.delete(
    "/producto/{id}",
    response_model=schemas.schema_producto.Producto,
    tags=["Productos"]
)
async def delete_producto(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user),  # 🔒
):
    db_producto = crud.crud_producto.delete_producto(db=db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="El Producto no existe, no se pudo eliminar")
    return db_producto