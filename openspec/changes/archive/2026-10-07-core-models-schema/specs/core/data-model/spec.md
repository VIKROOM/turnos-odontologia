# Spec Delta

## Purpose

Define el modelo relacional base del consultorio en PostgreSQL 15: entidades de administración, agenda, pacientes e historia clínica, con su integridad referencial, checks, índices y timestamps, y la garantía declarativa de no-solapamiento de reservas (`EXCLUDE USING gist` con `btree_gist`, semántica `[inicio, fin)`) que sostiene RN-AGE-03 y RN-AGE-05 sin depender del backend.

## ADDED Requirements

### Requirement: Migración inicial con el modelo de entidades completo

El sistema SHALL disponer de un esquema inicial en PostgreSQL 15 que crea las tablas `usuario`, `recurso`, `practica`, `practicaduracion`, `disponibilidad_semanal`, `paciente`, `historiaclinica` y `reserva_agenda`, con integridad referencial obligatoria hacia sus tablas padre y `created_at`/`updated_at` en cada tabla. Trazabilidad: RN-AGE-01, RN-AGE-02, RN-AGE-05.

#### Scenario: La migración inicial crea las ocho tablas

- **GIVEN** una base `postgres:15-alpine` recién levantada sin esquema
- **WHEN** se aplica la migración inicial de alembic (`upgrade head`)
- **THEN** las ocho tablas SHALL existir en el esquema público
- **AND** la migración SHALL registrar su revisión en `alembic_version`

#### Scenario: La integridad referencial es obligatoria

- **GIVEN** existe una práctica pero no existe el recurso referenciado
- **WHEN** se inserta una fila de `practicaduracion` con un `recurso_id` inexistente
- **THEN** la base SHALL rechazar el insert con una violación de foreign key (SQLSTATE `23503`)
- **AND** no SHALL quedar persistida ninguna fila

#### Scenario: Toda fila queda con timestamps

- **GIVEN** el esquema inicial está aplicado
- **WHEN** se inserta cualquier fila en cualquiera de las ocho tablas
- **THEN** `created_at` y `updated_at` SHALL quedar poblados con valores no nulos

### Requirement: Reservas de agenda en tabla única con discriminador `tipo`

Los turnos y los bloqueos SHALL persistirse como filas de la tabla única `reserva_agenda` mediante el discriminador `tipo` (`turno` o `bloqueo`) — no SHALL existir tablas `turno` ni `bloqueo` separadas. Las columnas `estado`, `motivo_cancelacion` y `token_publico` viven en la propia `reserva_agenda`; `paciente_id` y `practica_id` son obligatorias para `tipo = 'turno'` y nulas para `tipo = 'bloqueo'`. Trazabilidad: RN-AGE-03, RN-AGE-05.

#### Scenario: Un turno se persiste con paciente y práctica

- **GIVEN** existen un paciente, una práctica y un recurso
- **WHEN** se inserta una fila con `tipo = 'turno'`, `paciente_id`, `practica_id`, `recurso_id`, `inicio`, `fin` y `estado = 'confirmado'`
- **THEN** la fila SHALL quedar persistida en `reserva_agenda`

#### Scenario: Un turno sin paciente o sin práctica es rechazado

- **GIVEN** el esquema inicial está aplicado
- **WHEN** se inserta una fila con `tipo = 'turno'` y `paciente_id` nulo (o `practica_id` nulo)
- **THEN** la base SHALL rechazar el insert con una violación de check (SQLSTATE `23514`)
- **AND** no SHALL quedar persistida ninguna fila

#### Scenario: Un bloqueo no admite datos de turno

- **GIVEN** el esquema inicial está aplicado
- **WHEN** se inserta una fila con `tipo = 'bloqueo'` y `paciente_id` no nulo
- **THEN** la base SHALL rechazar el insert con una violación de check (SQLSTATE `23514`)

### Requirement: Garantía declarativa de no-solapamiento en `reserva_agenda`

