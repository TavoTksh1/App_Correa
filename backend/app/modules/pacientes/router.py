# backend/app/modules/pacientes/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.modules.pacientes.schemas import PacienteCrear, PacienteRespuesta, SesionCrear, SesionRespuesta
from app.modules.pacientes import service

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=PacienteRespuesta, status_code=201)
def crear_paciente(
    datos: PacienteCrear,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.crear_paciente(db, datos, psicologo_id=usuario["sub"])

@router.get("/", response_model=List[PacienteRespuesta])
def listar_pacientes(
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.listar_pacientes(db, psicologo_id=usuario["sub"])

@router.get("/{paciente_id}", response_model=PacienteRespuesta)
def obtener_paciente(
    paciente_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.obtener_paciente(db, paciente_id, psicologo_id=usuario["sub"])

@router.delete("/{paciente_id}", status_code=204)
def eliminar_paciente(
    paciente_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    service.eliminar_paciente(db, paciente_id, psicologo_id=usuario["sub"])

@router.post("/{paciente_id}/sesiones", response_model=SesionRespuesta, status_code=201)
def crear_sesion(
    paciente_id: UUID,
    datos: SesionCrear,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.crear_sesion(db, paciente_id, psicologo_id=usuario["sub"], datos=datos)

@router.get("/{paciente_id}/sesiones", response_model=List[SesionRespuesta])
def listar_sesiones(
    paciente_id: UUID,
    db: Session = Depends(get_db),
    usuario: dict = Depends(get_current_user)
):
    return service.listar_sesiones(db, paciente_id, psicologo_id=usuario["sub"])