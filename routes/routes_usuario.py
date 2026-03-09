from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm  # ✅ Corregido: faltaba la 't' en Request
from sqlalchemy.orm import Session
from typing import List
import config.db
import crud.crud_usuario
import schemas.schema_usuario
import models.model_usuario
from config.security import get_current_user, verify_password, create_access_token  # ✅ Faltaban imports


usuario = APIRouter()

models.model_usuario.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── GET ──────────────────────────────────────────────────────────────────────
@usuario.get("/usuario/", response_model=List[schemas.schema_usuario.Usuario], tags=["Users"])
async def read_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒 protegido
):
    return crud.crud_usuario.get_usuario(db=db, skip=skip, limit=limit)

# ─── POST crear usuario ───────────────────────────────────────────────────────
@usuario.post("/usuario/", response_model=schemas.schema_usuario.Usuario, tags=["Users"])
def create_usuario(
    usuario: schemas.schema_usuario.UsuarioCreate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒 protegido
):
    db_usuario = crud.crud_usuario.get_usuario_by_nombre(db, nombre=usuario.nombre)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuario existente intenta nuevamente")
    return crud.crud_usuario.create_usuario(db=db, usuario=usuario)

# ─── PUT ──────────────────────────────────────────────────────────────────────
@usuario.put("/usuario/{id}", response_model=schemas.schema_usuario.Usuario, tags=["Users"])
async def update_usuario(
    id: int,
    usuario: schemas.schema_usuario.UsuarioUpdate,
    db: Session = Depends(get_db),
    #current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒 protegido
):
    db_usuario = crud.crud_usuario.update_usuario(db=db, id=id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no existe, no actualizado")
    return db_usuario

# ─── DELETE ───────────────────────────────────────────────────────────────────
@usuario.delete("/usuario/{id}", response_model=schemas.schema_usuario.Usuario, tags=["Users"])
async def delete_usuario(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.model_usuario.Usuario = Depends(get_current_user)  # 🔒 protegido
):
    db_usuario = crud.crud_usuario.delete_usuario(db=db, id=id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="El Usuario no existe, no se pudo eliminar")
    return db_usuario

# ─── LOGIN (ruta pública, sin protección) ────────────────────────────────────
@usuario.post("/login", tags=["🔐 Autenticación"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # ✅ Corregido orden de parámetros
    db: Session = Depends(get_db)
):
    # Buscar usuario por correo
    db_usuario = db.query(models.model_usuario.Usuario).filter(
        models.model_usuario.Usuario.correo_electronico == form_data.username
    ).first()

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # ✅ Corregido: UNAUTHORIXED → UNAUTHORIZED
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, db_usuario.contrasena):  # ✅ Corregido: form_data:password → form_data.password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not db_usuario.estado:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    access_token = create_access_token(data={"sub": db_usuario.correo_electronico})  # ✅ Corregido: "sub": faltaba el valor

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": db_usuario.Id,
            "nombre": f"{db_usuario.nombre} {db_usuario.primer_apellido}",
            "correo": db_usuario.correo_electronico,
            "rol_id": db_usuario.rol_Id
        }
    }