# Explore — crear-turno-sin-solapamientos

> **Fase**: `explore` (OPSX) · **Fecha**: 2026-10-06
> **Change candidato**: `[C-04] pacientes-turnos-core` (`CHANGES.md:134-143`)
> **Alcance de esta nota**: relevamiento (read + write-docs). Sin código de producción, sin artifacts bajo `openspec/changes/`.
> **Idioma**: español. Los keywords estructurales de OpenSpec (`proposal.md`, `design.md`, `tasks.md`, `Change`, `spec`) se mantienen en inglés.

---

## Problema

El problema de negocio es el **doble booking de la agenda**: dos pacientes (o un paciente y el odontólogo) tomando el mismo espacio físico al mismo tiempo.

- Discovery determinó que el recurso escaso es **el sillón/box, no el profesional**: "Discovery identificó el recurso —y no el profesional— como lo escaso, y por eso el modelo de datos de `04_modelo_de_datos.md` indexa los turnos por recurso (DD-03)" (`knowledge-base/05_reglas_de_negocio.md:22-24`, "Qué es un 'recurso'").
- La consecuencia operativa está en la raíz del producto: "El paciente odia llamar por teléfono" → "la reserva se completa en menos de un minuto" (`05_reglas_de_negocio.md:115`). Una reserva en línea que choca es exactamente el fallo que mataría la propuesta.
- El mecanismo del problema está descrito en `04_modelo_de_datos.md` §"La restricción que evita el doble booking": "si la validación de disponibilidad vive solo en el backend, dos peticiones simultaneas pueden leer el mismo slot libre y escribir dos turnos". Y de forma cruda en `07_flujos_principales.md` §Flujo 2 (dos pacientes, mismo milisegundo): "este flujo no se puede probar con un test unitario. Requiere Postgres real y dos conexiones concurrentes".
- Las reglas que lo expresan son **RN-AGE-03** (turno vs turno, mismo recurso) y **RN-AGE-05** (bloqueos del odontólogo que compiten por el mismo recurso), más **RN-GEN-01** ("Ninguna escritura de turno se completa sin pasar la validación de disponibilidad y la restricción de exclusión de la base").

### Relación con el alcance de `[C-04] pacientes-turnos-core`

`CHANGES.md:134-143` define el scope de C-04 como: **"ABM paciente, crear/cancelar/reprogramar turnos, validación app + DB, cancelación anticipada, token autogendamiento"**, governance **ALTO**, dependencias `C-03`.

El objetivo más angosto —*"crear un turno evitando solapamientos por profesional y por sillón/box"*— se relaciona con C-04 así:

1. **C-04 es quien implementa el "crear turno"** (Flujo 1 de `07_flujos_principales.md`), el único punto donde la regla RN-AGE-03 se ejerce en escritura. Pero **la garantía no vive en C-04**: vive en el esquema que crea `C-02` (`EXCLUDE USING gist`, ver `CHANGES.md:104-117`). C-04 consume la restricción, no la define. La validación de aplicación (motor de disponibilidad) es "optimización y experiencia de usuario, no garantía de integridad" (`04_modelo_de_datos.md:188-190`).
2. **El eje "sillón/box" sí está en el modelo; el eje "por profesional" NO.** RN-AGE-03 dice textualmente "del mismo recurso (sillón o box)" y DD-03 fija que "el turno cuelga de un recurso (el sillón), no de un profesional ni de un consultorio". **No es evidenciado en la KB** ninguna restricción de exclusión por profesional; `04_modelo_de_datos.md` solo modela `recurso_id` en el `EXCLUDE`. Si el objetivo pide ambas dimensiones, eso es una decisión nueva que debe pasar por Propose (ver *Preguntas abiertas*).
3. **El eje "bloqueo" (RN-AGE-05) queda fuera del alcance garantizado de C-04**: C-04 sólo crea turnos; el turno-vs-bloqueo depende de la deuda A/B sin decidir y se reparte entre `C-02` (esquema) y `C-05 disponibilidad-bloqueos` (`CHANGES.md:145-154`). Hoy la KB es explícita: la garantía de DD-05 "es **parcial**: cubre turno contra turno... pero no cubre turno contra bloqueo, que RN-AGE-05 y US-004-CA-1 dan por sentado" (`04_modelo_de_datos.md:222-224`).
4. **Cadena de dependencias**: `C-01 → C-02 → C-03 → C-04` (`CHANGES.md:21-36`). No hay forma legítima de empezar C-04 hoy: no existe el esquema (C-02), ni auth (C-03), ni infraestructura (C-01). Además, la **decisión A/B es obligatoria en C-01** (`CHANGES.md:95`) y su resultado redefine el esquema sobre el que C-04 escribe.

