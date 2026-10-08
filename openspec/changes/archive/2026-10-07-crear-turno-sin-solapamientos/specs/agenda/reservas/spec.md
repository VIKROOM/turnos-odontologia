# Spec Delta

## Purpose

Permite crear turnos de la agenda del consultorio sin doble booking: el sistema valida la disponibilidad en el servidor como primera línea de experiencia y PostgreSQL garantiza de forma declarativa que dos reservas del mismo recurso nunca se solapen, con semántica de intervalo semiabierta `[inicio, fin)`.

## ADDED Requirements

### Requirement: Creación y persistencia de un turno

El sistema SHALL crear y persistir un turno cuando su intervalo no se solape con ninguna reserva existente del mismo recurso. La duración MUST derivarse de la configuración de la práctica, nunca de un valor libre del cliente (RN-AGE-01), y la validación MUST ejecutarse en el servidor (RN-GEN-04). El turno MUST nacer en un estado cubierto por la restricción de exclusión desde la escritura (estado inicial `confirmado`). Trazabilidad: RN-AGE-01, RN-GEN-04.

#### Scenario: Camino feliz — turno creado y persistido
- **GIVEN** el sillón 1 no tiene reservas a las 10:00 y existe una práctica de 30 minutos asociada al paciente P
- **WHEN** se pide crear un turno en el sillón 1 para P iniciando a las 10:00 con esa práctica
- **THEN** el turno SHALL quedar persistido con inicio 10:00 y fin 10:30
- **AND** una lectura posterior del turno devuelve esos mismos valores

#### Scenario: La duración no es un parámetro libre del cliente
- **GIVEN** la práctica configurada para el sillón 1 dura 30 minutos
- **WHEN** se pide crear un turno iniciando a las 10:00 informando además una duración de 60 minutos
- **THEN** la petición SHALL ser rechazada como inválida (HTTP 422)
- **AND** ningún turno SHALL quedar persistido

### Requirement: Rechazo de creación solapada sobre el mismo recurso

No SHALL existir solapamiento entre turnos confirmados del mismo recurso (sillón o box). El sistema MUST rechazar con un error de negocio claro cualquier creación cuyo intervalo intersecte el de un turno confirmado existente del mismo recurso; turnos en recursos distintos MUST compararse por separado. Trazabilidad: RN-AGE-03.

#### Scenario: Solapamiento parcial rechazado
- **GIVEN** existe un turno confirmado de 10:00 a 10:30 en el sillón 1
- **WHEN** se pide crear un turno de 10:15 a 10:45 en el sillón 1
- **THEN** la creación SHALL ser rechazada con un error de conflicto (HTTP 409)
- **AND** el error SHALL identificar claramente que el intervalo está ocupado

#### Scenario: Intervalo contenido rechazado
- **GIVEN** existe un turno confirmado de 10:00 a 11:00 en el sillón 1
- **WHEN** se pide crear un turno de 10:20 a 10:40 en el sillón 1
- **THEN** la creación SHALL ser rechazada con un error de conflicto (HTTP 409)

#### Scenario: Mismo intervalo en otro recurso permitido
- **GIVEN** existe un turno confirmado de 10:00 a 10:30 en el sillón 1 y el sillón 2 está libre
- **WHEN** se pide crear un turno de 10:00 a 10:30 en el sillón 2
- **THEN** el turno SHALL quedar persistido

#### Scenario: El servidor valida aunque el cliente no
- **GIVEN** existe un turno confirmado de 10:00 a 10:30 en el sillón 1 y la petición omite cualquier chequeo previo de disponibilidad
- **WHEN** se envía la creación de 10:10 a 10:20 en el sillón 1 directamente al servidor
- **THEN** el servidor SHALL rechazar la creación con un error de conflicto (HTTP 409)

### Requirement: Intervalos semiabiertos `[inicio, fin)`

Los intervalos de turno MUST tratarse como semiabiertos `[inicio, fin)`: un turno que inicia exactamente cuando otro finaliza (o que finaliza exactamente cuando otro inicia) no se solapa y SHALL ser aceptado. Dos turnos que comparten un instante extremo abierto se solapan y MUST ser rechazados. Trazabilidad: RN-AGE-01, RN-AGE-03.

