# Decisiones y Supuestos

> Fuente: `.active-orchestrator-state.json` → `discovery`, `docs/discovery/informe-discovery.md`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).
>
> Distinción importante: las **decisiones** son elecciones tomadas para este
> sistema. Los **supuestos** son cosas que se asumen porque ningún documento
las confirma. Un supuesto marcado como
riesgo alto es una bomba con mecha.

## Decisiones documentadas

### DD-01 — Sin integraciones externas obligatorias en el v1
**Decisión**: el v1 no se integra con obras sociales, pasarelas ni servicios de
mensajería.
**Contexto**: Discovery no encontró dependencias externas obligatorias para el
flujo mínimo de agenda, y determinó que sumar integraciones agrega al menos seis
meses de trabajo. Solo **1 de 19** sistemas del relevamiento gestiona obras
sociales o prepagas, y el competidor más parecido a nuestra v1 (DentalFLOW)
declaraba WhatsApp como «en camino» en lugar dearlo activo (hallazgo H-03).
**Alternativas consideradas**: (a) integrar obras sociales desde el arranque;
(b) integrar solo recordatorios por email; (c) sin integraciones.
**Justificación**: el flujo de reserva no necesita ningún tercero. Agregar
integraciones convierte un problema de agenda en un problema de integración. Y la
ventana de oportunidad es concreta: el plan Consultorio de **DentalSaaS**
($59.000/mes) excluye el servicio de WhatsApp del precio publicado.
**Trade-offs aceptados**: el consultorio sigue gestionando a mano las obras
sociales y el envío de recordatorios en el v1.

### DD-02 — Instalación única, no multi-tenant
**Decisión**: una instalación atiende a un consultorio.
**Contexto**: el mercado objetivo inicial es el profesional unipersonal.
**Alternativas consideradas**: (a) multi-tenant desde el inicio; (b)
mono-tenant.
**Justificación**: el multi-tenant agrega aislamiento de datos, migraciones por
cliente y soporte, todo eso para un cliente que no existe todavía.
**Trade-offs aceptados**: si dos consultorios quieren compartir sistema, hay que
migrar. `needs_infra` sigue siendo `true` por otros motivos, no por multi-tenancy.

### DD-03 — El recurso asignable es el eje del modelo
**Decisión**: el turno cuelga de un recurso (el sillón), no de un profesional ni
de un consultorio.
**Contexto**: es la forma en que describen su operación los 19 sistemas
relevados; la agregación por sillón es el patrón dominante del rubro.
**Alternativas consideradas**: (a) turno por profesional; (b) turno por recurso.
**Justificación**: un mismo profesional puede atender en dos recursos en la misma
franja. El modelo por profesional no puede expresar eso.
**Trade-offs aceptados**: obliga a configurar recursos aunque haya uno solo. Se
paga con una tabla de una fila.

### DD-04 — El paciente no tiene cuenta en el v1
**Decisión**: la reserva y la gestión del turno ocurren por token de un solo uso.
**Contexto**: la consigna de Discovery es que el paciente **odia llamar por
teléfono**. Pedirle que cree una cuenta con password contradice el objetivo.
**Alternativas consideradas**: (a) cuenta de paciente; (b) link firmado por
turno; (c) turno confirmado por el consultorio a mano.
**Justificación**: (b) elimina la fricción sin perder trazabilidad.
**Trade-offs aceptados**: no hay historial del lado del paciente. Para pedir un
turno anterior tiene que usar el enlace que recibio. Si lo perdio, llama.

### DD-05 — El conflicto de horario se resuelve en la base de datos
**Decisión**: exclusión constraint con GiST sobre `recurso_id` y
`tstzrange(inicio, fin)`.
**Contexto**: es el único requisito técnico que descarta bases más simples.
**Alternativas consideradas**: (a) solo validación en el backend; (b) bloqueo
pesimista en la aplicación; (c) exclusión constraint.
**Justificación**: (a) y (b) fallan ante concurrencia real. Dos peticiones
simultaneas leen el mismo horario libre y las dos escriben. El problema aparece
justo cuando más turnos hay, que es cuando más duele.
**Trade-offs aceptados**: Postgres deja de ser reemplazable. El test de
conflicto tiene que correr contra una base real, no contra un doble.

