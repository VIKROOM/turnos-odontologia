# Tasks

> Gobernanza: CRITICO. Este change toca el schema de base de un sistema con datos de salud; apply MUST detenerse y reportar en el gate 1.1 si C-01 o el entorno no están listos, en vez de escribir una migración contra una base no prevista.

## 1. Prerequisitos y gate de entorno (dependencia C-01)

- [x] 1.1 Verificar que C-01 `foundation-setup` está aplicado: existe `docker-compose.yml` con servicio `db` (`postgres:15-alpine`), la base está arriba y accesible (`docker compose ps`), `backend/` tiene `alembic.ini`/`env.py` configurados, `psycopg` está instalado y `pytest` corre desde `backend/` — verify: el checklist imprime el estado por ítem y el ítem 1 confirma conexión real a PostgreSQL; si algún ítem falta, apply SE DETIENE ACÁ y reporta "bloqueado por C-01/entorno" sin escribir nada (design.md D5/D6; mismo patrón que el gate de crear-turno).

- [x] 1.2 Verificar versión y capacidades de la base de destino — verify: `SELECT version()` reporta PostgreSQL 15.x (DD-11), `SELECT gen_random_uuid()` devuelve un uuid (D3) y `CREATE EXTENSION IF NOT EXISTS btree_gist` se ejecuta sin error (D2). Si el host responde otra versión (p. ej. el PostgreSQL 17 nativo), se registra y se detiene, no se adopta como sustituto (DD-11).

## 2. RED — Tests de integridad de la garantía escritos primero

> Estos tests se escriben ANTES de la migración: el esquema aún no existe, así que el RED legítimo es `relation "reserva_agenda" does not exist`. Si un test fallara por otra razón cuando el esquema exista, es un bug real del schema, no del test.

- [x] 2.1 Crear fixture pytest (p. ej. `backend/tests/conftest.py`) que conecta a la base `db` del compose usando `DATABASE_URL` del `.env` de C-01 — verify: `pytest --collect-only` desde `backend/` lista el archivo y la fixture establece conexión a `postgres:15-alpine` real (DD-10; NUNCA SQLite ni dobles en memoria).

- [x] 2.2 Escribir test "turno solapado rechazado" (RN-AGE-03): insertar directo, vía `psycopg`, un turno `confirmado` de 10:00–10:30 en recurso R; luego insertar otro `confirmado` 10:15–10:45 en R esperando `psycopg.errors.ExclusionViolation` (SQLSTATE `23P01`) — verify: el test corre y FALLA con "relation reserva_agenda does not exist" (RED), no por consulta/assert erróneos.

- [x] 2.3 Escribir test "mismo intervalo en otro recurso admitido": con un `confirmado` 10:00–10:30 en R1, insertar `confirmado` 10:00–10:30 en R2 debe persistir — verify: RED por esquema ausente (mismo motivo que 2.2); el caso se documenta citando RN-AGE-03 (comparación por recurso).

- [x] 2.4 Escribir tests de semántica semiabierta `[inicio, fin)` (RN-AGE-01/RN-AGE-03): (a) contiguo `finA == inicioB` → INSERT admitido; (b) `inicioA == inicioB` → `23P01`; (c) fila con `fin <= inicio` → `psycopg.errors.CheckViolation` (`23514`) — verify: los tres casos corren y FALLAN por esquema ausente (los casos (a) y (c) también ejercitan el `CHECK (fin > inicio)`).

- [x] 2.5 Escribir test "turno cancelado no ocupa el índice": insertar `turno` `estado='cancelado'` 10:00–10:30 en R y luego `turno` `confirmado` en el MISMO rango de R → admitido (el predicado parcial de D2 excluye cancelados) — verify: RED por esquema ausente; el docstring cita RN-AGE-03 y el predicado `WHERE (tipo='bloqueo' OR estado='confirmado')`.

- [x] 2.6 Escribir tests turno-vs-bloqueo y bloqueo-vs-bloqueo (RN-AGE-05): (a) `confirmado` 10:00–10:30 en R + `bloqueo` 10:15–11:00 en R → `23P01`; (b) `bloqueo` 10:00–12:00 en R + `bloqueo` 11:00–13:00 en R → `23P01` — verify: RED por esquema ausente; son los dos casos por separado que exige la KB (`04_modelo_de_datos.md:238-249`).

