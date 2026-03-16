#!/bin/bash
# Ejecutar desde: ~/AppCorrea/backend
# Uso: bash setup_backend.sh

echo "🚀 Configurando backend de PsicoApp..."

# ── requirements.txt ──────────────────────────────
cat > requirements.txt << 'PYEOF'
fastapi==0.111.0
uvicorn==0.30.0
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
httpx==0.27.0
openai==1.30.1
python-dotenv==1.0.1
email-validator==2.1.1
PYEOF

# ── .env.example ──────────────────────────────────
cat > .env.example << 'PYEOF'
DATABASE_URL=postgresql://usuario:password@host.rds.amazonaws.com:5432/psicoapp
SECRET_KEY=cambia_esto_por_una_clave_larga_y_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_API_KEY=sk-placeholder
PYEOF

# ── app/core/config.py ────────────────────────────
cat > app/core/config.py << 'PYEOF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
PYEOF

# ── app/core/database.py ──────────────────────────
cat > app/core/database.py << 'PYEOF'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
PYEOF

# ── app/core/security.py ──────────────────────────
cat > app/core/security.py << 'PYEOF'
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
PYEOF

# ── app/shared/dependencies.py ────────────────────
cat > app/shared/dependencies.py << 'PYEOF'
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    return payload
PYEOF

# ── app/modules/auth/models.py ────────────────────
cat > app/modules/auth/models.py << 'PYEOF'
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
PYEOF

# ── app/modules/auth/schemas.py ───────────────────
cat > app/modules/auth/schemas.py << 'PYEOF'
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UsuarioRegistro(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioRespuesta(BaseModel):
    id: UUID
    nombre: str
    apellido: str
    email: str
    es_activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
PYEOF

# ── app/modules/auth/service.py ───────────────────
cat > app/modules/auth/service.py << 'PYEOF'
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
PYEOF

# ── app/modules/auth/router.py ────────────────────
cat > app/modules/auth/router.py << 'PYEOF'
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
PYEOF

# ── app/main.py ───────────────────────────────────
cat > app/main.py << 'PYEOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.router import router as auth_router

app = FastAPI(
    title="PsicoApp API",
    description="Backend clínico para psicólogos",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "PsicoApp API corriendo"}
PYEOF

# ── alembic/env.py ────────────────────────────────
cat > alembic/env.py << 'PYEOF'
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core.database import Base
from app.modules.auth.models import Usuario

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
PYEOF

# ── alembic.ini ───────────────────────────────────
cat > alembic.ini << 'PYEOF'
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://psicoapp_admin:psicopassword123@psicoapp-db.c8oqmpiy0vyd.us-east-1.rds.amazonaws.com:5432/psicoapp

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
PYEOF

echo "✅ Todos los archivos listos"
echo ""
echo "Próximos pasos:"
echo "  alembic revision --autogenerate -m 'create usuarios table'"
echo "  alembic upgrade head"
echo "  uvicorn app.main:app --reload"