# Reglas de Negocio

> Fuente: `.active-orchestrator-state.json` → `discovery.reglas_de_negocio`,
> `discovery.restricciones`, `discovery.riesgos`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

Cada regla tiene un código `RN-{DOMINIO}-{NN}` para trazabilidad con las historias
de usuario de `06_funcionalidades.md`.

Las reglas marcadas con **Origen: Discovery** provienen literalmente del
relevamiento. Las marcadas como **Propuesta** son decisiónes de diseño de este
sistema y no fueron verificadas contra el mercado.

## Dominio: Agenda (RN-AGE)

### Qué es un "recurso"

En todo este documento, **recurso** es el puesto físico agendable: el **sillón**,
el **box** o el puesto de atención de un consultorio multiespecialidad. No es el
profesional.

Discovery identificó el recurso —y no el profesional— como lo escaso, y por eso el modelo
de datos de `04_modelo_de_datos.md` indexa los turnos por recurso (DD-03). En un
consultorio unipersonal hay un único recurso, que suele ser el sillón del propio
profesional; la abstracción existe para que el mismo código soporte el caso
multisillón sin cambiar las reglas.

### Reglas

- **RN-AGE-01**: Un turno ocupa un intervalo cerrado `[inicio, fin)` y tiene una
  duración asociada a la práctica. Origen: Discovery. La duración la define el
  odontólogo por práctica y **no es un parámetro libre del paciente**: es lo que
  impide que un turno de 15 minutos bloquee el sillón una hora.
- **RN-AGE-02**: La disponibilidad se define por franjas semanales por recurso
  (sillón o box). Origen: Discovery. Un mismo profesional puede tener varias
  franjas, y un mismo recurso puede tener franjas que cambian por semana.
- **RN-AGE-03**: No puede existir solapamiento entre turnos confirmados del mismo
  recurso (sillón o box). Origen: Discovery. Implementado en la capa de datos, ver
  `04_modelo_de_datos.md`.
- **RN-AGE-04**: Un turno debe quedar dentro de una franja de disponibilidad.
  Origen: Discovery. Si la franja se reduce después, los turnos ya confirmados se
  respetan y se avisa al odontólogo de los que quedaron fuera.
- **RN-AGE-05**: El odontólogo puede bloquear una franja (feriado, vacaciones,
  uso personal). Origen: Discovery. El bloqueo es un objeto de primera clase, no
  un turno ficticio.
- **RN-AGE-06**: Un paciente puede tener varios turnos simultaneos para Prácticas
  distintas siempre que no se solapen en el tiempo. Origen: Discovery.
- **RN-AGE-07**: La reprogramación cancela el turno anterior y crea uno nuevo, en
  una sola transacción. Origen: Propuesta. Un turno nunca se "mueve": se
  reemplaza, para conservar el historial.

## Dominio: Cancelaciones y ausencias (RN-CAN)

- **RN-CAN-01**: El paciente puede cancelar sin costo hasta un plazo mínimo
  definido por el consultorio. Origen: Propuesta. Discovery no evidencio cual es
  el plazo que el mercado considera aceptable. Ver PREG-04.
- **RN-CAN-02**: Pasado el plazo mínimo, la cancelación queda registrada con la
  marca temporal y la razon (`cancelado_por`, `cancelado_at`). Origen: Propuesta.
- **RN-CAN-03**: El odontólogo puede cancelar un turno sin restricción de plazo.
  Origen: Propuesta. El motivo es obligatorio en ese caso.
- **RN-CAN-04**: Registrar un turno como `no_asístio` es una operación exclusiva
  del odontólogo y siempre genera auditoría. Origen: Propuesta.

## Dominio: Autenticación (RN-AU)

- **RN-AU-01**: Sólo el odontólogo tiene credenciales. El paciente no se
  autentica en el v1. Origen: Discovery.
- **RN-AU-02**: La sesión del odontólogo usa JWT en cookie httpOnly con SameSite
  estricto. Origen: Propuesta. No hay tokens en localStorage.
- **RN-AU-03**: Tras un intento fallido de login se aplica rate limiting por IP y
  por email. Origen: Propuesta.
- **RN-AU-04**: La sesión caduca a las 8 horas de inactividad. Origen: Propuesta.

## Dominio: Privacidad y datos sensibles (RN-PRIV)

- **RN-PRIV-01**: El historial clínico es **dato sensible** bajo la Ley 25.326.
  Origen: Discovery. No es el mismo tratamiento que un dato de contacto.
- **RN-PRIV-02**: Los datos de salud se cifran en reposo y el cifrado se registra
  en el diseño. Origen: Propuesta.
- **RN-PRIV-03**: Todo acceso a un historial clínico escribe una fila en
  `AuditoríaAcceso` con usuario, recurso, accion, fecha e IP. Origen: Discovery.
- **RN-PRIV-04**: Los datos personales del paciente se anulan, no se borran, para
  preservar la trazabilidad de los turnos historicos. Origen: Propuesta.
- **RN-PRIV-05**: La exportacion de datos que realiza el odontólogo también se
  audita. Origen: Propuesta.
- **RN-PRIV-06**: El asístente IA no recibe el historial clínico. Sólo recibe
  disponibilidad. Origen: Propuesta. Es una decisión deliberada para acotar la
  superficie de datos sensibles expuesta a un tercero. Ver DD-07.
- **RN-PRIV-07**: El sistema registra y muestra el consentimiento del paciente
  para tratar datos de salud, con versión del documento y fecha. Origen:
  Discovery.

## Dominio: Excepciones y limites globales (RN-GEN)

- **RN-GEN-01**: Ninguna escritura de turno se completa sin pasar la validación de
  disponibilidad y la restricción de exclusión de la base. Origen: Propuesta.
- **RN-GEN-02**: Toda operación que cambie la agenda escribe una fila de
  auditoría. Origen: Propuesta.
- **RN-GEN-03**: El sistema no envia recordatorios en el v1. Origen: Discovery.
  Si se agrega después, el envío pasa a ser una entidad con su propio estado, no
  un efecto secundario del alta del turno.
- **RN-GEN-04**: El horario de operación es del consultorio y se valida en el
  servidor, nunca solo en el navegador. Origen: Propuesta.
- **RN-GEN-05**: Si el servicio no puede confirmar un turno, la interfaz nunca
  muestra éxito. Origen: Propuesta. Es la regla que evita el falso positivo en la
  reserva en línea.

## Reglas heredadas del contexto de Discovery

No son codificables todavía, pero condicionan el diseño:

| Regla de contexto | Donde impacta |
|-------------------|---------------|
| El odontólogo unipersonal no tiene tiempo para administrar un sistema complejo | Toda la UI: pocas pantallas, cero configuración inicial obligatoria |
| El paciente odia llamar por teléfono | El paciente no tiene cuenta: la reserva se completa en menos de un minuto |
| Los software del rubro son todos feos y se crítican entre sí | Sin marcas de terceros en la interfaz, sin comparativas visibles al paciente |
| La agenda electrónica ya la ofrecen los 19 sistemas relevados | La agenda no se presenta como innovacion; ver DD-06 |