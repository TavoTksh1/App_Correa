# backend/app/modules/tareas/service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.modules.tareas.models import Tarea
from app.modules.tareas.schemas import TareaCrear, TareaActualizar

def crear_tarea(db: Session, datos: TareaCrear, psicologo_id: UUID) -> Tarea:
    tarea = Tarea(**datos.model_dump(), psicologo_id=psicologo_id)
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea

def listar_tareas(db: Session, psicologo_id: UUID) -> list:
    return db.query(Tarea).filter(
        Tarea.psicologo_id == psicologo_id
    ).order_by(Tarea.creado_en.desc()).all()

def listar_tareas_paciente(db: Session, paciente_id: UUID, psicologo_id: UUID) -> list:
    return db.query(Tarea).filter(
        Tarea.paciente_id == paciente_id,
        Tarea.psicologo_id == psicologo_id
    ).order_by(Tarea.creado_en.desc()).all()

def obtener_tarea(db: Session, tarea_id: UUID, psicologo_id: UUID) -> Tarea:
    tarea = db.query(Tarea).filter(
        Tarea.id == tarea_id,
        Tarea.psicologo_id == psicologo_id
    ).first()
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return tarea

def actualizar_tarea(db: Session, tarea_id: UUID, psicologo_id: UUID, datos: TareaActualizar) -> Tarea:
    tarea = obtener_tarea(db, tarea_id, psicologo_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)
    db.commit()
    db.refresh(tarea)
    return tarea

def eliminar_tarea(db: Session, tarea_id: UUID, psicologo_id: UUID) -> None:
    tarea = obtener_tarea(db, tarea_id, psicologo_id)
    db.delete(tarea)
    db.commit()