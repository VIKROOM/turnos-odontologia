# Spec Delta

## Purpose

Proveer un entorno de desarrollo e integración reproducible para todo el monorepo: servicios Docker Compose (con PostgreSQL 15 real como base de integridad), contrato de variables de entorno sin secretos y tooling base de validación, sobre el cual los changes posteriores implementan, testean y despliegan.

## ADDED Requirements

### Requirement: Stack local reproducible con Docker Compose
El repositorio SHALL incluir un `docker-compose.yml` que define los servicios `db` (imagen `postgres:15-alpine`), `backend` (FastAPI, Python 3.11) y `frontend` (Vite, React 18), de modo que el entorno completo se levante con un único comando (DD-11).

#### Scenario: La base de datos se levanta de forma aislada
- **WHEN** se ejecuta `docker compose up -d db`
- **THEN** el servicio `db` corre con la imagen `postgres:15-alpine` y queda sano/healthcheck OK

#### Scenario: El stack completo levanta las tres piezas
- **WHEN** se ejecuta `docker compose up -d`
- **THEN** `db`, `backend` y `frontend` quedan corriendo en la red interna del compose, y `backend` y `frontend` se conectan a la base usando `DATABASE_URL`

### Requirement: PostgreSQL real como única base para tests de integridad
Los tests de integridad de agenda (solapamiento) SHALL ejecutarse contra el servicio `db` real; MUST NOT correr contra SQLite ni contra ningún doble en memoria, porque esas bases no implementan `EXCLUDE USING gist` (DD-10, RN-AGE-03).

#### Scenario: Corrida de tests sin la base disponible
- **WHEN** se ejecutan los tests de integridad con el servicio `db` caído
- **THEN** la corrida FALLA con un error de conexión a la base

#### Scenario: Corrida de tests con la base disponible
- **WHEN** se ejecutan los tests de integridad con `docker compose up -d db` en ejecución
- **THEN** los tests usan la base PostgreSQL 15 del servicio `db` vía `DATABASE_URL`

### Requirement: Contrato de variables de entorno sin secretos
El repositorio SHALL publicar un `.env.example` que documenta `DATABASE_URL`, `SECRET_KEY`, `ENCRYPTION_KEY`, `TOKEN_TTL_HOURS`, `COOKIE_SECURE`, `APP_ENV` y `LOG_LEVEL`, con `SECRET_KEY` y `ENCRYPTION_KEY` como variables separadas, y MUST NOT contener valores de secretos reales (ningún secreto en el repositorio).

#### Scenario: Onboarding de un desarrollador
- **WHEN** un desarrollador copia `.env.example` a `.env`, completa los valores y ejecuta `docker compose up -d`
- **THEN** el stack levanta usando esas variables

#### Scenario: El repositorio no contiene secretos reales
- **WHEN** se inspeccionan los archivos versionados buscando valores de `SECRET_KEY` o `ENCRYPTION_KEY`
- **THEN** sólo se encuentran placeholders documentados en `.env.example`, nunca valores reales

### Requirement: Tooling base de validación configurado
El backend SHALL incluir configuración de `pytest` y `alembic`; el frontend SHALL incluir configuración de `eslint`, `vitest` y un `tsconfig` estricto en el que el uso de `any` está prohibido.

#### Scenario: El backend tiene un runner de tests operativo
- **WHEN** se ejecuta `pytest` desde `backend/`
- **THEN** el runner arranca y reporta la corrida (0 tests es válido en C-01)

#### Scenario: El frontend valida tipado estricto
- **WHEN** se ejecuta la verificación de tipos (`tsc --noEmit`) o `eslint` sobre `frontend/`
- **THEN** la verificación corre con configuración estricta y sin usar `any`

### Requirement: Estructura de monorepo con dependencia de capas en un solo sentido
El repositorio SHALL exponer la estructura `backend/`, `frontend/`, `docker/`, `docs/` y `openspec/specs/`, y en `backend/` la capa `domain/` MUST NOT importar nada de `infrastructure/` (08_arquitectura_propuesta.md).

#### Scenario: Dirección de dependencia verificable
- **WHEN** se analizan los imports de `backend/`/`app/domain/`
- **THEN** no existe ninguna importación hacia `infrastructure/`
