# Design

## Context

Ver `proposal.md` — *Why*. Estado que gobierna este diseño: el repo sigue en fase 0 (solo KB, changes y tooling; `backend/` y `docker-compose.yml` los crea C-01 en apply). C-02 depende de C-01 (`CHANGES.md:112`). Las premisas ya cerradas que este change NO re-abre:

- **Opción A** decidida en D1 de `crear-turno-sin-solapamientos/design.md`: tabla única `reserva_agenda` con `tipo`; registrada además en D1 de `foundation-setup/design.md`. Re-scope de C-05/C-09 ya aceptado.
- **Shape del `EXCLUDE`** propuesto en D2 de `crear-turno-sin-solapamientos/design.md:`: restricción parcial `WHERE (tipo = 'bloqueo' OR estado = 'confirmado')` sobre `EXCLUDE USING gist (recurso_id WITH =, tstzrange(inicio, fin, '[)') WITH &&)`. Un turno cancelado no ocupa el índice.
- **El turno nace `confirmado`** (Open Question 1 de crear-turno, resuelta). **Eje "por profesional"** fuera de alcance (solo exclusión por `recurso_id`).
- Restricciones duras (AGENTS.md): garantía en `EXCLUDE USING gist` + `btree_gist`, nunca en backend (DD-05); tests contra PostgreSQL 15 real en Docker, nunca SQLite/dobles (DD-10); toda RN citada como `RN-XX` (trazabilidad).

Este change cierra la Open Question 3 de `crear-turno-sin-solapamientos/design.md` (ubicación de `estado`/`motivo_cancelacion`/`token_publico` en el modelo unificado), que el roadmap dejó específicamente para C-02.

## Goals / Non-Goals

**Goals:**

- Materializar el modelo unificado de la Opción A en una única migración Alembic aplicable sobre `postgres:15-alpine` (C-01 ya levanta la base).
- Cerrar la Open Question 3: columnas `estado`, `motivo_cancelacion` y `token_publico` sobre la propia `reserva_agenda`.
- Fijar el DDL exacto de la restricción de exclusión parcial (D2 de crear-turno) y de todos los checks/índices/timestamps.
- Que apply deje evidencia verificable ejecutable: tests de integración (PostgreSQL real) que comprueban 23P01, admisión en otro recurso, adyacencia y cancelado-no-compite; además de suelo real de datos para los changes C-03..C-10.

**Non-Goals:**

- Escribir código de aplicación, endpoints, DTOs, repositorios o dominio (eso lo consumen C-04/C-05 sobre este esquema).
- Crear `entrada_odontograma` ni `auditoria_acceso` (C-06/C-09).
- Seed data de negocio; solo el mínimo verifiable que exija algún test de apply.
- Motor de disponibilidad UX (C-05).
- Ningún `EXCLUDE` cruzado entre tablas: con Opción A la exclusión es intra-tabla y no aplica.

## Decisions

### D1 — Modelo unificado plano: `reserva_agenda` como tabla única (cierra OQ3 de crear-turno)

**Decisión**: `reserva_agenda` porta el discriminador `tipo` (`turno`/`bloqueo`) y TODAS las columnas del turno en la misma tabla. No se crea tabla de detalle. Cierre de la Open Question 3 de `crear-turno-sin-solapamientos/design.md`:

- `estado` — sobre `reserva_agenda` (requerido para `tipo='turno'`, `NULL` para `bloqueo`), porque el predicado del `EXCLUDE` de D2 opera sobre esta columna en el modelo unificado.
- `motivo_cancelacion` — sobre `reserva_agenda` (nullable).
- `token_publico` — sobre `reserva_agenda` (nullable, `UNIQUE`; los NULLs múltiples de bloques/otros estados están permitidos por Postgres en una unique).
- `paciente_id`, `practica_id` — sobre `reserva_agenda`, requeridas para `tipo='turno'`, nulas para `tipo='bloqueo'`.

**Nota de re-scope (registrada, no renegociada)**: D1 de `crear-turno-sin-solapamientos` mencionaba "tabla de detalle relacionada" como parte de la Opción A. Al cerrar la OQ3, este change decide el **detalle plano** (columnas en la propia `reserva_agenda`) porque (1) el predicado `estado = 'confirmado'` del shape D2 asume `estado` sobre la tabla única, (2) ningún requerimiento de los consumers exige desnormalizar el detalle, y (3) simplifica la escritura/lectura del Flujo 1 (`07_flujos_principales.md` paso 5-8). Es un refinamiento dentro del modelo A ya aceptado; C-05/C-09 lo consumen sin cambios adicionales.

