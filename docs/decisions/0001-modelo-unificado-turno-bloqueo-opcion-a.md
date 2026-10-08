# Decisión 0001 — Modelo unificado de reserva de agenda (Opción A)

> Puntero de acceso rápido para changes posteriores (C-02 `core-models-schema`,
> C-05, C-09). No reabre el debate: lo registra. Fuente canónica en
> `knowledge-base/04_modelo_de_datos.md` y decisión **D1** de
> `openspec/changes/crear-turno-sin-solapamientos/design.md`.

## Estado

**Cerrada — Opción A.** Registrada por C-01 (`foundation-setup`) conforme a la
obligación de `CHANGES.md:95`.

## Decisión

`Turno` y `Bloqueo` conviven como filas de una **tabla única** `reserva_agenda`
con campo discriminador `tipo = 'turno' | 'bloqueo'`. La restricción
`EXCLUDE USING gist (tstzrange(inicio, fin, '[)') WITH &&)` vive **una sola vez**
sobre esa tabla (con la extensión `btree_gist`). Los datos de negocio del turno
(paciente, práctica, token) van en una tabla de detalle relacionada.

El no-solapamiento SHALL quedar garantizado en el declarativo
(`EXCLUDE USING gist`) y MUST NOT resolverse con triggers ni lógica de
aplicación (DD-05; hard rule de `AGENTS.md`). El motor de disponibilidad es UX,
no integridad.

## Justificación (resumen)

- Un trigger de exclusión es un bug silencioso y viola DD-05/AGENTS.md.
- La Opción B deja turno-vs-bloqueo "a responsabilidad de la aplicación" — el
  estado parcial que la KB diagnostica como defecto.
- Opción A concentra el camino de fallo en un único constraint (menor superficie
  de tests bajo DD-10) y su costo de reescritura de esquema es cero hoy (fase 0).

## Referencias cruzadas

- `knowledge-base/04_modelo_de_datos.md:195` — §"Deuda de diseño: la exclusión
  entre `Turno` y `Bloqueo`.
- `knowledge-base/04_modelo_de_datos.md:226-237` — §"Las dos salidas".
- `openspec/changes/crear-turno-sin-solapamientos/design.md` — decisión **D1**.
- `openspec/changes/foundation-setup/design.md` — decisión **D1** (registro).
- `CHANGES.md:95` — obligación de registro de la deuda A/B.

## Consecuencias (ya aceptadas, TBD se resuelven en C-02)

- Re-scope de C-02 / C-05 / C-09 sobre el modelo unificado.
- Ubicación final de `estado`, `motivo_cancelacion` y `token_público` en el
  modelo unificado queda `(TBD)` para C-02.
- Los tests de exclusión/concurrencia corren contra PostgreSQL 15 real en Docker
  (`postgres:15-alpine`); prohibidos SQLite y dobles en memoria (DD-10).
