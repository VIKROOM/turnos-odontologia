# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto turnos-odontologia (SaaS Odontología).
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier /opsx:propose.**

Stack confirmado: FastAPI 3.11 + PostgreSQL 15 + React 18 (Vite) + Docker Compose.

---

## Alcance

Los changes de este roadmap derivan del MVP imprescindible definido en la sección D.3 del informe de Discovery (`docs/discovery/informe-discovery.md`). Cada change se alinea con ese alcance.

## Cómo usar este documento

1. **Identificar change**: elegí `C-XX` según prioridad/dependencias.
2. **Leer KB**: revisá los "Leer antes" del change elegido.
3. **Proponer**: `opsx propose C-XX-nombre-kebab`.
4. **Archivar**: tras merge, mover specs/changes/C-XX-* a `openspec/changes/archive/`.
5. **Marcar avance**: actualizar checkbox `[x]` cuando esté completado.

---

## Árbol de dependencias

```
C-01-foundation-setup
│
├── C-02-core-models-schema
│   ├── C-03-auth-users-roles
│   │   └── C-04-pacientes-turnos-core
│   │       ├── C-05-disponibilidad-bloqueos
│   │       └── C-06-historia-clinica-odontograma
│   └── C-07-ui-base-frontend
│       └── C-08-agenda-ui-reserva
│
└── C-09-tests-integracion-solapamientos
    └── C-10-seed-datos-iniciales
```

### Paralelismo por fase

**GATE 0**: C-01 ✓  
  → C-02 foundation models (DB schema base) [Agente A — Backend Core]  
  → C-07 UI base (layout/rutas/theme) [Agente C — Frontend]  
  *(Paralelismo posible tras completar C-01)*

**GATE 1**: C-02 ✓  
  → C-03 Auth/RBAC [Agente A — Backend Core]  
  → C-07 puede continuar [Agente C — Frontend]  
  *(Fork tras tener esquema base)*

**GATE 2**: C-03 ✓  
  → C-04 Pacientes/Turnos core (con validación negocio) [Agente A — Backend Core]  
  → C-08 Agenda/UI reserva (depende parcialmente de C-07) [Agente C — Frontend]

**GATE 3**: C-04 ✓  
  → C-05 Disponibilidad/Bloqueos [Agente B — Backend Aux]  
  → C-06 Historia clínica/odontograma [Agente B — Backend Aux]  
  *(Paralelo entre ellos tras tener Turno/Paciente base)*

**GATE 4**: C-05 ✓ + C-06 ✓  
  → C-09 Tests integración solapamientos [Agente B — Backend Aux]  
  *(Debe cubrir turno-vs-turno y turno-vs-bloqueo)*

**GATE 5**: C-09 ✓  
  → C-10 Seed datos iniciales [Agente A — Backend Core]

### Camino crítico (8 changes)

C-01 → C-02 → C-03 → C-04 → C-05 → C-09 → C-10  
*(C-06, C-07, C-08 pueden ejecutarse en paralelo en fases intermedias; no bloquean salida a validación integral)*

### Plan óptimo con 3 agentes

| Paso | Agente A (Backend Core) | Agente B (Backend Aux) | Agente C (Frontend) |
|---|---|---|---|
| 1 | C-01 foundation-setup | — | — |
| 2 | C-02 core-models-schema | — | C-07 ui-base-frontend |
| 3 | C-03 auth-users-roles | — | C-07 (continuar) |
| 4 | C-04 pacientes-turnos-core | C-05 disponibilidad-bloqueos / C-06 historia-clinica-odontograma | C-08 agenda-ui-reserva |
| 5 | — | C-06 historia-clinica-odontograma (si no hecho) | C-08 (continuar) |
| 6 | — | C-09 tests-integracion-solapamientos | C-08 (ajustes) |
| 7 | C-10 seed-datos-iniciales | C-09 (ajustes/tests) | Ajustes UI menores |

---

## FASE 1 — Fundación e Infra

### [C-01] `foundation-setup`

- **Estado**: `[x]` aplicado (pendiente `/opsx:archive`)
- **Scope**:
  - Estructura monorepo: `backend/`, `frontend/`, `docker/`, `docs/`, `openspec/specs/`
  - `docker-compose.yml` con `postgres:15-alpine`, `backend` (FastAPI), `frontend` (Vite)
  - `.env.example` con variables DB/SECRET_KEY/JWT
  - Configuración base (alembic/pytest, eslint/vitest)
  - **Decisión obligatoria A/B**: registrar en `design.md` (o `docs/decisions/`) **Opción A** (tabla única `reserva_agenda` con `tipo` + EXCLUDE GIST sobre esa tabla) vs **Opción B** (triggers cruzados entre `turno` y `bloqueo`). Incluir justificación. Ver deuda en `knowledge-base/04_modelo_de_datos.md`.
- **Dependencias**: ninguna
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §"EXCLUDE USING gist" y §"Deuda de diseño: Turno vs Bloqueo"
  - `knowledge-base/08_arquitectura_propuesta.md`
  - `knowledge-base/05_reglas_de_negocio.md` RN-AGE-01..RN-AGE-05
  - `knowledge-base/09_decisiones_y_supuestos.md` DD-05, DD-09, DD-11

### [C-02] `core-models-schema`

