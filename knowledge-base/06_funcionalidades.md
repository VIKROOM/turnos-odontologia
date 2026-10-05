# Funcionalidades

> Fuente: `.active-orchestrator-state.json` → `discovery.casos_de_uso`,
> `discovery.funcionalidades`, `docs/discovery/informe-discovery.md` sección D.4.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

Organizadas por épica y luego por historia de usuario (`US-NNN`). Los criterios
de aceptación son los que se usan para escribir los tests.

## Épica 1: Configuración inicial

### US-001 — Instalar el consultorio en un solo paso
**Como** odontólogo
**Quiero** definir mis datos, mis prácticas y mi disponibilidad al instalar
**Para** empezar a recibir reservas sin configurar nada más

**Criterios de aceptación**:
- [ ] CA-1: el asístente pide nombre del consultorio, email y password del odontólogo
- [ ] CA-2: se crean Usuario, Recurso y las Prácticas iniciales en una transacción
- [ ] CA-3: se puede arrancar sin configurar una sola franja de disponibilidad

**Reglas relacionadas**: RN-AU-01, RN-GEN-04

### US-002 — Cargar mi disponibilidad semanal
**Como** odontólogo
**Quiero** definir mis franjas por día y recurso
**Para** que el sistema solo ofrezca horarios que yo atiendo

**Criterios de aceptación**:
- [ ] CA-1: se pueden agregar y quitar franjas por día de la semana
- [ ] CA-2: una franja con `hora_fin` menor o igual a `hora_inicio` se rechaza
- [ ] CA-3: las franjas se aplican a todas las prácticas del recurso

**Reglas relacionadas**: RN-AGE-02

## Épica 2: Agenda del odontólogo

### US-003 — Ver mi día de turnos
**Como** odontólogo
**Quiero** ver los turnos del día en orden
**Para** saber a quién atiendo y en qué orden

**Criterios de aceptación**:
- [ ] CA-1: los turnos se muestran ordenados por hora de inicio
- [ ] CA-2: cada turno muestra hora, paciente, práctica y teléfono
- [ ] CA-3: los turnos cancelados se distinguen de los confirmados
- [ ] CA-4: la pantalla carga sin JavaScript de terceros

**Reglas relacionadas**: RN-AGE-01

### US-004 — Bloquear una franja
**Como** odontólogo
**Quiero** bloquear un rango de tiempo con un motivo
**Para** no recibir reservas cuando no atiendo

**Criterios de aceptación**:
- [ ] CA-1: no se puede crear un bloqueo que solape un turno confirmado
- [ ] CA-2: el motivo es obligatorio
- [ ] CA-3: el bloqueo desaparece de la disponibilidad pública de inmediato

**Reglas relacionadas**: RN-AGE-05, RN-AGE-03

### US-005 — Registrar una ausencia
**Como** odontólogo
**Quiero** marcar un turno como `no_asístio`
**Para** saber la tasa de ausencias real

**Criterios de aceptación**:
- [ ] CA-1: sólo el odontólogo puede marcar la ausencia
- [ ] CA-2: la operación escribe una fila de auditoría
- [ ] CA-3: el turno no se libera automáticamente

**Reglas relacionadas**: RN-CAN-04, RN-PRIV-03

## Épica 3: Reserva autogestiónada

### US-006 — Ver horarios disponibles
**Como** paciente
**Quiero** ver los horarios libres de una fecha y práctica
**Para** elegir sin llamar por teléfono

**Criterios de aceptación**:
- [ ] CA-1: solo devuelve horarios dentro de una franja de disponibilidad
- [ ] CA-2: excluye horas ya reservadas, bloqueadas o pasadas
- [ ] CA-3: respeta la duración de la práctica elegida
- [ ] CA-4: no devuelve ningún dato personal de otro paciente

**Reglas relacionadas**: RN-AGE-01, RN-AGE-02, RN-AGE-04, RN-PRIV-06

### US-007 — Reservar un turno
**Como** paciente
**Quiero** reservar un horario con mis datos
**Para** tener mi turno confirmado sin llamar

**Criterios de aceptación**:
- [ ] CA-1: pide nombre, teléfono y consentimiento de datos de salud
- [ ] CA-2: si el horario fue tomado mientras el paciente completaba el formulario, la reserva **falla** y se informa que ya no está disponible
- [ ] CA-3: devuelve un enlace con token de un solo uso para gestiónar el turno
- [ ] CA-4: nunca muestra éxito si la reserva no se confirmó

**Reglas relacionadas**: RN-AGE-03, RN-GEN-01, RN-GEN-05, RN-PRIV-07

### US-008 — Consultar mi turno sin cuenta
**Como** paciente
**Quiero** abrir el enlace que recibí
**Para** ver los datos de mi turno

**Criterios de aceptación**:
- [ ] CA-1: el token es aleatorio, de un solo uso para operaciónes de escritura y no adivinable
- [ ] CA-2: un token inexistente responde 404 sin revelar si el turno existe
- [ ] CA-3: la respuesta no incluye datos clínicos

**Reglas relacionadas**: RN-AU-01, RN-GEN-04

## Épica 4: Gestión de turnos

### US-009 — Cancelar mi turno
**Como** paciente
**Quiero** cancelar con un clic
**Para** avisar que no voy

