# backend/app/modules/tareas/schemas.py

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TareaCrear(BaseModel):
    paciente_id: UUID
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: Optional[datetime] = None

class TareaActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None
    fecha_limite: Optional[datetime] = None

class TareaRespuesta(BaseModel):
    id: UUID
    psicologo_id: UUID
    paciente_id: UUID
    titulo: str
    descripcion: Optional[str]
    completada: bool
    fecha_limite: Optional[datetime]
    creado_en: datetime

    class Config:
        from_attributes = True