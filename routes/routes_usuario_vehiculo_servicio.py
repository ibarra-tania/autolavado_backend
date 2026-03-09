'''Rutas para UsuarioVehiculoServicio — CRUD protegido con JWT
   + GET con JOIN para reporte detallado por fecha'''
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from typing import List
from datetime import date

import config.db
import crud.crud_usuario_vehiculo_servicio
import schemas.schema_usuario_vehiculo_servicio
import schemas.schema_reporte_uvs
import models.model_usuario_vehiculo_servicio
import models.model_usuario
import models.model_servicio
import models.model_vehiculos
from config.security import get_current_user

usuario_vehiculo_servicio = APIRouter()

models.model_usuario_vehiculo_servicio.Base.metadata.create_all(bind=config.db.engine)


def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── GET lista general ────────────────────────────────────────────────────────
@usuario_vehiculo_servicio.get(
    "/usuario_vehiculo_servicio/",
    response_model=List[schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio],
    tags=["Vehiculo Servicios"]
)
async def read_usuario_vehiculo_servicios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user),
):
    return crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio(
        db=db, skip=skip, limit=limit
    )


# ─── GET reporte con JOIN por fecha ───────────────────────────────────────────
@usuario_vehiculo_servicio.get(
    "/usuario_vehiculo_servicio/reporte/{fecha}",
    response_model=List[schemas.schema_reporte_uvs.ReporteUVSPorFecha],
    tags=["Vehiculo Servicios"],
    summary="Reporte detallado por fecha",
    description=(
        "Retorna el detalle completo de los servicios registrados en una fecha específica. "
    ),
)
async def get_reporte_por_fecha(
    fecha: date,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user),
):
    # Alias para diferenciar cajero y operativo (ambos vienen de tbb_usuarios)
    Cajero = aliased(models.model_usuario.Usuario, name="cajero")
    Operativo = aliased(models.model_usuario.Usuario, name="operativo")

    UVS = models.model_usuario_vehiculo_servicio.UsuarioVehiculoServicio
    Servicio = models.model_servicio.Servicio
    Vehiculo = models.model_vehiculos.Vehiculo

    resultados = (
        db.query(
            # Nombre completo cajero
            func.concat(Cajero.nombre, " ", Cajero.primer_apellido, " ", Cajero.segundo_apellido)
            .label("cajero_nombre_completo"),

            # Nombre completo operativo
            func.concat(Operativo.nombre, " ", Operativo.primer_apellido, " ", Operativo.segundo_apellido)
            .label("operativo_nombre_completo"),

            # Servicio
            Servicio.nombre.label("nombre_servicio"),
            Servicio.costo.label("costo_servicio"),
            Servicio.descripcion.label("descripcion_servicio"),

            # Vehículo
            Vehiculo.placas.label("placas"),
            Vehiculo.marca.label("marca"),
            Vehiculo.modelo.label("modelo"),
            Vehiculo.color.label("color"),

            # Registro
            UVS.fecha.label("fecha"),
            UVS.hora.label("hora"),
            UVS.descuento.label("descuento"),

            # Costo total = costo - (costo * descuento / 100)
            (Servicio.costo - (Servicio.costo * UVS.descuento / 100.0))
            .label("costo_total"),

            UVS.estatus.label("estatus"),
        )
        .join(Cajero, UVS.cajero_Id == Cajero.Id)
        .join(Operativo, UVS.operativo_Id == Operativo.Id)
        .join(Servicio, UVS.servicio_Id == Servicio.Id)
        .join(Vehiculo, UVS.vehiculo_Id == Vehiculo.Id)
        .filter(UVS.fecha == fecha)
        .all()
    )

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron registros para la fecha {fecha}"
        )

    # Convertir las filas SQLAlchemy a dicts para Pydantic
    return [
        schemas.schema_reporte_uvs.ReporteUVSPorFecha(
            cajero_nombre_completo=r.cajero_nombre_completo,
            operativo_nombre_completo=r.operativo_nombre_completo,
            nombre_servicio=r.nombre_servicio,
            costo_servicio=r.costo_servicio,
            descripcion_servicio=r.descripcion_servicio,
            placas=r.placas,
            marca=r.marca,
            modelo=r.modelo,
            color=r.color,
            fecha=r.fecha,
            hora=r.hora,
            descuento=r.descuento,
            costo_total=round(r.costo_total, 2),
            estatus=r.estatus.value if hasattr(r.estatus, "value") else r.estatus,
        )
        for r in resultados
    ]


# ─── POST ─────────────────────────────────────────────────────────────────────
@usuario_vehiculo_servicio.post(
    "/usuario_vehiculo_servicio/",
    response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    tags=["Vehiculo Servicios"]
)
def create_usuario_vehiculo_servicio(
    usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioCreate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user),
):
    db_uvs = crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio_by_nombre(
        db, fecha=usuario_vehiculo_servicio.fecha, hora=usuario_vehiculo_servicio.hora
    )
    if db_uvs:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un registro con esa fecha y hora, intenta nuevamente"
        )
    return crud.crud_usuario_vehiculo_servicio.create_usuario_vehiculo_servicio(
        db=db, usuario_vehiculo_servicio=usuario_vehiculo_servicio
    )


# ─── PUT ──────────────────────────────────────────────────────────────────────
@usuario_vehiculo_servicio.put(
    "/usuario_vehiculo_servicio/{id}",
    response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    tags=["Vehiculo Servicios"]
)
async def update_usuario_vehiculo_servicio(
    id: int,
    usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user),
):
    db_uvs = crud.crud_usuario_vehiculo_servicio.update_usuario_vehiculo_servicio(
        db=db, id=id, usuario_vehiculo_servicio=usuario_vehiculo_servicio
    )
    if db_uvs is None:
        raise HTTPException(status_code=404, detail="Registro no existe, no actualizado")
    return db_uvs


# ─── DELETE ───────────────────────────────────────────────────────────────────
@usuario_vehiculo_servicio.delete(
    "/usuario_vehiculo_servicio/{id}",
    response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    tags=["Vehiculo Servicios"]
)
async def delete_usuario_vehiculo_servicio(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user),
):
    db_uvs = crud.crud_usuario_vehiculo_servicio.delete_usuario_vehiculo_servicio(db=db, id=id)
    if db_uvs is None:
        raise HTTPException(
            status_code=404,
            detail="El registro no existe, no se pudo eliminar"
        )
    return db_uvs