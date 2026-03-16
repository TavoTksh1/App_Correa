from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre    = Column(String(100), nullable=False)
    apellido  = Column(String(100), nullable=False)
    email     = Column(String(255), unique=True, nullable=False, index=True)
    password  = Column(String(255), nullable=False)
    es_activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