#### Scenario: Turno que empieza cuando otro termina — permitido
- **GIVEN** existe un turno confirmado de 10:00 a 10:30 en el sillón 1
- **WHEN** se pide crear un turno que inicia a las 10:30 en el sillón 1
- **THEN** la creación SHALL ser aceptada y el turno SHALL quedar persistido

#### Scenario: Turno que termina cuando otro empieza — permitido
- **GIVEN** existe un turno confirmado de 10:30 a 11:00 en el sillón 1
- **WHEN** se pide crear un turno de 10:00 a 10:30 en el sillón 1
- **THEN** la creación SHALL ser aceptada y el turno SHALL quedar persistido

#### Scenario: Turno que empieza cuando otro empieza — rechazado
- **GIVEN** existe un turno confirmado de 10:00 a 10:30 en el sillón 1
- **WHEN** se pide crear un turno que inicia a las 10:00 en el sillón 1
- **THEN** la creación SHALL ser rechazada con un error de conflicto (HTTP 409)

### Requirement: Concurrencia arbitrada por la base de datos

Ante dos creaciones simultáneas del mismo intervalo sobre el mismo recurso, el resultado MUST ser exactamente un éxito y un rechazo, determinado por PostgreSQL y no por el código de aplicación. Creaciones simultáneas sobre recursos distintas MUST poder completarse ambas. Trazabilidad: RN-AGE-01, RN-GEN-01.

#### Scenario: Dos escrituras simultáneas del mismo intervalo — un solo éxito
- **GIVEN** el sillón 1 está libre de 10:00 a 10:30 y dos clientes envían la misma creación en paralelo
- **WHEN** ambas peticiones se ejecutan concurrentemente contra la misma base
- **THEN** exactamente una creación SHALL reportar éxito
- **AND** la otra SHALL reportar un error de conflicto (HTTP 409)

#### Scenario: Escrituras simultáneas en recursos distintos — ambas exitosas
- **GIVEN** el sillón 1 y el sillón 2 están libres de 10:00 a 10:30 y dos clientes envían una creación por recurso en paralelo
- **WHEN** ambas peticiones se ejecutan concurrentemente contra la misma base
- **THEN** las dos creaciones SHALL reportar éxito

### Requirement: Garantía de exclusión declarativa en la base

La no-existencia de solapamientos MUST estar garantizada por una restricción de exclusión en PostgreSQL (`EXCLUDE USING gist` con extensión `btree_gist`), nunca sólo por validación de la aplicación. Un escritor que evade la validación de dominio y escribe directo contra la base MUST ser rechazado igualmente. Trazabilidad: RN-GEN-01.

#### Scenario: Escritura que evade la validación de dominio igualmente rechazada
- **GIVEN** existe un turno confirmado de 10:00 a 10:30 en el sillón 1 y la restricción de exclusión está aplicada en el esquema
- **WHEN** se inserta directamente en la base, sin pasar por la validación de la aplicación, un turno de 10:15 a 10:45 en el sillón 1
- **THEN** la base SHALL rechazar el insert con una violación de exclusión
- **AND** no SHALL quedar persistida ninguna fila nueva

### Requirement: El conflicto de exclusión se mapea a un error de dominio

Cuando la base rechace una escritura por violación de la restricción de exclusión, el sistema MUST mapearla a un error de dominio tipado de conflicto y responder HTTP 409 con un mensaje claro de solapamiento. El sistema MUST NOT reportar éxito cuando la escritura no se confirmó. Trazabilidad: RN-GEN-05.

#### Scenario: Violación de exclusión responde 409 sin éxito falso
- **GIVEN** un turno confirmado ocupa 10:00 a 10:30 en el sillón 1 y la validación de dominio no interceptó el conflicto
- **WHEN** la escritura falla en la base con una violación de exclusión
- **THEN** la API SHALL responder HTTP 409 con un mensaje que indique que el intervalo está ocupado
- **AND** la respuesta SHALL NOT ser una confirmación de creación
