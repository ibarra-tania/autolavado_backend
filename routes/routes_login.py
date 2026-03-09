'''Ruta de autenticación - Login con JWT'''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import config.db
import config.security
import models.model_usuario

login_router = APIRouter()


def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@login_router.post(
    "/login",
    tags=["🔐 Autenticación"],
    summary="Iniciar sesión",
    description="Ingresa con tu **correo electrónico** y **contraseña** para obtener un token de acceso."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
    Autentica al usuario con correo y contraseña.
    Retorna un token Bearer para usar en los demás endpoints.
    
    - **username**: correo electrónico del usuario
    - **password**: contraseña del usuario
    '''
    # Buscar usuario por correo
    usuario = db.query(models.model_usuario.Usuario).filter(
        models.model_usuario.Usuario.correo_electronico == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not config.security.verify_password(form_data.password, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.estado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo, contacta al administrador"
        )

    # Crear token JWT
    access_token = config.security.create_access_token(
        data={"sub": usuario.correo_electronico},
        expires_delta=timedelta(minutes=config.security.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.Id,
            "nombre": f"{usuario.nombre} {usuario.primer_apellido}",
            "correo": usuario.correo_electronico,
            "rol_id": usuario.rol_Id
        }
    }