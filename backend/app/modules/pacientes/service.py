# backend/app/modules/pacientes/service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.modules.pacientes.models import Paciente, Sesion
from app.modules.pacientes.schemas import PacienteCrear, SesionCrear

def crear_paciente(db: Session, datos: PacienteCrear, psicologo_id: UUID) -> Paciente:
    paciente = Paciente(**datos.model_dump(), psicologo_id=psicologo_id)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

def listar_pacientes(db: Session, psicologo_id: UUID) -> list:
    return db.query(Paciente).filter(Paciente.psicologo_id == psicologo_id).all()

def obtener_paciente(db: Session, paciente_id: UUID, psicologo_id: UUID) -> Paciente:
    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id,
        Paciente.psicologo_id == psicologo_id
    ).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    return paciente

def eliminar_paciente(db: Session, paciente_id: UUID, psicologo_id: UUID) -> None:
    paciente = obtener_paciente(db, paciente_id, psicologo_id)
    db.delete(paciente)
    db.commit()

def crear_sesion(db: Session, paciente_id: UUID, psicologo_id: UUID, datos: SesionCrear) -> Sesion:
    obtener_paciente(db, paciente_id, psicologo_id)
    sesion = Sesion(**datos.model_dump(), paciente_id=paciente_id)
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion

def listar_sesiones(db: Session, paciente_id: UUID, psicologo_id: UUID) -> list:
    obtener_paciente(db, paciente_id, psicologo_id)
    return db.query(Sesion).filter(Sesion.paciente_id == paciente_id).all()