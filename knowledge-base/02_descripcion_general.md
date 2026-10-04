# Descripción General

> Fuente: `docs/discovery/informe-discovery.md`, `discovery/verificacion-fuentes.md`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

## Stack tecnológico

> **Decidido por el equipo el 2026-10-03.** Discovery no eligió tecnologías —la
> consigna del trabajo las deja libres— así que el stack es una decisión del equipo,
> no un hallazgo de la investigación. Queda registrada como **DD-11** en
> `09_decisiones_y_supuestos.md`.

| Capa | Tecnología | Versión mínima | Estado |
|------|-----------|-----------------|--------|
| Backend | FastAPI (Python) | 3.11 | Decidido |
| Base de datos | PostgreSQL | 15 | Decidido |
| Frontend | React + Vite | React 18 | Decidido |
| Autenticación | JWT con cookies httpOnly | — | Decidido |
| Despliegue | Docker Compose | — | Decidido |

PostgreSQL no es una preferencia de gusto: es el único requisito duro del proyecto.
La ausencia de solapamiento de turnos tiene que garantizarse **en la capa de datos**,
no en el código de aplicación, y eso exige una restricción de exclusión con rangos
(`EXCLUDE USING gist`), que solo Postgres ofrece de forma nativa. El argumento
completo está en `04_modelo_de_datos.md` y la decisión en `09_decisiones_y_supuestos.md`
(DD-05).

## Arquitectura general

Arquitectura por capas, en tres niveles, con el motor de reglas de disponibilidad
como núcleo aislado del dominio clínico.

```
   NAVEGADOR (odontólogo)        NAVEGADOR (paciente)
            |                              |
            +---------------+--------------+
                            v
                   API REST (FastAPI)
                            |
     +---------+---------+---+-------+----------+
     v         v         v       v          v
  Auth     Agenda   Pacientes  Historia   Reportes
  (RN-AU)  (RN-AGE)  (RN-PAC)  (RN-CLI)   (post-v1)
     |         |
     |         +--> Motor de disponibilidad  <-- reglas de negocio puras
     |                  |
     +-------------> PostgreSQL
                        (restriccion de exclusion: sin solapamiento)
```

Decisiones de alto nivel y su motivo:

1. **API REST + render en el servidor para la agenda del odontólogo.** El
   consultorio tiene un solo usuario con acceso diario. Una SPA completa agrega
   complejidad de build, cache y estado sin aporte de valor real en el v1.
2. **El paciente no tiene cuenta en el v1.** Reserva con un enlace firmado por
   turno. Ver `09_decisiones_y_supuestos.md`, DD-04.
3. **La disponibilidad es una funcion pura y testeable.** Todas las reglas de
   `05_reglas_de_negocio.md` se evaluan contra una lista de intervalos, sin
   tocar la base de datos. Eso permite cubrirlas con tests unitarios sin
   levantar infraestructura.
4. **El conflicto de horario no se resuelve en el backend de aplicación.** Se
   resuelve con una restricción de base de datos. Ver DD-05.

## Integraciónes externas

Discovery conclusión: **ninguna integración externa es obligatoria en el v1**.
Este es un hallazgo con confianza alta, verificado en `discovery/verificacion-fuentes.md`.

| Servicio | Propósito | Tipo | Estado |
|----------|-----------|------|--------|
| WhatsApp Business API | Recordatorios | API de proveedor | Fuera de v1 |
| Servicio de email transacciónal | Confirmaciones | SMTP o API | Fuera de v1 |
| AFIP / ARCA | Facturación electrónica | API SOAP | Fuera de v1 |
| Obras sociales / coseguros | Credenciales y aceptacion | Sin definir | Fuera de v1 |
| Pasarela de pago | Cobro de anticipos | Sin definir | No fue evaluado |

`needs_infra` es de todos modos `true`: aunque no haya integraciones de terceros, el
sistema necesita backend, base de datos y despliegue propio.

## API REST (propuesta)

Orientado a recursos. Todas las rutas bajo `/api/v1`. Las públicas de paciente van
en `/api/v1/public` y no requieren sesión.

### Disponibilidad y reservas

| Método | Ruta | Auth | Propósito |
|--------|------|------|-----------|
| GET | `/api/v1/public/disponibilidad?fecha=&practica=` | No | Horarios libres para un día |
| POST | `/api/v1/public/turnos` | No | Crear reserva (enlace firmado) |
| GET | `/api/v1/public/turnos/{token}` | No | Consultar turno por token |
| POST | `/api/v1/public/turnos/{token}/cancelar` | No | Cancelar con reglas de plazo |
| POST | `/api/v1/public/turnos/{token}/reprogramar` | No | Reagendar |
| GET | `/api/v1/agenda/turnos?desde=&hasta=` | Si | Agenda del odontólogo |
| POST | `/api/v1/agenda/bloqueos` | Si | Bloquear una franja |
| DELETE | `/api/v1/agenda/bloqueos/{id}` | Si | Liberar un bloqueo |

### Pacientes

| Método | Ruta | Auth | Propósito |
|--------|------|------|-----------|
| GET | `/api/v1/pacientes` | Si | Listar y buscar |
| GET | `/api/v1/pacientes/{id}` | Si | Ficha |
| POST | `/api/v1/pacientes` | Si | Alta |
| PUT | `/api/v1/pacientes/{id}` | Si | Editar |
| GET | `/api/v1/pacientes/{id}/turnos` | Si | Historial de turnos |
| GET | `/api/v1/pacientes/{id}/historia` | Si | Historia clínica |

### Salud del paciente (endpoint sensible)

| Método | Ruta | Auth | Propósito |
|--------|------|------|-----------|
| GET | `/api/v1/pacientes/{id}/salud` | Si + auditoría | Odontograma y atenciones |
| PUT | `/api/v1/pacientes/{id}/salud/entradas` | Si + auditoría | Registrar atención |

Todo acceso a `/salud` escribe una fila de auditoría antes de devolver datos.
Ver RN-PRIV-03 en `05_reglas_de_negocio.md`.

### Autenticación

| Método | Ruta | Auth | Propósito |
|--------|------|------|-----------|
| POST | `/api/v1/auth/login` | No | Iniciar sesión |
| POST | `/api/v1/auth/logout` | No | Cerrar sesión |
| GET | `/api/v1/auth/me` | Si | Usuario actual |

## Base de la competencia (por qué el problema sigue abierto)

Relevamiento de 19 sistemas del rubro odontológico argentino. La tabla completa,
con la matriz de puntuación y la fecha de consulta, está en el informe de
Discovery. El dato que sostiene el proyecto:

| Capacidad | Sistemas que la ofrecen |
|-----------|--------------------------|
| Agenda electrónica | 19 de 19 |
| Recordatorios automáticos | 13 de 19 |
| Historia clínica electrónica | 17 de 19 |
| Recordatorios por WhatsApp | 12 de 19 |

Consecuencia de producto: **la agenda no es un diferencial**. La agregacion por
sillón tampoco lo es, porque el competidor de mejor puncionacion ya lo hace.
Ver DD-06.