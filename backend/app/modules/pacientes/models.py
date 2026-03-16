# backend/app/modules/pacientes/models.py

from sqlalchemy import Column, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    psicologo_id   = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    nombre         = Column(String(100), nullable=False)
    apellido       = Column(String(100), nullable=False)
    fecha_nac      = Column(Date, nullable=True)
    telefono       = Column(String(20), nullable=True)
    email          = Column(String(255), nullable=True)
    motivo_consulta= Column(Text, nullable=True)
    creado_en      = Column(DateTime, default=datetime.utcnow)

    sesiones       = relationship("Sesion", back_populates="paciente", cascade="all, delete")

class Sesion(Base):
    __tablename__ = "sesiones"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id  = Column(UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False)
    fecha        = Column(DateTime, nullable=False)
    notas        = Column(Text, nullable=True)
    diagnostico  = Column(Text, nullable=True)
    creado_en    = Column(DateTime, default=datetime.utcnow)

    paciente     = relationship("Paciente", back_populates="sesiones")