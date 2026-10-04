# Checklist de once puntos — Discovery: Turnos Odontológicos

> Resultado estructurado de la skill `discovery-research`, guardado en la misma carpeta que el informe según la consigna.
> El informe con las secciones A, B, C y D está en [`informe-discovery.md`](informe-discovery.md) y en su versión PDF.

**Fecha**: 2026-10-03
**Fuentes investigadas**: 19 sistemas del mercado argentino (todos con URL y fecha de consulta en §4)
**Alcance de esta etapa**: Discovery de producto y mercado. No define stack ni arquitectura — eso es `kb-creator`.

---

## 1. Problema que resuelve

El consultorio odontológico unipersonal coordina los turnos en papel, cuaderno o
WhatsApp. Eso produce dos pérdidas concretas y medibles:

1. **Ausencias.** Un turno vacío es tiempo de sillón que no se recupera. Ningún
   competidor argentino resuelve esto mejor que los demás: 8 de 19 publican
   recordatorios por WhatsApp, o sea que la tooling existe pero no es lo que
   diferencia a nadie.
2. **Pérdida de control sobre la agenda.** El problema de fondo del unipersonal no
   es la doble reserva — es que no tiene forma de **reservar** un slot (un
   paciente recurrente que viene cada 6 meses, una urgencia, un bloque para un
   tratamiento largo) sin que un autoagendado se lo quede.

El eje que casi nadie modela bien: en odontología el recurso escaso es el **sillón
o box físico**, no el profesional. Los diecinueve sistemas
organizan la agenda "por profesional". Sólo **Órbita** nombra la agenda por
sillón como eje del producto, y **DentalFLOW** declara duración por consulta
configurable. El resto trata al sillón como un detalle de la interfaz.

**En una frase**: dar al consultorio unipersonal una agenda que se arma sola
cuando puede, pero que nunca le roba un slot que él reservó a propósito.

## 2. Usuarios / roles

- **Odontólogo** (dueño-operador): es a la vez administrador y profesional. Define
  horarios, duración por práctica, bloquea slots, atiende y documenta.
- **Paciente**: se agenda solo, sin llamar. Ve disponibilidad real, reserva,
  cancela o reprograma.

**Fuera de alcance en v1**: recepción, secretaria, odontólogo asistente,
administración de múltiples profesionales o sedes. El unipersonal es
 deliberado — es el segmento con precio de referencia claro (TurnosUno AR$6.000,
 Dentatools $30.000) y con la menor complejidad de liquidaciones.

## 3. Casos de uso

1. Como paciente, quiero ver los horarios libres de un sillón y reservar sin
   llamar, para no depender del horario de atención del consultorio.
2. Como odontólogo, quiero que la agenda se complete sola **pero poder bloquear y
   reservar los slots que necesito**, para no perder control operativo.
3. Como odontólogo, quiero ver la semana **por sillón** con la duración de cada
   práctica, para detectar huecos muertos y decidir cuánto tiempo ofrecer.
4. Como paciente, quiero cancelar o reprogramar mi turno yo mismo, sin llamar.
5. Como odontólogo, quiero la ficha del paciente con odontograma siempre a mano
   durante la consulta.

## 4. Competidores / soluciones existentes

**Fecha de consulta de todas las fuentes: 2026-10-03.**

