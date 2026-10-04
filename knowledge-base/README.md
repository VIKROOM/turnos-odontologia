# Turnos Odontológicos — Base de Conocimiento

Base de conocimiento generada a partir de los documentos de Discovery del
proyecto (`docs/discovery/` y `.active-orchestrator-state.json`).

Generada con la skill `kb-creator` en **Modo A (silencioso)**, a partir de
documentos existentes. `source: "ingest"`.

## Índice de archivos

| Archivo | Contenido |
|---------|-----------|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, objetivos por actor, alcance v1, fuera de alcance, métricas |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack decidido, arquitectura, integraciones, API REST |
| [03_actores_y_roles.md](03_actores_y_roles.md) | Actores, matriz RBAC, rutas públicas y privadas |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | 5 dominios, ERD, 11 entidades, seed, restricción de exclusión |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | 4 dominios de reglas con códigos RN, más excepciones globales |
| [06_funcionalidades.md](06_funcionalidades.md) | 7 épicas, 18 historias de usuario con criterios de aceptación |
| [07_flujos_principales.md](07_flujos_principales.md) | 8 flujos extremo a extremo, incluido el intento de doble reserva |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, estructura de directorios, seguridad, variables de entorno |
| [09_decisiónes_y_supuestos.md](09_decisiónes_y_supuestos.md) | 8 decisiónes documentadas y 8 supuestos con su riesgo |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | 4 inconsistencias, 10 puntos no evidenciados, 12 preguntas priorizadas |

## Quick Start para Desarrolladores

1. Entender el dominio → [01](01_vision_y_objetivos.md),
   [03](03_actores_y_roles.md)
2. Entender los datos → [04](04_modelo_de_datos.md)
3. Entender las reglas → [05](05_reglas_de_negocio.md)
4. Entender la arquitectura → [02](02_descripcion_general.md),
   [08](08_arquitectura_propuesta.md)
5. Implementar → [06](06_funcionalidades.md), [07](07_flujos_principales.md)
6. **Antes de codificar** → [10](10_preguntas_abiertas.md)

## Resumen Ejecutivo

Una agenda de turnos para consultorios odontológicos unipersonales: el
odontólogo publica su disponibilidad y el paciente reserva sin llamar por
teléfono. El dato de mercado que sostiene el proyecto es que los 19 sistemas
relevados ya ofrecen agenda electrónica, así que **la agenda no es el
diferencial**: la oportunidad está en el borde (ausentismo, derivación de
urgencias, auditoría, exportación).

La decisión técnica que define el resto es que el conflicto de horario se
resuelve en la capa de datos, con una restricción de exclusión sobre el recurso
y un rango de tiempo. Eso descarta bases de datos más simples a propósito.

## Advertencia de honestidad

El stack tecnológico **está decidido** (FastAPI + PostgreSQL + React + Docker,
DD-11), pero esa decisión la tomó el equipo el 2026-10-03: **Discovery no eligió
tecnologías**, porque la consigna las deja libres. Conviene tener presente la
diferencia, porque una decisión nuestra no es un hallazgo de la investigación.

Los diez puntos que el relevamiento no pudo responder están
en [10_preguntas_abiertas.md](10_preguntas_abiertas.md), y se repiten como
supuestos o como "No evidenciado" en los archivos que los usan. **Ninguno se rellenó
con una estimación.**

No inventes valores para completar esta base. Si algo no está escrito, es porque
no se sabe, y si está escrito como decisión, es porque lo decidimos nosotros.
