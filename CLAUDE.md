# AGENTS.md — Reglas del proyecto (turnos-odontologia)

> Específico del proyecto. No duplica reglas globales. Lee esto antes de actuar.

## Propósito
Este archivo fija reglas duras que gobiernan a todo agente que trabaje en este repo.

## Hard Rules (stack-aware)

### Integridad de datos (PostgreSQL 15 / DD-05, DD-10, DD-11)
- NUNCA resolver el solapamiento de turnos en el backend → dejá la garantía a `EXCLUDE USING gist` + `btree_gist`; el motor de disponibilidad es UX, no integridad.
- NUNCA testear solapamiento contra SQLite o un doble en memoria → PostgreSQL real en Docker.
- NUNCA cambiar la base de datos → sin `EXCLUDE USING gist` no hay DD-05.

### Arquitectura (08_arquitectura_propuesta.md)
- NUNCA importar `infrastructure/` desde `domain/` → la dependencia va en un solo sentido.
- NUNCA saltar la validación Pydantic en el borde → el navegador no es la frontera (RN-GEN-04).
- NUNCA reprogramar moviendo un turno → cancelar + crear en una sola transacción (RN-AGE-07).

### Seguridad / Privacidad (RN-AU-02, RN-PRIV-*)
- NUNCA guardar el JWT en `localStorage` → cookie `httpOnly` + `SameSite` + validación de `Origin`/CSRF en escrituras (DD-09).
- NUNCA generar `token_público` con `uuid4()`/`random()` → fuente criptográfica, ≥128 bits medidos.
- NUNCA hardcodear secretos → env vars, con `SECRET_KEY` y `ENCRYPTION_KEY` separadas.
- NUNCA devolver un error que revele si un paciente o turno existe.
- NUNCA enviar historial clínico al asistente IA → solo disponibilidad (DD-07).
- NUNCA editar ni borrar `AuditoríaAcceso` → append-only; auditar **antes** de leer (RN-PRIV-03).
- NUNCA borrar datos de contacto de un paciente → se anulan (RN-PRIV-04).
- NUNCA mostrar éxito en la UI si la reserva no se confirmó (RN-GEN-05).

### Frontend (React 18/Vite/TS)
- NUNCA usar `any` → `tsconfig` estricto; componentes en `PascalCase`.

### Trazabilidad
- Toda regla de negocio implementada se referencia por su código `RN-XX` en el change y sus tests.

### Universales
- NUNCA commitear/pushear sin pedido explícito. NUNCA buildear ni correr migraciones sin pedido.
- Commits convencionales, sin co-autoría IA.

## Referencias
- `knowledge-base/` — 10 canonicals (lectura obligatoria según change)
- `CHANGES.md` — índice operativo con dependencias, gates, camino crítico
- `.atl/skill-registry.md` — skills con compact rules
- `openspec/changes/` — specs por change