En síntesis: el change que *resuelve* el problema en el aire es la pareja `C-02` (EXCLUDE declarativa) + `C-04` (escritura de turno con validación); C-04 es la cara visible del Flujo 1, pero sin C-01/C-02/C-03 (y sin la decisión A/B) no hay por dónde implementarlo.

---

## Estado del código

### Existe (evidencia: listado de filesystem, 2026-10-06)

```
turnos-odontologia/
├── .atl/skill-registry.md
├── .claude/, .opencode/           # comandos y skills OPSX (propose/apply/archive/explore/sync/update)
├── .active-orchestrator-state.json
├── AGENTS.md                      # reglas duras del proyecto
├── CHANGES.md                     # roadmap, 10 changes, ninguno completado
├── CLAUDE.md, README.md
├── capturar-evidencia.ps1
├── discovery/                     # discovery.md, verificacion-fuentes.md, sources/*.md (20 fuentes)
├── docs/
│   ├── discovery/                 # informe-discovery.md/.pdf, checklist-discovery.md
│   └── etapa0/                    # README, harnesses-instalados.md, 2 PNG
├── knowledge-base/                # 01..10 canonicals completos
└── openspec/
    ├── config.yaml                # schema: spec-driven; artifacts en español, keywords en inglés
    ├── specs/.gitkeep
    └── changes/archive/.gitkeep
```

### NO existe (verificado con glob + `Test-Path`, no asumido)

| Artefacto | Verificado |
|---|---|
| `backend/`, `frontend/`, `src/`, `tests/` | `Test-Path` → `False` |
| `docker-compose.yml` | `Test-Path` → `False` |
| `pyproject.toml` / `package.json` / alembic / migraciones | no en el listado glob `**/*` |
| `openspec/changes/*` con contenido | sólo `openspec/changes/archive/.gitkeep`; `openspec list --json` → `{"changes": []}` (0 changes) |
| `.env.example` | no en el listado |

**Estado**: el proyecto está en **fase 0 — sólo knowledge base y tooling**. Cero de los 10 changes de `CHANGES.md` tienen estado `[x]`. No hay código que testear, no hay baseline de tests, no hay infraestructura. Todo lo que este relevamiento describe es *diseño previsto*, no implementación existente.

---

## Reglas de negocio aplicables

Citadas textualmente de `knowledge-base/05_reglas_de_negocio.md`. Origen tal como lo marca la KB (`Discovery` = del relevamiento; `Propuesta` = decisión de diseño sin verificar en el mercado).

### Dominio Agenda (RN-AGE) — creación de turno

- **RN-AGE-01**: "Un turno ocupa un intervalo cerrado `[inicio, fin)` y tiene una duración asociada a la práctica. Origen: Discovery. La duración la define el odontólogo por práctica y **no es un parámetro libre del paciente**: es lo que impide que un turno de 15 minutos bloquee el sillón una hora." (`:30-33`)
- **RN-AGE-02**: "La disponibilidad se define por franjas semanales por recurso (sillón o box). Origen: Discovery. Un mismo profesional puede tener varias franjas, y un mismo recurso puede tener franjas que cambian por semana." (`:34-36`)
- **RN-AGE-03** *(decisiva — no overlap)*: "No puede existir solapamiento entre turnos confirmados del mismo recurso (sillón o box). Origen: Discovery. Implementado en la capa de datos, ver `04_modelo_de_datos.md`." (`:37-39`)
- **RN-AGE-04**: "Un turno debe quedar dentro de una franja de disponibilidad. Origen: Discovery. Si la franja se reduce después, los turnos ya confirmados se respetan y se avisa al odontólogo de los que quedaron fuera." (`:40-42`)
- **RN-AGE-05** *(bloqueos)*: "El odontólogo puede bloquear una franja (feriado, vacaciones, uso personal). Origen: Discovery. El bloqueo es un objeto de primera clase, no un turno ficticio." (`:43-45`)
- **RN-AGE-06**: "Un paciente puede tener varios turnos simultaneos para Prácticas distintas siempre que no se solapen en el tiempo. Origen: Discovery." (`:46-47`) *(texto tal cual; la redacción es internamente ambigua — ver Preguntas abiertas)*
- **RN-AGE-07** *(reprogramación)*: "La reprogramación cancela el turno anterior y crea uno nuevo, en una sola transacción. Origen: Propuesta. Un turno nunca se 'mueve': se reemplaza, para conservar el historial." (`:48-50`)

