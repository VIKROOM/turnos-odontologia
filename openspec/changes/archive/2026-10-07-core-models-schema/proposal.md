# Proposal

## Why

El repo es un monorepo de planificación sin esquema de base: no existe ninguna tabla, ninguna migración y ninguna garantía de integridad en PostgreSQL. Todos los changes de la fase 1 y 2 (C-03 auth, C-04 crear turnos, C-05 bloqueos, C-06 historia clínica) escriben contra un modelo que aún no está materializado, y la decisión más importante del proyecto — que la no-existencia de solapamientos la garantice la base y no el backend (DD-05, RN-AGE-03) — no puede demostrarse ni cumplirse sin un esquema real que porte la restricción `EXCLUDE USING gist`. Además, la Opción A (tabla única `reserva_agenda`) quedó decidida en `crear-turno-sin-solapamientos/design.md` D1 y registrada en C-01, y su Open Question 3 (ubicación de `estado`/`motivo_cancelacion`/`token_público` en el modelo unificado) está explícitamente reservada para este change.

## What Changes

- Migración inicial de Alembic (creada y aplicada en apply, no en propose) con las entidades `usuario`, `recurso`, `practica`, `practicaduracion`, `disponibilidad_semanal`, `paciente`, `historiaclinica` y `reserva_agenda`.
- **Modelo unificado (Opción A)**: NO existen tablas `turno` ni `bloqueo`; ambas son filas de `reserva_agenda` con discriminador `tipo` (`turno` / `bloqueo`). Re-scope ya aceptado en D1 de `crear-turno-sin-solapamientos` y en C-01.
- **Cierre de la Open Question 3** de `crear-turno-sin-solapamientos/design.md`: `estado`, `motivo_cancelacion` y `token_publico` (opcional) viven como columnas de la propia `reserva_agenda`; los datos del turno (`paciente_id`, `practica_id`) también. No se crea tabla de detalle.
- **EXCLUDE USING gist parcial** sobre `reserva_agenda` con `btree_gist`: `EXCLUDE USING gist (recurso_id WITH =, tstzrange(inicio, fin, '[)') WITH &&) WHERE (tipo = 'bloqueo' OR estado = 'confirmado')`. Cubre RN-AGE-03 (turno-vs-turno) **y** RN-AGE-05 (turno-vs-bloqueo y bloqueo-vs-bloqueo) con una sola restricción — el mismo predicado que D2 propuso y que este change cierra. Un turno `cancelado` no ocupa el índice.
- Semántica semiabierta `[inicio, fin)` explícita a nivel de datos: `finA == inicioB` NO solapa; `inicioA == inicioB` SÍ solapa.
- Índices de lectura (`recurso_id, inicio` y los que exijan las FK), `CHECK (fin > inicio)`, consistencia del discriminador `tipo`, y `created_at`/`updated_at` en todas las tablas.
- Verificación de apply contra `postgres:15-alpine` real en Docker: `INSERT` directo que dispara SQLSTATE `23P01` (`exclusion_violation`) y admisión del mismo intervalo en otro recurso.

## Capabilities

### New Capabilities

- `core/data-model`: modelo relacional base del consultorio — entidades de administración/agenda/pacientes, integridad referencial, checks, índices y timestamps, y la garantía declarativa de no-solapamiento (`EXCLUDE USING gist` + `btree_gist`) con semántica `[inicio, fin)` a nivel de base. Es la capa que consume (no define) cualquier change que escriba turnos.

### Modified Capabilities

<!-- Ninguna: no existen specs principales en openspec/specs/ todavía (openspec list --specs → vacío).
     deliberadamente NO se toca agenda/reservas acá: ese capability lo introduce
     crear-turno-sin-solapamientos con sus requisitos de aplicación; los requisitos
     de esquema/garantía de este change viven en core/data-model para no duplicar
     requisitos entre dos deltas concurrentes del mismo capability. -->

## Impact

- **Código/infra (creado en apply, no aquí)**: primera migración Alembic de `backend/` (la configuración base la dejó C-01), extensión `btree_gist` habilitada en la base, tests de integración nuevos contra PostgreSQL real en Docker (DD-10).
- **Dependencia**: requiere C-01 `foundation-setup` YA aplicado (`docker-compose.yml` con `postgres:15-alpine` corriendo, `alembic.ini`/`env.py`, driver y `pytest` configurados). Si C-01 no está aplicado, apply se detiene en el gate de prerequisitos.
- **Habilita**: GATE 1 del roadmap (`CHANGES.md`); desbloquea C-03 (auth sobre `usuario`), C-04 (crear turno contra `reserva_agenda` + restricción ya existente), C-05 (bloqueos que compiten por la misma restricción) y C-09.
- **Consumers afectados por el re-scope Opción A** (ya aceptado): `crear-turno-sin-solapamientos`, C-05, C-09 — consultan `reserva_agenda`, no `turno`/`bloqueo`.
- **Roadmap**: la sección `[C-02]` de `CHANGES.md` sigue redactada con tablas separadas (`CHANGES.md:108`); apply MUST alinearla al modelo unificado.
- **Fuera de alcance**: `entrada_odontograma`, `auditoria_acceso` (C-06/C-09), cualquier endpoint o lógica de negocio, seed data más allá de lo mínimo para verificar, y el motor de disponibilidad UX (C-05).
