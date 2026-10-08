# Design

## Context

Ver `proposal.md` — *Why*. Contexto mínimo que forma este diseño: el repo está en fase 0 (sólo knowledge base y tooling; `backend/`, `docker-compose.yml` y tests no existen), la cadena `C-01 → C-02 → C-03 → C-04` está entera pendiente (`CHANGES.md:21-36`), y `CHANGES.md:95` convierte la deuda A/B de `knowledge-base/04_modelo_de_datos.md:195-249` en una decisión obligatoria que este change registra aquí porque es la premisa del esquema sobre el que se escribe.

Restricciones duras que gobiernan el diseño (AGENTS.md / KB):

- La garantía de no-solapamiento vive en `EXCLUDE USING gist` + `btree_gist`, nunca en el backend (DD-05).
- Los tests de solapamiento corren contra PostgreSQL real en Docker; SQLite y dobles en memoria están prohibidos (DD-10).
- `domain/` nunca importa `infrastructure/` (`knowledge-base/08_arquitectura_propuesta.md:57`).
- Stack fijado: FastAPI + PostgreSQL 15 + React 18 + Docker Compose (DD-11).

## Goals / Non-Goals

**Goals:**

- Resolver la deuda A/B con una decisión explícita y justificada (Opción A).
- Fijar el constraint de exclusión concreto (extensión, predicado, semántica de operadores) que C-02 debe materializar y este change consume.
- Fijar el mapeo error-de-base → error-de-dominio y la estrategia de tests (PostgreSQL real en Docker).
- Dejar documentado, sin maquillar, el bloqueo de entorno que impide correr los tests hoy.

**Non-Goals:**

- Escribir código, esquema, migraciones, `docker-compose.yml` o tests (eso es apply).
- Implementar bloqueos (RN-AGE-05 → C-05), auth (C-03), ABM pacientes o frontend.
- Diseñar el motor de disponibilidad UX (C-05) — este change sólo garantiza no-solapamiento.

## Decisions

### D1 — Deuda A/B resuelta: Opción A (tabla única `reserva_agenda` con `tipo` + `EXCLUDE USING gist`)

**Decisión**: `Turno` y `Bloqueo` conviven como filas de una tabla única de reserva de agenda con campo discriminador `tipo`; la restricción `EXCLUDE USING gist` vive **una sola vez**, sobre esa tabla. Los datos de negocio del turno (paciente, práctica, token) quedan en una tabla de detalle relacionada, tal como describe la KB (`04_modelo_de_datos.md:230`).

**Alternativa rechazada — Opción B (triggers `AFTER INSERT OR UPDATE` cruzados entre `turno` y `bloqueo`)**, y por qué:

1. La garantía depende de código, no del declarativo: "un trigger mal escrito es un bug silencioso" (`04_modelo_de_datos.md:231`). Esto choca frontalmente con la hard rule de AGENTS.md ("dejá la garantía a `EXCLUDE USING gist`… el motor de disponibilidad es UX, no integridad") y con el espíritu de DD-05.
2. B sólo cubre bien RN-AGE-03 (turno-vs-turno); turno-vs-bloqueo queda en "responsabilidad de la aplicación", que es exactamente el estado parcial que la KB diagnostica en `04_modelo_de_datos.md:222-224`. A cubre RN-AGE-03 **y** RN-AGE-05 con la misma restricción, dejando `US-004-CA-1` cubierto sin lógica extra.
3. Dos triggers deben mantenerse sincronizados de por vida y probarse por separado; A concentra el camino de fallo en un solo lugar (menor superficie de tests — relevante porque DD-10 exige PostgreSQL real, tests caros).
4. El costo de A es "reescritura del esquema", y **hoy no hay esquema que reescribir** (fase 0). Pagarlo ahora es gratis; pagarlo después de C-02..C-04 no.

**Contra-argumentos de A registrados (decisión informada, no por omisión)**:

- Obliga a re-leer/re-ajustar el scope de `C-02`, `C-05` y `C-09` en `CHANGES.md`, redactados suponiendo tablas separadas (`CHANGES.md:104-117`, `145-154`, `196-211`).
- Cambia el modelo de consultas y los DTOs que consumirá el Flujo 1 (US-006/US-007).
- El destino exacto de `estado`, `motivo_cancelacion` y `token_público` en el modelo unificado **no está decidido en la KB** → `(TBD)`, se cierra en C-02.

**Governance**: la deuda es de C-01 (CRITICO, `CHANGES.md:95`), este change sólo la *registra*; la confirmación humana antes de tocar infraestructura ocurre al aplicar (AGENTS.md: governance CRITICO → aprobación previa).

### D2 — Constraint de exclusión concreto

La restricción que C-02 MUST crear y este change MUST consumir:

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

- **Extensión**: `btree_gist` es la que permite usar `=` sobre columnas de tipo entero/UUID en un índice GiST (GiST sólo indexa tipos de rango/geométricos de forma nativa). Sin ella, `recurso_id WITH =` no compila.
- **Predicado `WHERE`**: sólo compiten las filas que representan una reserva efectiva — turnos `confirmado` y cualquier `bloqueo`. Un turno cancelado NO debe ocupar el índice. El shape `WHERE (tipo = 'bloqueo' OR estado = 'confirmado')` es la propuesta; la ubicación final de `estado` en el modelo unificado queda `(TBD)` (ver Open Questions) y se cierra en C-02 junto con el esquema.
- **Semántica de operadores para `[inicio, fin)`**:
  - `&&` = intersección no vacía de rangos. Dos intervalos se solapan ⇔ `inicio < otro.fin AND otro.inicio < fin`.
  - `tstzrange(inicio, fin, '[)')` es semiabierto por la derecha (la KB ya señala que `tstzrange(inicio, fin)` es semiabierto por defecto, `08_arquitectura_propuesta.md:77-79`; el `'[)'` se escribe explícito para que la convención sea indiscutible en el DDL).
  - Consecuencia observable: `finA == inicioB` ⇒ intersección vacía ⇒ **permitido**; `inicioA == inicioB` ⇒ intersección no vacía ⇒ **rechazado**. Ésta es la semántica que el spec exige en *Intervalos semiabiertos*.
- **Violación**: PostgreSQL la reporta con SQLSTATE **`23P01` (`exclusion_violation`)** — éste es el código que el mapeo de D4 captura.
- **Costo aceptado**: Postgres deja de ser reemplazable (DD-05) — sin cambio respecto de lo ya decidido.

### D3 — Layering: dominio puro, infraestructura contiene al repositorio

Siguiendo el layout de `08_arquitectura_propuesta.md:30-59`:

- `domain/agenda/` — aritmética de intervalos `[inicio, fin)`, cálculo de `fin` a partir de la duración de la práctica (RN-AGE-01) y la validación de disponibilidad como **primera línea de UX**. Puro: sin I/O, sin framework. `domain/` MUST NOT importar `infrastructure/`.
- `application/services/` — caso de uso `crear_turno`: orquesta validación de dominio → repositorio; es el lugar donde se traduce la excepción de infraestructura a error de dominio (D4).
- `infrastructure/db/` — repositorio que ejecuta el INSERT contra PostgreSQL y traduce errores SQL; es el único punto que conoce la BD.
- `api/routers/` — endpoint con validación Pydantic en el borde (RN-GEN-04: "el navegador nunca es la frontera").

El orden importa: la validación de dominio rechaza el 95% de los conflictos con buen mensaje; la restricción de la base es la red de seguridad (`04_modelo_de_datos.md:240-243`: "La exclusión nunca fue la primera línea, fue la red").

### D4 — Mapeo error de base → error de dominio

