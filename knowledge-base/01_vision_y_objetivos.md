# Visión y Objetivos

> Fuente: `docs/discovery/informe-discovery.md` y `.active-orchestrator-state.json` → `discovery`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

## Propósito del sistema

Una agenda de turnos por consultorio odontológico que le permita a un profesional
independiente dejar de administrar sus turnos a mano, y que le permita al paciente
reservar, reprogramar y cancelar sin llamar por teléfono.

El problema que Discovery documentó: el odontólogo unipersonal es el dueño y a la vez
el único operador de su sistema. Hoy planifica, cobra, agenda y atiende. La
agenda es la operación diaría que más tiempo le consume y la que más errores le
genera, porque depende de que alguien la mantenga.

El sistema cubre **autogestión**: el profesional publica su disponibilidad y el
paciente reserva sobre ella. La atención clínica y el cobro quedan fuera.

## Contexto competitivo

Esta sección existe para que la base no sea un producto genérico: todo lo que
sigue sale de las secciones A, B y C del informe de Discovery, con los puntajes de
la matriz oficial (7 criterios, escala 0–5) y la fecha de consulta 2026-10-03.

**El hallazgo que condiciona todo el diseño**: los **19 de 19** sistemas
relevados ya ofrecen agenda electrónica. La agenda no es un diferencial, y este
proyecto no compite por ahí. Ver DD-06 en `09_decisiones_y_supuestos.md`.

| Sistema | Total (0-5) | Precio publicado | Qué nos importa de él |
|---|---|---|---|
| **Órbita Gestión** (AR, La Plata) | **4,88** | USD 25/mes el plan Consultorio | El líder. Ya ofrece agenda **por sillón** con «choque imposible» y ficha con odontograma e historia clínica firmada. Publica precio en **dólares**, así que no hay hueco de precio que explotar |
| **DentalSaaS / DelRioTech** (AR) | 4,30 | $59.000 / $149.000 / $349.000 por mes | Agenda y ficha clínica excelente, integraciones flojas. Su plan Consultorio **excluye el servicio de WhatsApp** del precio publicado y limita a 300 pacientes / 300 turnos: ahí está nuestra ventana |
| **ClinIA / OdontoClinIA** (AR) | 3,50 | No publicado. Demo gratuita con acompañamiento inicial | **El techo normativo.** Único del relevamiento con recetario electrónico inscripto en **ReNaPDiS (248)**, verificación de cobertura por **API de PUCO** y facturación por **AFIP**. Lidera integraciones (5,0), pero su informe lo marca como **no igualable sin un equipo de integraciones y un cliente institucional detrás**: es exactamente la dependencia que `08_arquitectura_propuesta.md` rechaza. Su fuente pública **no evidencia** el circuito de reserva ni los recordatorios |
| **DentalFLOW / TrapelTech** (AR) | 3,30 | No publicado | El más parecido a nuestra v1. **Garantiza la ausencia de doble reserva a nivel de base de datos**, con la mejor evidencia de seguridad del relevamiento |
| **Dentatools** (AR) | 2,58 | $30.000/mes | Nuestro ancla de precio y segmento (unipersonal, particulares). **Declara explícitamente que no gestiona obras sociales, prepagas ni factura electrónica AFIP**: ese es el posicionamiento a replicar |
| **TurnosUno** (AR) | 1,57 | AR$6.000/mes (promoción de lanzamiento) | El piso de precio. Si es solo promoción, el piso real es más alto y da margen para el rango de $25.000–35.000 recomendado |

Solo **7 de 19** proveedores publican precio; los 12 restantes exigen contacto
comercial, lo que impide comparar costos sobre una base común.

### Vacíos del mercado argentino que el Discovery identificó

Estos son los que justifican el alcance de `06_funcionalidades.md`:

