# Design

## Context

Ver `proposal.md` — ¿Por qué. Estado actual: repo sin código ni infraestructura (fase 0), con el stack ya fijado en DD-11 (FastAPI + PostgreSQL 15 + React 18 + Docker Compose) y la deuda A/B de `04_modelo_de_datos.md` §"Deuda de diseño: Turno vs Bloqueo" pendiente de registro obligatorio (`CHANGES.md:95`). La decisión A fue **cerrada** en `openspec/changes/crear-turno-sin-solapamientos/design.md` (decisión D1): este change la registra, no la re-abre.

## Goals / Non-Goals

**Goals:**

- Materializar la estructura de monorepo prevista en `08_arquitectura_propuesta.md` con dependencia de capas en un solo sentido (`domain/` no importa `infrastructure/`).
- Proveer `docker-compose.yml` con `db` (`postgres:15-alpine`), `backend` (FastAPI) y `frontend` (Vite) que levante con un comando y deje una base PostgreSQL **real** disponible para los tests de integridad de C-02..C-10 (DD-10).
- Publicar el contrato de `.env.example` sin secretos reales y con `SECRET_KEY`/`ENCRYPTION_KEY` separadas (DD-09).
- Configurar tooling base: alembic + pytest (backend); eslint + vitest + `tsconfig` estricto (frontend, NUNCA `any`).
- Registrar la **decisión A** en este change, con justificación y fuente, cumpliendo `CHANGES.md:95`.
- Incluir un gate de prerequisitos (docker en PATH + WSL2) que bloquee el apply si el entorno no está listo.

**Non-Goals:**

- Escribir código de negocio, endpoints, migraciones o esquema de base (eso es C-02+). `docker-compose.yml`, `.env.example`, configs y esqueletos mínimos SÍ se crean en apply (scope de C-01).
- No aplicar `EXCLUDE USING gist` sobre ninguna tabla en este change — la extensión y el constraint los crea C-02 siguiendo la Opción A registrada acá.
- No resolver el motor de disponibilidad UX (C-05), auth (C-03) ni frontend funcional (C-07/C-08).
- No ejecutar nada en producción / ningún despliegue: sólo entorno de desarrollo local reproducible.

## Decisions

### D1 — Decisión A/B registrada: **Opción A** (tabla única `reserva_agenda` con `tipo` + `EXCLUDE USING gist`)

**Decisión (registro, no re-apertura)**: `Turno` y `Bloqueo` conviven como filas de una tabla única de reserva de agenda con campo discriminador `tipo = 'turno' | 'bloqueo'`; la restricción `EXCLUDE USING gist` vive **una sola vez** sobre esa tabla con la extensión `btree_gist`, y los datos de negocio del turno (paciente, práctica, token) quedan en una tabla de detalle relacionada.

**Fuente / trazabilidad**: decisión D1 de `openspec/changes/crear-turno-sin-solapamientos/design.md` (resuelta en Etapa 6 de OPSX) y `knowledge-base/04_modelo_de_datos.md:226-237` (§"Las dos salidas"), siguiendo la obligación de `CHANGES.md:95`.

**Justificación (resumen de D1)**: la garantía no-solapamiento debe vivir en el declarativo (`EXCLUDE USING gist`) y NUNCA en triggers de código — un trigger mal escrito es un bug silencioso y viola la hard rule de AGENTS.md/DD-05. La Opción B deja turno-vs-bloqueo en "responsabilidad de la aplicación", el estado parcial que la KB diagnostica como defecto. Además, A concentra el camino de fallo en un solo constraint (menor superficie de tests bajo DD-10) y su costo (reescritura de esquema) es cero hoy, en fase 0, porque no hay esquema que reescribir.

**Consecuencias aceptadas (registradas, no renegociadas)**: re-lectura/re-ajuste del scope de C-02, C-05 y C-09 en `CHANGES.md` (dependen de cómo queda el modelo unificado); cambio en el modelo de consultas/DTOs del Flujo 1; ubicación final de `estado`, `motivo_cancelacion` y `token_público` en el modelo unificado queda `(TBD)` para C-02.

**Decisión fija adjunta**: **el turno nace `confirmado`** (resuelto en apply de `crear-turno-sin-solapamientos`, design.md Open Questions 1). **Eje "por profesional"**: fuera de alcance de C-01 y C-02.

### D2 — Servicios de Docker Compose

Tres servicios en la red interna del compose:

- `db`: imagen `postgres:15-alpine` (DD-11 fija PostgreSQL 15; `15-alpine` es el tag del roadmap/`CHANGES.md:7`), volumen nombrado para persistencia, healthcheck (`pg_isready`), y exposición del puerto para desarrollo.
- `backend`: build de `backend/`, imagen base `python:3.11` (o `python:3.11-alpine`), command de uvicorn, env desde `.env`, depende de `db` healthy.
- `frontend`: build de `frontend/`, image base `node:lts` para Vite dev server, depende de `backend`.