| # | Sistema | URL | Señal de precio |
|---|---|---|---|
| 1 | DenPro | https://www.denpro.ar/ | $19.900 / $29.900 ARS — soporte **+34** (España), enfoque GDPR, no ARCA |
| 2 | DentalSaaS (DelRioTech) | https://dental.delriotech.com.ar/ | $59.000 / $149.000 ARS |
| 3 | Dentaly | https://www.dentaly.com.ar/ | $35.000 Pro / $100.000 Clínica ARS |
| 4 | Dentatools | https://dentatools.co/ar/ | $30.000 ARS — **no** obras sociales, **no** factura AFIP |
| 5 | TurnosUno | https://turnosuno.com/ | AR$6.000 prof. / AR$10.000 inst. |
| 6 | Bilog | https://bilog.com.ar/ | 1.500+ clínicas, 20+ años — sin precio público |
| 7 | DentalTec | https://web.dentaltec.com.ar/ | 2.000+ profesionales — sin precio público |
| 8 | DentalSoft | https://dentalsoft.com.ar/ | 300+ clínicas — sin precio público |
| 9 | Marfil Clinic | https://www.marfilclinic.com/ | "propuesta a medida" — sin precio público |
| 10 | DentalFLOW | https://dentalflow.ar/ | TrapelTech — sin precio público |
| 11 | DoctorYa | https://doctorya.com.ar/ | 1er mes gratis — factura por **ARCA** |
| 12 | ClinIA / OdontoClinIA | https://www.clinia.com.ar/odontologia | PUCO + ReNaPDiS 248 + HL7 FHIR + AFIP |
| 13 | Consultorio Digital | https://consultorio-digital.com.ar/ | sin precio público |
| 14 | Órbita | https://hiorbita.com/ | agenda **por sillón** + IA, La Plata |
| 15 | Benty | https://benty.com.ar/ | 1 mes bonificado |
| 16 | DentalPro | https://www.dentalpro.tech/ | **USD** 69 / 129 — no ARS |
| 17 | Turnos Online BB | https://turnosonlinebb.com/ | sin precio público |
| 18 | UDENTIVA | https://udentiva.com/pt-ar | precio "consulte" |
| 19 | Dentalink | https://softwaredentalink.com/ | sin precio público |

### Matriz comparativa ponderada

> ## ⚠️ Corrección H-05 — esta matriz fue reemplazada
>
> **La matriz de abajo es inválida: los pesos eran inventados y la escala estaba mal.** Se
> eligieron por densidad de decisión del MVP en lugar de usar los siete criterios
> oficiales, y la escala era 1–5 en vez de 0–5. Se conserva el registro del
> error, pero **no es la matriz que va en el entregable**.
>
> **La matriz oficial, con los pesos de la consigna (25/20/15/15/10/10/5) y escala
> 0–5, está en [`docs/discovery/informe-discovery.md`](../docs/discovery/informe-discovery.md)
> §B y en el PDF §B.** Ese es el entregable. La matriz oficial se reproduce á también en el [checklist de once puntos](checklist-discovery.md) de esta misma carpeta.
>
> Además, esta matriz estaba construida sobre cuatro datos que resultaron
> falsos. Ver la tabla de hallazgos en
> [`verificacion-fuentes.md`](verificacion-fuentes.md) y §E.1 del informe.
>
> **Por qué importa:** con los pesos correctos el ranking cambia. La versión
> inventada ponía a DentalSaaS primero (4,80) y a Órbita séptimo (3,55); la
> oficial pone a **Órbita primero (4,88/5) y a DentalSaaS segundo (4,30/5)**, porque
> el peso de turnos+automatización (25 %) y el de integraciones locales (15 %)
> castigan a un producto que tiene clínica impecable pero agenda genérica.

<details>
<summary><b>Matriz original (pesos inventados, escala 1–5) — conservada sólo como registro del error</b></summary>

Criterios y pesos (elegidos por densidad de decisión del MVP, no para favorecer
nuestra posición):

| Criterio | Peso | Por qué ese peso |
|---|---|---|
| A. Gestión de agenda y prevención de solapamientos | 25% | Es el producto. Sin anti-solapamiento no hay agenda. |
| B. Autogendamiento del paciente | 20% | Expectativa de mercado: el paciente no quiere llamar. |
| C. Alcance normativo argentino (ARCA/AFIP, obras sociales, receta electrónica) | 20% | Es lo que separa a los productos maduros de los restantes. |
| D. Historia clínica y odontograma | 15% | Necesario para atender, insuficiente para diferenciar. |
| E. Experiencia móvil / multidevice | 10% | El paciente reserva desde el teléfono. |
| F. Precio público y transparencia | 10% | 8 de 19 no publican precio: fricción real del sector. |

Escala 1–5. Ponderado = Σ(criterio × peso).

