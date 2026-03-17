# backend/app/modules/tareas/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.modules.tareas.schemas import TareaCrear, TareaActualizar, TareaRespuesta
from app.modules.tareas import service

router = APIRouter(prefix="/tareas", tags=["Tareas"])

@router.post("/", response_model=TareaRespuesta, status_code=201)
def crear_tarea(
    datos: TareaCrear,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.crear_tarea(db, datos, psicologo_id=usuario["sub"])

@router.get("/", response_model=List[TareaRespuesta])
def listar_tareas(
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.listar_tareas(db, psicologo_id=usuario["sub"])

@router.get("/paciente/{paciente_id}", response_model=List[TareaRespuesta])
def listar_tareas_paciente(
    paciente_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.listar_tareas_paciente(db, paciente_id, psicologo_id=usuario["sub"])

@router.get("/{tarea_id}", response_model=TareaRespuesta)
def obtener_tarea(
    tarea_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.obtener_tarea(db, tarea_id, psicologo_id=usuario["sub"])

@router.patch("/{tarea_id}", response_model=TareaRespuesta)
def actualizar_tarea(
    tarea_id: UUID,
    datos: TareaActualizar,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.actualizar_tarea(db, tarea_id, psicologo_id=usuario["sub"], datos=datos)

@router.delete("/{tarea_id}", status_code=204)
def eliminar_tarea(
    tarea_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    service.eliminar_tarea(db, tarea_id, psicologo_id=usuario["sub"])