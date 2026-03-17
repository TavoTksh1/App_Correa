# backend/app/modules/agenda/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.modules.agenda.schemas import CitaCrear, CitaActualizar, CitaRespuesta
from app.modules.agenda import service

router = APIRouter(prefix="/agenda", tags=["Agenda"])

@router.post("/", response_model=CitaRespuesta, status_code=201)
def crear_cita(
    datos: CitaCrear,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.crear_cita(db, datos, psicologo_id=usuario["sub"])

@router.get("/", response_model=List[CitaRespuesta])
def listar_citas(
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.listar_citas(db, psicologo_id=usuario["sub"])

@router.get("/{cita_id}", response_model=CitaRespuesta)
def obtener_cita(
    cita_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.obtener_cita(db, cita_id, psicologo_id=usuario["sub"])

@router.patch("/{cita_id}", response_model=CitaRespuesta)
def actualizar_cita(
    cita_id: UUID,
    datos: CitaActualizar,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.actualizar_cita(db, cita_id, psicologo_id=usuario["sub"], datos=datos)

@router.delete("/{cita_id}", status_code=204)
def eliminar_cita(
    cita_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    service.eliminar_cita(db, cita_id, psicologo_id=usuario["sub"])