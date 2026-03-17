from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
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

@router.post("/token", response_model=Token)
def token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    datos = UsuarioLogin(email=form.username, password=form.password)
    return service.login_usuario(db, datos)