- SQLSTATE **`23P01` (`exclusion_violation`)** y **`40P01` (`deadlock_detected`)** en el INSERT ⇒ el repositorio MUST lanzar un error de dominio tipado `SolapamientoDetectado` (o equivalente); el caso de uso MUST NOT reintentar en silencio; la API responde **HTTP 409** con mensaje claro de intervalo ocupado (spec: *El conflicto de exclusión se mapea a un error de dominio*). Estos dos SQLSTATE se mapean a conflicto; cualquier otro error de integridad (FK, unique, check) ⇒ NO es solapamiento: mapeo propio (422/500 según corresponda) — detalle de implementación, no de spec.
- **Justificación de incluir `40P01`**: en este camino de escritura un deadlock SÓLO puede surgir de dos transacciones que contenden sobre el mismo rango de exclusión (`recurso_id` + intervalo `&&`), es decir, una escritura conflictiva — el detector de deadlock de PostgreSQL aborta al perdedor con `40P01` en lugar de dejarlo recibir `23P01` (ocurre en ~20-25% de las corridas reales). Por eso `40P01` es un conflicto, nunca un éxito: mapearlo a 409 preserva RN-GEN-05 (sin confirmación en escritura fallida) y garantiza el escenario de concurrencia (1 éxito + 1×409).
- **2026-10-07 — AJUSTAR aprobado por usuario**: se amplía el mapeo de conflicto de `23P01` a `{23P01, 40P01}` tras detectar en apply que el detector de deadlock de PostgreSQL aborta al perdedor de una escritura concurrente con `40P01` (~20% de las corridas), lo que hoy devolvería 500 y violaría el escenario de concurrencia (1 éxito + 1×409).
- La regla de negocio RN-GEN-05 queda cubierta por construcción: si no hay confirmación de la escritura, la respuesta MUST ser error, nunca éxito.
- El spec exige además que un escritor que evite la validación de dominio sea rechazado por la base: eso no requiere código de mapeo — es el constraint actuando solo (D2).

### D5 — Estrategia de tests: PostgreSQL real en Docker, nunca SQLite ni dobles en memoria

- **Tests del guarantee (exclusión, concurrencia)**: integración contra PostgreSQL real levantado en Docker, imagen **`postgres:15-alpine`** (DD-11 / `CHANGES.md:7`). Prohibidos SQLite y cualquier doble en memoria: no implementan `EXCLUDE USING gist`, un verde allí sería el falso positivo exacto que DD-10 y RN-AGE-03 buscan evitar (`09_decisiones_y_supuestos.md:133-145`).
- **Test de concurrencia** (Flujo 2, `07_flujos_principales.md`): dos conexiones/hilos insertando el mismo intervalo en paralelo → **exactamente 1 éxito + 1 rechazo** (garantía del test). El perdedor puede manifestarse legítimamente como `23P01` (`exclusion_violation`) **o** como `40P01` (`deadlock_detected`) — ambos cuentan COMO ese rechazo; los tests que pasan por el camino de la aplicación MUST devolver 409 en ambos casos (D4). Sólo posible con Postgres real y dos conexiones; no es testeable unitariamente.
- **Tests unitarios del dominio**: la aritmética de intervalos y la convención de borde (`finA == inicioB` no solapa) son funciones puras y SÍ se prueban sin base — es lo que la decisión de layout de `08_arquitectura_propuesta.md:57-59` habilita. Lo que **no** se prueba nunca sin Postgres es la *garantía*.
- Cobertura por escenario: cada `#### Scenario:` del spec es un caso de test; el spec es la lista de casos.

### D6 — Realidad de la entorno (registrada sin adornos)

- **Docker Desktop 4.94.0.241994** está instalado (`C:\Program Files\Docker\Docker\Docker Desktop.exe`), pero `docker` NO está en el PATH y `wsl --status` responde que WSL2 no está instalado: **el reinicio pendiente de la máquina no ocurrió**. Consecuencia: **los tests NO pueden correr en la fase de propuesta**, y mientras el reinicio no se complete tampoco en apply. Es blocker explícito del change, no un detalle a silenciar.
- La máquina tiene **PostgreSQL 17.11 nativo** (servicio `postgresql-x64-17`, en ejecución; `psql` fuera del PATH). **No es un sustituto válido**: DD-11/`CHANGES.md:7` fijan PostgreSQL 15 y DD-10 exige el contenedor; el stack decidido es `postgres:15-alpine`. El 17 nativo queda descartado como destino de tests (además, `btree_gist`/`EXCLUDE` existen en ambas versiones, así que el descarte es de proceso, no de funcionalidad).
- Riesgo residual: `docker-compose.yml` y la imagen `postgres:15-alpine` nunca se levantaron en esta máquina — la primera corrida puede fallar por configuración además del PATH.