- [x] 2.7 Escribir tests de checks del discriminador e integridad referencial: `tipo='turno'` sin `paciente_id`/`practica_id` → `23514`; `tipo='bloqueo'` con `paciente_id` → `23514`; `practicaduracion` con `recurso_id` inexistente → `psycopg.errors.ForeignKeyViolation` (`23503`) — verify: RED por esquema ausente.

## 3. GREEN — Migración Alembic inicial que materializa el esquema

- [x] 3.1 Crear la migración inicial `backend/alembic/versions/*_core_models_schema.py` siguiendo el orden del design.md D6: `CREATE EXTENSION IF NOT EXISTS btree_gist`; tablas `usuario`, `recurso`, `practica`, `practicaduracion`, `disponibilidad_semanal`, `paciente`, `historiaclinica`, `reserva_agenda` (PKs uuid `gen_random_uuid()`, `created_at`/`updated_at`); checks y tipado de D3; índices de D4; y terminar con `ALTER TABLE reserva_agenda ADD CONSTRAINT reserva_agenda_sin_solapamiento EXCLUDE USING gist (recurso_id WITH =, tstzrange(inicio, fin, '[)') WITH &&) WHERE (tipo = 'bloqueo' OR estado = 'confirmado')` — verify: `alembic upgrade head --sql` emite el DDL completo (extensión, tablas, constraint, índices) y el texto del EXCLUDE coincide con el shape D2 de `crear-turno-sin-solapamientos`.

- [x] 3.2 Aplicar la migración contra la base real — verify: `alembic current` muestra la nueva revisión; `pg_catalog.pg_constraint` contiene `reserva_agenda_sin_solapamiento`, `pg_extension` contiene `btree_gist` y `information_schema.tables` lista las ocho tablas.

- [x] 3.3 Correr la suite completa del grupo 2 — verify: TODOS los tests del grupo 2 pasan en verde contra PostgreSQL real; el runner evidencia al menos una observación de `23P01`, `23514` y `23503` y cada caso cita la RN correspondiente (trazabilidad AGENTS.md). Cualquier test que falle con un error distinto de "schema ausente" es un bug del schema y detiene el grupo.

- [x] 3.4 Escribir y correr el test de concurrencia (spec *Dos escrituras simultáneas*): dos conexiones insertando el mismo intervalo `confirmado` en R en paralelo → exactamente un éxito y un `23P01`; verificar también que a la par, un insert con el mismo intervalo en R2 tiene éxito — verify: test verde contra la `db` real con dos conexiones `psycopg` simultáneas (DD-10/DD-05); cita RN-AGE-03 y RN-GEN-01.

## 4. Verificación de esquema, trazabilidad y cierre

- [x] 4.1 Verificar reversibilidad: `alembic downgrade base` deriva el constraint, las ocho tablas y la extensión; un nuevo `alembic upgrade head` deja el esquema idéntico y reproducible — verify: comandos ejecutados y `alembic current` vuelve y re-aplica sin error; la base queda en el estado del spec *La migración inicial crea las ocho tablas* (si el entorno lo permite, reseteo duro con `docker compose down -v` + reapply).

- [x] 4.2 Verificar trazabilidad completa: todo `Requirement`/`Scenario` del spec `core/data-model` tiene al menos un caso de test o verificación explícita (incluyendo *Toda fila queda con timestamps* y *La integridad referencial es obligatoria*), y cada test/docstring referencia su `RN` — verify: tabla de mapeo spec→test en la raíz del grupo de tests; `pytest` reporta la colección completa en verde.

- [x] 4.3 Alinear `CHANGES.md`: reescribir la sección `[C-02]` para reflejar el modelo unificado (tabla única `reserva_agenda` con `tipo`, sin tablas `turno`/`bloqueo`) y marcar el estado del change cuando el resto esté completo — verify: la sección `[C-02]` ya no lista `turno`/`bloqueo` como tablas y enlaza a este change. SIN commitear ni archivar (prohibido sin pedido explícito).

## Workflow follow-up

- Tras la aprobación de C-02, correr `openspec archive --change core-models-schema` para sincronizar el delta `core/data-model` al spec principal y cerrar el change.
- El GATE 1 de `CHANGES.md` queda liberado para los changes que consumen este esquema (C-03, C-04, C-05).