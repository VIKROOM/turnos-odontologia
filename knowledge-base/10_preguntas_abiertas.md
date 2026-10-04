# Preguntas Abiertas

> Fuente: `.active-orchestrator-state.json` → `discovery.preguntas_abiertas`,
> `discovery.no_evidenciado`, `discovery/verificacion-fuentes.md`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).
>
> Esta seccion existe para que lo que no sabemos quede escrito. Ningún valor
> fue inventado para completar un campo.

## Inconsistencias detectadas

### IN-01 — La nota de Discovery sobre el competidor mejor puntuado quedó desactualizada
**Documento A dice**: `discovery/sources/orbita.md` afirma que el competidor de
mejor puntuación no publica agenda por sillón y que es el único del rubro en
tenerla.
**Documento B dice**: el informe de Discovery, en la correccion H-01, sostiene
justamente lo contrario: que el competidor de mejor puntuación sí ofrece agenda
por sillón y es el único en hacerlo.
**Impacto**: si alguien lee solo la nota de la fuente, conclude que la agenda por
sillón es un hueco de mercado. Si lee el informe, concluye que ya esta cubierto.
Las dos lecturas dan decisiónes de producto opuestas.
**Resolucion propuesta**: la nota de la fuente tiene que quedar marcada como
corregida o directamente reescribirla. El hallazgo H-01 y la nota no pueden
seguir coexistiendo.

### IN-02 — Dos escalas de puntuación conviviendo en los artefactos
**Documento A dice**: el informe de Discovery y `.active-orchestrator-state.json`
usan una matriz de 7 criterios con escala de 0 a 5.
**Documento B dice**: `docs/discovery/checklist-discovery.md` conserva la matriz
anterior, con puntajes sobre 10 y un total de 9,75.
**Impacto**: los números de ambos documentos no son comparables. Un 4,88 sobre 5
y un 9,75 sobre 10 parecen la misma calidad y no lo son.
**Resolucion propuesta**: dejar 0-5 como única escala oficial en todo el
proyecto y reescribir el checklist con esa escala.

### IN-03 — El competidor mejor puntuado ya no coincide con la afirmacion de precio
**Documento A dice**: `discovery/sources/orbita.md` registra que no hay precio
público verificable.
**Documento B dice**: el relevamiento posterior confirmo que ese competidor si
publica precios en su sitio.
**Impacto**: usar el texto viejo para una justificación de precio en la propuesta
comercial sería mostrar un dato que ya se sabe desactualizado.
**Resolucion propuesta**: corregir la nota antes de usarla como fuente de precio.

### IN-04 — La muestra no representa al mercado
**Documento A dice**: el relevamiento cubre 19 sistemas.
**Documento B dice**: los 19 tienen presencia digital, por lo sesgo de seleccion
es inevitable: un consultorio que no aparece en internet no aparece en la
muestra.
**Impacto**: cualquier afirmacion del tipo "el mercado tiene N competidores" o
"ningún competidor hace X" solo es valida **dentro** de la muestra, no del
mercado.
**Resolucion propuesta**: toda conclusión de mercado debe llevar la coletilla
"en la muestra relevada". Es una restricción de lenguaje, no de análisis.

## Lo que Discovery no evidencio

Este bloque es el más importante del archivo. Son diez preguntas que el
relevamiento **no pudo responder**, y que por lo tanto no pueden darse por
certainas en ninguna parte del sistema.

| # | Cuestion no evidenciada | Por que importa | Como se podria responder |
|---|------------------------|-----------------|-------------------------|
| 1 | Facturación a obras sociales sin sistema previo: no se evaluó ningún caso | La integración agrega al menos seis meses | Contactar a un consultorio que facture a obra social |
| 2 | Recordatorios automáticos: no hay medición pública de reducción de ausencias | Es la justificación del valor de esa funcionalidad | Medir ausencias con y sin recordatorio en un consultorio piloto |
| 3 | Historia clínica: no se sabe si se completa una sola vez o con mínimo de notas por turno | Cambia el modelo de datos y el tiempo de atención | Observar a un odontólogo durante una semana |
| 4 | App móvil: 0 de 19 sistemas, pero el consultorio de un profesional tiene flujo limitado | No se sabe si la demanda de app existe | Preguntar a tres odontólogos si usan el celular en el consultorio |
| 5 | IA: no se evaluó ningún competidor con evidencia pública | No permite afirmar que la IA sea un diferencial | Revisar los sitios de los 19 y buscar funciones de IA publicadas |
| 6 | Portafolio electrónico y facturación: 1 de 19 lo tiene | Es el único dato de penetración real que hay | Repetir el relevamiento con la variable "facturación" |
| 7 | El mercado objetivo no esta segmentado; la versión apunta a unipersonal | Si el segmento real es otro, el producto esta mal definido | Segmentar por tamano de consultorio y comparar resultados |
| 8 | Los sistemas no tienen un ejecutor, así que no se pueden comparar tiempos reales | Toda comparación es sobre features declaradas, no sobre uso | Necesita instalarlos y probarlos |
| 9 | No hay una muestra representativa del rubro | Ver IN-04 | Muestreo aleatorio sobre un padron, no sobre una busqueda |
| 10 | No hay verificación de uso real por parte de profesionales | Todo el relevamiento es sobre lo que el proveedor dice, no sobre lo que el odontólogo hace | Entrevistas con usuarios de los 19 sistemas |