El servicio que los tests usan es `db`; la imagen `15-alpine` no es sustituible por PostgreSQL 17 nativo de la máquina ni por dobles (DD-10/DD-11, ver D1 de `crear-turno-sin-solapamientos` sobre el PostgreSQL 17 local descartado).

**Alternativa rechazada**: SQLite/do-bblo en memoria para el entorno → no implementa `EXCLUDE USING gist` (DD-10). Docker Compose es el mecanismo fijado por DD-11.

### D3 — Contrato de variables de entorno (`.env.example`)

Variables documentadas, todas con placeholder y ninguna con valor real:

| Variable | Uso | Sensible |
|----------|-----|----------|
| `DB_USER` / `DB_PASSWORD` / `DB_NAME` / `DB_PORT` | Credenciales del servicio `db` | Sí (sólo placeholder en `.env.example`) |
| `DATABASE_URL` | Cadena de conexión hacia `db` (`postgresql://user:pass@db:5432/turnos`) | Sí |
| `SECRET_KEY` | Firma de JWT (`openssl rand -hex 32`) | Sí |
| `ENCRYPTION_KEY` | Cifrado de datos de salud (`openssl rand -hex 32`) | Sí |
| `TOKEN_TTL_HOURS` | Duración de sesión | No |
| `COOKIE_SECURE` | Exigir HTTPS en cookie (DD-09) | No |
| `APP_ENV`, `LOG_LEVEL` | Entorno/log | No |

Decisión de seguridad: `SECRET_KEY` y `ENCRYPTION_KEY` **separadas** (08_arquitectura_propuesta.md:113-115) — que un token de sesión se filtre no debe volcar las historias clínicas. `.env` se agrega a `.gitignore`; ningún secreto versionado.

### D4 — Layout de monorepo y dirección de dependencias

```
backend/app/{domain,application,infrastructure,api}   (layout 08_arquitectura_propuesta.md)
frontend/src/{pages,components,lib}
docker/                                               (docker-compose.yml, profiles, scripts aux)
docs/
openspec/specs/
```

`domain/` MUST NOT importar `infrastructure/`; la validación Pydantic vive en el borde API (RN-GEN-04). En C-01 el esqueleto crea los directorios con `__init__.py`/`.gitkeep` y configs; la dirección de capas se verifica con la herramienta de análisis de imports elegida en C-02+ (el spec ya la exige como comportamiento).

### D5 — Tooling base

- **Backend**: `pyproject.toml` con `pytest` como runner, `alembic` para migraciones (sólo configuración en C-01; la primera migración es C-02), `.env.example` alimentando `DATABASE_URL`. Sin dependencia alguna de SQLite.
- **Frontend**: Vite + React 18 + TypeScript con `tsconfig` estricto (`noImplicitAny: true`; el `any` explícito prohibido por AGENTS.md), `eslint` y `vitest`. Un componente/esqueleto mínimo (`main.tsx`) para que el build de Vite levante.

### D6 — Gate de prerequisitos (checks antes de aplicar)

El apply SHALL verificar, **como primera tarea**, que el entorno puede materializar la infraestructura: `docker --version` en PATH y motor arriba (`docker info`/`docker version --json`), y en Windows WSL2 con distro instalada (subsistema para Docker Desktop). Si el gate falla → apply se reporta **bloqueado** sin crear archivos de infraestructura; el entorno ya está verificado por el orquestador (Docker 29.8.2 motor arriba, WSL2 con Ubuntu), pero el gate lo re-confirma dentro del repo.

## Risks / Trade-offs

- **[puertos en uso] → Mitigación**: el compose fija binds de desarrollo (`5432`, `8000`, `5173`); si chocan, el gate de prerequisitos los detecta (`docker compose up` reporta bind conflict) y la tarea documenta cómo cambiarlos en `.env`.
- **[imagen Python/Node no disponible offline] → Mitigación**: apply verifica pull de `postgres:15-alpine` primero (es la pieza crítica DD-10); los demás servicios pueden diferirse.
- **[secretos en el repo] → Mitigación**: `.env` en `.gitignore` desde la primera tarea; `.env.example` con placeholders; verificación final de que ningún valor real quedó versionado.
- **[Decisión A arrastra re-scope de C-02/C-05/C-09] → Mitigación**: ya aceptado y documentado (D1); no es un riesgo nuevo, es costo registrado.
- **[gate demasiado rígido (WSL2)] → Mitigación**: el check reporta estado, no exige configuración manual; si WSL2 no está, se informa el bloqueo con instrucciones de `wsl --install` en lugar de saltar el control.

## Migration Plan

No aplica rollback de producción: C-01 es infraestructura de desarrollo. Si algo falla, el apply borra lo creado (directorios/esqueletos) y el entorno vuelve al estado fase-0. La base Docker (`db`) usa volumen nombrado: `docker compose down -v` lo elimina si es necesario resetear. No hay migraciones de esquema en este change (la primera es C-02).

## Open Questions

Ninguna que cambie specs, enfoque o división de tareas: la Opción A está decidida, el stack está fijado (DD-11) y los `TBD` del modelo unificado de la reserva se resuelven en C-02 sin afectar este change.