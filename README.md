# SaaS Odontología — turnos-odontologia

Sistema de gestión de turnos y agenda de pacientes para consultorios odontológicos
(mercado argentino). Proyecto de la materia Metodología I — prueba de Spec-Driven
Development con OpenSpec y Active Stack: la fundación (Discovery, knowledge-base,
roadmap, reglas) seguida de un ciclo OPSX completo sobre el change
`crear-turno-sin-solapamientos`.

## Stack

- Backend: FastAPI (Python ≥ 3.11) + SQLAlchemy + Pydantic
- Base de datos: PostgreSQL 15 (`postgres:15-alpine`) en Docker
- Migraciones: Alembic
- Tests: pytest (integración contra PostgreSQL real en Docker, nunca SQLite)
- Frontend: React 18 + Vite (esqueleto; el change implementado es backend)

## Prerequisitos

- Docker Desktop con WSL2 activo (la base de datos corre en contenedor)
- Python 3.11+
- Git

## Instalación

```bash
# 1. Clonar y copiar la configuración de entorno (NUNCA commitear .env)
git clone <url-del-repo> turnos-odontologia
cd turnos-odontologia
cp .env.example .env

# 2. Completar .env con valores propios (al menos DB_PASSWORD, SECRET_KEY, ENCRYPTION_KEY)
#    Generar claves: openssl rand -hex 32
#    ⚠ Si el host ya tiene un PostgreSQL en el puerto 5432, usar DB_PORT=5433
#    (por defecto del repo para desarrollo local). El servicio `db` del contenedor
#    sigue escuchando en 5432 internamente.

# 3. Levantar la base de datos (postgres:15-alpine)
docker compose up -d db

# 4. Entorno virtual del backend e instalación (incluye dependencias de dev)
cd backend
python -m venv .venv
.\.venv\Scripts\activate        # Windows
source .venv/bin/activate       # Linux/macOS
pip install -e ".[dev]"

# 5. Aplicar migraciones (esquema + restricción EXCLUDE USING gist)
alembic upgrade head
```

## Correr los tests

```bash
cd backend
python -m pytest tests -v
```

- Todos los tests de solapamiento y concurrencia corren contra el PostgreSQL 15 real
  del contenedor Docker. Deben estar la base arriba y el `.env` configurado.
- La verificación de la salud de la base:

```bash
docker compose exec -T db psql -U $env:DB_USER -d $env:DB_NAME -c "SHOW server_version"
# debe devolver 15.x
```

## Correr la API

```bash
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload
```

Documentación interactiva en http://localhost:8000/docs

O bien todo el stack:

```bash
docker compose up --build
```

## Reproducción (verificación del change)

Evidencia operativa en `docs/opsx/`:

- `explore-crear-turno-sin-solapamientos.md` — fase Explore
- `verify-crear-turno-sin-solapamientos.txt` — corrida completa de la suite (44/44), fase Verify
- `memoria-engram.md` — etapa 7, consulta real a la memoria persistente

Referencias: `AGENTS.md` (reglas del proyecto), `CHANGES.md` (roadmap),
`knowledge-base/` (10 archivos canónicos), `openspec/` (specs y changes archivados).