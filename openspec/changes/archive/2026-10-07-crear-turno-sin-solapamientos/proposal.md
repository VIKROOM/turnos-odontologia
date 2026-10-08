# Proposal

> **Change**: `crear-turno-sin-solapamientos` · **Schema**: `spec-driven` · **Fecha**: 2026-10-06
> **Origen**: scope recortado de `[C-04] pacientes-turnos-core` (`CHANGES.md:134-143`).

## Why

El doble booking de la agenda es el fallo que mata la propuesta de producto: la reserva en línea debe completarse en menos de un minuto (`knowledge-base/05_reglas_de_negocio.md:115`) y dos pacientes que toman el mismo sillón al mismo milisegundo es exactamente el error que el usuario percibe como roto. Este change sale de `[C-04] pacientes-turnos-core` —el MVP recomendado en `CHANGES.md`— porque es la única regla de negocio de C-04 con criterio de aceptación binario y verifiable (RN-AGE-03: existe o no existe solapamiento), y es lo suficientemente acotada como para terminarse en un solo change sin tocar el resto de C-04.

## What Changes

- **Nuevo endpoint/servicio de creación de turno** que persiste un turno confirmado sobre un recurso (sillón/box) con intervalo `[inicio, fin)` y duración derivada de la configuración de la práctica (RN-AGE-01), con validación de disponibilidad en el servidor (RN-GEN-04) como línea de UX **y** la restricción `EXCLUDE USING gist` + `btree_gist` como garantía de integridad (RN-GEN-01).
- **Garantía de no-solapamiento por recurso** (RN-AGE-03) materializada en la base: dos inserts simultáneos del mismo intervalo sobre el mismo recurso SHALL producir **exactamente** un éxito y un rechazo, impuesto por la base de datos, no por el código de aplicación.
- **Mapeo de error de base → error de dominio**: la violación de la restricción de exclusión se traduce a un error de negocio tipado (`conflict`/solapamiento) que la API devuelve con un mensaje claro; la interfaz MUST NOT mostrar éxito si no hubo confirmación (RN-GEN-05).
- **Decisión de diseño A/B registrada**: `CHANGES.md:95` obliga a decidir entre Opción A (tabla única `reserva_agenda` con `tipo` + `EXCLUDE USING gist`) y Opción B (triggers cruzados) en C-01. Este change la resuelve en `design.md` (recomendación del Explore: **Opción A**) porque su esquema es la premisa de todo lo demás.
- **NO se implementa** ninguna de las otras faces de C-04 (ver out of scope).

### Out of scope (explícito)

| Fuera de alcance | Change dueño | Nota |
|---|---|---|
| Autenticación, roles, RBAC, JWT httpOnly | `[C-03] auth-users-roles` | El caso de uso se expone sin integrar auth; el wiring con C-03 queda `(TBD)` |
| ABM de pacientes (alta/baja/anulación) | `[C-04] pacientes-turnos-core` (resto) | El turno referencia un `paciente_id` existente; crear pacientes no forma parte de este change |
| Frontend / UI de reserva (React 18/Vite) | `[C-07]`, `[C-08] agenda-ui-reserva` | Sin componentes, sin rutas, sin llamadas HTTP desde el navegador |
| Bloqueos del odontólogo (turno-vs-bloqueo, RN-AGE-05) | `[C-05] disponibilidad-bloqueos` | Ver *Dependencias* abajo: A lo habilita, este change no lo implementa |
| Cancelación / reprogramación (RN-CAN-01/02, RN-AGE-07) | `[C-04] pacientes-turnos-core` (resto) | Extraído del scope para que este change sea terminable |
| Token público de un solo uso | `[C-04] pacientes-turnos-core` (resto) | `(TBD)` — mecanismo de entrega/invalidación no evidenciado en la KB |
| Motor de disponibilidad UX (franjas semanales, RN-AGE-02/04) | `[C-05] disponibilidad-bloqueos` | Este change sólo garantiza no-solapamiento, no "dentro de una franja" |

### Dependencias C-01 / C-02 / C-03 — cómo se manejan

La cadena del roadmap es `C-01 → C-02 → C-03 → C-04` (`CHANGES.md:21-36`) y **los tres están `[ ]` pendientes**; el repo está en fase 0 (sólo knowledge base y tooling, cero código). Este proposal **no** implementa ni re-implementa C-01/C-02/C-03. El manejo es:

1. **Decisión A/B adelantada a `design.md`**: el artefacto que `CHANGES.md:95` manda registrar en C-01 se registra aquí, porque es la premisa del esquema sobre el que este change escribe. No se crea infraestructura al hacerlo — sólo se decide.
2. **Gate de prerequisitos en `tasks.md`**: la tarea 1 verifica la existencia de `docker-compose.yml` con `postgres:15-alpine`, del esquema con `EXCLUDE USING gist` y del tooling de tests. Si no existen, apply se declara **bloqueado** y el change queda a la espera de C-01/C-02 — OPSX es fluido para *proponer*, no para *implementar* contra un esquema inexistente.
3. **Auth diferida**: el caso de uso se diseña como servicio puro sin dependencia de sesión; cómo lo envuelve C-03 (roles, JWT) queda `(TBD)` y se resuelve en el change de auth.
4. **Bloqueos (RN-AGE-05) diferidos a C-05**: con A elegido, la restricción de la tabla única ya cubre turno-vs-bloqueo *cuando los bloqueos existan*; este change sólo prueba turno-vs-turno y deja anotado en `design.md` que el caso turno-vs-bloqueo MUST probarse en C-05 (DD-10 exige los dos por separado).

## Capabilities

### New Capabilities

- `agenda/reservas`: creación de turnos sobre la agenda sin solapamiento por recurso — validación de disponibilidad en el servidor, restricción de exclusión declarativa en PostgreSQL, semántica `[inicio, fin)`, mapeo de conflicto a error de dominio y garantía de concurrencia. Cubre RN-AGE-01, RN-AGE-03, RN-GEN-01, RN-GEN-04, RN-GEN-05.

### Modified Capabilities

*(ninguno — `openspec list --specs --json` devuelve `{"specs": []}`: no hay specs existentes que modificar.)*

## Impact

- **Código (futuro — apply)**: `backend/` FastAPI: caso de uso puro en `domain/`, repositorio en `infrastructure/`, endpoint Pydantic validado en el borde. **Nada de esto se escribe en este change (fase proposal).**
- **Esquema de base**: requiere (no crea) la tabla de reserva con `btree_gist` y `EXCLUDE USING gist` — nace en C-02 bajo la Opción A decidida aquí.
- **Dependencias**: PostgreSQL 15 (`postgres:15-alpine`, DD-11) **en Docker**; el motor de exclusión hace que la DB no sea reemplazable (DD-05, costo aceptado).
- **Restricciones de proceso**: los tests de solapamiento exigen PostgreSQL real en Docker (AGENTS.md, DD-10) — hoy bloqueados: Docker Desktop 4.94.0 está instalado pero WSL2 requiere un reinicio pendiente (ver `design.md`).
- **Roadmap**: desbloquea la parte verificable de C-04; A habilita el scope de C-05 (turno-vs-bloqueo sobre la misma restricción) y obliga a re-leer C-02/C-05/C-09 en `CHANGES.md`, redactados hoy suponiendo tablas separadas.