### Dominio Excepciones y límites globales (RN-GEN) — restringen crear turno

- **RN-GEN-01**: "Ninguna escritura de turno se completa sin pasar la validación de disponibilidad y la restricción de exclusión de la base. Origen: Propuesta." (`:95-96`)
- **RN-GEN-04**: "El horario de operación es del consultorio y se valida en el servidor, nunca solo en el navegador. Origen: Propuesta." (`:102-103`)
- **RN-GEN-05**: "Si el servicio no puede confirmar un turno, la interfaz nunca muestra éxito. Origen: Propuesta. Es la regla que evita el falso positivo en la reserva en línea." (`:104-106`)
- **RN-GEN-02**: "Toda operación que cambie la agenda escribe una fila de auditoría. Origen: Propuesta." (`:97-98`)

### Cancelación anticipada (en scope de C-04)

- **RN-CAN-01**: "El paciente puede cancelar sin costo hasta un plazo mínimo definido por el consultorio. Origen: Propuesta. Discovery no evidencio cual es el plazo que el mercado considera aceptable. Ver PREG-04." (`:54-56`)
- **RN-CAN-02**: "Pasado el plazo mínimo, la cancelación queda registrada con la marca temporal y la razon (`cancelado_por`, `cancelado_at`). Origen: Propuesta." (`:57-58`)

### Restricciones de trazabilidad (AGENTS.md, hard rules)

De `AGENTS.md` (inyectado como reglas del repo):

- "NUNCA resolver el solapamiento de turnos en el backend → dejá la garantía a `EXCLUDE USING gist` + `btree_gist`; el motor de disponibilidad es UX, no integridad." (DD-05, DD-10, DD-11)
- "NUNCA testear solapamiento contra SQLite o un doble en memoria → PostgreSQL real en Docker."
- "NUNCA reprogramar moviendo un turno → cancelar + crear en una sola transacción (RN-AGE-07)."
- "NUNCA saltar la validación Pydantic en el borde → el navegador no es la frontera (RN-GEN-04)."
- "Toda regla de negocio implementada se referencia por su código `RN-XX` en el change y sus tests."

### La restricción concreta (modelo, no código todavía)

`knowledge-base/04_modelo_de_datos.md:175-181`:

```sql
EXCLUDE USING gist (
  recurso_id WITH =,
  tstzrange(inicio, fin) WITH &&
)
WHERE (estado = 'confirmado')
```

Cubre **turno-vs-turno** con `btree_gist`. Efectos declarados (`:183-193`): dos inserts simultáneos → uno falla y la API responde conflicto; el test es de integración contra Postgres real; el motor de disponibilidad sigue siendo necesario pero como UX. Costo aceptado: Postgres deja de ser reemplazable (DD-05).

---

## Decisión de diseño pendiente

Fuente: `knowledge-base/04_modelo_de_datos.md` §"Deuda de diseño: la exclusión entre `Turno` y `Bloqueo`" (`:195-249`).

> **Estado según KB**: "abierta. No decidida. Requiere decisión del equipo antes de implementar el turno y el bloqueo. Registrada el 2026-10-05". `CHANGES.md:95` la convierte en **decisión obligatoria de C-01**, a registrar en `design.md` (o `docs/decisions/`).

### El problema

Una restricción `EXCLUDE USING gist` pertenece a **una sola tabla**; no puede abarcar `Turno` y `Bloqueo` a la vez. Con el esquema actual, "Turno confirmado: 10:00 a 10:30 en el sillón 1 → se guarda / Bloqueo del odontólogo: 10:15 a 11:00 en el sillón 1 → TAMBIÉN se guarda" (`:212-215`). La garantía de DD-05 queda **parcial**: cubre RN-AGE-03 pero no RN-AGE-05 ni US-004-CA-1 (`:222-224`).

