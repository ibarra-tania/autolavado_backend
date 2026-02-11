


from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    ''' Clase para modificar los campos de tabla usuarios'''

    nombre: str
    papellido = str
    sapellido = str
    usuario = str
    direccion = str
    correo = str
    telefono = str
    contrasena = str
    estatus = bool
    fecha_registro = datetime
    fecha_modificacion = datetime

class UserCreate(UserBase):
    pass



class UserUpdate(UserBase):
    pass


class User(UserBase):
    Id : int
    class Config:
        orm:mode = True


class UserLogin(BaseModel):
    telefono : Optional[str] = None
    correo : Optional[str] = None
    contrasena : str