- **Estado**: `[x]` aplicado (pendiente `/opsx:archive`)
- **Change**: `openspec/changes/core-models-schema/`
- **Scope**:
  - Migración inicial con entidades: `usuario`, `recurso`, `practica`, `practicaduracion`, `disponibilidad_semanal`, `paciente`, `historiaclinica`, `reserva_agenda` (tabla única con discriminador `tipo` — Opción A; **no** existen tablas `turno`/`bloqueo`)
  - **EXCLUDE USING gist** parcial sobre `reserva_agenda` (`recurso_id WITH =`, `tstzrange(inicio, fin, '[)') WITH &&`, `WHERE (tipo = 'bloqueo' OR estado = 'confirmado')`) con `btree_gist`. Una sola restricción cubre **turno-vs-turno** (RN-AGE-03) y **turno-vs-bloqueo / bloqueo-vs-bloqueo** (RN-AGE-05); un turno cancelado no ocupa el índice.
  - Modelo unificado (Opción A): `turno` y `bloqueo` son filas de `reserva_agenda`; ya no aplica el EXCLUDE cruzado entre tablas.
  - Índices, timestamps
- **Dependencias**: `C-01`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md`
  - `knowledge-base/05_reglas_de_negocio.md` RN-AGE-03, RN-AGE-05
  - `knowledge-base/07_flujos_principales.md`

---

## FASE 2 — Autenticación, Pacientes y Turnos

### [C-03] `auth-users-roles`

- **Estado**: `[ ]` pendiente
- **Scope**: JWT httpOnly (DD-09), roles (Odontólogo, Recepcionista/Secretaria, Paciente), RBAC, login/logout/me
- **Dependencias**: `C-02`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md`
  - `knowledge-base/05_reglas_de_negocio.md` RN-SEG-*
  - `knowledge-base/09_decisiones_y_supuestos.md` DD-09

### [C-04] `pacientes-turnos-core`

- **Estado**: `[ ]` pendiente
- **Scope**: ABM paciente, crear/cancelar/reprogramar turnos, validación app + DB, cancelación anticipada, token autogendamiento
- **Dependencias**: `C-03`
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md`
  - `knowledge-base/07_flujos_principales.md` (Flujo 1)
  - `knowledge-base/05_reglas_de_negocio.md` RN-AGE-*

### [C-05] `disponibilidad-bloqueos`

- **Estado**: `[ ]` pendiente
- **Scope**: Disponibilidad semanal por recurso, bloqueos. Garantizar no-solapamiento turno-vs-bloqueo según A/B. Motor disponibilidad UX.
- **Dependencias**: `C-04`
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` (deuda)
  - `knowledge-base/05_reglas_de_negocio.md` RN-AGE-05
  - `knowledge-base/06_funcionalidades.md`

### [C-06] `historia-clinica-odontograma`

- **Estado**: `[ ]` pendiente
- **Scope**: HC mínima, odontograma básico, permisos profesionales, auditoría básica
- **Dependencias**: `C-04`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` (HC)
  - `knowledge-base/06_funcionalidades.md`
  - `knowledge-base/05_reglas_de_negocio.md` (RN-SEG)

---

## FASE 3 — Frontend y UX

### [C-07] `ui-base-frontend`

- **Estado**: `[ ]` pendiente
- **Scope**: Vite + React 18, routing, estado base, componentes, API client, auth context, rutas protegidas
- **Dependencias**: `C-01`
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/08_arquitectura_propuesta.md` §Frontend
  - `knowledge-base/07_flujos_principales.md`

### [C-08] `agenda-ui-reserva`

- **Estado**: `[ ]` pendiente
- **Scope**: Vista agenda por sillón (semana), autogendamiento 24/7, reserva/cancelación/reprogramación, manejo conflictos
- **Dependencias**: `C-07`, `C-04`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` US-001
  - `knowledge-base/07_flujos_principales.md` Flujo 1
  - `knowledge-base/01_vision_y_objetivos.md`

---

## FASE 4 — Validación, Calidad y Datos

### [C-09] `tests-integracion-solapamientos`

- **Estado**: `[ ]` pendiente
- **Scope**:
  - **OBLIGATORIO**: test `turno-vs-turno` → debe rechazar por EXCLUDE/DB
  - **OBLIGATORIO**: test `turno-vs-bloqueo` → debe rechazarse según decisión A/B
  - Concurrencia básica (2 requests simultáneos)
  - Tests cancelación/reprogramación
  - Ejecutar contra PostgreSQL real (Docker)
  - Validar RN-AGE-03, RN-AGE-05
- **Dependencias**: `C-05`, `C-06`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` (EXCLUDE + deuda)
  - `knowledge-base/05_reglas_de_negocio.md` RN-AGE-03, RN-AGE-05
  - `knowledge-base/09_decisiones_y_supuestos.md` DD-05, DD-10

### [C-10] `seed-datos-iniciales`

- **Estado**: `[ ]` pendiente
- **Scope**: Seed mínimo (odontólogo demo, recurso sillón, prácticas+duraciones, disponibilidad semanal), script idempotente
- **Dependencias**: `C-09`
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §"Seed data inicial"
  - `knowledge-base/03_actores_y_roles.md`

### [C-11] `exportacion-datos-pacientes`

- **Estado**: `[ ]` pendiente
- **Scope**: Exportación total de datos propios (impr esc. #9 de D.3) en formato portable (CSV/JSON) para paciente/usuario, incluyendo historial clínico mínimo, con permisos adecuados, sin pedir permisos adicionales.
- **Dependencias**: `C-03`, `C-04`, `C-06`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md`
  - `knowledge-base/05_reglas_de_negocio.md` (protección de datos)
  - `docs/discovery/informe-discovery.md` §D.3

---

## Resumen

- **Total changes**: 11
- **Fases**: 4
- **Gates de paralelismo**: 6
- **Camino crítico**: 7 changes (C-01→C-02→C-03→C-04→C-05→C-09→C-10)
- **Primer change recomendado**: `C-01` (`foundation-setup`) — incluye decisión A/B para deuda Turno vs Bloqueo

> CHANGES.md generado con enfoque en cumplimiento de RN-AGE-03/RN-AGE-05 y en la deuda explícita entre Turno/Bloqueo.
