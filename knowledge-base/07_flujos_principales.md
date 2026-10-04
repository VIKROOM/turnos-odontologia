# Flujos Principales

> Fuente: `docs/discovery/informe-discovery.md`, `.active-orchestrator-state.json`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

## Flujo 1: Reserva autogestiónada por el paciente

**Disparador**: el paciente abre el enlace público de reserva.
**Actor**: paciente (no autenticado).
**Precondición**: existe al menos una franja de disponibilidad con horas libres.

**Pasos**:

1. El paciente elige práctica y fecha.
2. La API calcula los horarios aplicando RN-AGE-01, RN-AGE-02 y RN-AGE-04 sobre
   franjas, turnos y bloqueos.
3. La API devuelve los horarios libres. **Ningún dato personal** viaja en esta
   respuesta.
4. El paciente elige un horario y completa nombre, teléfono y consentimiento.
5. La API inserta el turno dentro de una transacción.
6. La base de datos aplica la restricción de exclusión sobre `recurso_id`.
7. Si la insercion es valida, la API devuelve el enlace con `token_público`.
8. Si la insercion viola la restricción, la API responde conflicto y el cliente
   vuelve a pedir disponibilidad. **No** muestra éxito.

```
Paciente ──▶ API ──▶ Motor de disponibilidad
   ▲          │
   │          └──▶ PostgreSQL ──▶ [EXCLUDE] ──▶ ok | conflicto
   └──── enlace con token ◀──────────────────────────┘
```

**Casos de error**:

| Caso | Manejo |
|------|--------|
| No hay horarios libres | Se informa y se ofrecen otras fechas |
| El horario se ocupó entre el paso 2 y el 5 | Conflicto, se recalcula la lista. Nunca se confirma a medias |
| Faltan datos o el consentimiento | Error de validación, no se inserta nada |
| Dos pacientes exactamente en el mismo milisegundo | La restricción de exclusión deja pasar **una** reserva |

**Por qué el paso 8 es el importante**: es el único escenario donde el sistema
puede prometer algo que no cumple. RN-GEN-05 existe para que la interfaz nunca
haga eso.

## Flujo 2: Intento de doble reserva

**Disparador**: dos pacientes intentan tomar el mismo slot a la vez.
**Actor**: dos pacientes concurrentes.

**Pasos**:

1. Ambas peticiones llegan al backend.
2. Ambas pasan la validación de disponibilidad, que leyó el mismo estado.
3. Ambas intentan insertar.
4. La primera insercion toma el lock de la fila en GiST.
5. La segúnda espera y, al despertar, viola la restricción.
6. La segúnda recibe un error de restricción, que la API traduce a 409.

```
P1 ──▶ INSERT ──▶ ok          ──▶ 201 Created
P2 ──▶ INSERT ──▶ espera ──▶ EXCLUDE violation ──▶ 409 Conflict
```

**Notas**: este flujo no se puede probar con un test unitario. Requiere Postgres
real y dos conexiones concurrentes. Es el test de integración más importante del
proyecto.

## Flujo 3: Bloqueo de franja por el odontólogo

**Disparador**: el odontólogo marca un rango como no disponible.
**Actor**: odontólogo.

**Pasos**:

1. El odontólogo elige fecha, hora de inicio y fin, y escribe un motivo.
2. La API valida que el motivo no esté vacío.
3. Se intenta insertar el bloqueo, sujeto a la misma restricción de exclusión.
4. Si un turno confirmado solapa, la operación falla con conflicto y se muestra
   cuáles turnos son los que chocan.
5. Si no hay solape, el bloqueo queda activo y desaparece de la disponibilidad
   publica.

**Casos de error**:

| Caso | Manejo |
|------|--------|
| El bloqueo solapa un turno confirmado | Conflicto, con detalle de los turnos involucrados |
| La franja se reduce y quedan turnos fuera | Se permite, y se avisa cuáles turnos quedaron fuera del horario (RN-AGE-04) |

## Flujo 4: Cancelación por el paciente

**Disparador**: el paciente usa su enlace y cancela.
**Actor**: paciente.

**Pasos**:

1. Se valida el `token_público`.
2. Se comprueba el plazo mínimo de cancelación.
3. Si hay plazo, el turno pasa a `cancelado` con `cancelado_por` y marca temporal.
4. El horario se libera y vuelve a estar disponible.
5. Se escribe una fila de auditoría.

**Casos de error**:

| Caso | Manejo |
|------|--------|
| Fuera de plazo | Se rechaza con la fecha límite. El turno queda intacto |
| El turno ya estaba cancelado | Operación idempotente: responde éxito sin cambiar nada |
| Token invalido | 404 sin revelar si el turno existe |

## Flujo 5: Reprogramación

**Disparador**: el paciente cambia la fecha de su turno.
**Actor**: paciente.

**Pasos**:

1. Se elige el nuevo horario.
2. En **una sola transacción**: el turno anterior pasa a `cancelado` y se crea
   uno nuevo con el mismo paciente y práctica.
3. Se escribe auditoría de las dos operaciónes.

**Casos de error**:

| Caso | Manejo |
|------|--------|
| El nuevo horario ya no está libre | Se aborta la transacción completa. El turno anterior **no** se cancela |
| El turno anterior ya estaba cancelado | No hay nada que reprogramar |

El detalle que importa: si algo falla en el paso 2, no se cancela nada. Por eso
RN-AGE-07 exige transacción única.

## Flujo 6: Acceso a la historia clínica con auditoría

**Disparador**: el odontólogo abre los datos de salud de un paciente.
**Actor**: odontólogo.

**Pasos**:

1. El navegador pide `/api/v1/pacientes/{id}/salud`.
2. La API valida la sesión.
3. **Antes** de leer, escribe una fila en `AuditoríaAcceso` con usuario, recurso,
   accion, fecha e IP.
4. Se descifra y devuelve el contenido.
5. El registro de auditoría es append-only.

```
Navegador ──▶ API ──▶ INSERT AuditoríaAcceso ──▶ commit
                         │
                         └──▶ SELECT HistorialClinico ──▶ respuesta
```

**Notas**: la auditoría se escribe aunque la lectura devuelva 404 o no haya datos.
Un intento fallido también es un evento de seguridad.

**Casos de error**:

| Caso | Manejo |
|------|--------|
| Sin sesión | 401, y queda registrado el intento |
| Paciente inexistente | 404, con auditoría registrada |

## Flujo 7: Registro de una atención

**Disparador**: el odontólogo cierra el turno y registra lo que hizo.
**Actor**: odontólogo.

**Pasos**:

1. Se elige la pieza, la cara y el estado.
2. Se valida que no exista ya una entrada para esa pieza y cara.
3. Se inserta la entrada, vinculada al turno si lo hubo.
4. Se descifra el historial, se agrega la entrada y se vuelve a cifrar.
5. Se audita.

**Casos de error**:

| Caso | Manejo |
|------|--------|
| Pieza y cara ya registradas | Se rechaza el duplicado |
| El paciente no tiene historial todavía | Se crea en el primer registro |

## Flujo 8: Exportación de datos de un paciente

**Disparador**: el odontólogo exporta la ficha.
**Actor**: odontólogo.

**Pasos**:

1. Se solicita la exportación.
2. Se escribe la auditoría.
3. Se arma un archivo con turnos e historial clínico.
4. Se devuelve por un canal de un solo uso.

**Casos de error**:

| Caso | Manejo |
|------|--------|
| Sin sesión | 401 |
| El paciente no existe | 404, con auditoría registrada |