**Alternativa descartada**: tabla de detalle `detalle_turno(id, reserva_id, paciente_id, practica_id, ...)`. Añade un join obligatorio a cada lectura de agenda sin aportar a la garantía ni a las reglas; el único argumento (separación semántica) no justifica el costo.

### D2 — DDL normativo de la restricción de no-solapamiento

La migración MUST culminar creando exactamente esto (shape D2 de crear-turno, texto íntegro):

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE reserva_agenda
  ADD CONSTRAINT reserva_agenda_sin_solapamiento
  EXCLUDE USING gist (
    recurso_id WITH =,
    tstzrange(inicio, fin, '[)') WITH &&
  )
  WHERE (tipo = 'bloqueo' OR estado = 'confirmado');
```

- `btree_gist` habilita `WITH =` sobre columnas escalares (UUID/integer) en un índice GiST; sin ella el DDL no compila.
- Predicado parcial: solo compiten las filas que representan reserva efectiva — turnos `confirmado` y cualquier `bloqueo`. Un turno `cancelado`/`completado`/`no_asistio` no ocupa el índice.
- `[inicio, fin)` explícito en el `tstzrange`: `finA == inicioB` ⇒ intersección vacía ⇒ **permitido**; `inicioA == inicioB` ⇒ intersección no vacía ⇒ **rechazado** (spec *Intervalos semiabiertos*).
- Violación ⇒ SQLSTATE `23P01` (`exclusion_violation`) — único código que los tests de apply buscan.
- Con la tabla única, esta restricción cubre turno-vs-turno (RN-AGE-03) y turno-vs-bloqueo/bloqueo-vs-bloqueo (RN-AGE-05) a la vez (`04_modelo_de_datos.md:238-249` exige probar ambos casos por separado).

**Alternativa descartada**: predicado `WHERE (estado = 'confirmado' OR tipo = 'bloqueo')` (mismo, reordenado) o sin predicado (haría competir también a las cancelaciones). El predicado parcial es el shape decidido y no se re-abre.

### D3 — Tipado y checks de columnas

- PKs: `uuid` con `gen_random_uuid()` (nativo en PostgreSQL 13+, sin extensión adicional).
- `inicio`/`fin`: `timestamptz NOT NULL`; `CHECK (fin > inicio)` en `reserva_agenda` (RNAGE-01).
- `estado`: `varchar(20)`, con `CHECK (tipo = 'turno' AND estado IN ('confirmado','cancelado','completado','no_asistio') OR tipo = 'bloqueo' AND estado IS NULL)`.
- `tipo`: `varchar(10) NOT NULL CHECK (tipo IN ('turno','bloqueo'))`.
- `dia_semana` (disponibilidad_semanal): `smallint NOT NULL CHECK (dia_semana BETWEEN 0 AND 6)`; `hora_inicio`/`hora_fin` `time` con `CHECK (hora_fin > hora_inicio)`; `UNIQUE (recurso_id, dia_semana)` para que una franja no se duplique por día y recurso.
- `usuario.password_hash` `varchar(255)`; `email` `varchar(160) UNIQUE NOT NULL`.
- `paciente.telefono` índice único parcial `WHERE anulado_at IS NULL` (RN-PRIV-04); `email` nullable.
- `practica.duracion_minutos` `CHECK (> 0)`; `nombre` `varchar(80) UNIQUE`.
- `practicaduracion.duracion_minutos` `CHECK (> 0)`; `UNIQUE (practica_id, recurso_id)`.
- `disponibilidad_semanal.hora_inicio`/`hora_fin` y demás nombres exactamente en snake_case (roadmap/KB).
- Timestamps: `created_at`/`updated_at` `timestamptz NOT NULL DEFAULT now()` en las ocho tablas.

### D4 — Índices

- `reserva_agenda`: `btree (recurso_id)` + `btree (recurso_id, inicio)` (lectura de franja por recurso, misma convención que KB Bloqueo); `btree (paciente_id)` (turnos por paciente); `btree (practica_id)`.
- `practicaduracion`: índice cubriente `(recurso_id, practica_id)` (KB).
- Resto de FK: índice `btree` sobre la columna referenciante cuando no exista ya uno (p. ej. `historiaclinica(paciente_id)`, `disponibilidad_semanal(recurso_id)`, `practicaduracion(practica_id)`).
- El índice de exclusión (GiST) que crea la restricción es por construcción el de búsqueda de solapamiento; no se agrega otro GiST.

### D5 — Estrategia de verificación en apply (PostgreSQL real en Docker)

- **Gate prerequisito**: si C-01 no está aplicado (falta `docker-compose.yml` con servicio `db` `postgres:15-alpine` arrancado, `alembic.ini`/`env.py` y driver instalado), apply SE DETIENE y reporta "bloqueado por C-01" sin escribir migración (mismo patrón que el task 1 de crear-turno).
- **Tests de integración** (pytest, fijan la fixture a la `db` real): ejecutan la migración (`alembic upgrade head`) y luego, vía `psycopg`, pruebas de esquema e integridad. Los asserts de exclusión usan `psycopg.errors.ExclusionViolation` (SQLSTATE `23P01`), los de FK `psycopg.errors.ForeignKeyViolation` (`23503`) y los de check `psycopg.errors.CheckViolation` (`23514`).
- Casos mínimos obligatorios: solapamiento turno-vs-turno → 23P01; mismo intervalo en otro recurso → OK; turno `cancelado` solapante → OK (no ocupa índice); turno-vs-bloqueo → 23P01; bloqueo-vs-bloqueo → 23P01; adyacencia `finA == inicioB` → OK; mismo `inicio` → 23P01; `fin <= inicio` → 23514; turno sin `paciente_id` → 23514; FK inexistente → 23503. Cada test cita `RN-AGE-03`/`RN-AGE-05`/`RN-AGE-01` en su docstring/parametrización (trazabilidad AGENTS.md).
- El test de concurrencia (dos conexiones, exactamente un éxito) se incluye porque es la garantía de la restricción misma (spec *Dos escrituras simultáneas*), no del backend.

### D6 — Orden y contenido de la migración Alembic

Orden de operaciones en `upgrade()`:

1. `CREATE EXTENSION IF NOT EXISTS btree_gist;`
2. `CREATE TABLE` en orden topológico de FKs: `usuario` → `recurso` → `practica` → `practicaduracion` → `disponibilidad_semanal` → `paciente` → `historiaclinica` → `reserva_agenda`.
3. Checks e índices (D3/D4).
4. `ALTER TABLE reserva_agenda ADD CONSTRAINT reserva_agenda_sin_solapamiento EXCLUDE ...` (shape D2).

`downgrade()`: drop del constraint de exclusión → drop de las ocho tablas (orden inverso) → drop de la extensión. Rollback reproducible con `alembic downgrade base`; la base Docker se resetea con `docker compose down -v` (volumen nombrado, C-01).

## Risks / Trade-offs

- **[Bloqueo de entorno: Docker no operativo hasta reiniciar la máquina (`crear-turno-sin-solapamientos/design.md` D6)]** → apply arranca con un gate que verifica `docker compose ps`/conexión real a `postgres:15-alpine`; si falla, se reporta bloqueado y no se escribe migración ni se "adopta" el PostgreSQL 17 nativo como sustituto (violaría DD-11/DD-10).
- **[Detalle plano vs "tabla de detalle" del D1 original de crear-turno]** → registrado como re-scope dentro del modelo A (D1 de este change); C-05/C-09 consumen `reserva_agenda` igual. Mitigado por trazabilidad: la decisión queda escrita, no invisible.
- **[Ejecutar tests de exclusión sobre la `db` compartida de compose puede pisar datos]** → los tests usan esquemas/transacciones desechables (p. ej. `SAVEPOINT` por caso, o base efímera creada por fixture) y nunca datos de seed de negocio; la base se puede recrear con `down -v` sin pérdida (solo infra).
- **[`gen_random_uuid()` exige PG ≥ 13]** → fijado PostgreSQL 15 (DD-11); verificación: check de versión en el gate de prerequisitos.
- **[Re-scope del roadmap: `CHANGES.md:108` aún lista `turno`/`bloqueo` como tablas]** → apply actualiza la sección `[C-02]` a `reserva_agenda` (tarea de cierre, sin commit).

## Migration Plan

- **Deploy**: C-01 levanta la infraestructura; este change genera la **primera migración** Alembic (`backend/alembic/versions/xxxx_core_models_schema.py`), la aplica con `alembic upgrade head` contra `postgres:15-alpine` y la verifica con los tests de D5.
- **Rollback**: `alembic downgrade base` (deriva el constraint + las ocho tablas + la extensión). Para state limpio: `docker compose down -v` + reapply.
- **Post-migración**: se registra la revisión en `alembic_version` (spec *La migración inicial crea las ocho tablas*), y C-03..C-05 podrán escribir contra el esquema.

## Open Questions

Ninguna: la OQ3 de crear-turno se cierra en D1 de este change; el resto de supuestos son los ya resueltos por la cadena D1/D2 de crear-turno y C-01 (ver Context). Si apply descubre un supuesto de datos nuevo (p. ej. hornario de disponibilidad con franja madre-marco), se reporta como hallazgo, no como TBD de diseño.