### Opción A vs Opción B (tal como la KB las plantea)

| | **Opción A — Tabla única de reserva de agenda** | **Opción B — Trigger de verificación cruzada** |
|---|---|---|
| **Cómo funciona** | `Turno` y `Bloqueo` pasan a ser filas de una tabla `ReservaAgenda` con campo discriminador (`tipo`). La restricción `EXCLUDE` vive **una sola vez**, sobre esa tabla. Los datos de `Turno` (paciente, práctica, token) quedan en una tabla aparte relacionada | Se conserva el esquema actual y se agrega un trigger `AFTER INSERT OR UPDATE` sobre ambas tablas que consulta la tabla hermana y aborta si encuentra solapamiento |
| **Costo (según KB)** | "Reescritura del esquema. `Turno` deja de ser una tabla y pasa a ser un detalle de la reserva. Es la solución que un motor de agenda real usa" | "Dos triggers que se mantienen sincronizados. Un trigger mal escrito es un bug silencioso: la garantía depende de código, no del declarativo" |

### Lo que la KB exige **cualquiera sea la opción** (`:238-249`)

- La validación de disponibilidad debe seguir existiendo: "La exclusión nunca fue la primera línea, fue la red."
- El test de solapamiento debe cubrir **los dos casos por separado**: turno-vs-turno y turno-vs-bloqueo (DD-10).
- Ambas opciones conservan el requisito duro de PostgreSQL → DD-05 no se ve afectada.

### RECOMMENDATION

> ⚠️ ***Propuesta, pendiente de aprobar en `design.md` (C-01). No es una decisión tomada.***

**Recomendación: Opción A (tabla única `reserva_agenda` + `EXCLUDE USING gist` una sola vez).**

Justificación, acotada a lo que la KB dice:

1. **El costo de A se paga cero hoy.** El coste de A es "reescritura del esquema", y el repo **no tiene esquema**: `openspec list --json` → 0 changes, `Test-Path backend/src/tests/docker-compose.yml` → `False`. Reescribir un esquema que no existe no cuesta nada; hacerlo después de C-02..C-04 sí costaría caro.
2. **Cumple ambas reglas de forma declarativa.** A resuelve RN-AGE-03 **y** RN-AGE-05 con la misma restricción, mientras que B sólo garantiza RN-AGE-03 y deja turno-vs-bloqueo en "código que puede fallar en silencio". `US-004-CA-1` queda cubierto sin lógica extra.
3. **Alinea con la hard rule de `AGENTS.md`**: "dejá la garantía a `EXCLUDE USING gist`... la integridad no depende de que el código de aplicación la respete" (también `08_arquitectura_propuesta.md:21`, patrón "Exclusión constraint"). Un trigger parcialmente sincronizado acerca la garantía al código, que es lo que DD-05 rechazó explícitamente.
4. **Reduce la superficie de tests**: una restricción, un camino de fallo, un test de concurrencia cubre ambos casos — relevante porque DD-10 exige Postgres real y los tests son caros (ver bloqueo Docker más abajo).
5. La propia KB señala a A como "la solución que un motor de agenda real usa" y a B con el adjetivo "bug silencioso"; no hay adjetivo equivalente del lado de B.

**Contra-argumentos a registrar en `design.md`** (para que la decisión sea informada, no por omisión):

- A obliga a **re-escribir el scope de `C-02`, `C-05` y `C-09`** en `CHANGES.md`, que hoy están redactados suponiendo tablas separadas (`CHANGES.md:104-117`, `145-154`, `196-211`).
- A cambia el modelo de consultas y los DTOs que consumirá C-04 (Flujo 1, US-006/US-007).
- Queda por diseñar el predicado del `EXCLUDE` en el modelo unificado: la restricción actual filtra `WHERE (estado = 'confirmado')`, pero `Bloqueo` no tiene `estado` → algo como `WHERE (tipo = 'bloqueo' OR estado = 'confirmado')`. **Detalle no evidenciado en la KB**; corresponde a `design.md`.

