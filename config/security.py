"""Configuracion de seguridad JWT"""

import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import config.db

# ─── Configuración ────────────────────────────────────────────────────────────
SECRET_KEY = "autolavado_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ─── Utilidades ───────────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Verifica si la contraseña plana coincide con el hash'''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    '''Genera el hash bcrypt de una contraseña'''
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    '''Crea un token JWT con los datos proporcionados'''
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ─── Dependency: usuario actual autenticado ───────────────────────────────────
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''Dependencia que valida el token JWT y retorna el usuario actual'''
    import models.model_usuario  # import aquí para evitar circular imports

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(models.model_usuario.Usuario).filter(
        models.model_usuario.Usuario.correo_electronico == correo
    ).first()

    if usuario is None:
        raise credentials_exception
    if not usuario.estado:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    return usuario