**Como se propaga esto en el resto de la KB**: los «Objetivo de diseño, no
medido» de `01_vision_y_objetivos.md`, el supuesto SU-08 sobre la IA, y la
pregunta 5 de esta misma tabla (la IA no es un diferencial demostrado). La entrada
`[RESUELTO] stack` de más abajo se cerró por decisión del equipo, no por
evidencia, así que sigue sin ser una respuesta del relevamiento.

## Preguntas abiertas priorizadas

| Prioridad | Pregunta | Bloquea | Decisor |
|-----------|----------|---------|---------|
| Alta | ¿Qué profesional y consultorio se valida? | Sprint 1 | Equipo |
| Alta | ¿Se requiere verificación de identidad del paciente? | Sprint 1 | Equipo + legal |
| Alta | ¿El paciente necesita autenticación propia en el v1? | Sprint 1 | Producto |
| Alta | ¿La IA puede tocar datos de salud bajo la Ley 25.326? | Sprint 2 | Legal |
| Alta | ¿Qué plazo mínimo de cancelación es aceptable en el rubro? | Sprint 2 | Producto + odontólogo |
| Media | ¿Cómo se documenta el marco legal de las historias clínicas? | Sprint 2 | Legal |
| Media | ¿Los precios se fijan en pesos o en dolares? | Lanzamiento | Producto |
| Media | ¿Qué formato de exportacion necesita el paciente? | Sprint 3 | Producto |
| Media | ¿Se implementa la agenda responsive en el v1? | Sprint 3 | Equipo |
| Media | ¿Qué tecnologias del curso se aceptan? | Sprint 1 | Equipo |
| Baja | ¿Cómo se miden las metricas de éxito del sistema? | Post-lanzamiento | Producto |
| Baja | ¿Qué limites de uso y quotas necesita un consultorio? | Post-lanzamiento | Equipo |

## Campos que la generación automática no pudo inferir

Esta seccion la escribio `kb-creator` siguiendo la regla de baja confianza del
contrato: cuando un valor no se puede inferir con seguridad, se marca y se
pregunta. **Nunca se inventa.**

### `[RESUELTO] stack`

> **Resuelto el 2026-10-03.** El stack quedó decidido: **FastAPI + PostgreSQL +
> React + Docker**. Ya no es una pregunta abierta. Se registra acá para que quede
> trazable que en algún momento fue unaIncógnita y cómo se cerró.

La pregunta original era si el stack podía inferirse de los documentos fuente.
**No podía**: la consigna del trabajo deja las tecnologías libres y ningún documento
de `docs/` fija ninguna. Por eso se marcó como *No evidenciado* en lugar de
inventarla.

Cómo se cerró: el equipo decidió el stack explícitamente el **2026-10-03**, y la
decisión quedó anotada como **DD-11** en `09_decisiones_y_supuestos.md`. La tabla de
`02_descripcion_general.md` y la estructura de `08_arquitectura_propuesta.md` pasan
a ser decisiónes, no propuestas.

El riesgo que se había signaled sigue en pie y ahora hay que sostenerlo: PostgreSQL
no es negociable, porque la restricción `EXCLUDE USING gist` que garantiza la
ausencia de solapamientos no existe en SQLite ni en MySQL. Si alguien propone
cambiar de base de datos, hay que volver a `04_modelo_de_datos.md`.

### `[DISCOVERY] system_type`

Se infijo `web_app` con confianza alta, por dos senales concordantes: el
odontólogo necesita una interfaz de uso diario y el paciente accede por web pública sin instalar nada. Se registra igual para que quede explícito.

### `[DISCOVERY] needs_infra`

Se fijo `true` con confianza alta, y **no** por las integraciones de terceros,
que son todas post-v1. Es `true` porque el modelo de datos exige una base
relacional con exclusión constraints y porque hay que desplegar backend y base
de datos propios.

### `[DISCOVERY] scale`

Se infijo `public_multi_user`: el odontólogo es un usuario único de uso diario y
el paciente es público y no autenticado. Lo que este valor **no** implica es
multi-tenant; ver DD-02.

## Lo que hay que resolver antes de escribir código

En este orden:

1. **Stack tecnologico.** Sin esto no se puede escribir ni una linea.
2. **Identidad y autenticación del paciente.** Ver PREG-02 y PREG-03.
3. **Marco legal de la historia clínica.** Ver PREG-05 y PREG-06.
4. **Consultorio piloto.** Ver PREG-01 y SU-03. Sin un piloto real, el resto de
   las decisiónes son theory.