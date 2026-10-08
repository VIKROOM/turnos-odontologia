# Tasks

## 1. Gate de prerequisitos

- [x] 1.1 Verificar que `docker` está en PATH y el motor responde: ejecutar `docker --version` y `docker version --json` y confirmar que el Server reporta OK. Si falla o el motor está apagado, el apply se declara **BLOQUEADO** y se reporta al orquestador sin continuar (no crear archivos de infraestructura).
- [x] 1.2 Verificar WSL2 operativo: en Windows ejecutar `wsl --status` y `wsl -l --quiet` y confirmar una distro instalada (Ubuntu). Si no hay distro, reportar bloqueo con la instrucción `wsl --install --no-distribution` como guía, sin saltarse el control. Criterio de éxito: `docker version --json` Server OK + distro WSL listada.

## 2. Estructura de monorepo

- [x] 2.1 Crear la estructura base del monorepo: `backend/app/{domain,application,infrastructure,api}`, `frontend/src/{pages,components,lib}`, `docker/`, `docs/` y `openspec/specs/`, con `.gitkeep` (y `__init__.py` donde corresponda para que los paquetes importen). Verificación: `Get-ChildItem -Recurse` muestra todos los directorios y no existe ninguna importación en `domain/` que apunte a `infrastructure/`.

## 3. Docker Compose y base PostgreSQL

- [x] 3.1 Crear `docker-compose.yml` (en `docker/` o raíz) con los servicios `db` (imagen `postgres:15-alpine`, volumen nombrado, healthcheck `pg_isready`, port bind de desarrollo), `backend` (build sobre Python 3.11, command de uvicorn, env desde `.env`, `depends_on: db` healthy) y `frontend` (build React 18/Vite, depende de backend). Verificación: `docker compose config` valida el YAML sin errores.
- [x] 3.2 Crear `.env.example` con `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`, `DATABASE_URL` (apuntando a `db`, no a localhost), `SECRET_KEY`, `ENCRYPTION_KEY` (variables separadas, con placeholder `openssl rand -hex 32` documentado), `TOKEN_TTL_HOURS`, `COOKIE_SECURE`, `APP_ENV` y `LOG_LEVEL`. Agregar `.env` a `.gitignore`. Verificación: `.env.example` contiene esas variables sin valores reales y `git check-ignore .env` responde que está ignorado.
- [x] 3.3 Levantar la base: ejecutar `docker compose up -d db` desde el repo (en Windows vía Docker Desktop/WSL2) y verificar que `docker compose ps` muestra `db` con estado **healthy** (o `pg_isready` respondiendo). Criterio base real lista para DD-10.

## 4. Backend: esqueleto + tooling

- [x] 4.1 Crear el esqueleto del backend: `pyproject.toml` (deps `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic-settings`; dev deps `pytest`, `alembic`), `app/__init__.py`, directorio `app/config/` con settings que leen `.env` (sin valores hardcodeados). Verificación: `docker compose up -d db` + `python -c "import app"` desde `backend/` funciona y los settings leen las env vars de `.env`.
- [x] 4.2 Configurar tooling de backend: `pytest` (test de sanidad con 0 tests o un smoke test trivial) y `alembic` (sólo configuración `alembic.ini`/env.py, SIN escribir la primera migración — eso es C-02). Verificación: `pytest` desde `backend/` arranca y reporta 0 tests (o el smoke test en verde), y `alembic` responde al comando `alembic --version`.
- [x] 4.3 Verificar la dirección de capas (spec *Estructura de monorepo*): correr una búsqueda de imports en `backend/app/domain/` y confirmar cero referencias a `infrastructure/`. Si aparece alguna, corregir antes de pasar al frontend.

## 5. Frontend: esqueleto + tooling

- [x] 5.1 Crear el esqueleto Vite + React 18 + TypeScript: `frontend/` con `package.json`, `vite.config.ts`, `tsconfig.json` estricto (`strict: true`, `noImplicitAny: true`, sin `any`), `index.html` y `src/main.tsx` mínimo. Verificación: `npm install` en `frontend/` termina sin errores y `npm run build` (o `tsc --noEmit`) pasa.
- [x] 5.2 Configurar `eslint` + `vitest` en el frontend: reglas que prohíban `any` explícito y un test de humo de `vitest`. Verificación: `npm run lint` y el test de humo (`npm run test`) pasan; la búsqueda de `: any` en `src/` retorna 0 coincidencias.

## 6. Verificación de integración

- [x] 6.1 Levantar el stack completo con `docker compose up -d` y confirmar que `db`, `backend` y `frontend` quedan arriba en la red interna (`docker compose ps`) y que `backend` se conecta al servicio `db` vía `DATABASE_URL` (log de arranque sin error de conexión).
- [x] 6.2 Verificar los escenarios del spec `foundation/dev-environment`: (a) base aislada `docker compose up -d db` → healthy; (b) stack completo arriba; (c) `.env.example` sin secretos reales y `.env` ignorado; (d) `pytest` y `tsc --noEmit`/`eslint` verdes; (e) `domain/` sin imports de `infrastructure/`. Documentar en el resumen del apply cuál scenario se cumplió y cuál quedó pendiente (si alguno).
- [x] 6.3 Guardar la decisión D1 (Opción A) como puntero accesible: registrar en `docs/decisions/` (o confirmar que `design.md` la contiene) la referencia cruzada a `04_modelo_de_datos.md` y al D1 de `crear-turno-sin-solapamientos`, de modo que C-02 la encuentre sin re-leer todo el change. Verificación: el archivo de decisión existe y cita la Opción A con su justificación.

## Workflow follow-up

- El apply de C-01 es governance **CRITICO**: confirmar aprobación humana antes de aplicar infraestructura.
- Actualizar el checkbox de `[C-01]` en `CHANGES.md` y alinear el scope de C-02/C-05/C-09 con la Opción A (re-scope ya aceptado en D1).
- Tras el apply, `/opsx:archive` sync specs y archiva el change.