| Sistema | A 25% | B 20% | C 20% | D 15% | E 10% | F 10% | **Ponderado** |
|---|---|---|---|---|---|---|---|
| DentalSaaS (DelRioTech) | 5 | 5 | 4 | 5 | 5 | 5 | **4.80** |
| DentalSoft | 5 | 5 | 4 | 5 | 4 | 1 | **4.30** |
| DoctorYa | 5 | 5 | 4 | 3 | 4 | 2 | **4.10** |
| DentalFLOW | 5 | 5 | 2 | 4 | 5 | 1 | **3.85** |
| ClinIA / OdontoClinIA | 4 | 3 | 5 | 5 | 3 | 1 | **3.75** |
| Dentatools | 4 | 5 | 1 | 4 | 4 | 5 | **3.70** |
| Dentaly | 4 | 2 | 3 | 5 | 4 | 5 | **3.65** |
| Órbita | 5 | 3 | 3 | 4 | 4 | 1 | **3.55** |
| DentalTec | 4 | 3 | 4 | 4 | 4 | 1 | **3.50** |
| Bilog | 4 | 3 | 4 | 4 | 3 | 1 | **3.40** |
| Dentalink | 4 | 4 | 2 | 4 | 3 | 1 | **3.20** |
| Marfil Clinic | 4 | 2 | 3 | 4 | 4 | 1 | **3.10** |
| DenPro | 4 | 2 | 1 | 4 | 3 | 5 | **3.00** |
| TurnosUno | 3 | 5 | 1 | 1 | 3 | 5 | **2.90** |
| DentalPro | 4 | 2 | 1 | 4 | 4 | 3 | **2.90** |
| Consultorio Digital | 3 | 2 | 2 | 4 | 4 | 1 | **2.65** |
| Benty | 3 | 2 | 1 | 3 | 3 | 2 | **2.30** |
| UDENTIVA | 2 | 2 | 2 | 3 | 3 | 1 | **2.15** |
| Turnos Online BB | 2 | 4 | 1 | 1 | 2 | 1 | **1.95** |

**Posición de nuestra v1 en esta matriz**: A=5, B=5, C=1, D=4, E=4, F=5 →
**3.95**.

</details>

**Lectura honesta de esa posición.** No ganamos por amplitud: pierdo
 deliberadamente en C (normativa) para no depender de APIs de terceros. Lo que
compro es que en el eje C nadie puede seguirnos sin un equipo de integraciones, y
que F (precio público en pesos) es un hueco confirmado: 8 de 19 no publican
precio y 2 cobran en dólares. La combinación "agenda por sillón correcta +
precio público en pesos" no la ofrece ninguno de los 19.

### Qué está "No evidenciado"

- **No evidenciado** — duración promedio real por práctica odontológica. Ningún
  competitor publica un nomenclador de duraciones abierto; hay que configurarlas
  a mano.
- **No evidenciado** — precio real de la mayoría. 8 de 19 no publican precio;
  DentalPro y Lumident cobran en USD,turnosuno publica promo con 80% off.
- **No evidenciado** — que la agenda por sillón sea un factor de compra
  decisionario. Sólo Órbita la nombra como eje y no publica su precio, así que
  no hay forma de saber si se cobra.
- **No evidenciado** — número real de usuarios activos. DenPro declara "+500
  profesionales", DentalSoft "300+ clínicas", DentalTec "2.000+ profesionales":
  son cifras declaradas por el vendedor, sin auditoría ni fuente primaria.
- **No evidenciado** — si algún competidor argentino cumple efectivamente la Ley
  27.553 de receta electrónica en producción. ClinIA declara identificador 248 en
  ReNaPDiS, pero no hay verificación pública de uso real.

## 5. Funcionalidades necesarias (MVP)

- Agenda por sillón con **duración por práctica configurable**.
- Prevención de solapamientos sobre esa duración.
- **Autogendamiento del paciente 24/7** desde link propio, sin instalación.
- Gestión de pacientes (datos de contacto, DNI).
- Historia clínica con odontograma por pieza.
- Cancelación y reprogramación por el paciente.
- Bloqueo de horarios por el odontólogo (feriados, vacaciones, uso propio).
- Reglas de reserva de slots por el odontólogo (protegidos del autoagendado).

## 6. Funcionalidades opcionales (backlog post-lanzamiento)

- Recordatorios y confirmaciones automáticas por WhatsApp.
- Lista de espera con disparo por el paciente.
- Sobreturnos para urgencias.
- Pacientes recurrentes con turno fijo.
- Google Calendar bidireccional.
- Workspaces multi-profesional y multi-sede.
- Detección de pacientes inactivos y reactivación.

