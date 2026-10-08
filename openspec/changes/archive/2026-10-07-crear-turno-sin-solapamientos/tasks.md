# Tasks

## 1. Gate de prerequisitos y aclaraciones previas

- [x] 1.1 Ejecutar el checklist de prerequisitos (docker en el PATH, WSL2 activo, `docker-compose.yml` con `postgres:15-alpine`, esquema con la restricción de exclusión de `design.md` D2, tooling pytest) — verify: el checklist imprime estado por ítem; si algún ítem falta, apply SE DETIENE ACÁ y se reporta "bloqueado por C-01/C-02/entorno" sin escribir código
- [x] 1.2 Verificar que el PostgreSQL de los tests es la imagen Docker `postgres:15-alpine` y NO el 17.11 nativo de la máquina — verify: `docker compose exec -T db psql ... -c "SHOW server_version"` devuelve 15.x
- [x] 1.3 Resolver con el usuario el `(TBD)` de `design.md` Open Questions 1 (estado inicial del turno: ¿nace `confirmado`?) antes de escribir cualquier código — verify: la decisión queda registrada en `design.md` y el spec se ajusta si hiciera falta
- [x] 1.4 Confirmar que el eje "por profesional" (`design.md` Open Questions 2) sigue fuera de alcance de este change — verify: no aparece ninguna tarea ni test que implemente exclusión por profesional; si el usuario lo pide, se abre un cambio nuevo

## 2. Dominio puro: duración e intervalos (TDD unitario, sin base)

- [x] 2.1 RED: escribir el test unitario `fin_derivado_de_practica` (dado inicio 10:00 y práctica de 30 min → fin 10:30) — verify: el test FALLA porque el módulo `domain/agenda/` no existe
- [x] 2.2 GREEN: implementar en `domain/` el cálculo `fin = inicio + duración(práctica)` — verify: el test 2.1 pasa
- [x] 2.3 RED: escribir el test unitario de semántica semiabierta — `finA == inicioB` NO solapa, `inicioA == inicioB` SÍ solapa, `inicioA == inicioB` con otro recurso no compara — verify: el test FALLA porque la función de solapamiento no existe
- [x] 2.4 GREEN: implementar la comprobación de solapamiento `[inicio, fin)` en `domain/` — verify: el test 2.3 pasa
- [x] 2.5 TRIANGULAR: ampliar los tests con intervalo contenido, intervalo disjunto, intervalo que termina cuando otro empieza y el mismo intervalo en otro recurso — verify: suite unitaria verde; si un caso nuevo rompe la lógica, generalizar la implementación
- [x] 2.6 REFACTOR: extraer constantes/nombres en `domain/agenda/` sin cambiar comportamiento — verify: la suite unitaria sigue 100% verde

## 3. Caso de uso y endpoint de creación (TDD integración, PostgreSQL real)

- [x] 3.1 RED: escribir el test de integración del camino feliz (turno 10:00–10:30 en sillón 1 → persistido y legible) — verify: el test FALLA porque no hay repositorio/caso de uso/endpoint
- [x] 3.2 GREEN: implementar repositorio (`infrastructure/db/`), caso de uso (`application/services/`) y endpoint con validación Pydantic en el borde (`api/routers/`) — verify: el test 3.1 pasa
- [x] 3.3 RED: escribir los tests de integración de rechazo — solapamiento parcial (10:15–10:45) y contenido (10:20–10:40) sobre el mismo recurso devuelven conflicto; servidor rechaza aunque el cliente no haya chequeado (RN-GEN-04) — verify: los tests FALLAN porque no hay validación de solapamiento
- [x] 3.4 GREEN: cablear la validación de dominio (grupo 2) en el caso de uso — verify: los tests 3.3 pasan
- [x] 3.5 RED: escribir el test de que una duración informada por el cliente (60 min para una práctica de 30) responde 422 y no persiste nada — verify: el test FALLA (hoy no se valida)
- [x] 3.6 GREEN: agregar la validación de borde Pydantic que impide fijar la duración — verify: el test 3.5 pasa; además cada test del grupo referencia su código `RN-XX` (RN-AGE-01, RN-AGE-03, RN-GEN-04) — verify: `grep -r "RN-" <tests>` muestra trazabilidad en todos

## 4. Garantía declarativa, concurrencia y mapeo de conflicto (PostgreSQL real)

