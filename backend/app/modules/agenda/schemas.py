# backend/app/modules/agenda/schemas.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CitaCrear(BaseModel):
    paciente_id: UUID
    titulo: str
    fecha_inicio: datetime
    fecha_fin: datetime
    notas: Optional[str] = None

class CitaActualizar(BaseModel):
    titulo: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    notas: Optional[str] = None
    confirmada: Optional[bool] = None

class CitaRespuesta(BaseModel):
    id: UUID
    psicologo_id: UUID
    paciente_id: UUID
    titulo: str
    fecha_inicio: datetime
    fecha_fin: datetime
    notas: Optional[str]
    confirmada: bool
    creado_en: datetime

    class Config:
        from_attributes = True