# backend/app/modules/agenda/service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime
from app.modules.agenda.models import Cita
from app.modules.agenda.schemas import CitaCrear, CitaActualizar

def crear_cita(db: Session, datos: CitaCrear, psicologo_id: UUID) -> Cita:
    if datos.fecha_fin <= datos.fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )
    cita = Cita(**datos.model_dump(), psicologo_id=psicologo_id)
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

def listar_citas(db: Session, psicologo_id: UUID) -> list:
    return db.query(Cita).filter(
        Cita.psicologo_id == psicologo_id
    ).order_by(Cita.fecha_inicio).all()

def obtener_cita(db: Session, cita_id: UUID, psicologo_id: UUID) -> Cita:
    cita = db.query(Cita).filter(
        Cita.id == cita_id,
        Cita.psicologo_id == psicologo_id
    ).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    return cita

def actualizar_cita(db: Session, cita_id: UUID, psicologo_id: UUID, datos: CitaActualizar) -> Cita:
    cita = obtener_cita(db, cita_id, psicologo_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(cita, campo, valor)
    db.commit()
    db.refresh(cita)
    return cita

def eliminar_cita(db: Session, cita_id: UUID, psicologo_id: UUID) -> None:
    cita = obtener_cita(db, cita_id, psicologo_id)
    db.delete(cita)
    db.commit()