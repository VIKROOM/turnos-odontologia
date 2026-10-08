# Etapa 7 — Memoria del agente (Engram)

> Evidencia de la memoria persistente del agente sobre el proyecto `turnos-odontologia`.
> Consulta real ejecutada el 2026-10-07. Se muestra en vivo en el video de defensa.

## Qué quedó guardado

Engram (proyecto `turnos-odontologia`, 1 sesión, 16 observaciones) guarda decisiones,
hallazgos y convenciones de cada fase:

| Fase | Observaciones guardadas (título abreviado) |
|---|---|
| Entorno (Etapa 0) | Setup Go/Docker/WSL2/Active Stack Full; reinicio pendiente |
| Explore (Etapa 6) | Relevamiento del problema doble-booking, RN-AGE-03/RN-AGE-05 |
| Propose | Artefactos de `crear-turno-sin-solapamientos` (13 escenarios, Opción A) |
| Apply C-01/C-02 | `foundation-setup` y `core-models-schema` aplicados (migración Alembic + EXCLUDE USING gist) |
| Hallazgo local | Conflicto de puerto 5432 (PG 17 nativo ensombrece el contenedor) |
| Ajustar | Ampliación del mapeo de conflicto a `{23P01, 40P01}` → 409 |
| Apply (24 tasks) | TDD completado: 39/39 tareas, 44 tests verdes, conteos RN-XX |
| Archive | Change archivado 2026-10-07; spec promovida a `openspec/specs/agenda/reservas/spec.md` |

## Consulta real que recupera contexto de una sesión anterior

Comando (herramienta `mem_search` de Engram):

```
query: "puerto 5432 PostgreSQL nativo ensombrece contenedor db"
project: turnos-odontologia
```

Resultado — observación #9 de la sesión del 2026-10-06:

> **Conflicto de puerto 5432: PostgreSQL nativo ensombrece el contenedor db**
> El host tiene PostgreSQL 17 nativo escuchando en 0.0.0.0:5432 (PID postgres.exe)
> que ENSOMBRECE el puerto publicado del contenedor `db`. La conexión del host a
> localhost:5432 cae en el Postgres nativo (rechaza password), no en el contenedor.
> **Mitigación** = publicar el contenedor en `DB_PORT=5433` (interno sigue 5432) y que
> el fixture `tests/conftest.py` reconstruya la URL hacia `localhost:$DB_PORT`.
> (creada: 2026-10-06 23:31:06, topic: config/local-db-port-conflict)

## Cómo esta consulta evita arrancar de cero

1. **La información ya existía** de la sesión anterior: el hallazgo del puerto se guardó
   automáticamente como parte del protocolo de memoria (trigger: descubrimiento no obvio).
2. **Se recuperó al briefear el apply**: al continuar el ciclo OPSX en una sesión nueva
   (sin contexto), el sub-agente de apply recibió el dato de que `localhost:5432` cae en el
   PG 17 nativo y que los tests deben correr contra `DB_PORT=5433`. Sin esa memoria, el
   primer run de tests habría fallado por contraseña (PG nativo) o habría tentado a
   testear contra el PG 17, violando DD-11 (`postgres:15-alpine`).
3. **Ahorro medido**: se saltó todo el diagnóstico del puerto (netstat, identificación del
   PID postgres.exe, decisión de overrides) y la suite corrió contra el contenedor correcto
   desde el primer intento — 44/44 verdes.

El patrón general: cada cambio guarda su estado en `opsx/<change>/<fase>`, de modo que una
sesión nueva — o un agente subcontratado sin contexto — puede reconstruir el proyecto con
una consulta en lugar de releer todo el repositorio.

## Para el video (pantalla real, ~1 minuto)

1. Abrir el cliente de OpenCode/Claude con Engram conectado.
2. Mostrar `mem_context` (proyecto `turnos-odontologia`) → lista de observaciones.
3. Ejecutar la consulta `puerto 5432 PostgreSQL nativo` → mostrar la observación #9 recuperada.
4. Explicar el vínculo: ese hallazgo se usó en apply (`.env` con `DB_PORT=5433`, conftest) y
   permitió correr los tests contra PostgreSQL 15 real sin rediagnosticar.