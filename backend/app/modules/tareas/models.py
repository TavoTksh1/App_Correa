# backend/app/modules/tareas/models.py

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

class Tarea(Base):
    __tablename__ = "tareas"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    psicologo_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    paciente_id  = Column(UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False)
    titulo       = Column(String(200), nullable=False)
    descripcion  = Column(Text, nullable=True)
    completada   = Column(Boolean, default=False)
    fecha_limite = Column(DateTime, nullable=True)
    creado_en    = Column(DateTime, default=datetime.utcnow)

    paciente     = relationship("Paciente")