# backend/app/modules/pacientes/schemas.py

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

class PacienteCrear(BaseModel):
    nombre: str
    apellido: str
    fecha_nac: Optional[date] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    motivo_consulta: Optional[str] = None

class PacienteRespuesta(BaseModel):
    id: UUID
    psicologo_id: UUID
    nombre: str
    apellido: str
    fecha_nac: Optional[date]
    telefono: Optional[str]
    email: Optional[str]
    motivo_consulta: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True

class SesionCrear(BaseModel):
    fecha: datetime
    notas: Optional[str] = None
    diagnostico: Optional[str] = None

class SesionRespuesta(BaseModel):
    id: UUID
    paciente_id: UUID
    fecha: datetime
    notas: Optional[str]
    diagnostico: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True