`reserva_agenda` SHALL poseer una restricción de exclusión parcial `EXCLUDE USING gist` sobre `recurso_id WITH =` y `tstzrange(inicio, fin, '[)') WITH &&`, con extensión `btree_gist` habilitada y predicado `WHERE (tipo = 'bloqueo' OR estado = 'confirmado')`. Cualquier escritura que la viole SHALL ser rechazada por la base con SQLSTATE `23P01` (`exclusion_violation`), sin importar quién la emita. Trazabilidad: RN-AGE-03, RN-AGE-05, RN-GEN-01.

#### Scenario: Escritura directa solapada rechazada por la base

- **GIVEN** existe una fila `tipo = 'turno'`, `estado = 'confirmado'`, de 10:00 a 10:30 en el recurso R
- **WHEN** se inserta directamente en la base, sin pasar por aplicación, un turno de 10:15 a 10:45 en R
- **THEN** la base SHALL rechazar el insert con SQLSTATE `23P01` (`exclusion_violation`)
- **AND** no SHALL quedar persistida ninguna fila nueva

#### Scenario: Un turno cancelado no ocupa el índice

- **GIVEN** existe una fila `tipo = 'turno'`, `estado = 'cancelado'`, de 10:00 a 10:30 en el recurso R
- **WHEN** se inserta un turno `confirmado` de 10:00 a 10:30 en R
- **THEN** la inserción SHALL ser admitida

#### Scenario: Turno contra bloqueo del mismo recurso rechazado

- **GIVEN** existe una fila `tipo = 'turno'`, `estado = 'confirmado'`, de 10:00 a 10:30 en el recurso R
- **WHEN** se inserta una fila `tipo = 'bloqueo'` de 10:15 a 11:00 en R
- **THEN** la base SHALL rechazar el insert con SQLSTATE `23P01`

#### Scenario: Bloqueo contra bloqueo del mismo recurso rechazado

- **GIVEN** existe una fila `tipo = 'bloqueo'` de 10:00 a 12:00 en el recurso R
- **WHEN** se inserta otra fila `tipo = 'bloqueo'` de 11:00 a 13:00 en R
- **THEN** la base SHALL rechazar el insert con SQLSTATE `23P01`

#### Scenario: Mismo intervalo en otro recurso admitido

- **GIVEN** existe una fila `confirmado` de 10:00 a 10:30 en el recurso R1 y el recurso R2 está libre
- **WHEN** se inserta una fila `confirmado` de 10:00 a 10:30 en R2
- **THEN** la inserción SHALL ser admitida

#### Scenario: Dos escrituras simultáneas del mismo intervalo — un solo éxito

- **GIVEN** el recurso R está libre de 10:00 a 10:30
- **WHEN** dos conexiones insertan concurrentemente la misma fila `confirmado` de 10:00 a 10:30 en R
- **THEN** exactamente una inserción SHALL tener éxito
- **AND** la otra SHALL fallar con SQLSTATE `23P01`

### Requirement: Intervalos semiabiertos `[inicio, fin)` a nivel de base

Los intervalos de `reserva_agenda` SHALL tratarse como semiabiertos `[inicio, fin)` mediante `tstzrange(inicio, fin, '[)')`, y toda fila SHALL cumplir `fin > inicio`. Tres filas del mismo recurso en competencia: adyacentes NO se solapan; misma marca de inicio SÍ se solapan. Trazabilidad: RN-AGE-01, RN-AGE-03.

#### Scenario: Intervalo contiguo admitido

- **GIVEN** existe una fila `confirmado` de 10:00 a 10:30 en el recurso R
- **WHEN** se inserta una fila `confirmado` de 10:30 a 11:00 en R (otra de 09:30 a 10:00 en R también SHALL ser admitida)
- **THEN** la inserción SHALL ser admitida

#### Scenario: Mismo instante de inicio rechazado

- **GIVEN** existe una fila `confirmado` de 10:00 a 10:30 en el recurso R
- **WHEN** se inserta una fila `confirmado` de 10:00 a 10:15 en R
- **THEN** la base SHALL rechazar el insert con SQLSTATE `23P01`

#### Scenario: Intervalo invertido o vacío rechazado

- **GIVEN** el esquema inicial está aplicado
- **WHEN** se inserta una fila con `fin <= inicio`
- **THEN** la base SHALL rechazar el insert con una violación de check (SQLSTATE `23514`)