**Criterios de aceptación**:
- [ ] CA-1: se permite hasta el plazo mínimo definido por el consultorio
- [ ] CA-2: pasado el plazo, se rechaza y se informa la fecha límite
- [ ] CA-3: el turno queda en estado `cancelado` y libera el horario
- [ ] CA-4: se registra `cancelado_por = paciente` y la hora

**Reglas relacionadas**: RN-CAN-01, RN-CAN-02

### US-010 — Reprogramar mi turno
**Como** paciente
**Quiero** cambiar la fecha de mi turno
**Para** atenderme otro día sin perderlo

**Criterios de aceptación**:
- [ ] CA-1: sólo hay un turno activo: el anterior queda `cancelado`
- [ ] CA-2: ambas operaciónes ocurren en una sola transacción
- [ ] CA-3: si el nuevo horario no está disponible, no se cancela el anterior

**Reglas relacionadas**: RN-AGE-07, RN-AGE-03

### US-011 — Cancelar desde el consultorio
**Como** odontólogo
**Quiero** cancelar un turno con motivo
**Para** reagendar sin fricción con el paciente

**Criterios de aceptación**:
- [ ] CA-1: el motivo es obligatorio
- [ ] CA-2: no hay restricción de plazo
- [ ] CA-3: queda registrado `cancelado_por = consultorio`

**Reglas relacionadas**: RN-CAN-03

## Épica 5: Ficha del paciente

### US-012 — Buscar un paciente
**Como** odontólogo
**Quiero** buscar por nombre o teléfono
**Para** encontrar la ficha rápido en el momento de la atención

**Criterios de aceptación**:
- [ ] CA-1: la búsqueda es tolerante a errores de tipeo en el teléfono
- [ ] CA-2: los resultados no incluyen datos clínicos
- [ ] CA-3: los pacientes anulados no aparecen por defecto

**Reglas relacionadas**: RN-PRIV-01

### US-013 — Ver la ficha de un paciente
**Como** odontólogo
**Quiero** ver datos de contacto e historial de turnos
**Para** tener el contexto antes de atender

**Criterios de aceptación**:
- [ ] CA-1: muestra los turnos en orden cronológico inverso
- [ ] CA-2: los datos clínicos están en un acceso separado, no en la misma vista

**Reglas relacionadas**: RN-PRIV-01, RN-PRIV-03

### US-014 — Anular los datos de un paciente
**Como** odontólogo
**Quiero** anular los datos de contacto de un paciente que ya no viene
**Para** cumplir con la ley sin perder el historial de turnos

**Criterios de aceptación**:
- [ ] CA-1: los turnos históricos siguen existiendo y visibles
- [ ] CA-2: los datos de contacto quedan vacíos con `anulado_at` registrado
- [ ] CA-3: el paciente deja de aparecer en las búsquedas

**Reglas relacionadas**: RN-PRIV-04

## Épica 6: Historia clínica mínima

### US-015 — Registrar una atención
**Como** odontólogo
**Quiero** registrar lo que hice en cada pieza tratada
**Para** tener el historial del paciente

**Criterios de aceptación**:
- [ ] CA-1: una entrada por pieza y cara, sin duplicados
- [ ] CA-2: queda asociado al turno que la originó, si lo hubo
- [ ] CA-3: la entrada es inmutable una vez registrada

**Reglas relacionadas**: RN-PRIV-02, RN-PRIV-03

### US-016 — Ver el odontograma
**Como** odontólogo
**Quiero** ver el estado de las piezas del paciente
**Para** decidir el tratamiento

**Criterios de aceptación**:
- [ ] CA-1: muestra solo piezas con estado registrado
- [ ] CA-2: el acceso queda auditado

**Reglas relacionadas**: RN-PRIV-03

## Épica 7: Privacidad y trazabilidad

### US-017 — Consultar quién accede a datos de salud
**Como** odontólogo
**Quiero** ver el registro de accesos a historias clínicas
**Para** saber qué pasó si un paciente reclama

**Criterios de aceptación**:
- [ ] CA-1: muestra usuario, recurso, acción, fecha e IP
- [ ] CA-2: el registro no se puede editar ni borrar desde la interfaz

**Reglas relacionadas**: RN-PRIV-03

### US-018 — Exportar los datos de un paciente
**Como** odontólogo
**Quiero** exportar la ficha de un paciente
**Para** atender un reclamo o un traslado

**Criterios de aceptación**:
- [ ] CA-1: la exportación incluye turnos e historial clínico
- [ ] CA-2: la exportación se audita
- [ ] CA-3: el formato es legible fuera del sistema

**Reglas relacionadas**: RN-PRIV-05

## Fuera de alcance del v1

Discovery los dejo explícitamente para después. No son historias pendientes:
están decisiónadas como **no hacer** en esta versión.

| Capacidad | Donde se registro |
|-----------|--------------------|
| Recordatorios por WhatsApp, SMS o email | `01_vision_y_objetivos.md`, alcance v1 |
| Reportes, indicadores y facturación | `01_vision_y_objetivos.md`, alcance v1 |
| Estudios de imagen de diagnóstico | `01_vision_y_objetivos.md`, alcance v1 |
| Multi-usuario, roles y permisos | `03_actores_y_roles.md`, matriz RBAC |
| Integración con obras sociales | `02_descripcion_general.md`, integraciones |
| Aplicación móvil nativa | `01_vision_y_objetivos.md`, alcance v1 |
| Importación masíva de historia clínica | `01_vision_y_objetivos.md`, alcance v1 |