# Actores y Roles

> Fuente: `docs/discovery/informe-discovery.md`, `.active-orchestrator-state.json` → `discovery.usuarios`.
> Generado por `kb-creator` en modo silencioso (Mode A, `source: "ingest"`).

## Actores del sistema

| Actor | Descripción | Como interactua |
|-------|-------------|------------------|
| Odontólogo (dueño-operador) | Profesional independiente que atiende en su propio consultorio. Es a la vez dueno, operador y único usuario administrativo del sistema. | Sesión propia. Define disponibilidad, practices, bloqueos; ve toda la agenda; accede a fichas e historias clínicas. |
| Paciente | Persona que busca un turno. No es usuario registrado: no tiene contraseña ni cuenta en el v1. | Entra por enlace público, elige horario, deja sus datos una sola vez y recibe un enlace firmado para cancelar o reprogramar. |
| Asistente IA | Asistente de-orientación al paciente dentro del flujo de reserva. No decide disponibilidad ni confirma turnos por su cuenta. | Responde consultas de disponibilidad y guía la carga de datos. Toda reserva que produce pasa por las mismas reglas de negocio que una manual. |

Sobre la asistencia IA con datos de salud: aplica la Ley 25.326 de Protección de
Datos Personales, que clasifica el historial clínico como **dato sensible**. Ver
RN-PRIV-01 y el alcance real en `10_preguntas_abiertas.md`, PREG-05.

## RBAC — Matriz de permisos

El v1 tiene **un solo rol con acceso completo**. La matriz completa se documenta
aun así porque la consigna la pide, y porque deja registrado de forma explícita
que no existe separación de roles todavía.

| Rol | Recurso | Crear | Leer | Actualizar | Borrar |
|-----|---------|-------|------|-----------|--------|
| Odontólogo | Agenda (turnos) | Si | Si | Si | Si |
| Odontólogo | Bloqueos de franja | Si | Si | Si | Si |
| Odontólogo | Disponibilidad semanal | Si | Si | Si | Si |
| Odontólogo | Prácticas y duraciones | Si | Si | Si | Si |
| Odontólogo | Pacientes | Si | Si | Si | Si |
| Odontólogo | Historia clínica | Si | Si | Si | Si |
| Odontólogo | Datos de contacto del paciente | Si | Si | Si | No |
| Odontólogo | Exportación de datos | Si | Si | No | No |
| Odontólogo | Usuarios y roles | No | Si | No | No |
| Paciente | Su propio turno (via token) | Si | Si | Si | Si |
| Paciente | Su propia ficha | No | No | No | No |
| Paciente | Ficha de otro paciente | No | No | No | No |
| Asistente IA | Reglas de disponibilidad | No | Si | No | No |
| Asistente IA | Turnos | No | No | No | No |

Tres filas de esa tabla son restricciónes deliberadas y no olvidos:

1. **El paciente no puede leer su ficha ni su historia clínica.** Sólo su turno.
2. **El asístente IA no puede crear ni modificar turnos.** Consulta y orienta.
3. **El odontólogo no puede borrar datos de contacto del paciente.** Se anulan,
   no se borran. Ver RN-PRIV-04.

## Rutas públicas

Accesibles sin autenticación. La lista es corta a propósito: cada ruta pública es
superficie de ataque sobre datos de salud.

| Ruta | Método | Que expone | Protección |
|------|--------|-----------|------------|
| `/` | GET | Landing con info pública del consultorio | Ninguna |
| `/reservar` | GET | Formulario de reserva | Token de práctica en query |
| `/api/v1/public/disponibilidad` | GET | Horarios libres por fecha y práctica | Sólo disponibilidad, no datos personales |
| `/api/v1/public/turnos` | POST | Alta de reserva | Firma del enlace, rate limit |
| `/api/v1/public/turnos/{token}` | GET | Datos del turno del pacienteportador | Token aleatorio de un solo uso |
| `/api/v1/public/turnos/{token}/cancelar` | POST | Cancelación | Token + plazo mínimo |
| `/api/v1/public/turnos/{token}/reprogramar` | POST | Reprogramación | Token + disponibilidad real |

`/api/v1/public/disponibilidad` es deliberadamente la más expuesta: devuelve
horarios libres y **nunca** datos del paciente. Exponer menos no es posible si el
paciente tiene que elegir una hora.

## Rutas privadas

| Prefijo | Requiere | Rol |
|---------|----------|-----|
| `/agenda/*` | Sesión | Odontólogo |
| `/pacientes/*` | Sesión | Odontólogo |
| `/pacientes/*/salud/*` | Sesión + auditoría | Odontólogo |
| `/configuración/*` | Sesión | Odontólogo |
| `/api/v1/*` | Sesión, salvo las `/public` | Odontólogo |

## Modelo de escala

`scale` de la discovery: **`public_multi_user`**.

Se infiere del cruce de dos señales, no de una sola:

- El odontólogo es un usuario único, pero con uso diario intensification.
- El paciente es público y no autenticado: el sistema es de alcance público con
  multiples usuarios.

Lo que este dato **no** dice: el sistema no es multi-tenant. Cada instalación
sirve a un consultorio. Ver DD-02 en `09_decisiones_y_supuestos.md`.