### DD-06 — La agenda no se presenta como diferencial
**Decisión**: el material de producto **no** comunica "tenemos agenda
electrónica" como beneficio principal.
**Contexto**: los 19 sistemas relevados tienen agenda electrónica, y **Órbita
Gestión**, el mejor puntuado (4,88/5), ya ofrece agenda **por sillón** con
«choque imposible» desde USD 25/mes. DentalFLOW además la garantiza a nivel de
base de datos. Es decir: la agenda por sillón no es un diferencial propio
(hallazgos H-01 y H-06 del informe).
**Alternativas consideradas**: (a) competir por la agenda; (b) competir por lo
que pasa en el borde (ausentismo, derivación, auditoría, exportación).
**Justificación**: (a) es entrar en un terreno donde todos están empatados, y
contra un competidor que publica precio. Los vacíos del mercado argentino que sí
están abiertos están en el borde y en la confianza, no en la agenda.
**Trade-offs aceptados**: obliga a construir funciones más pesadas para el v1
simple. Se asume el costo.

### DD-07 — El asístente IA no recibe datos clínicos
**Decisión**: la IA solo consulta disponibilidad. Nunca recibe ni devuelve el
historial clínico.
**Contexto**: la Ley 25.326 clasifica el historial clínico como dato sensible, y
mandarlo a un tercero sin acuerdo de tratamiento es una exposición real.
**Alternativas consideradas**: (a) IA con contexto clínico completo; (b) IA con
solo disponibilidad; (c) sin IA en el v1.
**Justificación**: el beneficio de la IA esta en reducir la fricción de agendar,
no en interpretar clínica.
**Trade-offs aceptados**: la IA no puede sugerir prácticas ni anticipar lo que
necesita el paciente.

### DD-08 — Aislamiento de datos desde el inicio
**Decisión**: Row Level Security activa sobre las tablas de datos de salud.
**Contexto**: en un sistema donde un único operador ve todo, RLS parece
innecesaría.
**Alternativas consideradas**: (a) solo permisos en la API; (b) RLS desde el
inicio.
**Justificación**: (a) deja que un error de programación en un endpoint exponga
historias clínicas. (b) es una red que hoy no se nota y después no se agrega.
**Trade-offs aceptados**: una capa más que aprender.

### DD-09 — La sesión viaja en cookie httpOnly, no en localStorage
**Decisión**: JWT firmado dentro de una cookie `httpOnly`, `SameSite=Lax`,
`Secure` en producción.
**Contexto**: el frontend es una SPA y el camino corto para guardar una sesión es
`localStorage`.
**Alternativas consideradas**: (a) `localStorage`; (b) cookie `httpOnly`;
(c) tokens de sesión en base con cookies firmadas.
**Justificación**: `localStorage` es legible desde cualquier XSS, y el sistema guarda
datos de salud. La cookie `httpOnly` mueve el token fuera del alcance del
JavaScript de la página. (c) es más robusta todavía, pero agrega una tabla y un
ciclo de revocación que la v1 no necesita.
**Trade-offs aceptados**: con cookies hay que vigilar CSRF en los métodos que
escriben, así que el backend tiene que validar `Origin` o un token CSRF.

### DD-10 — Los tests de conflicto corren contra PostgreSQL real
**Decisión**: el test de solapamiento se ejecuta contra un PostgreSQL real
levantado en Docker, nunca contra un doble en memoria ni contra SQLite.
**Contexto**: DD-05 garantiza la ausencia de solapamientos con una restricción
`EXCLUDE USING gist`.
**Alternativas consideradas**: (a) SQLite para los tests, por velocidad;
(b) PostgreSQL real en cada corrida.
**Justificación**: un doble en memoria no implementa `EXCLUDE USING gist`, así que
un test que pase contra él no probaría lo que la decisión DD-05 afirma. El test
sería verde y el bug seguiría existiendo: es exactamente el falso positivo que
**RN-AGE-03** (no puede existir solapamiento entre turnos confirmados del mismo
recurso) busca evitar, replicado en la infraestructura de tests.
**Trade-offs aceptados**: los tests necesitan Docker y son más lentos.

