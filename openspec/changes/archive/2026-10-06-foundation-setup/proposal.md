# Proposal

## Why

El repo es hoy un monorepo de planificación: existe la Knowledge Base, el roadmap y los changes de OpenSpec, pero no hay código, ni infraestructura, ni tooling que pueda ejecutar nada. Todos los changes del camino crítico (C-02 → C-10) presuponen un stack levantado — FastAPI + PostgreSQL 15 + React 18 + Docker Compose (DD-11) — y una base real de tests (DD-10) sin que nadie la haya creado. Sin `foundation-setup`, el primer change que escriba código no tendría dónde correr, contra qué base testear, ni dónde se registran las decisiones estructurales; y la deuda A/B de `knowledge-base/04_modelo_de_datos.md` (§"Deuda de diseño: Turno vs Bloqueo") seguiría abierta en el punto exacto en que el roadmap la declara obligatoria.

## What Changes

- **Estructura de monorepo**: se crean los directorios base `backend/`, `frontend/`, `docker/`, `docs/` (ya existe) y `openspec/specs/`, con el layout de capas de `knowledge-base/08_arquitectura_propuesta.md` (`domain/`, `application/`, `infrastructure/`, `api/` en backend; `pages/`, `components/`, `lib/` en frontend).
- **`docker-compose.yml`** con tres servicios: `db` (`postgres:15-alpine`, fijado por DD-11 y `CHANGES.md:7`), `backend` (FastAPI sobre Python 3.11) y `frontend` (Vite + React 18), con healthcheck en la base y red interna.
- **`.env.example`** con el contrato de variables de entorno: `DATABASE_URL`, `SECRET_KEY`, `ENCRYPTION_KEY` (separadas, por diseño), `JWT`/`TOKEN_TTL_HOURS`, `COOKIE_SECURE`, `APP_ENV`, `LOG_LEVEL`. Sin ningún valor sensible real (regla: NUNCA hardcodear secretos).
- **Configuración base del tooling**: alembic + pytest en backend, eslint + vitest y `tsconfig` estricto (NUNCA `any`) en frontend, más un esqueleto mínimo de cada app para que `docker compose up` tenga algo que levantar.
- **Registro obligatorio de la decisión A/B** en `design.md`: se documenta la **Opción A** (tabla única `reserva_agenda` con campo `tipo` (`turno`/`bloqueo`) + `EXCLUDE USING gist (tstzrange(inicio, fin, '[)') WITH &&)` sobre `btree_gist`) con su justificación, citando la fuente (`04_modelo_de_datos.md` §"Las dos salidas" y la decisión D1 de `openspec/changes/crear-turno-sin-solapamientos/design.md`). El debate A/B NO se reabre: está cerrado.
- **Gate de prerequisitos** en `tasks.md`: verificación de `docker` en PATH y WSL2 operativo antes de crear cualquier archivo de infraestructura; si el gate falla, apply se declara bloqueado.

## Capabilities

### New Capabilities

- `foundation/dev-environment`: entorno reproducible de desarrollo e integración del monorepo — servicios de Docker Compose (especialmente PostgreSQL 15 real, requerido por DD-05/DD-10), contrato de variables de entorno sin secretos, y tooling base de validación (pytest/alembic/eslint/vitest) con el que los changes posteriores corren y se testean.

### Modified Capabilities

<!-- Ninguno: `openspec list --specs` devuelve "No specs found" — el proyecto aún no tiene specs de capacidades publicadas. -->

## Impact

- **Archivos nuevos**: `docker-compose.yml`, `.env.example`, `backend/` (app + configs), `frontend/` (Vite + TS), `docker/`, `openspec/specs/`. No se modifica ningún archivo existente salvo, eventualmente, nada fuera de `openspec/`.
- **Lo que NO cambia**: no se esquema de base de datos, no hay migraciones, no hay endpoints, no hay lógica de negocio. El esquema (incluida la `EXCLUDE USING gist` real sobre `reserva_agenda`) lo crea C-02 bajo la Opción A registrada acá.
- **Governance CRITICO (C-01)**: este change es propuesta/planificación; la fase apply sobre infraestructura requiere aprobación humana explícita.
- **Habilita el GATE 0 del roadmap**: al cerrarse, quedan desbloqueados en paralelo C-02 (`core-models-schema`, Agente A) y C-07 (`ui-base-frontend`, Agente C).
- **Ripple sobre changes vecinos**: la Opción A implica re-scope del esquema de C-02, C-05 y C-09 ya aceptado en la decisión D1 de `crear-turno-sin-solapamientos`; C-01 sólo lo registra, no lo re-abre.
- **Trazabilidad**: DD-05 (integridad en la base), DD-09 (cookie httpOnly → `.env.example` lleva `SECRET_KEY`), DD-10 (PostgreSQL real en Docker → el servicio `db` existe para eso), DD-11 (stack fijado). RN-AGE-03 y RN-AGE-05 no se implementan acá: sólo condicionan la decisión A/B que se registra.
