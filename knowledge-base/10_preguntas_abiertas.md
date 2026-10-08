# Preguntas Abiertas

> Fuente: `.active-orchestrator-state.json` → `discovery.preguntas_abiertas`,
> `discovery.no_evidenciado`, `discovery/verificacion-fuentes.md`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).
>
> Esta sección existe para que lo que no sabemos quede escrito. Ningún valor
> fue inventado para completar un campo.

## Inconsistencias detectadas

### IN-01 — La nota de Discovery sobre el competidor mejor puntuado quedó desactualizada
**Documento A dice**: `discovery/sources/orbita.md` afirma que el competidor de
mejor puntuación no publica agenda por sillón y que es el único del rubro en
tenerla.
**Documento B dice**: el informe de Discovery, en la corrección H-01, sostiene
justamente lo contrario: que el competidor de mejor puntuación sí ofrece agenda
por sillón (con choque imposible) y no es exclusivo suyo.
**Impacto**: si alguien lee solo la nota de la fuente, concluye que la agenda por
sillón es un hueco de mercado. Si lee el informe, concluye que ya está cubierto.
**Resolución propuesta**: la nota de la fuente debe quedar marcada como corregida
(o reescribirse), dado que H-01 y la nota no pueden coexistir.
**Estado**: **[RESUELTO — 2026-10-05, protocolo Ajustar, H-01]**. El informe
de Discovery documenta la corrección; la fuente original se conserva como registro
histórico y la verificación queda registrada en `discovery/verificacion-fuentes.md`
y en `docs/discovery/informe-discovery.md`.

### IN-02 — Dos escalas de puntuación conviviendo en los artefactos
**Documento A dice**: el informe de Discovery y `.active-orchestrator-state.json`
usan una matriz de 7 criterios con escala de 0 a 5.
**Documento B dice**: `docs/discovery/checklist-discovery.md` conservaba la matriz
anterior, con puntajes sobre 10 y un total de 9,75 (versión previa al ajuste).
**Impacto**: los números no eran comparables. Un 4,88 sobre 5 y un 9,75 sobre 10
parecían la misma calidad y no lo son.
**Resolución**: 0-5 es la única escala oficial en todo el proyecto. El
`checklist-discovery.md` actualiza la referencia a la matriz oficial de 0-5,
marcando la matriz inventada como superada dentro de `<details>`.
**Estado**: **[RESUELTO — 2026-10-05, protocolo Ajustar, H-05]**. La matriz
oficial está en `docs/discovery/informe-discovery.md` §B, con pesos
25/20/15/15/10/10/5.

### IN-03 — El competidor mejor puntuado ya no coincide con la afirmación de precio
**Documento A dice**: `discovery/sources/orbita.md` registraba que no había precio
público verificable.
**Documento B dice**: el relevamiento posterior confirmó que ese competidor sí
publica precios en su sitio (plan Consultorio desde USD 25/mes).
**Impacto**: usar el texto viejo para justificar precio sería mostrar un dato
desactualizado.
**Resolución**: corregido en el informe (H-06). La verificación manual de fuentes
confirma el precio público publicado por Órbita.
**Estado**: **[RESUELTO — 2026-10-05, protocolo Ajustar, H-06]**. Ver
`docs/discovery/informe-discovery.md` (D y E) y
`discovery/verificacion-fuentes.md` para el registro de lo verificado.
### IN-04 — La muestra no representa al mercado
**Documento A dice**: el relevamiento cubre 19 sistemas.
**Documento B dice**: los 19 tienen presencia digital, por lo sesgo de selección
es inevitable: un consultorio que no aparece en internet no aparece en la
muestra.
**Impacto**: cualquier afirmación del tipo "el mercado tiene N competidores" o
"ningún competidor hace X" solo es valida **dentro** de la muestra, no del
mercado.
**Resolución propuesta**: toda conclusión de mercado debe llevar la coletilla
"en la muestra relevada". Es una restricción de lenguaje, no de análisis.

## Lo que Discovery no evidencio

Este bloque es el más importante del archivo. Estos son los puntos que el
Discovery dejó como "No evidenciado", tal como figuran en `discovery/discovery.md`.

- **No evidenciado** — duración promedio real por práctica odontológica. Ningún
  competitor publica un nomenclador de duraciones abierto; hay que configurarlas
  a mano.
- **No evidenciado** — precio real de la mayoría. 8 de 19 no publican precio;
  DentalPro y Lumident cobran en USD, turnosuno publica promo con 80% off.
- **No evidenciado** — que la agenda por sillón sea un factor de compra
  decisionario. Sólo Órbita la nombra como eje y no publica su precio, así que
  no hay forma de saber si se cobra.
- **No evidenciado** — número real de usuarios activos. DenPro declara "+500
  profesionales", DentalSoft "300+ clínicas", DentalTec "2.000+ profesionales":
  son cifras declaradas por el vendedor, sin auditoría ni fuente primaria.
- **No evidenciado** — si algún competidor argentino cumple efectivamente la Ley
  27.553 de receta electrónica en producción. ClinIA declara identificador 248 en
  ReNaPDiS, pero no hay verificación pública de uso real.

Otros hallazgos y preguntas abiertas se mantienen en las secciones siguientes para preservar el contenido original.

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
| Media | ¿Qué formato de exportación necesita el paciente? | Sprint 3 | Producto |
| Media | ¿Se implementa la agenda responsive en el v1? | Sprint 3 | Equipo |
| Media | ¿Qué tecnologías del curso se aceptan? | Sprint 1 | Equipo |
| Baja | ¿Cómo se miden las metricas de éxito del sistema? | Post-lanzamiento | Producto |
| Baja | ¿Qué limites de uso y quotas necesita un consultorio? | Post-lanzamiento | Equipo |

## Campos que la generación automática no pudo inferir

Esta sección la escribio `kb-creator` siguiendo la regla de baja confianza del
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
a ser decisiones, no propuestas.

El riesgo que se había signaled sigue en pie y ahora hay que sostenerlo: PostgreSQL
no es negociable, porque la restricción `EXCLUDE USING gist` que garantiza la
ausencia de solapamientos no existe en SQLite ni en MySQL. Si alguien propone
cambiar de base de datos, hay que volver a `04_modelo_de_datos.md`.

### `[DISCOVERY] system_type`

Se inferí `web_app` con confianza alta, por dos senales concordantes: el
odontólogo necesita una interfaz de uso diario y el paciente accede por web pública sin instalar nada. Se registra igual para que quede explícito.

### `[DISCOVERY] needs_infra`

Se fijo `true` con confianza alta, y **no** por las integraciones de terceros,
que son todas post-v1. Es `true` porque el modelo de datos exige una base
relacional con exclusión constraints y porque hay que desplegar backend y base
de datos propios.

### `[DISCOVERY] scale`

Se inferí `public_multi_user`: el odontólogo es un usuario único de uso diario y
el paciente es público y no autenticado. Lo que este valor **no** implica es
multi-tenant; ver DD-02.

## Lo que hay que resolver antes de escribir código

En este orden:

1. **Stack tecnológico.** Sin esto no se puede escribir ni una línea.
2. **Identidad y autenticación del paciente.** Ver PREG-02 y PREG-03.
3. **Marco legal de la historia clínica.** Ver PREG-05 y PREG-06.
4. **Consultorio piloto.** Ver PREG-01 y SU-03. Sin un piloto real, el resto de
   las decisiones son theory.