### DD-11 — El stack tecnológico queda fijado en FastAPI + PostgreSQL + React + Docker
**Decisión**: backend en FastAPI (Python 3.11), base de datos PostgreSQL 15,
frontend en React 18 con Vite, autenticación con JWT en cookie `httpOnly`
(DD-09) y despliegue con Docker Compose.
**Fecha de decisión**: 2026-10-03.
**Contexto**: la consigna del trabajo deja el stack libre, y ningún documento de
`docs/` fija tecnologías. Por eso el stack no se pudo inferir del Discovery y se
registró como «No evidenciado» en `10_preguntas_abiertas.md`. La decisión es
**del equipo**, no un hallazgo de la investigación, y conviene que la diferencia
quede escrita.
**Alternativas consideradas**: (a) SQLite por simplicidad; (b) Node/Express con
PostgreSQL; (c) Django con PostgreSQL; (d) esta combinación.
**Justificación**: PostgreSQL no es una preferencia, es el único componente
imprescindible: sin `EXCLUDE USING gist` no hay forma de garantizar el requisito
central del producto (DD-05). Sobre esa base, FastAPI da tipado estático y
OpenAPI para definir la API, y React cubre el caso de uso real, que es una vista
de agenda más un formulario de reserva para el paciente.
**Trade-offs aceptados**: Python y JavaScript en el mismo repositorio, con dos
cadenas de dependencias que mantener; y el despliegue necesita Docker, que
`needs_infra` ya anticipaba en el estado del proyecto.
**Consecuencia operativa**: si alguien propone cambiar la base de datos, hay que
volver a `04_modelo_de_datos.md` y a DD-05 antes de aceptar el cambio.

## Supuestos inferidos

### SU-01 — El segmento inicial es el profesional unipersonal
**Supuesto**: el odontólogo que atiende solo y no tiene sistema de gestiona.
**Origen**: `discovery.casos_de_uso`.
**Riesgo si es falso**: alto. Si el cliente real es un consultorio con secretaría
y varios profesionales, casi todos los roles y pantallas cambian.
**Cómo validar**: una entrevista con un consultorio que tenga dos o más profesionales.

### SU-02 — El paciente completa un formulario web sin asistencia
**Supuesto**: un paciente con teléfono y acceso a internet puede elegir horario y
cargar sus datos solo.
**Origen**: `discovery.casos_de_uso`.
**Riesgo si es falso**: medio. Si una parte de los pacientes necesita asistencia
telefonica, el canal no se puede eliminar del todo.
**Cómo validar**: prueba de usabilidad con 5 a 10 pacientes reales.

### SU-03 — La migración de la agenda actual es el principal freno
**Supuesto**: el odontólogo hoy gestiona sus turnos en Excel, WhatsApp o cuaderno,
y ese es el punto de dolor.
**Origen**: `discovery.riesgos`.
**Riesgo si es falso**: alto. Si el problema real es la falta de pacientes y no
la agenda, el sistema no resuelve nada.
**Cómo validar**: preguntar en la primera entrevista por el flujo actual, paso a
paso.

### SU-04 — La duración de cada práctica es estable
**Supuesto**: cada práctica tiene una duración fija que no cambia por paciente.
**Origen**: `discovery.reglas_de_negocio`.
**Riesgo si es falso**: bajo. Se resuelve con duración por práctica y recurso,
que ya esta en el modelo.
**Cómo validar**: preguntar si hay prácticas que duren más según el caso.

### SU-05 — Un consultorio arranca con un solo sillón
**Supuesto**: el volumen inicial no requiere varios recursos en paralelo.
**Origen**: inferencia del segmento objetivo.
**Riesgo si es falso**: bajo. El modelo ya soporta N recursos; sólo hay que
cargar la disponibilidad de cada uno.
**Cómo validar**: preguntar en la validación inicial.

### SU-06 — El paciente acepta entregar sus datos de salud por formulario web
**Supuesto**: completar el consentimiento no frena la reserva.
**Origen**: `discovery.restrcciones`.
**Riesgo si es falso**: medio-alto. Afecta directo la tasa de conversión.
**Cómo validar**: medir la tasa de abandono en el paso del consentimiento.

### SU-07 — El odontólogo adopta software sin resistencia
**Supuesto**: si la herramienta es simple, la va a usar.
**Origen**: `discovery.riesgos`.
**Riesgo si es falso**: medio. El sistema sin uso no aporta nada, por bien que
este construido.
**Cómo validar**: observar el uso real en las primeras cuatro semanas.

### SU-08 — La asistencia IA es un diferencial y no una distractor
**Supuesto**: la IA aporta valor real al paciente que agenda.
**Origen**: `discovery.funcionalidades`.
**Riesgo si es falso**: alto. El relevamiento no encontró ningún competidor con
asistente IA con evidencia pública, lo que puede significar que no sirve y no
que somos los primeros. Ver PREG-08.
**Cómo validar**: probarlo con usuarios reales antes de construirlo en serio.