**Si el equipo eligiera B**, exijamos al menos: triggers `AFTER` con verificación + `RAISE EXCEPTION`, tests de los dos caminos en C-09, y una nota explícita en `design.md` de que la garantía RN-AGE-05 depende de código, contra el espíritu de DD-05.

---

## Riesgos y bloqueos

1. **🔴 BLOQUEO ABIERTO — Docker/WSL2 sin reinicio (verificado en esta sesión).**
   - Docker Desktop **4.94.0.241994** instalado en `C:\Program Files\Docker\Docker\Docker Desktop.exe`, pero **`docker` no está en el PATH** de la shell (`docker version` → comando no reconocido).
   - `wsl --status` → **"El Subsistema de Windows para Linux no está instalado"** — WSL2 requiere el reinicio pendiente + `wsl --install`.
   - `AGENTS.md` prohíbe testear solapamiento contra SQLite o doble en memoria y exige "PostgreSQL real en Docker"; `DD-10` (`09_decisiones_y_supuestos.md:133-145`) exige PostgreSQL real en Docker; el Flujo 2 necesita "Postgres real y dos conexiones concurrentes" (`07_flujos_principales.md:65-67`).
   - **Consecuencia**: la fase **verify/apply no puede correr ningún test de solapamiento hasta reiniciar la máquina, completar la instalación de WSL2 y tener `docker` en el PATH**. Debe tratarse como blocker explícito del change, no silenciarse. Riesgo residual: Docker Compose y `postgres:15-alpine` (C-01) nunca se levantaron en esta máquina — la primera corrida puede fallar por configuración además del PATH.
2. **🔴 Sin infraestructura previa**: C-04 depende de C-01 → C-02 → C-03 y los tres están `[ ]`. Además el test de C-04 no tiene dónde correr: no existe `docker-compose.yml`, ni tooling de tests (pytest/vitest), ni baseline ("X tests pasando") que sea posible capturar.
3. **🔴 Decisión A/B sin tomar y con fecha límite**: debe resolverse en **C-01** (`CHANGES.md:95`). Si C-02 se implementa con el esquema actual y después se elige A, hay migración extra. C-04 no debería arrancar antes de que `design.md` fije A/B.
4. **🟡 Mismatch de versión de PostgreSQL**: DD-11 y `CHANGES.md:7` fijan **PostgreSQL 15** (`postgres:15-alpine`); en esta máquina corre **PostgreSQL 17.11 nativo** (servicio `postgresql-x64-17`, estado `Running`; `psql` tampoco está en el PATH). La DB nativa **no sirve como sustituto** de Docker según DD-10. Riesgo bajo pero a registrar: ¿se testea contra 15 (stack decidido) o 17 (lo instalado)? `EXCLUDE USING gist` existe en ambas; la decisión de imagen la toma C-01.
5. **🟡 Ambigüedad "por profesional"**: el objetivo nomina solapamiento "por profesional", la KB sólo garantiza "por recurso". Sin clarificación, C-04 podría implementar una validación que nadie pidió o faltar una que sí (ver Preguntas abiertas).
6. **🟡 Frontera de scope C-04 vs C-05**: crear turno sin conocer bloqueos deja RN-AGE-05 a medias en el Flujo 1 (el paciente no ve los bloqueos si el motor de disponibilidad de C-05 no existe). C-04 debe decidir si valida sólo turno-vs-turno (garantizado por C-02) o también contra bloqueos (depende de A/B y de C-05).
7. **🟡 RN-GEN-02 vs modelo de auditoría**: "toda operación que cambie la agenda escribe una fila de auditoría", pero `AuditoríaAcceso` está modelada orientada a accesos a datos de salud (`04_modelo_de_datos.md:154-164`). No está evidenciado en la KB qué tabla/modelo audita cancelación y reprogramación de turnos.
8. **🟡 Governance**: C-04 es ALTO (implementar con checkpoints y decisiones visibles); C-01, C-02 y C-09 son CRITICO. La decisión A/B cae en un change CRITICO → confirmación humana antes de escribir.

---

## Preguntas abiertas

Cosas **no decididas** que deben volver a **Propose** (y donde corresponda, resolverse en `design.md` de C-01 antes que C-02/C-04):

