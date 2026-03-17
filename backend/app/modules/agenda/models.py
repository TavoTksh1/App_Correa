# backend/app/modules/agenda/models.py

from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

class Cita(Base):
    __tablename__ = "citas"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    psicologo_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    paciente_id  = Column(UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False)
    titulo       = Column(String(200), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin    = Column(DateTime, nullable=False)
    notas        = Column(Text, nullable=True)
    confirmada   = Column(Boolean, default=False)
    creado_en    = Column(DateTime, default=datetime.utcnow)

    paciente     = relationship("Paciente")