## 7. Reglas de negocio

- **Duración por práctica**: cada tipo de consulta tiene una duración en minutos,
  configurada por el odontólogo.
- **Un sillón por consulta**: un turno ocupa un sillón durante su duración completa.
- **No solapamiento**: dos turnos no pueden ocupar el mismo sillón en el mismo
  intervalo de tiempo, sea quien sea el paciente o el profesional que los agenda.
- **Reservas protegidas**: los slots que el odontólogo bloquea o reserva a un
  paciente recurrente no son ofrecidos al autoagendado.
- **Cancelación anticipada**: el paciente puede cancelar o reprogramar hasta una
  anticipación mínima configurable.
- **Vista por sillón**: la agenda se presenta sobre el recurso físico, no sólo
  sobre el profesional.

## 8. Integraciones

**Ninguna integración externa obligatoria en v1.** Decisión consciente: el
producto entra sin depender de un tercero. La confirmación por WhatsApp queda
como canal del consultorio, no como funcionalidad del sistema.

Esto deja afuera las integraciones que sí ofrecen los incumbentes —MercadoPago,
Google Calendar, API de WhatsApp, PUCO— y es el motivo por el que el puntaje en
el criterio C es 1.

## 9. Restricciones

- **Stack libre**: la consigna no impone tecnología. Se elige en función del MVP.
- **Plazo ~2 meses** hasta el primer release funcional. Supuesto, no restricción
  de la consigna.
- **Ley 25.326** (protección de datos personales): la historia clínica es dato
  sensible de salud. Obliga a consentimiento, control de acceso y definir
 responsable del tratamiento de datos.
- **Alcance legal ambiguo**: al excluir receta electrónica, el producto **no puede
  recetar**. Si el odontólogo quiere prescribir, esa parte sale del sistema. Hay
  que dejarlo explícito para no inducir a uso fuera del alcance.

## 10. Riesgos

- **Pérdida de control de la agenda** — el riesgo estructural del autoagendamiento.
  Si un paciente recurrente que reserva hace 6 meses puede ser expropiado por uno
  nuevo, el consultorio pierde el motivo principal para adoptar el sistema.
  Mitigación prevista: reservas protegidas y bloqueos explícitos.
- **Resistencia a la auto-reserva** — el odontólogo ya tiene al paciente en su
  ficha y prefiere llamar. Si el consultorio tiene baja rotación, la agenda por
  sillón no le aporta nada visible. **Supuesto sin probar**: no tenemos validación
  con odontólogos reales.
- **Ausencia de recordatorios por WhatsApp** — 8 de 19 competidores los ofrecen.
  Sin ellos, el ausentismo (el problema que declaramos resolver) queda a medias.
  Es el hueco más expuesto de la v1.
- **Cumplimiento de la Ley 25.326 y alcance legal** — historia clínica sensible +
  exclusión de receta electrónica. Sin definir responsable de tratamiento,
  consentimiento y hosting, el producto queda expuesto. En un TPI académico esto
  se documenta como decisión de diseño, no como cumplimiento real.

## 11. Preguntas abiertas

- ¿WhatsApp entra en la v1 o queda en backlog? Está tensionado: se eligió "sin
  integraciones" y a la vez se marcó como riesgo. **Decisión pendiente.**
- ¿Cómo se protege el slot del paciente recurrente frente al autoagendado, y
  quién tiene prioridad cuando hay conflicto?
- ¿Cuál es la anticipación mínima para cancelar, y puede el odontólogo cancelar
  un turno del paciente?
- ¿Dónde se hospeda la historia clínica y cómo se documenta el cumplimiento de la
  Ley 25.326 en un proyecto académico?
- ¿El precio público en pesos es un diferencial real o sólo una decisión de
  marketing?
- ¿Las duraciones por práctica se precargan desde un nomenclador o las carga
  siempre el odontólogo? No hay fuente para precargarlas.

---

*Nota de consistencia: la escala oficial de la consigna es **0–5**, no 0–10. Las cifras 9,75 y 8,60 que aparecen en notas anteriores de este archivo corresponden a una conversión obsoleta y están corregidas aquí: los valores vigentes sobre la matriz oficial son **4,88/5** (Órbita) y **4,30/5** (DentalSaaS).*