1. **A vs B**: ¿tabla única `reserva_agenda` o triggers cruzados? Recomendación arriba (*propuesta, pendiente de aprobar en `design.md`*). Incluye: predicado del `EXCLUDE` en el modelo unificado y destino de `token_público`, `estado`, `motivo_cancelacion`.
2. **¿Solapamiento "por profesional"?** El objetivo lo pide; RN-AGE-03 y DD-03 sólo garantizan por recurso. **No evidenciado en la KB**. Si dos profesionales comparten sillón, ¿importa el choque por profesional? Si sí, es una RN nueva (p. ej. RN-AGE-08) + restricción o validación nueva.
3. **Alcance exacto de C-04**: ¿sólo ABM paciente + crear/cancelar/reprogramar con validación turno-vs-turno, o también la dimensión bloqueo (RN-AGE-05)? Depende de 1 y de la secuencia respecto de C-05.
4. **Plazo mínimo de cancelación** (RN-CAN-01): valor por defecto no definido ("Discovery no evidencio cual es el plazo"; PREG-04). `08_arquitectura_propuesta.md:108` sólo ofrece `CANCELLATION_MIN_HOURS=24` como *ejemplo*. ¿Es 24h el valor del v1 y quién lo configura?
5. **Semántica del estado inicial**: el `EXCLUDE` filtra `estado = 'confirmado'`; el Flujo 1 inserta y la base aplica la restricción de inmediato, lo que sugiere que el turno nace `confirmado`. No hay estado "pendiente" en el enum. **Confirmar en design/tasks**: ¿nace siempre `confirmado`?
6. **Token "de un solo uso"** (US-008 CA-1, scope C-04 "token autogendamiento"): el modelo sólo dice `token_público uuid UNIQUE NOT NULL` y `AGENTS.md` exige fuente criptográfica ≥128 bits. **No evidenciado en la KB**: cómo se invalida tras una escritura, ni el mecanismo de entrega (¿e-mail? ¿link?).
7. **Auditoría de agenda** (RN-GEN-02): ¿qué entidad/modelo registra crear/cancelar/reprogramar turno, si `AuditoríaAcceso` está pensada para datos de salud?
8. **Ambigüedad de redacción de RN-AGE-06**: "varios turnos simultaneos... siempre que no se solapen en el tiempo" es contradictorio en sus términos. Requiere aclaración antes de escribir tests que la referencien.
9. **Versión de PostgreSQL para tests**: 15 (DD-11/stack) vía imagen Docker vs 17.11 nativo de la máquina. Recomendación implícita: respetar la imagen de C-01 (`postgres:15-alpine`); la nativa queda descartada por DD-10.
10. **Secuencia práctica**: ¿C-04 se propone antes de que exista C-01..C-03 (proposal adelantada) o recién tras C-03? `CHANGES.md` dice dependencia de C-03; OPSX es fluido, pero implementar contra un esquema inexistente no es posible.

---

### Trazabilidad de fuentes

| Fuente | Uso en este relevamiento |
|---|---|
| `CHANGES.md` | scope/dependencias de C-01..C-10, decisión A/B obligatoria en C-01 |
| `knowledge-base/05_reglas_de_negocio.md` | RN-AGE-01..07, RN-GEN-01/02/04/05, RN-CAN-01/02, definición de recurso |
| `knowledge-base/04_modelo_de_datos.md` | entidades turno/recurso/practica/paciente, `EXCLUDE USING gist`, deuda A/B |
| `knowledge-base/08_arquitectura_propuesta.md` | layering (`domain/` no importa `infrastructure/`), stack DD-11, patrones |
| `knowledge-base/07_flujos_principales.md` | Flujo 1 (reserva), Flujo 2 (concurrencia), Flujo 4/5 (cancelar/reprogramar) |
| `knowledge-base/06_funcionalidades.md` | US-007 (reservar), US-006 (ver horarios), US-004 (bloquear), US-009/010 (cancelar/reprogramar), US-014 (anular paciente) |
| `knowledge-base/09_decisiones_y_supuestos.md` | DD-03, DD-05, DD-10, DD-11 |
| `AGENTS.md` | hard rules de integridad, arquitectura, seguridad, trazabilidad RN-XX |
| Filesystem + CLI | `Test-Path`, glob `**/*`, `openspec list --json`, `docker`/`wsl`/`psql` probes |
