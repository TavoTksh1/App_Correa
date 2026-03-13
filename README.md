<div align="center">

# Ψ PsicoApp

**Plataforma clínica digital para psicólogos**

*Historia clínica inteligente · Diagnóstico asistido por IA*

[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?style=flat-square&logo=flutter)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql)](https://postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-f59e0b?style=flat-square)]()

</div>

---

## ¿Qué es PsicoApp?

PsicoApp es una aplicación móvil (iOS + Android) diseñada exclusivamente para psicólogos clínicos. Combina historia clínica digital, gestión de pacientes y un asistente de IA que clasifica trastornos según el **CIE-11**, todo en una interfaz intuitiva pensada para el flujo de trabajo clínico real.

---

## Características principales

| Módulo | Descripción |
|---|---|
| 🔐 **Auth** | Registro y login seguro con JWT |
| 🧠 **IA + CIE-11** | Observaciones clínicas → sugerencias de diagnóstico automáticas |
| 📋 **Historia clínica** | Expedientes por paciente adaptados a psicología |
| 📅 **Agenda** | Gestión de citas y recordatorios |
| ✅ **Tareas** | Asignación de actividades terapéuticas al paciente |

---

## Stack tecnológico

```
┌─────────────────────────────────────────┐
│          Flutter (iOS + Android)         │
│   Módulos: Auth · Pacientes · CIE-11    │
│            Agenda · Tareas              │
├─────────────────────────────────────────┤
│         FastAPI (Python 3.11+)           │
│        REST API · JWT · CIE-11 IA       │
├──────────────────────┬──────────────────┤
│      PostgreSQL      │      Redis       │
└──────────────────────┴──────────────────┘
```

**Frontend (Flutter)**
- `flutter_bloc` — gestión de estado
- `dio` — cliente HTTP
- `go_router` — navegación
- `flutter_secure_storage` — tokens seguros

**Backend (FastAPI)**
- `sqlalchemy` + `alembic` — ORM y migraciones
- `pydantic` — validación de datos
- `python-jose` — JWT

---

## Estructura del proyecto

```
psicoapp/
├── mobile/                    # Flutter App
│   └── lib/
│       ├── core/              # Tema, constantes, red
│       ├── modules/
│       │   ├── auth/
│       │   ├── pacientes/
│       │   ├── cie11/
│       │   ├── agenda/
│       │   └── tareas/
│       └── shared/
│
└── backend/                   # FastAPI
    └── app/
        ├── core/
        ├── modules/
        │   ├── auth/
        │   ├── pacientes/
        │   ├── cie11/
        │   ├── agenda/
        │   └── tareas/
        └── shared/
```

---

## Roadmap

- [x] Definición de arquitectura
- [x] Diseño de base de datos
- [ ] Autenticación JWT
- [ ] CRUD de pacientes
- [ ] Historia clínica
- [ ] Integración CIE-11 con IA
- [ ] Agenda y notificaciones
- [ ] Exportación de expediente en PDF

---

## Estado del proyecto

Este repositorio forma parte de un proyecto en desarrollo activo. El código no está disponible públicamente — este README tiene fines de portafolio.

Para consultas sobre el proyecto, puedes escribir a través de los canales de contacto del perfil.

---

<div align="center">

Hecho con ❤️ para la salud mental

*PsicoApp — Clínica digital*

</div>
