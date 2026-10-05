# Arquitectura

> Fuente: `docs/discovery/informe-discovery.md`, `discovery/verificacion-fuentes.md`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).
>
> **Estado**: arquitectura **decidida** sobre el stack que el equipo fijó el
> 2026-10-03 (FastAPI + PostgreSQL + React + Docker). Discovery no eligió
> tecnologías, así que esto no es un hallazgo de la investigación sino una decisión
> documentada: DD-11 en `09_decisiones_y_supuestos.md`.

## Patrones aplicados

| Patron | Donde se usa | Por que |
|--------|--------------|---------|
| Repository | Acceso a datos | Permite testear las reglas de negocio sin base de datos |
| Service / Dominio puro | Motor de disponibilidad | Las reglas son funciones puras sobre intervalos: testeables en memoria |
| Unit of Work | Reservar, reprogramar | Cancelar y crear turno en una sola transacción (RN-AGE-07) |
| Dependency Injection | Rutas de FastAPI | Los tests reemplazan el repositorio por un doble en memoria |
| Row Level Security | Tablas de datos de salud | Defensa en profundidad si un endpoint expone datos de otro paciente |
| Append-only log | `AuditoríaAcceso` | La auditoría no se puede reescribir, ni por error ni por malicioso |
| Exclusión constraint | Solapamiento de turnos | La integridad no depende de que el código de aplicación la respete |

Sobre **Row Level Security**: el usuario único del v1 lo haría redundante. Se
documenta igual porque es la red que impide que un error de programación en un
endpoint de paciente termine en una fuga de historia clínica. Es barato
activarlo ahora y caro agregarlo después.

## Estructura de directorios

```
turnos-odontologia/
├── backend/
│   └── app/
│       ├── domain/
│       │   ├── agenda/          # motor de disponibilidad, intervalos
│       │   ├── pacientes/       # reglas de ficha y consentimiento
│       │   └── clínica/         # odontograma, atenciones
│       ├── application/
│       │   ├── dto/             # esquemas de entrada y salida
│       │   └── services/        # casos de uso: reservar, cancelar, reprogramar
│       ├── infrastructure/
│       │   ├── db/              # repositorios, migraciones, RLS
│       │   ├── security/        # auth, cifrado, auditoría
│       │   └── config/          # settings, variables de entorno
│       └── api/
│           ├── routers/         # endpoints por recurso
│           └── deps.py
├── frontend/
│   └── src/
│       ├── pages/              # agenda, pacientes, configuración
│       ├── components/
│       └── lib/                # cliente HTTP, helpers
├── knowledge-base/              # esta base de conocimiento
└── docs/discovery/              # informe de Discovery
```

Decisión de layout: `domain/` no importa nada de `infrastructure/`. Esa regla
es la que permite que el motor de disponibilidad se pruebe sin base de datos ni
sin levantar el servidor.

## La pieza central: motor de disponibilidad

Recibe las franjas, los turnos y los bloqueos; devuelve los horarios libres. No
escribe nada.

```
disponibilidad(disponibilidad_semanal, turnos, bloqueos, practica, fecha)
      -> lista de intervalos [inicio, fin)
```

Se apoya en una operación de conjuntos: **disponibilidad menos turnos menos
bloqueos**. El orden importa, y hay un caso límite que hay que tratar de forma
explícita: si un turno termina exactamente cuando otro empieza, no hay
solapamiento y el intervalo es compartido. Los intervalos son cerrados por la
izquierda y abiertos por la derecha, `[inicio, fin)`.

Ese mismo criterio se aplica en la base de datos con `tstzrange(inicio, fin)`,
que ya es semiabierto por defecto. La lógica del servidor y la restricción de la
base coinciden porque comparten la misma convención.

## Seguridad

| Aspecto | Enfoque | Referencia |
|---------|---------|------------|
| Autenticación | JWT en cookie httpOnly, SameSite estricto | RN-AU-02 |
| Autorización | Un solo rol; el paciente accede por token de un solo uso | `03_actores_y_roles.md` |
| Validación de input | Esquemas Pydantic en el borde; el navegador nunca es la frontera | RN-GEN-04 |
| Datos sensibles | Cifrado en reposo de `HistorialClinico` | RN-PRIV-02 |
| Aislamiento de datos | Row Level Security sobre tablas de salud | DD-08 |
| Auditoría | Append-only, escribe antes de leer | RN-PRIV-03 |
| Rate limiting | En login y en la reserva pública | RN-AU-03 |
| Secrets | Varíables de entorno; ningún secreto en el repositorio | tabla de abajo |
| Transport | TLS obligatorio entre navegador y servidor | — |

Sobre el token del paciente: se genera con fuente criptografica, no con
`random()`. Un token adivinable sería un token de acceso a una cita médica de
otra persona. El test de seguridad correspondiente es que el token tenga al menos
128 bits de entropia real, medidos sobre las implementaciones que se usen.

## Varíables de entorno

| Varíable | Descripción | Ejemplo | Sensible |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Conexión a Postgres | `postgresql://user:pass@db:5432/turnos` | Si |
| `SECRET_KEY` | Firma de los JWT | `generar con openssl rand -hex 32` | Si |
| `ENCRYPTION_KEY` | Cifrado de datos de salud | `generar con openssl rand -hex 32` | Si |
| `TOKEN_TTL_HOURS` | Duración de la sesión | `8` | No |
| `CANCELLATION_MIN_HOURS` | Plazo mínimo de cancelación | `24` | No |
| `COOKIE_SECURE` | Exigir HTTPS en la cookie | `true` | No |
| `APP_ENV` | Entorno de ejecución | `production` | No |
| `LOG_LEVEL` | Nivel de log | `INFO` | No |

La separación entre `SECRET_KEY` y `ENCRYPTION_KEY` es intencional: son
compromisos distintos con alcances distintos. Que un token de sesión se filtre no
debe volcar las historias clínicas.

## Requisitos de infraestructura

`needs_infra` es `true`, y no por las integraciones de terceros, que son todas
post-v1. Es `true` por esto:

1. **Base de datos relacional con exclusión constraints.** Postgres. La
   integridad de la agenda depende de una función que SQLite y MySQL no ofrecen
   de forma nativa. Ver DD-05.
2. **Backend propio con despliegue propio.** No hay un esquema serverless que
   resuelva esto sin decidir la base de datos primero.
3. **Migraciones versiónadas.** El esquema tiene una restricción que no se puede
   crear desde la aplicación y hay que poder volver atrás.
4. **Certificado TLS.** Obligatorio, no opcional.

No se necesita: cola de mensajes, cache distribuida, cluster, ni orquestador de
contenedores. Un único contenedor de backend, uno de base de datos y uno de
frontend los cubre.

## Lo que la arquitectura NO incluye a propósito

| No incluido | Motivo |
|-------------|--------|
| Cola de mensajes | No hay trabajo asíncrono en el v1. Los recordatorios, que si lo necesitarían, están fuera |
| Cache distribuida | Un consultorio con un odontólogo y agenda semanal no genera carga que justifique Redis |
| Multi-instalación por tenant | Ver DD-02 |
| Microservicios | Un único dominio con una transacción crítica. Partirlo sólo agrega complejidad de consistencia |