- [x] 4.1 RED: escribir el test que INSERTA DIRECTO en la base, evadiendo el dominio, un turno solapado esperando `exclusion_violation` (SQLSTATE 23P01) — verify: si el test falla porque la restricción no existe, SE REPORTA prerequisito C-02 ausente y el change queda bloqueado (NO se crea esquema en este change); si falla por otro motivo, es un bug real
- [x] 4.2 Verificar que la restricción rechaza la escritura sin participación de código de aplicación — verify: el test 4.1 pasa contra `postgres:15-alpine`
- [x] 4.3 RED: escribir el test de que un `23P01` producido en la escritura se responde como HTTP 409 con mensaje de intervalo ocupado y NUNCA como confirmación (RN-GEN-05) — verify: el test FALLA (hoy el error de base se escaparía como 500)
- [x] 4.4 GREEN: implementar el mapeo `23P01 → error de dominio tipado → 409` de `design.md` D4 — verify: el test 4.3 pasa
- [x] 4.5 RED: escribir el test de concurrencia — dos conexiones insertan el mismo intervalo en el mismo recurso en paralelo → exactamente 1 éxito y 1 rechazo — verify: el test FALLA (sin restricción/mapeo, o devuelve 500)
- [x] 4.6 GREEN: verificar que con la restricción (D2) y el mapeo (D4) la corrida concurrente da 1×201/creado y 1×409 — verify: el test 4.5 pasa en 10 corridas seguidas
- [x] 4.7 Escribir y ejecutar el test de concurrencia en recursos distintos (sillón 1 y sillón 2, mismo intervalo) → ambas creaciones exitosas — verify: el test pasa

## 5. Verificación explícita por escenario del spec

- [x] 5.1 Verificar escenario «Camino feliz — turno creado y persistido» — verify: su test pasa y referencia RN-AGE-01
- [x] 5.2 Verificar escenario «La duración no es un parámetro libre del cliente» — verify: su test pasa (422) y referencia RN-AGE-01
- [x] 5.3 Verificar escenario «Solapamiento parcial rechazado» — verify: su test pasa (409) y referencia RN-AGE-03
- [x] 5.4 Verificar escenario «Intervalo contenido rechazado» — verify: su test pasa (409) y referencia RN-AGE-03
- [x] 5.5 Verificar escenario «Mismo intervalo en otro recurso permitido» — verify: su test pasa (creado) y referencia RN-AGE-03
- [x] 5.6 Verificar escenario «El servidor valida aunque el cliente no» — verify: su test pasa (409 desde la API) y referencia RN-GEN-04
- [x] 5.7 Verificar escenario «Turno que empieza cuando otro termina — permitido» — verify: su test pasa (creado) y referencia RN-AGE-01/RN-AGE-03
- [x] 5.8 Verificar escenario «Turno que termina cuando otro empieza — permitido» — verify: su test pasa (creado) y referencia RN-AGE-01/RN-AGE-03
- [x] 5.9 Verificar escenario «Turno que empieza cuando otro empieza — rechazado» — verify: su test pasa (409) y referencia RN-AGE-03
- [x] 5.10 Verificar escenario «Dos escrituras simultáneas del mismo intervalo — un solo éxito» — verify: su test de concurrencia pasa (1 éxito + 1×409) contra PostgreSQL real
- [x] 5.11 Verificar escenario «Escrituras simultáneas en recursos distintos — ambas exitosas» — verify: su test de concurrencia pasa contra PostgreSQL real
- [x] 5.12 Verificar escenario «Escritura que evade la validación de dominio igualmente rechazada» — verify: su test pasa (23P01 en insert directo) y referencia RN-GEN-01
- [x] 5.13 Verificar escenario «Violación de exclusión responde 409 sin éxito falso» — verify: su test pasa y referencia RN-GEN-05

## 6. Cierre: validación y trazabilidad

- [x] 6.1 Ejecutar `openspec validate crear-turno-sin-solapamientos --strict` — verify: reporta 0 issues
- [x] 6.2 Ejecutar la suite completa de integración contra `postgres:15-alpine` — verify: todos los tests en verde, y confirmar por `grep` que ningún test corre sobre SQLite ni un doble en memoria (DD-10)
- [x] 6.3 Verificar que cada `RN-XX` citado en el spec (RN-AGE-01, RN-AGE-03, RN-GEN-01, RN-GEN-04, RN-GEN-05) aparece al menos una vez en los tests o en el código — verify: `grep` por cada código arroja al menos un resultado

## Workflow follow-up

- Archive the change (`openspec archive crear-turno-sin-solapamientos`) only after every tracked task above is `[x]` and `openspec validate crear-turno-sin-solapamientos --strict` reports 0 issues.
- Verify the archived result with `openspec validate --archived` and confirm the delta spec became `openspec/specs/agenda/reservas/spec.md`.
- Registrar el resultado en Engram (`opsx/crear-turno-sin-solapamientos/archive`).
