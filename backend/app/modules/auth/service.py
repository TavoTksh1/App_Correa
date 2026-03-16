from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.auth.models import Usuario
from app.modules.auth.schemas import UsuarioRegistro, UsuarioLogin
from app.core.security import hash_password, verify_password, create_access_token

def registrar_usuario(db: Session, datos: UsuarioRegistro) -> Usuario:
    existe = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese correo"
        )
    usuario = Usuario(
        nombre=datos.nombre,
        apellido=datos.apellido,
        email=datos.email,
        password=hash_password(datos.password)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def login_usuario(db: Session, datos: UsuarioLogin) -> dict:
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if not usuario or not verify_password(datos.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    token = create_access_token(data={"sub": str(usuario.id), "email": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
