import models.model_usuario
import schemas.schema_usuario
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
import models, schemas


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_usuario(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.model_usuario.Usuario).offset(skip).limit(limit).all()

def get_usuario_by_nombre(db: Session, nombre: str):
    return db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.nombre == nombre).first()

def create_usuario(db:Session, usuario: schemas.schema_usuario.UsuarioCreate):
    password_plana = str(usuario.contrasena).strip()
    hashed_password = pwd_context.hash(password_plana)
    db_usuario = models.model_usuario.Usuario(
        rol_Id = usuario.rol_Id,
        nombre = usuario.nombre,
        primer_apellido = usuario.primer_apellido,
        segundo_apellido = usuario.segundo_apellido,
        direccion = usuario.direccion,
        correo_electronico = usuario.correo_electronico,
        numero_telefono = usuario.numero_telefono,
        contrasena = hashed_password,
        estado = usuario.estado,
        fecha_registro = usuario.fecha_registro,
        fecha_actualizacion = usuario.fecha_actualizacion
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, id: int, usuario: schemas.schema_usuario.UsuarioUpdate):
    db_usuario = db.query(models.model_usuario.Usuario).filter(
        models.model_usuario.Usuario.Id == id
    ).first()
    
    if not db_usuario:
        return None  # Retorna None explícitamente si no existe
    
    for var, value in vars(usuario).items():
        if value is not None:
            setattr(db_usuario, var, value)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, id: int):
    db_usuario = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

    def authenticat_user(db: Session, email_o_tel: str, contrasena: str):
        usuario = db.query(models.model_usuario.Usuario).filter(
            (models.model_usuario.Usuario.correo_electronico == email_o_tel) |
            (models.model_usuario.Usuario.numero_telefono == email_o_tel)
        ).first()

        if not usuario:
            return None
        try:
            if not pwd_context.verify(contrasena, usuario.contrasena):
                return None
        except UnknownHashError:
            print(f"ERROR: El usuario {email_o_tel} tiene un hash inválidp en la BD.")
            return None
        return usuario