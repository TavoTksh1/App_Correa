from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.schemas import UsuarioRegistro, UsuarioLogin, UsuarioRespuesta, Token
from app.modules.auth import service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registro", response_model=UsuarioRespuesta, status_code=201)
def registro(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    return service.registrar_usuario(db, datos)

@router.post("/login", response_model=Token)
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    return service.login_usuario(db, datos)
