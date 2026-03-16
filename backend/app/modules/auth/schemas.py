from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UsuarioRegistro(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioRespuesta(BaseModel):
    id: UUID
    nombre: str
    apellido: str
    email: str
    es_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
