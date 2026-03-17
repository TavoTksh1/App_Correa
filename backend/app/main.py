from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.pacientes.router import router as pacientes_router
from app.modules.agenda.router import router as agenda_router

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
app.include_router(pacientes_router)
app.include_router(agenda_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "PsicoApp API corriendo"}