1. **El borde, no el centro.** Ningún sistema de la muestra ataca el ausentismo
   de forma verificable. Recordatorios, lista de espera y sobreturnos son, en el
   mejor de los casos, «en camino» (hallazgo H-03, sobre DentalFLOW).
2. **Confianza como estándar, no como módulo.** Exportación total y auditoría de
   accesos a historia clínica están en la lista de deseos del sector, pero no
   en el producto base de los líderes.
3. **Cero integraciones obligatorias.** Solo 1 de 19 gestiona obras sociales o
   prepagas. Instalar el sistema sin depender de Meta, AFIP ni de un proveedor
   externo de historia clínica es una posición, no una ausencia.
4. **Precio en pesos, sin exposición cambiaria.** La referencia de precio del
   segmento (Dentatools, $30.000) está en pesos; la del líder (Órbita, USD 25) está
   en dólares. Facturar en pesos es la diferencia.

> **Advertencia de honestidad**: esto describe lo que los proveedores **publican**.
> No dice nada sobre lo que hacen realmente, y por eso la verificación de las
> cinco fuentes críticas (E.5 del informe) no resolvió ninguno de los diez puntos
> «No evidenciado» de `10_preguntas_abiertas.md`. La agenda por sillón, en
> particular, **ya no es un diferencial propio**: la tienen Órbita y la garantiza
> DentalFLOW en su base de datos (hallazgos H-01 y H-06).

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|-------|-------------------|----------------------|
| Odontólogo (dueño-operador) | Dejar de gestiónar turnos manualmente | No perder ocupación por ausencias; tener trazabilidad de quién accedió a qué dato clínico; cobrar sin registrar la cobranza a mano |
| Paciente | Poder reservar sin llamar por teléfono | Ver disponibilidad real; reprogramar o cancelar sin penalización; no repetir sus datos personales en cada visita |

## Alcance v1

Tres listas cerradas, según la sección D.4 del informe de Discovery:

1. **Agenda y turnos**: disponibilidad semanal, reservas autogestiónables, slots por
   duración de práctica, bloqueo de franjas, cancelación y reprogramación.
2. **Ficha del paciente**: datos de contacto, identificación del paciente, consentimiento de
   datos de salud, historial de turnos.
3. **Historia clínica mínima**: odontograma básico y registro de atenciones.

Explícitamente fuera del MVP y presente en el informe como "posterior":

- Recordatorios automáticos (WhatsApp/SMS/email) con unificación de canal.
- Reportes, indicadores y facturación.
- Estudios de imagen de diagnóstico.
- Multi-usuario, roles, permisos y auditoría.
- Integración con obras sociales.
- Aplicación móvil nativa.
- Importación masíva de historia clínica.

## Fuera de alcance

- Diagnóstico, indicación clínica y prescripción.
- Integraciones obligatorias con terceros en v1: **Discovery no encontró dependencias externas obligatorias**.
- Soporte de obras sociales y facturación a terceros.
- Multi-tenant desde el día uno (ver `09_decisiones_y_supuestos.md`, DD-02).

## Métricas de éxito

No hay línea de base medida para el consultorio, por lo que Discovery las dejó
como referencia. Las cuatro que se proponen para seguimiento:

| Métrica | Objetivo |
|---------|----------|
| Reservas hechas sin intervención del consultorio | Objetivo de diseño, no medido en Discovery |
| Ausencias sobre turnos reservados | Objetivo de diseño, no medido en Discovery |
| Tiempo de administración semanal de agenda | Objetivo de diseño, no medido en Discovery |
| Sobrevivencia de recordatorios | Sin dato: depende de recordatorios, fuera de v1 |

> Las tres primeras son objetivos de diseño todavía **sin medir** — ver
> `10_preguntas_abiertas.md`, PREG-11.

## Próximos pasos declarados

- Validar con un odontólogo real (Discovery alcanzó a 9 profesionales, sin
  entrevistas a profundidad).
- Medir las tres métricas de diseño de arriba como línea de base antes de
  construir.