## Risks / Trade-offs

- **[Apply bloqueado hasta reiniciar la máquina y completar WSL2 + PATH de `docker`]** → blocker documentado arriba (D6); el task de prerequisitos de `tasks.md` lo verifica y detiene el change antes de escribir código.
- **[No existe esquema ni infraestructura (C-01/C-02 pendientes)]** → task 1 de `tasks.md` es un gate verificable: si `docker-compose.yml`/esquema/`EXCLUDE` no existen, apply se declara bloqueado en lugar de fabricar una base alternativa (que además violaría DD-10).
- **[A re-escribe el scope de C-02/C-05/C-09 en `CHANGES.md`]** → registrado en D1; la actualización del roadmap es parte del trabajo de C-01/C-02, no de este change.
- **[Predicado del `EXCLUDE` con columna `estado` cuya ubicación en el modelo unificado no está decidida]** → `(TBD)`, se cierra en C-02; hasta entonces el shape del predicado es una propuesta, no un hecho.
- **[El spec afirma que el turno nace `confirmado`]** → **RESUELTO en apply (2026-10-06): el turno nace siempre `confirmado`**. La KB no tiene estado "pendiente" en el enum y el Flujo 1 inserta directo bajo la restricción; el turno queda cubierto por el `EXCLUDE` desde la escritura.
- **[Costo de A: re-scope de changes vecinos y DTOs distintos]** → aceptado explícitamente en D1; documentado para que el trade-off sea visible, no sorpresivo.
- **[Tests de concurrencia más lentos y dependientes de Docker]** → aceptado por DD-10; la alternativa (velocidad a costa de un verde falso) está rechazada.

## Migration Plan

Ninguno en este change: no se escribe código ni esquema (fase proposal). El esquema lo crea C-02 bajo la Opción A decidida en D1; cuando A esté confirmada, C-01/C-02 MUST re-leer `CHANGES.md` para alinear el scope de C-02, C-05 y C-09. Rollback: N/A.

## Open Questions

1. **Estado inicial del turno** — **RESUELTA (2026-10-06, tarea 1.3): el turno nace siempre `confirmado`.** Sin estado "pendiente" en el enum y con el Flujo 1 insertando directo bajo la restricción, se confirma que nace `confirmado`; el spec queda sin ajustes (sólo se removió la nota `(TBD)`).
2. **Eje "por profesional"** — **CONFIRMADO fuera de alcance (2026-10-06, tarea 1.4).** El objetivo de curso nomina solapamiento "por profesional", pero RN-AGE-03 y DD-03 sólo garantizan por **recurso** (sillón/box); no hay evidencia de la RN en la KB. Este change implementa exclusión por recurso únicamente. Si aplica, requiere una RN nueva (p. ej. RN-AGE-08) + restricción o validación adicional en un change nuevo.
3. **Predicado del `EXCLUDE` en el modelo unificado** — ubicación de `estado`/`motivo_cancelacion`/`token_público` en `reserva_agenda` vs tabla de detalle. `(TBD)` — se cierra en C-02.
4. **Turno-vs-bloqueo (RN-AGE-05)** — con Opción A la restricción ya lo cubre *cuando los bloqueos existan*, pero este change NO lo implementa ni lo prueba: el escenario "slot bloqueado" queda deliberadamente fuera del spec y DEBE agregarse en C-05, porque DD-10 exige cubrir turno-vs-turno y turno-vs-bloqueo por separado (`04_modelo_de_datos.md:244-247`).
5. **Prerequisitos C-01/C-02/C-03** — este proposal se emitió con OPSX fluido (propose antes de C-01..C-03); implementar exige que existan el stack, el esquema y — para el endpoint expuesto públicamente — el envoltorio de auth de C-03. Si no existen, apply se detiene en el task 1.
6. **Auditoría de agenda (RN-GEN-02)** — la KB no evidencia qué entidad audita crear turnos (`AuditoríaAcceso` está orientada a datos de salud). `(TBD)` — fuera del alcance de este change.
