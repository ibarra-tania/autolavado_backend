'''CRUD para la tabla de productos del autolavado'''
from sqlalchemy.orm import Session
import models.model_producto
import schemas.schema_producto


def get_producto(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.model_producto.Producto).offset(skip).limit(limit).all()


def get_producto_by_id(db: Session, id: int):
    return db.query(models.model_producto.Producto).filter(
        models.model_producto.Producto.Id == id
    ).first()


def get_producto_by_nombre(db: Session, nombre: str):
    return db.query(models.model_producto.Producto).filter(
        models.model_producto.Producto.nombre == nombre
    ).first()


def create_producto(db: Session, producto: schemas.schema_producto.ProductoCreate):
    db_producto = models.model_producto.Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        categoria=producto.categoria,
        marca=producto.marca,
        unidad_medida=producto.unidad_medida,
        precio_unitario=producto.precio_unitario,
        stock=producto.stock,
        stock_minimo=producto.stock_minimo,
        estado=producto.estado,
        fecha_registro=producto.fecha_registro,
        fecha_actualizacion=producto.fecha_actualizacion,
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_producto(db: Session, id: int, producto: schemas.schema_producto.ProductoUpdate):
    db_producto = db.query(models.model_producto.Producto).filter(
        models.model_producto.Producto.Id == id
    ).first()
    if db_producto:
        for var, value in vars(producto).items():
            setattr(db_producto, var, value) if value is not None else None
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
    return db_producto


def delete_producto(db: Session, id: int):
    db_producto = db.query(models.model_producto.Producto).filter(
        models.model_producto.Producto.Id == id
    ).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto