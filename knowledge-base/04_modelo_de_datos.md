# Modelo de Datos

> Fuente: `docs/discovery/informe-discovery.md`, `.active-orchestrator-state.json` → `discovery.casos_de_uso`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

## Dominios

| Dominio | Descripción |
|---------|-------------|
| Agenda | Disponibilidad, reservas, bloqueos de franja y duraciones por práctica |
| Pacientes | Datos de contacto, consentimiento y relación con sus turnos |
| Salud | Odontograma básico y registro de atenciones |
| Administración | Usuario único, prácticas, configuración del consultorio |
| Auditoría | Registro de accesos a datos sensibles y de operaciónes administrativas |

## ERD (Entity Relationship Diagram)

```
  Práctica ──< PracticaDuracion >── Recurso (sillón)
      |              |                      |
      |              v                      v
      +──────────> Turno ──────────> Bloqueo
                      |
                      v
  Paciente ──< Turno
      |
      +──< HistorialClinico
      |        └──< EntradaOdontograma
      |
      +──< AuditoríaAcceso >── Usuario
```

Relaciones clave:

- `Turno` pertenece a **un** `Recurso` (sillón) y a **una** `Práctica`.
- `PracticaDuracion` resuelve el intervalo real de un turno a partir de la práctica.
- `Paciente` tiene **cero o muchos** `Turno`; un turno tiene **exactamente una**
  `Paciente`.
- `Bloqueo` compite por el mismo recurso que `Turno` y por eso comparte su
  restricción de exclusión.

## Entidades

### Práctica
- `id` UUID PK
- `nombre` varchar(80) UNIQUE
- `duracion_minutos` int, CHECK > 0
- `color` varchar(7), para mostrar en la agenda
- `activa` boolean, default true
- Relaciones: `1:N` con `PracticaDuracion`, `1:N` con `Turno`
- Notas: la duración vive aquí como valor por defecto, pero se puede ajustar por
  recurso en `PracticaDuracion`.

### PracticaDuracion
- `id` UUID PK
- `practica_id` UUID FK
- `recurso_id` UUID FK
- `duracion_minutos` int, CHECK > 0
- UNIQUE (`practica_id`, `recurso_id`)
- Índice: (`recurso_id`, `practica_id`)
- Notas: modela el caso real de un consultorio donde una práctica dura 30 minutos
  en un sillón y 45 en otro.

### Recurso (sillón)
- `id` UUID PK
- `nombre` varchar(60)
- `activo` boolean, default true
- Relaciones: `1:N` con `PracticaDuracion`, `1:N` con `Turno`, `1:N` con `Bloqueo`
- Notas: en el v1 el consultorio tiene un único consultorio físico, así que la
  tabla se crea con una sola fila. La tabla existe para no tener que migrar el
  esquema si se agrega un segúndo sillón, que es el caso más probable según el
  relevamiento.

### DisponibilidadSemanal
- `id` UUID PK
- `dia_semana` int 0-6
- `hora_inicio` time
- `hora_fin` time
- `recurso_id` UUID FK
- CHECK (`hora_fin` > `hora_inicio`)
- Notas: patron recurrente semanal. No se modelan excepciones de fecha en el v1;
  las feriados y vacaciones se resuelven con `Bloqueo`.

### Turno
- `id` UUID PK
- `paciente_id` UUID FK, NOT NULL
- `practica_id` UUID FK, NOT NULL
- `recurso_id` UUID FK, NOT NULL
- `inicio` timestamptz, NOT NULL
- `fin` timestamptz, NOT NULL
- `estado` enum: `confirmado`, `cancelado`, `completado`, `no_asístio`
- `token_público` uuid UNIQUE, NOT NULL
- `motivo_cancelacion` text, nullable
- `cancelado_por` enum: `paciente`, `consultorio`, nullable
- CHECK (`fin` > `inicio`)
- **Restricción de exclusión (clave del modelo)**: dos turnos `confirmado` no
  pueden solaparse en el mismo `recurso_id`.

### Bloqueo
- `id` UUID PK
- `recurso_id` UUID FK, NOT NULL
- `inicio` timestamptz, NOT NULL
- `fin` timestamptz, NOT NULL
- `motivo` varchar(120), nullable
- CHECK (`fin` > `inicio`)
- Índice: (`recurso_id`, `inicio`)
- **Restricción de exclusión (NO resuelto, ver abajo):** esta tabla comparte
  `recurso_id` con `Turno`, pero una restricción `EXCLUDE` de PostgreSQL es
  **por tabla** y no puede cubrir las dos. Ver «Deuda de diseño: la exclusión
  entre `Turno` y `Bloqueo`».

### Paciente
- `id` UUID PK
- `nombre` varchar(120), NOT NULL
- `telefono` varchar(32), NOT NULL
- `email` varchar(160), nullable
- `documento` varchar(32), nullable
- `fecha_nacimiento` date, nullable
- `consentimiento_salud_at` timestamptz, nullable
- `consentimiento_salud_versión` varchar(16), nullable
- `anulado_at` timestamptz, nullable
- Índice único parcial: (`telefono`) WHERE `anulado_at` IS NULL
- Notas: el paciente no tiene credenciales. El acceso suyo es por `token_público`.
  Ver DD-04.

### HistorialClinico
- `id` UUID PK
- `paciente_id` UUID FK, NOT NULL
- `abierto_at` timestamptz, NOT NULL
- Notas: uno por paciente. Contiene datos sensibles: acceso auditado y cifrado en
  reposo según RN-PRIV-02.

### EntradaOdontograma
- `id` UUID PK
- `historial_id` UUID FK, NOT NULL
- `pieza` varchar(4), NOT NULL
- `cara` varchar(2), NOT NULL
- `estado` varchar(20), NOT NULL
- `turno_id` UUID FK, nullable
- `registrado_at` timestamptz, NOT NULL
- UNIQUE (`pieza`, `cara`, `historial_id`)
- Notas: el odontograma mínimo del v1 no usa una tabla de caras completa; el
  modelo queda deliberadamente simple. Ampliarlo es post-v1.

### Usuario
- `id` UUID PK
- `email` varchar(160) UNIQUE, NOT NULL
- `password_hash` varchar(255), NOT NULL
- `nombre` varchar(120), NOT NULL
- `activo` boolean, default true
- Notas: tabla de una sola fila en el v1. Existe por trazabilidad, para que la
  auditoría pueda atribuir cada operación a un responsable con nombre.

### AuditoríaAcceso
- `id` UUID PK
- `usuario_id` UUID FK, nullable
- `paciente_id` UUID FK, nullable
- `recurso_accedido` varchar(60), NOT NULL
- `accion` varchar(40), NOT NULL
- `ip` inet, nullable
- `user_agent` text, nullable
- `ocurrida_at` timestamptz, NOT NULL, default now()
- Índice: (`paciente_id`, `ocurrida_at` DESC)
- Notas: append-only. No se actualiza ni se borra. Ver RN-PRIV-03.

## La restricción que evita el doble booking

Es la decisión de datos más importante del proyecto, así que va explícita.

El problema: si la validación de disponibilidad vive solo en el backend, dos
peticiones simultaneas pueden leer el mismo slot libre y escribir dos turnos.

La solución: que la base de datos rechace el solapamiento.

```sql
EXCLUDE USING gist (
  recurso_id WITH =,
  tstzrange(inicio, fin) WITH &&
)
WHERE (estado = 'confirmado')
```

Efectos:

1. Dos inserciones simultaneas sobre el mismo slot: **una** falla. La que pierde
   recibe un error de restricción y la API responde con un conflicto.
2. El test que valida esto es de integración contra Postgres real, no unitario.
3. El motor de disponibilidad de `05_reglas_de_negocio.md` sigue siendo
   necesario, pero como optimización y como experiencia de usuario, no como
   garantia de integridad.

Costo aceptado: Postgres deja de ser reemplazable por una base relacional más
simple. Ver DD-05.

## Deuda de diseño: la exclusión entre `Turno` y `Bloqueo`

> **Estado: abierta. No decidida. Requiere decisión del equipo antes de
> implementar el turno y el bloqueo.** Registrada el 2026-10-05 durante la
> verificación de la fundación, al leer este modelo contra lo que PostgreSQL
> permite hacer.

### El problema

Este modelo dice que `Turno` y `Bloqueo` compiten por el mismo `recurso_id` y que
ambos la resuelven con una restricción de exclusión. **Eso no es implementable
como está escrito.**

Una restricción `EXCLUDE USING gist` pertenece a **una sola tabla**. No puede
abarcar `Turno` y `Bloqueo` a la vez, porque son dos tablas distintas con dos
conjuntos de índices separados. La consecuencia es la siguiente:

```sql
-- Turno confirmado: 10:00 a 10:30 en el sillón 1  -> se guarda
-- Bloqueo del odontólogo: 10:15 a 11:00 en el sillón 1 -> TAMBIÉN se guarda
```

Las dos escrituras pasan. La base no dice nada, porque cada restricción solo ve
su propia tabla.

Por eso el modelo debe decir que `Bloqueo` comparte el `recurso_id` con `Turno` y
**que el conflicto entre ambos es responsabilidad de la aplicación**, no de una
restricción declarativa. Y por eso la garantía de DD-05 es **parcial**: cubre
turno contra turno, que es el caso que RN-AGE-03 describe literalmente, pero no
cubre turno contra bloqueo, que RN-AGE-05 y US-004-CA-1 dan por sentado.

### Las dos salidas

| Opción | Cómo funciona | Costo |
|--------|---------------|-------|
| **A — Tabla única de reserva de agenda** | `Turno` y `Bloqueo` pasan a ser filas de una tabla `ReservaAgenda` con un campo discriminador (`tipo`). La restricción `EXCLUDE` vive **una sola vez**, sobre esa tabla. Los datos de `Turno` (paciente, práctica, token) quedan en una tabla aparte relacionada | Reescritura del esquema. `Turno` deja de ser una tabla y pasa a ser un detalle de la reserva. Es la solución que un motor de agenda real usa |
| **B — Trigger de verificación cruzada** | Se conserva el esquema actual y se agrega un trigger `AFTER INSERT OR UPDATE` sobre ambas tablas que consulta la tabla hermana y aborta si encuentra solapamiento | Dos triggers que se mantienen sincronizados. Un trigger mal escrito es un bug silencioso: la garantía depende de código, no del declarativo |

**Cuál usar no es una decisión de kb-creator.** Es una decisión de diseño con
consecuencias distintas sobre el modelo de datos, el modelo de consultas y los
tests, y por eso queda escrita acá para que el `design.md` del change la tome de
forma explícita en Propose, en lugar de resolverla por omisión durante Apply.

### Lo que esto obliga igual

- La validación de disponibilidad de `05_reglas_de_negocio.md` tiene que seguir
  existiendo: es la que da la experiencia de usuario y la que evita el viaje de
  ida y vuelta a la base para que el conflicto se rechace. La exclusión nunca fue
  la primera línea, fue la red.
- El test de solapamiento tiene que cubrir **los dos casos por separado**: turno
  contra turno, y turno contra bloqueo. Un test que solo cubre el primero deja el
  segundo sin verificar, que es exactamente el falso positivo que RN-AGE-03
  busca evitar. Ver DD-10.
- Cualquiera de las dos opciones conserva el requisito duro de PostgreSQL, así
  que DD-05 no se ve afectada.

## Seed data inicial

| Tabla | Contenido mínimo |
|-------|------------------|
| Usuario | Un odontólogo, email y password definidos por el que instala |
| Recurso | Un sillón, activo |
| Práctica | Consulta, Limpieza, Obturación, Extracción, Radiografia de pano |
| PracticaDuracion | Una fila por cada práctica con el sillón único |
| DisponibilidadSemanal | Las franjas que defina el odontólogo al instalar |
| HistorialClinico | Ninguna: se crea en el primer turno |

Ninguno de estos valores de ejemplo es un dato real de paciente. Discovery
prohibio explícitamente usar información de salud real en ejemplos.