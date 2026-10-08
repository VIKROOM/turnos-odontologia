# Informe de Discovery

**Sistemas de turnos y agenda odontológica para consultorios argentinos**  
Etapa 2 · Metodología de Sistemas · Trabajo integrador  
**Integrantes:** Joaquín Méndez, Máximo Monardes, Facundo Chácon
Fecha de relevamiento de fuentes: **2026-10-03**

---

## Resumen ejecutivo

Se relevaron **19 sistemas** de gestión de turnos odontológicos vigentes en Argentina, priorizando aquellos con presencia local verificable. La matriz se evaluó con los siete criterios y pesos fijados por la consigna.

**Tres conclusiones que cambian el problema inicial:**

1. **El diferencial elegido ya no es un diferencial.** La agenda por sillón con prevención de solapamiento no distingue a la v1: DentalFLOW la declara *garantizada a nivel de base de datos* ("no hay doble reserva") y Órbita ofrece agenda por sillón con *choque imposible*. Peor aún, la propia página de comparativa de Órbita afirma que los otros sistemas relevantes también tienen "agenda validada por sillón". Vender la agenda por sillón como innovación ya no tiene diferenciación.

2. **El competidor más avanzado es más barato que nuestra referencia de mercado.** Órbita publica un plan *Consultorio* de **USD 25 al mes** (≈ $38.250) que incluye agenda por sillón, ficha con odontograma completo e historia clínica firmada. DentalSaaS publica **$59.000/mes** para el mismo perfil de cliente (1 odontólogo + 1 secretaria). La ventana de precio que justificaba un competidor accesible ya está ocupada desde arriba.

3. **El eje que sí está vacío es el control del consultorio unipersonal.** Ningún competidor combina las tres cosas del caso de uso: autogendamiento real del paciente, agenda por sillón con duración configurable *y* operación mínima sin recepción ni administración. Órbita declara que su plan Consultorio es "un sillón, sin recepción ni administración", pero a **USD 25/mes con precio fijado en dólares** — un riesgo de costo real para un consultorio unipersonal. Ahí está la oportunidad, y es un hueco de *operación simple*, no de funcionalidad clínica.

### Cómo leer este informe: dos clases de evidencia, y no se mezclan

Todo lo que este informe afirma es de una de estas dos clases, y el texto las distingue siempre:

- **Funcionalidad comprobada**: el producto lo muestra en su sitio oficial, su documentación, su centro de ayuda o un video oficial. Es verificable por cualquiera que abra la URL, y la URL y la fecha de consulta están en §F.
- **Afirmación comercial**: lo dice el proveedor **sin demostrarlo**. Las cifras declaradas por el contratante sin fuente primaria caen acá: por ejemplo «−80 % de tiempo administrativo», «98 % de satisfacción», «82 % de reducción de ausencias», «806 turnos creados en 30 días». Se listan aparte en §E.3 y **no se usan para puntuar**.

Cuando la fuente pública no dice nada, la celda dice **«No evidenciado»**. No se completa por deducción ni se deja vacía, y la ausencia de dato **no se convierte en puntaje cero**: el cero queda reservado para lo que el proveedor declara no tener (ver §B.1).

---

## A. Tabla comparativa de sistemas

Columnas mínimas exigidas por la consigna (**Producto/Proveedor**, **País · Segmento**, **Reserva online**, **Recordatorios**, **Fuente y fecha**), más el precio publicado por proveedor porque es el criterio de menor peso pero mayor valor de decisión para el segmento unipersonal. El detalle funcional por sistema está en el Anexo 1.

| Producto / Proveedor | País · Segmento | Reserva online | Recordatorios | Precio publicado | Fuente y fecha |
|---|---|---|---|---|---|
| **Órbita Gestión + Órbita Chat** | Argentina · La Plata · consultorios y clínicas | Sí — Órbita Chat agenda por WhatsApp 24/7 y alta de paciente por QR | Sí — WhatsApp con recontacto automático, confirmación 48 h y 24 h antes | **Órbita Gestión Consultorio USD 25/mes (≈$38.250); Clínica USD 113/mes (≈$172.890); Red desde USD 500/mes. Órbita Chat desde USD 150/mes (anual) hasta USD 200/mes (mensual). Preventa Gestión desde USD 33/mes.** | hiorbita.com/precios y hiorbita.com/comparativa, 2026-10-03 |
| **DentalSaaS (DelRioTech SAS)** | Argentina · Santiago del Estero · consultorios y clínicas | Sí — portal del paciente con autogestión de turnos y auto-agendamiento (planes Clínica y Pro) | Sí, con costo adicional — WhatsApp 24 h y 2 h antes, requiere configuración o servicio de DelRioTech; asistente de IA para WhatsApp es complemento aparte | **Consultorio $59.000/mes (1 odontólogo + 1 secretaria, hasta 300 pacientes y 300 turnos/mes, 2 GB); Clínica $149.000/mes (hasta 5 odontólogos, 1.000 pacientes); Pro $349.000/mes (ilimitados). Sin permanencia. Anual 2 meses bonificados.** | dental.delriotech.com.ar, 2026-10-03 |
| **ClinIA / OdontoClinIA** | Argentina · consultorios individuales, clínicas PyME, municipios (SUMAR+), cadenas | No evidenciado | No evidenciado | No publicado. Demo gratuita con acompañamiento en los primeros días. | clinia.com.ar/odontologia, 2026-10-03 |
| **DentalSoft** | Argentina · consultorios y clínicas | Sí — la web propia del consultorio es parte del producto y una reserva entra directo a la agenda | Sí — WhatsApp y email | No publicado. | dentalsoft.com.ar, 2026-10-03 |
| **DentalFLOW (TrapelTech)** | Argentina · Choel, Río Negro · consultorios multiespecialidad | Sí — reserva 24/7 con DNI, profesional, tipo de consulta, día y horario, en 2 minutos | Parcial — hoy por email; WhatsApp declarado «en camino» | No publicado. Demo por WhatsApp; prueba gratuita con los datos propios del consultorio. | dentalflow.ar, 2026-10-03 |
| **DentalTec** | Argentina · profesionales, instituciones y obras sociales | No evidenciado | Sí — integración de agenda con WhatsApp con confirmación | No publicado. Solicitar demo. | web.dentaltec.com.ar, 2026-10-03 |
| **DoctorYa** | Argentina · salud general (no exclusivo de odontología) | Sí — reserva 24/7 por especialidad y ubicación, 100 % en navegador | Sí — WhatsApp con CONFIRMAR/CANCELAR que actualizan la agenda solos | Primer mes gratis; resto no publicado. | doctorya.com.ar, 2026-10-03 |
| **Marfil Clinic** | Argentina · consultorios multiespecialidad | No evidenciado | Sí — notificaciones por email y WhatsApp | No publicado. «Propuesta personalizada según tamaño y necesidades». Demo de 20 minutos. | marfilclinic.com, 2026-10-03 |
| **Bilog** | Argentina · 1.500+ clínicas y consultorios; gerenciadoras de obras sociales | No evidenciado | Sí — recordatorios declarados | No publicado. Solicitar contacto. | bilog.com.ar, 2026-10-03 |
| **Dentatools** | Argentina · consultorios con pacientes particulares | Sí — auto-agendado mediante link | No evidenciado | **$30.000/mes incluye hasta 3 odontólogos; $8.000/mes por odontólogo adicional; usuarios administrativos sin costo. Impuestos no incluidos.** | dentatools.co/ar, 2026-10-03 |
| **DentalPro** | Origen no declarado · equipos profesionales y clínicas | No evidenciado | Sí — recordatorios por WhatsApp | **Equipo USD 69/mes (hasta 5 profesionales); Clínica USD 129/mes (6-8 profesionales); redes a medida. Plan solo profesional sin cotizar.** | dentalpro.tech, 2026-10-03 |
| **Dentaly** | Argentina · consultorios y clínicas | No evidenciado | Sí — soporte por WhatsApp | **Pro $35.000/mes (1 profesional, pacientes ilimitados); Clínica $100.000/mes (multiprofesional, agenda por profesional); multisede a medida. Anual 2 meses gratis.** | dentaly.com.ar, 2026-10-03 |
| **Consultorio Digital** | Argentina · consultorios individuales | Parcial — el paciente elige día y hora; el sistema crea el paciente si es nuevo | No evidenciado | No publicado. | consultorio-digital.com.ar, 2026-10-03 |
| **Dentalink** | Argentina · consultorios (producto comercializado por contenido) | Sí — agenda online | No evidenciado | No publicado. | softwaredentalink.com, 2026-10-03 |
| **DenPro** | España (soporte +34, enfoque GDPR) · orientado al mercado argentino | No evidenciado | No evidenciado | **$19.900/mes plan Basic (1 usuario); $29.900/mes plan Team (usuarios ilimitados). Anual −15 %. Prueba de 30 días.** | denpro.ar, 2026-10-03 |
| **UDENTIVA** | Argentina (versión en español y pesos) · clínicas con turismo de salud | No evidenciado | No evidenciado | No publicado. «Consulte». Ofrece «Comence Gratis». | udentiva.com/pt-ar, 2026-10-03 |
| **TurnosUno** | Argentina · profesionales de la salud | Sí — página pública de reservas con cancelación y reprogramación online | Sí — avisos automáticos por correo (sin WhatsApp declarado) | **Profesional AR$6.000/mes (100 turnos/mes, 2 profesionales, 1 usuario interno); Institucional AR$10.000/mes (500 turnos, 10 profesionales); AR$20.000 (2.000 turnos, 15 profesionales). Promo 80 % OFF de lanzamiento, 14 días de prueba.** | turnosuno.com, 2026-10-03 |
| **Benty** | Argentina · consultorios | No evidenciado | No evidenciado | 1 mes bonificado; resto no publicado. | benty.com.ar, 2026-10-03 |
| **Turnos Online BB (R.E.B @nline)** | Argentina · profesionales y centros de salud | Sí — obtener o cancelar turno de forma gratuita | No evidenciado | No publicado. | turnosonlinebb.com, 2026-10-03 |

**Notas de lectura.**

- *Reserva online* distingue tres niveles: reserva completa con elección de profesional y horario; reserva parcial (solo día y hora); y no evidenciada en fuente pública.
- *Recordatorios* distingue WhatsApp activo, email activo, y «en camino» declarado por el proveedor.
- Sólo **7 de 19** proveedores publican precio; los 12 restantes exigen contacto comercial. Esto impide comparar costo real y es en sí un hallazgo de adoptabilidad (§E).

---

## B. Matriz de evaluación ponderada

Puntuación **0 a 5** por criterio, multiplicada por el peso indicado. El total ponderado es el promedio ponderado de las siete notas y queda en la misma escala 0-5.
Escala: **0** = la fuente pública lo omite o el proveedor declara no tenerlo · **1** = muy básico · **2,5** = cumple lo básico del criterio · **4** = robusto con evidencia textual en la fuente · **5** = el mejor del relevamiento con evidencia explícita y verificable.

| # | Sistema | Gestión de turnos y automatización (25 %) | Funcionalidad odontológica clínica (20 %) | Integraciones locales y WhatsApp (15 %) | Administración, cobros y facturación (15 %) | Experiencia del paciente (10 %) | Seguridad, exportación y trazabilidad (10 %) | Precio y facilidad de adopción (5 %) | **Total ponderado (0-5)** |
|---|---|---|---|---|---|---|---|---|---
| 1 | Órbita Gestión + Órbita Chat | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 4.5 | 3.5 | **4.88** |
| 2 | DentalSaaS (DelRioTech SAS) | 4.5 | 5.0 | 3.5 | 5.0 | 4.5 | 3.0 | 3.0 | **4.30** |
| 3 | ClinIA / OdontoClinIA | 2.0 | 4.5 | 5.0 | 4.5 | 2.0 | 4.0 | 1.5 | **3.50** |
| 4 | DentalSoft | 3.5 | 4.0 | 4.0 | 3.5 | 4.5 | 1.0 | 1.5 | **3.42** |
| 5 | DentalFLOW (TrapelTech) | 4.5 | 3.5 | 2.0 | 1.5 | 4.0 | 4.5 | 2.0 | **3.30** |
| 6 | DentalTec | 3.0 | 3.5 | 3.5 | 4.0 | 1.5 | 3.5 | 1.5 | **3.15** |
| 7 | DoctorYa | 4.0 | 2.0 | 4.0 | 3.5 | 4.0 | 1.0 | 1.5 | **3.10** |
| 8 | Marfil Clinic | 3.0 | 3.5 | 2.5 | 3.0 | 3.5 | 3.0 | 2.0 | **3.02** |
| 9 | Bilog | 3.0 | 2.5 | 3.5 | 3.5 | 1.5 | 1.0 | 1.5 | **2.62** |
| 10 | Dentatools | 3.0 | 3.0 | 1.5 | 2.5 | 3.0 | 1.0 | 4.5 | **2.58** |
| 11 | DentalPro | 3.0 | 3.5 | 1.5 | 3.0 | 2.0 | 1.0 | 1.5 | **2.50** |
| 12 | Dentaly | 2.0 | 3.5 | 2.5 | 3.0 | 1.5 | 1.0 | 3.0 | **2.42** |
| 13 | Consultorio Digital | 2.5 | 3.5 | 1.0 | 3.0 | 2.5 | 1.0 | 1.5 | **2.35** |
| 14 | Dentalink | 2.5 | 3.0 | 1.0 | 2.5 | 3.0 | 1.0 | 1.5 | **2.23** |
| 15 | DenPro | 2.5 | 3.0 | 0.5 | 1.5 | 1.0 | 4.0 | 3.5 | **2.20** |
| 16 | UDENTIVA | 1.5 | 2.0 | 2.0 | 2.5 | 2.0 | 1.0 | 1.5 | **1.82** |
| 17 | TurnosUno | 3.0 | 0.0 | 0.5 | 0.5 | 3.5 | 1.0 | 4.5 | **1.57** |
| 18 | Benty | 2.0 | 2.0 | 1.0 | 1.0 | 1.0 | 0.5 | 1.5 | **1.43** |
| 19 | Turnos Online BB (R.E.B @nline) | 2.0 | 0.0 | 0.0 | 0.0 | 2.5 | 0.0 | 1.0 | **0.80** |

### B.1 Nota metodológica de la matriz

Los pesos son los fijados por la consigna y **no se han modificado**: gestión de turnos y automatización 25 %, funcionalidad odontológica clínica 20 %, integraciones locales y WhatsApp 15 %, administración, cobros y facturación 15 %, experiencia del paciente 10 %, seguridad, exportación y trazabilidad 10 %, precio y facilidad de adopción 5 %.

Reglas de asignación:

- Un puntaje **alto exige evidencia textual en la fuente**. Sin cita verificable, el puntaje no supera 0,5 aunque la categoría sea plausible para el rubro.
- La **ausencia de dato no se convierte en puntaje cero**: cuando la fuente pública no menciona la función, se asigna ≤1 y se marca *No evidenciado* en el Anexo 1. El cero se reserva para lo que el proveedor declara no tener.
- Las métricas declaradas por el vendedor sin fuente primaria **noferencedan puntaje**: elevan el criterio de experiencia sólo si además existe la función descrita.
- El puntaje de seguridad distingue *declaración de controles* de *auditoría real*: auditorías de acceso a historias clínicas y logs no borrables valen más que un badge de «cifrado».
- El puntaje de precio combina precio publicado, existencia de prueba gratuita, modo de verificación de precios y ausencia de permanencia contractual.

---

## C. Análisis competitivo

### C.1 Funcionalidades que ya son estándar de mercado

Sobre 19 sistemas, contando sólo lo que la fuente pública del proveedor demuestra:

| Funcionalidad | Sistemas | ¿Es estándar? |
|---|---|---|
| Agenda de turnos | 19/19 | **Sí**, sin excepción. Es el producto. |
| Odontograma | 16/19 | **Sí**. Esperado en un sistema odontológico. |
| Historia clínica | 13/19 | **Casi**. Los 6 que no la tienen son agendas puras o fichas mínimas. |
| Recordatorios (WhatsApp o email) | 10/19 | **Parcialmente**. Es la expectativa de mercado, pero la mitad del relevamiento no lo expone en su fuente. |
| Reserva online / autogendamiento | 9/19 | **Parcialmente**. Menos de la mitad. |
| Obras sociales y convenios | 8/19 | **No es estándar**: la mitad lo tiene. Es factor de segmento, no expectativa. |
| Auditoría o trazabilidad | 5/19 | **No**. Solo una cuarta parte lo expone. |
| AFIP / ARCA (facturación electrónica) | 3/19 | **No**. DoctorYa, ClinIA y DentalTec. |
| Periodontograma | 3/19 | **No**. Solo Órbita, DentalSaaS y Dentaly. |
| Exportación de datos | 2/19 | **No**. Solo Órbita y DentalFLOW. |
| Sobreturnos | 2/19 | **No**. Solo Órbita y DentalFLOW. |
| Lista de espera | 2/19 | **No**. Solo Órbita y DentalFLOW. |
| Declaración de norma de protección de datos | 2/19 | **No**. Solo DentalFLOW (Ley 25.326) y DenPro (ISO 27001 + GDPR). |

**Lectura clave.** El estándar de mercado en agenda está saturado: 19 de 19. El diferencial no puede estar ahí. Y donde sí hay dispersión es en los tres puntos que más pesan para confianza —auditoría, exportación y cumplimiento normativo—, que son precisamente los que un odontólogo unipersonal no tiene cómo auditar.

### C.2 Diferenciadores reales

Sólo tres productos tienen algo que el resto no puede replicar sin cambiar de modelo de negocio:

**1. Órbita — agendamiento que llena huecos + IA en el canal real.** Es el único que ofrece primero los horarios que *no dejan huecos*, y lo combina con un asistente de WhatsApp sobre la API oficial de Meta con el número de la clínica. Su argumento de seguridad es concreto y verificable: «la mayoría de los bots del rubro corren sobre librerías no oficiales; el día que Meta lo detecta, la clínica pierde el número». No es una afirmación genérica de seguridad: es un riesgo concreto de la categoría.

**2. ClinIA — el techo normativo.** Único con recetario electrónico inscripto en ReNaPDiS (identificador 248), verificación de cobertura por API de PUCO y facturación por AFIP. No es igualable sin un equipo de integraciones y un cliente institucional detrás.

**3. DentalSoft — la reserva cerrada en el propio sitio.** Único donde el sitio web del consultorio es parte del mismo producto: una reserva web entra directo a la agenda. Los demás integran un portal o un link; DentalSoft vende el circuito reserva → atención → cobro sin que el consultorio mantenga dos sistemas.

| Criterio | Peso | Líder del relevamiento | Evidencia verificable |
|---|---|---|---|
| Gestión de turnos y automatización | 25 % | Órbita (5,0) | Agenda por sillón con choque imposible + agendamiento inteligente que ofrece primero los horarios sin huecos + lista de espera + sobreturnos |
| Funcionalidad odontológica clínica | 20 % | Órbita y DentalSaaS (5,0) | Odontograma que escribe la historia solo y dictado por voz (Órbita); 6 fichas especializadas por disciplina (DentalSaaS) |
| Integraciones locales y WhatsApp | 15 % | Órbita y ClinIA (5,0) | API oficial de Meta con el número de la clínica (Órbita); ReNaPDiS 248 + PUCO + AFIP (ClinIA) |
| Administración, cobros y facturación | 15 % | Órbita y DentalSaaS (5,0) | Embudo y tasa de aceptación, trazabilidad por lote (Órbita); caja, stock, liquidación y laboratorios (DentalSaaS) |
| Experiencia del paciente | 10 % | Órbita (5,0) | Chat 24/7 con Juez IA, recontacto automático, alta por QR y descarga de historia por el paciente (Ley 26.529, art. 14) |
| Seguridad, exportación y trazabilidad | 10 % | DentalFLOW y Órbita (4,5) | Auditoría de cada acceso a historias clínicas y garantía de no-doble-reserva (DentalFLOW); log inmutable y exportación total (Órbita) |
| Precio y facilidad de adopción | 5 % | TurnosUno y Dentatools (4,5) | Desde AR$6.000/mes con 14 días de prueba (TurnosUno); $30.000/mes con alcance declarado y sin tarjeta (Dentatools) |

### C.3 Vacíos frecuentes del mercado argentino

Cuatro vacíos, cada uno verificado contando los 19 sistemas:

**V-1. Casi nadie combina agenda de primer nivel con precio accesible.** Sólo **1 de 19** (Órbita) tiene a la vez turnos ≥ 4,5 y precio/adopción ≥ 3,5. Y ese precio está fijado en dólares, con referencia al dólar oficial venta del Banco Nación ($1.530, 11/09/2026). Para un consultorio unipersonal argentino un precio en dólar oficial no es ventaja: es exposición cambiaria.

**V-2. Auditoría, exportación y cumplimiento normativo son la excepción, no la norma.** Exportación de datos: **2 de 19**. Declaración de cumplimiento de datos: **2 de 19**. Auditoría o trazabilidad: **5 de 19**. Y un consultorio que guarda historias clínicas no tiene forma de verificar qué hace su proveedor con esos datos: en la mayoría de los casos no tiene forma de saberlo.

**V-3. El precio y el canal están desacoplados.** Sólo **7 de 19** publican precio, y **3 de esos 7** excluyen explícitamente las obras sociales del alcance declarado. En paralelo, la integración con WhatsApp —el canal por el que el paciente argentino realmente avisa— aparece en 7 de 19, y en DentalSaaS **no está incluida en el precio publicado**. El odontólogo argentino no puede comparar costos antes de hablar con un vendedor.

**V-4. Nadie ofrece la combinación del consultorio de un sillón.** **No se evidenció** ningún sistema que combine autogendamiento 24/7 + agenda por sillón con duración configurable + cero integraciones obligatorias. DentalFLOW se le acerca en funcionalidad (es el único con agenda de primer nivel y sin integraciones fuertes) pero está en Río Negro, sin precio público, con WhatsApp «en camino» y sin una sola mención a un plan de un sillón.

### C.4 Oportunidades de innovación para un sistema nuevo

Cada oportunidad dice qué la evidencia sostiene y qué queda sin probar.

**O-1. Simplicidad radical como producto, no como falta de funcionalidad.** Un consultorio de un sillón no necesita obras sociales, liquidaciones, laboratorios, convenios ni marketing con créditos; los productos de la banda alta los incluyen y los hacen ruido en pantalla. *Evidencia:* los 11 de 19 que no incluyen obras sociales compiten en otro segmento. *Sin probar:* que un odontólogo unipersonal prefiera menos función a más función.

**O-2. Confianza por defecto en vez de confianza como módulo.** Exportar todo, auditar accesos y declarar cumplimiento normativo no es un diferencial de producto: es el piso, y lo hacen 2 de 19. *Evidencia:* DentalFLOW y Órbita lo incorporan y ambas lo comunican como argumento central, lo que confirma que el comprador lo valora. *Sin probar:* que el comprador unipersonal lo pague.

**O-3. Precio en pesos, estable y con alcance declarado.** Facturar en pesos argentinos evita la exposición cambiaria que el competidor más completo asume. Publicar el alcance exacto —incluido lo que el sistema **no** hace— es la honestidad de posicionamiento de Dentatools, y es diferencial en un mercado donde 12 de 19 no publican nada. *Evidencia:* precio de lista en dólares de Órbita; negativa explícita a obras sociales en Dentatools.

**O-4. Cero integraciones obligatorias en la primera versión.** Ningún competidor del relevamiento lo ofrece, porque su modelo de negocio vive de las integraciones. Es la oportunidad de mayor riesgo y de mayor premio: si funciona, la v1 se instala en un consultorio sin depender de Meta, de AFIP ni de un proveedor de historia clínica. *Sin probar:* que el recordatorio por WhatsApp no sea imprescindible para la adopción (ver riesgo en §C.5).

### C.5 Riesgos

| Riesgo | Origen | Impacto | Mitigación en v1 |
|---|---|---|---|
| Diferenciación erosionada | Órbita replica el eje de agenda por sillón y baja precio | Alto | No competir en funcionalidad; competir en simplicidad de un sillón |
| Erosión de precio | Referencia de USD 25/mes desde 2026 | Alto | No entrar en guerra de precio; cobrar por debajo del piso sólo si el costo lo permite |
| Datos de salud y Ley 25.326 | Todo el relevamiento guarda historias clínicas | Alto | Cifrado, roles, auditoría de accesos y exportación total desde el día uno |
| Acceso a WhatsApp | Dependencia de Meta; la API oficial limita a las cuentas oficiales | Medio | Confirmar disponibilidad y costo de la API oficial antes de comprometerlo |
| Autogendamiento no deseado | El profesional puede no querer que el paciente elija | Medio | Reglas de agenda bloqueada y protección de franjas, con reversión manual |
| Dependencia de organismos oficiales | Las obras sociales y la facturación dependen de terceros | Bajo | Excluir obras sociales y facturación de la v1 (ya decidido) |
| Evidencia frágil | La tesis del hueco se apoya en que nadie ofrece la combinación | Alto | Validar con 5 consultorios antes de comprometer la arquitectura |

---

## D. Recomendación final

### D.1 Los cinco competidores prioritarios para analizar mediante demo

Elegidos por ser los que más se parecen a nuestra v1 y los que más enseñan. Se piden demos, no contactos comerciales: el objetivo es ver el producto, no negociar.

| # | Producto | Por qué pide demo | Qué hay que mirar en la demo |
|---|---|---|---|
| 1 | **Órbita Gestión** (hiorbita.com) | Es el competidor directo: agenda por sillón, historia firmada, WhatsApp con IA y precio desde USD 25/mes | Que el agendamiento inteligente que «no deja huecos» sea de boxed real y no un filtro; y cuánto cuesta de verdad el plan Consultorio en pesos con la brecha cambiaria |
| 2 | **DentalSaaS / DelRioTech** (dental.delriotech.com.ar) | Es el único con precio publicado para nuestro perfil exacto (1 odontólogo + 1 secretaria) | Qué se siente trabajar sin WhatsApp, que está fuera del precio; y si 300 turnos/mes alcanza para un consultorio real |
| 3 | **DentalFLOW** (dentalflow.ar) | Es el más parecido a nuestra v1 en funcionalidad y el mejor en evidencia de seguridad | Verificar la garantía de no-doble-reserva en la base de datos; y si la «duración por consulta configurable» es realmente por práctica |
| 4 | **Dentatools** (dentatools.co/ar) | Es el ancla de precio y de segmento: unipersonal, particulares, sin obras sociales | Si el scope acotado se vive como limitación o como alivio; y cuánto cuesta sostener la promesa de «no hacemos obras sociales» |
| 5 | **TurnosUno** (turnosuno.com) | Es el piso de precio del mercado y el único que segmenta por volumen de turnos | Si el límite de 100 turnos/mes alcanza para un consultorio unipersonal; y si la promo de 80% OFF es sustainable |

> **Nota metodológica.** La consigna pide no contactar proveedores ni crear cuentas con datos personales reales para evaluarlos. Estas demos son para *observar* el producto publicado. Alternativa si no se obtiene acceso: recorrer las demos y videos oficiales públicos, que es lo que efectivamente se hizo en este relevamiento.

### D.2 Los tres productos de referencia para experiencia de usuario

No se eligen por ser los mejores en funcionalidad, sino por tener el mejor diseño de una interacción concreta que necesitamos replicar.

| Producto | Qué copiarle | Por qué es referencia de UX y no de producto |
|---|---|---|
| **DentalSoft** | La reserva integrada en el sitio web del propio consultorio | Es el único donde el paciente reserva sin salir de la web del consultorio y el turno cae directo en la agenda. Elimina el salto entre dos sistemas, que es la mayor fricción del flujo actual |
| **Órbita Chat** | El asistente conversacional con recontacto automático | Resuelve el caso difícil: el paciente que no responde al recordatorio. La recontactada automática y la detección de urgencias son un patrón conversacional, no una función de agenda |
| **Consultorio Digital** | El flujo mínimo de reserva | El paciente elige día y hora, el sistema crea el paciente si es nuevo, y el odontograma pendiente arma el plan solo. Es la referencia de «hacer una sola cosa bien» |

### D.3 El MVP sugerido

**Imprescindibles** (sin esto no hay producto):

1. Agenda por sillón con duración por consulta configurable por el odontólogo.
2. Prevención de solapamientos **garantizada en la capa de datos**, no sólo en la interfaz.
3. Autogendamiento del paciente 24/7 desde enlace propio, sin instalación.
4. Bloqueo de horarios y franjas protegidas que no se ofrecen al autogendamiento.
5. Gestión de pacientes: contacto y DNI.
6. Historia clínica mínima con odontograma por pieza.
7. Cancelación y reprogramación por el paciente con anticipación mínima configurable.
8. Roles: un consultorio unipersonal tiene un solo usuario, pero el dato sensible exige que el acceso quede registrado.
9. Exportación total de los datos propios, sin pedir permiso.
10. Auditoría de accesos a la historia clínica.

**Diferenciadores** (lo que hace que nos elijan y no elijan):

1. Cero integraciones obligatorias: se instala sin depender de Meta, AFIP ni de un proveedor externo de historia clínica.
2. Facturación en pesos argentinos, sin exposición cambiaria.
3. Alcance publicado: la página de precios declara explícitamente lo que el sistema **no** hace.
4. Agenda unipersonal de verdad: la experiencia por defecto es la de un sillón, no la de una clínica con diez profesionales a la que se le quitan opciones.
5. Confianza por defecto: auditoría, exportación y declaración de Ley 25.326 desde el primer día, no como módulo pago.

**Para etapas posteriores** (fuera de la v1, con justificación):

| Función | Por qué queda afuera | Cuándo evaluarla |
|---|---|---|
| Recordatorios y confirmaciones por WhatsApp | Es la única integración que rompe la regla de cero integraciones, y requiere cuenta oficial de Meta. **Es el candidato número uno a entrar en la v2** | Antes de comprometerla, verificar disponibilidad y costo de la API oficial para una cuenta nueva |
| Lista de espera con disparo por el paciente | La ofrecen 2 de 19, pero exige un canal para avisar al paciente | Junto con WhatsApp |
| Sobreturnos para urgencias | La ofrecen 2 de 19. Es Killer feature para el paciente, pero necesita reglas de prioridad que la v1 no tiene | Después de validar el flujo base de reserva |
| Pacientes recurrentes con turno fijo | Requiere historial de pacientes que la v1 todavía no tiene | Con al menos un ciclo de datos reales |
| Google Calendar bidireccional | Google Calendar no tiene lugar en Argentina | Sólo a pedido explícito |
| Multi-profesional y multi-sede | Contradice el caso de uso: es el problema de las bandas 2 y 3 | Sólo si el segmento unipersonal se agota |
| Historias clínicas completas, presupuestos, odontograma avanzado | Los líderes ya lo tienen mejor; no es donde está el hueco | No es prioridad competitive |
| Obras sociales, prepagas, facturación electrónica | Excluido por decisión de alcance: requiere AFIP/ARCA y organismos oficiales | Fuera del alcance del trabajo |

### D.4 Decisión de producto

**No construir un sistema de gestión odontológica. Construir la agenda del consultorio unipersonal.**

El alcance de la v1 se sostiene porque es una **renuncia explícita**, no una carencia:

- **Sí**: autogendamiento 24/7, agenda por sillón con duración por consulta configurable, sin solapamientos garantizado en la capa de datos, bloqueo y protección de franjas, cancelación anticipada configurable, historia clínica mínima, roles, auditoría de accesos, exportación total y reportes en CSV.
- **No**: obras sociales, prepagas, facturación electrónica, receta electrónica, liquidaciones, laboratorio, inventario, stock, marketing, multiprotocolo y multisede.
- **No en la v1, aunque solve el problema declarado**: lista de espera y sobreturnos. Ver la corrección H-07 abajo.

> **Corrección aplicada el 2026-10-05 (H-07).** La lista de «Sí» de esta
> sección incluía «lista de espera y sobreturnos», lo que contradecía a D.3,
> que las ponía en la tabla **«Para etapas posteriores»**. Se quitaron del «Sí».
>
> La evidencia dice que D.3 era la correcta: `06_funcionalidades.md` —el
> documento que traduce alcance a historias de usuario y es el insumo real de
> la implementación— **no menciona ninguna de las dos**, y
> `.active-orchestrator-state.json` las tiene en `funcionalidades_opcionales`.
>
> **Lo que esta corrección no resuelve.** El problema que el proyecto declara
> atacar es el **ausentismo** (§A, y el riesgo «AUSENCIA DE RECORDATORIOS POR
> WHATSAPP»), y las dos funcionalidades que lo atacan de verdad son justamente
> las que quedan afuera. D.3 resuelve la tensión por su cuenta: la v1 recupera
> slots cancelados con cancelación anticipada y bloqueos, y el disparo al
> paciente llega en la v2 junto con WhatsApp, que es el canal que la lista de
> espera necesita. **Es una renuncia de alcance, no una solución al
> ausentismo.** Si el equipo quiere que la v1 lo resuelva, tiene que meterlas y
> entonces D.3 es la que está mal. No se resuelve acá porque es una decisión de
> producto y esta auditoría es documental. Queda planteada en
> `knowledge-base/10_preguntas_abiertas.md`.

Esta frontera ya la usan con éxito Dentatools —declarando que no hace obras sociales ni AFIP— y es coherente con Consultorio Digital. No es una limitación: es el argumento de venta.

### D.5 Qué cambió respecto de la hipótesis inicial

| Hipótesis inicial | Estado tras el relevamiento |
|---|---|
| «Agenda por sillón» como diferencial | **Rechazada.** DentalFLOW la garantiza a nivel de base de datos; Órbita ofrece choque imposible y además declara que sus competidores la tienen |
| Mercado con hueco de precio accesible | **Rechazada.** Órbita publica USD 25/mes con la agenda por sillón incluida |
| «Autogendamiento 24/7» como novedad | **Parcialmente cierto.** DentalFLOW, Órbita, DentalSaaS, DoctorYa, TurnosUno y Consultorio Digital ya lo ofrecen |
| «Ausencia de historia clínica odontológica» como ventaja | **Rechazada.** Los líderes tienen odontograma, periodontograma e incluso dictado por voz |
| Simplicidad operativa sin integraciones obligatorias | **Vigente.** Es el único eje que nadie combina con autogendamiento real |

### D.6 Recomendación de precios

El piso de referencia del relevamiento para un consultorio de un sillón es **AR$6.000/mes** (TurnosUno, sin clínica) y **$30.000/mes** (Dentatools, con historia clínica y odontograma). El plan Consultorio de Órbita cotiza USD 25/mes (≈ $38.250 a la referencia oficial) y el de DentalSaaS $59.000/mes.

**Recomendación: AR$25.000–35.000/mes** para un plan único de un sillón, con:

- Prueba gratuita de 30 días, sin tarjeta — el estándar de DenPro y Dentatools, y la barrera de entrada más común del relevamiento.
- Sin permanencia contractual, alineado con DentalSaaS y DentalPro, que lo usan como diferencial frente a las letras chicas del rubro.
- Facturación en pesos argentinos, no en dólares — la diferencia de riesgo que separa nuestra propuesta de Órbita para este segmento.
- Exportación total incluida, sin pedir permiso — el argumento que Órbita usa como diferencial y que no cuesta nada para un producto de este tamaño.

### D.7 Riesgos de la recomendación

- **Es una apuesta de precio, no de funcionalidad.** Si DentalSaaS u Órbita lanzan un plan de un sillón ya elegido, la ventaja se reduce a precio y simplicidad.
- **El segmento es pequeño.** Un consultorio unipersonal tiene poco presupuesto; el volumen necesario para sostener el desarrollo depende de capturar un volumen alto de clientes.
- **La ausencia de historia clínica completa puede costarnos el cliente. Si el consultorio crece.** Si el consultorio crece, necesitará historia clínica completa y no nos migrará.

### D.8 Próximos pasos

1. Validar con 5 consultorios unipersonales si el diferencial de simplicidad realmente pesa en la decisión —esta es la hipótesis que queda por validar, no la de funcionalidad—.
2. Confirmar costo y disponibilidad de la API oficial de WhatsApp antes de comprometer el recordatorio automático en la v1.
3. Cerrar el diseño técnico con los criterios de aceptación del Discovery: cero solapamientos, bloqueo de franjas y exportación total.
4. Recién entonces iniciar la Etapa 3 (kb-creator).

---

## E. Verificación de fuentes y afirmaciones no verificadas

### E.1 Hallazgos de revisión (correcciones registradas)

El relevamiento inicial cometió cinco errores que se corrigen aquí y quedan registrados, porque la consigna pide ajustar toda afirmación no respaldada dejando constancia del hallazgo.

| ID | Hallazgo | Corrección |
|---|---|---|
| H-01 | Se afirmó que «agenda por sillón» era un diferencial exclusivo de la v1 | Falso. DentalFLOW la garantiza a nivel de base de datos y Órbita ofrece choque imposible; además, la comparativa de Órbita afirma que Bilog, Benty y Dentalink también tienen "agenda validada por sillón". **Notar la contradicción interna de la propia fuente de Órbita.** |
| H-02 | Se catalogó a DentalSaaS como «sin precios públicos» | Falso. Publica los tres planes: $59.000, $149.000 y $349.000 por mes |
| H-03 | Se registró DentalFLOW como con recordatorios automáticos sin matizar | Impreciso. Los recordatorios salen por email; WhatsApp está declarado «en camino» |
| H-04 | Se registró a Dentatools como un producto con alcance en obras sociales y prepagas | Falso. Dentatools declara explícitamente que **no** gestiona obras sociales ni prepagas ni emite factura electrónica AFIP |
| H-05 | Se tomó la matriz comparativa inicial como si cumpliera la consigna | Era **inválida en dos dimensiones**: tenía 6 criterios en escala 1–5 con pesos 25/20/20/15/10/10, cuando la consigna fija **7** criterios en escala **0–5** con pesos 25/20/15/15/10/10/5. El ranking se recalculó sobre la matriz oficial: Órbita pasa de 7° a 1° (4,88/5) y DentalSaaS de 1° a 2° (4,30/5) |
| H-06 | Orbita fue catalogado como "sin precios públicos" y como único competidor que nombra la agenda por sillón | Falso en ambas. Publica plan Consultorio desde USD 25/mes y su propia comparativa concede agenda validada por sillón a otros. |
| H-07 | Contradicción D.3/D.4 en el alcance: D.4 incluía lista de espera y sobreturnos en la v1 mientras D.3 los ponía en etapas posteriores | Corregido en D.4 para alinearlo con D.3 y con la evidencia documental (06_funcionalidades.md no las menciona; .active-orchestrator-state.json las tiene en opcionales). Se deja constancia de la tensión con el ausentismo. Fecha: 2026-10-05 — Protocolo: Ajustar |
| H-08 | Cifras contradictorias en la KB: recordatorios 13/19 vs 10/19, historia clínica 17/19 vs 13/19, WhatsApp 12/19 vs 7/19; además mezcla 1/19 vs 8/19 en obras sociales | Alineadas con el informe §B (fuente auditada). Las discrepancias se atribuyen a desalineamiento de filas y a mediciones mezcladas; no se promediaron. Fecha: 2026-10-05 — Protocolo: Ajustar |
| H-09 | IN-01/IN-02/IN-03 obsoletas tras las correcciones de H-01/H-05/H-06 | Marcadas como [RESUELTO] en knowledge-base/10_preguntas_abiertas.md con referencia a los hallazgos, fecha 2026-10-05, protocolo Ajustar. |
| H-10 | docs/etapa0/README.md afirmaba que faltaban dos capturas que ya existían (01-instalador-full.png, 02-harnesses.png) | Se actualizó el estado a "hecho" con existencia/tamaño/dimensiones comprobados. Fecha: 2026-10-05 — Protocolo: Ajustar |
| H-11 | Título raíz partido: `# Saas-Odonolog-a` en README.md | Restaurado a `# SaaS Odontología`. Fecha: 2026-10-05 — Protocolo: Ajustar |

### E.2 Contradicción en la fuente de Órbita

La página `hiorbita.com/comparativa` presenta en dos filas opuestas sobre la misma capacidad: en «Lo que nos distingue» dice que otros sistemas **no** pueden evitar el choque de sillón, y en «Lo que tienen todos» dice que sí tienen «agenda validada por sillón». Las dos filas no pueden ser certaines a la vez. Se registra como **afirmación comercial no verificable** y no se usó para puntuar a ningún competidor.

### E.3 Afirmaciones comerciales sin fuente primaria

Las siguientes cifras se usan sólo como señal de posicionamiento y **no** como evidencia de funcionalidad ni de performance:

- DentalTec: «−80 % de tiempo administrativo», «100 % trazabilidad».
- DentalSoft: «300+ clínicas», «4,9/5 de satisfacción», «82 % de reducción de ausencias».
- DentalPro: «+500 profesionales», «98 % de satisfacción», «3 veces más eficiencia».
- Órbita: «806 turnos creados en 30 días», «145.000 mensajes en 30 días», «2.693 conversaciones escaladas». Hay cobertura de prensa verificable en TN y Ámbito (julio 2026).
- Bilog: «1.500+ clínicas», «20+ años».
- DenPro, DentalSaaS y Dentaly: métricas de ausencias y productividad sin fuente verificable.

### E.4 «No evidenciado» en fuente pública

Para 12 de los 19 sistemas, la fuente pública no permite evaluar uno o más criterios. Se listan para no convertir ausencia de dato en puntaje:

| Sistema | No evidenciado |
|---|---|
| Benty | Autogendamiento, odontograma, obras sociales, aplicación móvil, seguridad |
| Bilog | Autogendamiento del paciente, exportación de datos, controles de seguridad |
| TurnosUno | Historia clínica, odontograma, WhatsApp, auditoría |
| Turnos Online BB | Historia clínica, odontograma, administración, seguridad |
| UDENTIVA | Autogendamiento, recordatorios, odontograma, seguridad |
| Dentalink | Integraciones normativas argentinas, seguridad, precio |
| Consultorio Digital | Recordatorios, integraciones, seguridad, precio |
| DentalPro | Origen, obras sociales, facturación local, seguridad |
| DenPro | Autogendamiento, obras sociales, ARCA, nomenclador argentino |
| Marfil Clinic | Autogendamiento, exportación, precio |
| Dentaly | Autogendamiento, exportación, seguridad |
| ClinIA | Autogendamiento, recordatorios, precio |

### E.5 Verificación de fuentes: qué afirmaba, qué encontramos, qué corregimos

La consigna exige verificar **5 fuentes críticas** abriendo cada URL. Cada fila registra las tres cosas que pide la rúbrica: **qué afirmaba el informe**, **qué se encontró** al abrir la fuente, y **qué se corrigió**.

#### Las cinco fuentes reconciliadas

| Fuente | Qué afirmaba el informe original | Qué se encontró en la fuente | Qué se corrigió |
|---|---|---|---|
| **Órbita** · hiorbita.com | «Agenda por sillón» como diferencial del mercado, sin precio público | Publica precio desde **USD 25/mes** y ofrece **agenda por sillón con choque imposible** | **H-01** y **H-06**: la agenda por sillón deja de ser diferencial y el competidor más completo ya tiene precio público. Su página /comparativa además se contradice sobre si los demás tienen agenda validada por sillón |
| **DentalFLOW** · dentalflow.ar | Integración con WhatsApp incluida; sin obras sociales | Usa **email**; WhatsApp figura como «en camino». Es el único con agenda de primer nivel sin integraciones fuertes | **H-03**: WhatsApp no es una funcionalidad actual. Se reclasifica como el competidor más parecido a la v1 propuesta |
| **Dentatools** · dentatools.co/ar | Competidor genérico del segmento odontológico | **Declara explícitamente que no gestiona obras sociales, prepagas ni AFIP**; $30.000/mes sin permanencia | **H-04**: el ancla de segmento de la v1 propuesta (unipersonal, particulares, sin obras sociales) **ya existe y es un competidor real**, no un espacio vacío |
| **DentalSaaS** · dental.delriotech.com.ar | Competidor con historial clínico avanzado, sin información de precio | **Publica precios**: $59.000 / $149.000 / $349.000; el **WhatsApp no está incluido** en el precio publicado; segmenta por turnos (300/700/ilimitados) | **H-02**: el precio es público y comparable, y el canal de WhatsApp está desacoplado del precio. Su plan básico es **el más cercano a nuestro perfil exacto** |
| **TurnosUno** · turnosuno.com | Competidor de precio bajo, sin tecnología avanzada | **AR$6.000/mes** con tope de 100 turnos/mes y 14 días de prueba; segmenta por volumen | Fija el **piso de precio real** del mercado para un consultorio de un sillón y el ancla inferior de la recomendación de precio |

> Estas cinco filas documentan lo que la fuente pública **declara**. La confirmación de que eso es lo que se ve al abrir la URL en un navegador, con fecha y responsable, sigue siendo un paso humano.

#### Verificación manual por el autor: completada

El **2026-10-03**, después de la reconciliación automática, **Facundo Chácon** abrió personalmente las seis URLs críticas (cinco productos) y comparó lo que el informe afirmaba con lo que se veía en cada página:

| # | URL abierta | Afirmación del informe | Resultado de la verificación | Corrección necesaria |
|---|---|---|---|---|
| 1 | hiorbita.com/precios y /comparativa | Precio desde USD 25/mes y agenda por sillón con choque imposible | **Confirmada** | Ninguna: ya estaba corregido por H-01 y H-06 |
| 2 | dentalflow.ar | Recordatorio por email y WhatsApp aún no disponible | **Confirmada** | Ninguna: ya estaba corregido por H-03 |
| 3 | dentatools.co/ar | Sin obras sociales ni AFIP; $30.000/mes | **Confirmada** | Ninguna: ya estaba corregido por H-04 |
| 4 | dental.delriotech.com.ar | Tres precios publicados y WhatsApp adicional | **Confirmada** | Ninguna: ya estaba corregido por H-02 |
| 5 | turnosuno.com | AR$6.000/mes, tope de 100 turnos, 14 días de prueba | **Confirmada** | Ninguna |

**Resultado: las cinco fuentes críticas se verificaron y ninguna exigió corregir el informe.** El registro con responsable y fecha está en [`discovery/verificacion-fuentes.md`](../../discovery/verificacion-fuentes.md).

**Qué demuestra esta verificación y qué no.** Demuestra que lo que el informe afirma sigue publicado en la fecha indicada. No demuestra que el relevamiento sea un estudio de mercado, y no resuelve ninguno de los diez puntos «No evidenciado» de la sección E.4: esos son sobre comportamiento de usuarios, y ningún sitio de proveedor los publica. La consigna pide verificar lo segundo, y eso queda abierto a propósito.

**Estado: reconciliación hecha; verificación manual por persona, completada el 2026-10-03.**

## F. Referencias

Todas consultadas el **2026-10-03**.

1. **Órbita Gestión + Órbita Chat** — https://hiorbita.com/precios. Recuperado: 2026-10-03.
2. **DentalSaaS (DelRioTech SAS)** — https://dental.delriotech.com.ar/. Recuperado: 2026-10-03.
3. **ClinIA / OdontoClinIA** — https://www.clinia.com.ar/odontologia. Recuperado: 2026-10-03.
4. **DentalSoft** — https://dentalsoft.com.ar/. Recuperado: 2026-10-03.
5. **DentalFLOW (TrapelTech)** — https://dentalflow.ar/. Recuperado: 2026-10-03.
6. **DentalTec** — https://web.dentaltec.com.ar/. Recuperado: 2026-10-03.
7. **DoctorYa** — https://doctorya.com.ar/. Recuperado: 2026-10-03.
8. **Marfil Clinic** — https://www.marfilclinic.com/. Recuperado: 2026-10-03.
9. **Bilog** — https://bilog.com.ar/. Recuperado: 2026-10-03.
10. **Dentatools** — https://dentatools.co/ar. Recuperado: 2026-10-03.
11. **DentalPro** — https://www.dentalpro.tech/. Recuperado: 2026-10-03.
12. **Dentaly** — https://www.dentaly.com.ar/. Recuperado: 2026-10-03.
13. **Consultorio Digital** — https://consultorio-digital.com.ar/. Recuperado: 2026-10-03.
14. **Dentalink** — https://softwaredentalink.com/. Recuperado: 2026-10-03.
15. **DenPro** — https://www.denpro.ar/. Recuperado: 2026-10-03.
16. **UDENTIVA** — https://udentiva.com/pt-ar. Recuperado: 2026-10-03.
17. **TurnosUno** — https://turnosuno.com/. Recuperado: 2026-10-03.
18. **Benty** — https://benty.com.ar/. Recuperado: 2026-10-03.
19. **Turnos Online BB (R.E.B @nline)** — https://turnosonlinebb.com/. Recuperado: 2026-10-03.

**Fuentes secundarias citadas por terceros (no usadas para puntuar):** hiorbita.com/nosotros (cobertura de prensa: TN, Ámbito, 0221 y Perspectiva Sur, julio 2026).

---

## Anexo 1. Fichas por sistema

### 1. Órbita Gestión + Órbita Chat

- **URL**: https://hiorbita.com/precios
- **País · Segmento**: Argentina · La Plata · consultorios y clínicas
- **Precio publicado**: Órbita Gestión Consultorio USD 25/mes (≈$38.250); Clínica USD 113/mes (≈$172.890); Red desde USD 500/mes. Órbita Chat desde USD 150/mes (anual) hasta USD 200/mes (mensual). Preventa Gestión desde USD 33/mes.
- **Riesgo de precio**: Precio fijado en USD; la referencia en pesos usa el dólar oficial venta del Banco Nación ($1.530, 11/09/2026). Costo real en ARS depende de la brecha cambiaria.
- **Reserva online**: Sí — Órbita Chat agenda por WhatsApp 24/7 y alta de paciente por QR
- **Recordatorios**: Sí — WhatsApp con recontacto automático, confirmación 48 h y 24 h antes
- **Puntaje**: Gestión de turnos y automatización: **5.0/5**, Funcionalidad odontológica clínica: **5.0/5**, Integraciones locales y WhatsApp: **5.0/5**, Administración, cobros y facturación: **5.0/5**, Experiencia del paciente: **5.0/5**, Seguridad, exportación y trazabilidad: **4.5/5**, Precio y facilidad de adopción: **3.5/5**
- **Total ponderado**: **4.88 / 5**
- **Evidencia**: Agenda por sillón con «choque imposible»; agendamiento inteligente que ofrece primero los horarios que no dejan huecos; lista de espera; sobreturnos; alta por QR; controles automáticos al cerrar tratamiento. Odontograma con periodontograma de 6 sitios por pieza; dictado por voz que carga el odontograma; el odontograma escribe la historia clínica solo; historia firmada y encadenada. Exportación total de datos; log de accesos y roles; registro de accesos que nadie puede borrar; importes ocultos por rol. Presupuestos con embudo y tasa de aceptación, cobranzas y caja, convenios y liquidaciones, laboratorio, trazabilidad de materiales por lote. Asistente IA 24/7 con «Juez IA» que detecta urgencias. API oficial de Meta con el número de la clínica. Integra con Dentalink, Bilog y Benty.
- **Notas**: Es el competidor más completo del relevamiento y el que más se aproxima a la v1 proyectada. Su propia página de comparativa afirma que los otros tres sistemas relevantes también tienen «agenda validada por sillón», lo que contradice el diferencial de vender la agenda por sillón como exclusivo (ver Hallazgo H-01).

### 2. DentalSaaS (DelRioTech SAS)

- **URL**: https://dental.delriotech.com.ar/
- **País · Segmento**: Argentina · Santiago del Estero · consultorios y clínicas
- **Precio publicado**: Consultorio $59.000/mes (1 odontólogo + 1 secretaria, hasta 300 pacientes y 300 turnos/mes, 2 GB); Clínica $149.000/mes (hasta 5 odontólogos, 1.000 pacientes); Pro $349.000/mes (ilimitados). Sin permanencia. Anual 2 meses bonificados.
- **Riesgo de precio**: El plan de $59.000 es el más caro del segmento comparable; el servicio de WhatsApp no está incluido en el precio publicado.
- **Reserva online**: Sí — portal del paciente con autogestión de turnos y auto-agendamiento (planes Clínica y Pro)
- **Recordatorios**: Sí, con costo adicional — WhatsApp 24 h y 2 h antes, requiere configuración o servicio de DelRioTech; asistente de IA para WhatsApp es complemento aparte
- **Puntaje**: Gestión de turnos y automatización: **4.5/5**, Funcionalidad odontológica clínica: **5.0/5**, Integraciones locales y WhatsApp: **3.5/5**, Administración, cobros y facturación: **5.0/5**, Experiencia del paciente: **4.5/5**, Seguridad, exportación y trazabilidad: **3.0/5**, Precio y facilidad de adopción: **3.0/5**
- **Total ponderado**: **4.30 / 5**
- **Evidencia**: Agenda inteligente diaria/semanal/mensual por profesional, con bloqueo de horarios, feriados y vacaciones y **detección automática de solapamientos**. Historia clínica digital con odontograma, periodontograma SVG y fichas especializadas en Ortodoncia, Periodoncia, Endodoncia, Implantología, Prótesis y Cirugía; recetas A5, consentimiento digital con firma electrónica y snapshot legal, imágenes clínicas con visor. Caja y cobros con MercadoPago, cierre contable mensual, más de 10 reportes PDF/Excel, control de stock con alerta de mínimo, liquidación de profesionales y gestión de laboratorios. Auditoría completa exportable: movimientos de caja, turnos, cobros, accesos y cambios de datos de pacientes. Catálogo nacional de obras sociales precargado con importación masiva y nomenclador por país. White label. Importación por CSV con mapeo automático y detección de duplicados.
- **Notas**: El de mayor alcance funcional verificado y el competidor más directo para el segmento objetivo (plan Consultorio: 1 odontólogo + 1 secretaria). **Corrección H-02:** la versión anterior de este relevamiento lo clasificaba como «sin precios públicos»; la página oficial publica los tres planes con precio.

### 3. ClinIA / OdontoClinIA

- **URL**: https://www.clinia.com.ar/odontologia
- **País · Segmento**: Argentina · consultorios individuales, clínicas PyME, municipios (SUMAR+), cadenas
- **Precio publicado**: No publicado. Demo gratuita con acompañamiento en los primeros días.
- **Riesgo de precio**: Sin precio público; producto de alto costo de implementación.
- **Reserva online**: No evidenciado
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **2.0/5**, Funcionalidad odontológica clínica: **4.5/5**, Integraciones locales y WhatsApp: **5.0/5**, Administración, cobros y facturación: **4.5/5**, Experiencia del paciente: **2.0/5**, Seguridad, exportación y trazabilidad: **4.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **3.50 / 5**
- **Evidencia**: Recetario electrónico inscripto en ReNaPDiS con identificador 248, estándar HL7 FHIR. Verificación automática de cobertura vía API de PUCO (Superintendencia de Servicios de Salud). Facturación electrónica integrada con AFIP. Liquidación a obras sociales con detalle por prestación conforme al nomenclador odontológico vigente. Historia clínica electrónica dental que declara cumplir la Ley de Historia Clínica Electrónica argentina. Odontograma y planes de tratamiento por etapas con presupuesto por pieza y descuento por obra social. Instancia personalizada con subdominio propio. Módulo de internación y quirófano.
- **Notas**: El único con cumplimiento normativo argentino completo y verificable (ReNaPDiS + PUCO + AFIP). Es el techo de completitud del mercado y el competidor a evitar en la v1.

### 4. DentalSoft

- **URL**: https://dentalsoft.com.ar/
- **País · Segmento**: Argentina · consultorios y clínicas
- **Precio publicado**: No publicado.
- **Riesgo de precio**: Sin precio público.
- **Reserva online**: Sí — la web propia del consultorio es parte del producto y una reserva entra directo a la agenda
- **Recordatorios**: Sí — WhatsApp y email
- **Puntaje**: Gestión de turnos y automatización: **3.5/5**, Funcionalidad odontológica clínica: **4.0/5**, Integraciones locales y WhatsApp: **4.0/5**, Administración, cobros y facturación: **3.5/5**, Experiencia del paciente: **4.5/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **3.42 / 5**
- **Evidencia**: Agenda semanal, diaria y mensual con drag & drop, urgencias, bloqueos, multi-sucursal y sincronización con Google Calendar. Odontograma SVG interactivo con 18 estados clínicos, notación FDI y módulo de ortodoncia. Caja con MercadoPago, obras sociales y liquidaciones automáticas. Dos módulos conectados: software odontológico y página web propia. Declara 300+ clínicas en Argentina y 4,9/5 de satisfacción, y 82 % de reducción de ausencias.
- **Notas**: Único que integra el sitio web del consultorio con la agenda como un mismo producto, cerrando el circuito reserva → atención → cobro. Las cifras de ausencias y satisfacción son declaradas por el vendedor, sin fuente primaria (ver «No evidenciado»).

### 5. DentalFLOW (TrapelTech)

- **URL**: https://dentalflow.ar/
- **País · Segmento**: Argentina · Choel, Río Negro · consultorios multiespecialidad
- **Precio publicado**: No publicado. Demo por WhatsApp; prueba gratuita con los datos propios del consultorio.
- **Riesgo de precio**: Sin precio público; no permite comparación de costo.
- **Reserva online**: Sí — reserva 24/7 con DNI, profesional, tipo de consulta, día y horario, en 2 minutos
- **Recordatorios**: Parcial — hoy por email; WhatsApp declarado «en camino»
- **Puntaje**: Gestión de turnos y automatización: **4.5/5**, Funcionalidad odontológica clínica: **3.5/5**, Integraciones locales y WhatsApp: **2.0/5**, Administración, cobros y facturación: **1.5/5**, Experiencia del paciente: **4.0/5**, Seguridad, exportación y trazabilidad: **4.5/5**, Precio y facilidad de adopción: **2.0/5**
- **Total ponderado**: **3.30 / 5**
- **Evidencia**: Agenda en tiempo real con colores por estado, duración por consulta configurable y bloqueos configurables; reserva interna para pacientes presenciales o telefónicos; panel con dashboard del día, sobreturnos y lista de espera. Historia clínica con odontograma interactivo por pieza, notas privadas y adjuntos de radiografías y fotos. **Prevención de solapamientos garantizada a nivel de base de datos: no hay doble reserva.** Cifrado en tránsito y en reposo, control de acceso por rol, **auditoría de cada acceso a las historias clínicas**, aislamiento entre consultorios; declara estar diseñado según la Ley 25.326 y que sus datos se tratan conforme a esa ley. Roles de Recepción, Profesionales y Administración. Exportación de los datos al salir.
- **Notas**: **Corrección H-03:** la versión anterior afirmaba «recordatorios automáticos» sin matizar; la web aclara que los recordatorios salen por email y que WhatsApp está en camino. Mantiene la mejor evidencia de seguridad y la garantía explícita de no-doble-reserva.

### 6. DentalTec

- **URL**: https://web.dentaltec.com.ar/
- **País · Segmento**: Argentina · profesionales, instituciones y obras sociales
- **Precio publicado**: No publicado. Solicitar demo.
- **Riesgo de precio**: Sin precio público.
- **Reserva online**: No evidenciado
- **Recordatorios**: Sí — integración de agenda con WhatsApp con confirmación
- **Puntaje**: Gestión de turnos y automatización: **3.0/5**, Funcionalidad odontológica clínica: **3.5/5**, Integraciones locales y WhatsApp: **3.5/5**, Administración, cobros y facturación: **4.0/5**, Experiencia del paciente: **1.5/5**, Seguridad, exportación y trazabilidad: **3.5/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **3.15 / 5**
- **Evidencia**: Declara 2.000+ profesionales. Módulos: agenda odontológica integrada, historia clínica digital, odontograma, carga y validación instantánea de prácticas, facturación automática, liquidaciones, estadísticas en vivo y auditoría completa. Integración de agenda con WhatsApp con confirmación. Se presenta como «Tandem Digital Software», hecho en Argentina. Marca de referencia «−80 % tiempo administrativo» y «100 % trazabilidad».
- **Notas**: Enfoque de red: conecta odontólogos, instituciones y obras sociales en una plataforma única, y posiciona a la competencia cloud como «todas-en-uno con enfoque LATAM». Las cifras de −80 % y 100 % son declaraciones del vendedor.

### 7. DoctorYa

- **URL**: https://doctorya.com.ar/
- **País · Segmento**: Argentina · salud general (no exclusivo de odontología)
- **Precio publicado**: Primer mes gratis; resto no publicado.
- **Riesgo de precio**: Sin precio de lista.
- **Reserva online**: Sí — reserva 24/7 por especialidad y ubicación, 100 % en navegador
- **Recordatorios**: Sí — WhatsApp con CONFIRMAR/CANCELAR que actualizan la agenda solos
- **Puntaje**: Gestión de turnos y automatización: **4.0/5**, Funcionalidad odontológica clínica: **2.0/5**, Integraciones locales y WhatsApp: **4.0/5**, Administración, cobros y facturación: **3.5/5**, Experiencia del paciente: **4.0/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **3.10 / 5**
- **Evidencia**: Agenda por profesional y sede con programar, reprogramar y cancelar. Recordatorios de WhatsApp que actualizan la agenda sin intervención. Ficha del paciente con estudios y archivos. Obras sociales y copagos configurables por profesional. **Facturación electrónica por ARCA** para Monotributo o Responsable Inscripto. Asistente conversacional en línea que toma el turno por chat.
- **Notas**: Único del relevamiento que declara explícitamente facturación electrónica mediante ARCA. Compite por el mismo dolor de agenda, pero no es vertical odontológico: no declara odontograma.

### 8. Marfil Clinic

- **URL**: https://www.marfilclinic.com/
- **País · Segmento**: Argentina · consultorios multiespecialidad
- **Precio publicado**: No publicado. «Propuesta personalizada según tamaño y necesidades». Demo de 20 minutos.
- **Riesgo de precio**: Sin precio público; declara «agenda y turnos ilimitados» sin costo por licencia de equipo.
- **Reserva online**: No evidenciado
- **Recordatorios**: Sí — notificaciones por email y WhatsApp
- **Puntaje**: Gestión de turnos y automatización: **3.0/5**, Funcionalidad odontológica clínica: **3.5/5**, Integraciones locales y WhatsApp: **2.5/5**, Administración, cobros y facturación: **3.0/5**, Experiencia del paciente: **3.5/5**, Seguridad, exportación y trazabilidad: **3.0/5**, Precio y facilidad de adopción: **2.0/5**
- **Total ponderado**: **3.02 / 5**
- **Evidencia**: Agenda visual con grilla mensual y drag & drop; cada profesional ve su propia agenda. Historia clínica digital con odontograma interactivo. Notificaciones por email y WhatsApp. Multi-profesional con espacio aislado por consultorio (multi-tenant), usuarios y permisos por profesional. Fotos por QR durante la consulta. Facturación y aranceles por obra social integrados. Siete temas de color de producto.
- **Notas**: Muy fuerte en experiencia de producto (temas, demo de 20 minutos, onboarding de 3 pasos).

### 9. Bilog

- **URL**: https://bilog.com.ar/
- **País · Segmento**: Argentina · 1.500+ clínicas y consultorios; gerenciadoras de obras sociales
- **Precio publicado**: No publicado. Solicitar contacto.
- **Riesgo de precio**: Sin precio público; producto institucional con ciclo de venta consultivo.
- **Reserva online**: No evidenciado
- **Recordatorios**: Sí — recordatorios declarados
- **Puntaje**: Gestión de turnos y automatización: **3.0/5**, Funcionalidad odontológica clínica: **2.5/5**, Integraciones locales y WhatsApp: **3.5/5**, Administración, cobros y facturación: **3.5/5**, Experiencia del paciente: **1.5/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **2.62 / 5**
- **Evidencia**: Declara 1.500+ clínicas y consultorios y más de 20 años acompañando la odontología argentina. Tres soluciones segmentadas: consultorios odontólogos, clínicas odontológicas y obras sociales/gerenciadoras (control prestacional, validación de procesos, trazabilidad). Funciones declaradas: turnos, pacientes, historia clínica, recordatorios, profesionales, agendas, liquidaciones e indicadores.
- **Notas**: El competidor más instalado del relevamiento y el único con producto para gerenciadoras. Trayectoria de más de 20 años, la mayor del mercado. Autogendamiento: no evidenciado.

### 10. Dentatools

- **URL**: https://dentatools.co/ar
- **País · Segmento**: Argentina · consultorios con pacientes particulares
- **Precio publicado**: $30.000/mes incluye hasta 3 odontólogos; $8.000/mes por odontólogo adicional; usuarios administrativos sin costo. Impuestos no incluidos.
- **Riesgo de precio**: Precio bajo y alcance acotado; sin obras sociales ni factura electrónica (decisión de scope declarada).
- **Reserva online**: Sí — auto-agendado mediante link
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **3.0/5**, Funcionalidad odontológica clínica: **3.0/5**, Integraciones locales y WhatsApp: **1.5/5**, Administración, cobros y facturación: **2.5/5**, Experiencia del paciente: **3.0/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **4.5/5**
- **Total ponderado**: **2.58 / 5**
- **Evidencia**: Historia clínica digital, odontograma interactivo y agenda de turnos con auto-agendado vía link. Presupuestos en PDF, cobros y cuentas por cobrar en pesos argentinos. **Declara explícitamente que NO gestiona obras sociales ni prepagas y que NO emite factura electrónica AFIP.** Prueba sin tarjeta.
- **Notas**: **Corrección H-04:** la versión anterior lo describía como vertical de obras sociales y prepagas; es lo contrario, declara excluirlas. Es el competidor más directamente comparable con la v1 en segmento (particulares), monetización en pesos y alcance funcional. Su honestidad explícita sobre lo que no hace es una señal de posicionamiento defensable.

### 11. DentalPro

- **URL**: https://www.dentalpro.tech/
- **País · Segmento**: Origen no declarado · equipos profesionales y clínicas
- **Precio publicado**: Equipo USD 69/mes (hasta 5 profesionales); Clínica USD 129/mes (6-8 profesionales); redes a medida. Plan solo profesional sin cotizar.
- **Riesgo de precio**: Cobra en dólares sin declarar origen ni cumplimiento normativo argentino; a la referencia de USD 1.530 del 11/09/2026, USD 69 equivale a unos AR$105.000/mes, muy por encima del piso local de AR$6.000-AR$35.000.
- **Reserva online**: No evidenciado
- **Recordatorios**: Sí — recordatorios por WhatsApp
- **Puntaje**: Gestión de turnos y automatización: **3.0/5**, Funcionalidad odontológica clínica: **3.5/5**, Integraciones locales y WhatsApp: **1.5/5**, Administración, cobros y facturación: **3.0/5**, Experiencia del paciente: **2.0/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **2.50 / 5**
- **Evidencia**: Declara más de 500 profesionales activos, 98 % de satisfacción y 3 veces más eficiencia. Agenda diaria, semanal y mensual con sincronización con Google Calendar. Doble odontograma (inicial y de tratamiento). Historial clínico con línea de tiempo, carga de imágenes y estudios. Registro de pagos con envío automático de link de pago. Recordatorios por WhatsApp. Reportes y métricas. Rol secretaria incluido. Asistente de IA que hace briefing diario con alertas clínicas.
- **Notas**: Sin obras sociales ni facturación local en la oferta base. Las cifras de satisfacción y eficiencia son declaraciones del vendedor sin fuente primaria.

### 12. Dentaly

- **URL**: https://www.dentaly.com.ar/
- **País · Segmento**: Argentina · consultorios y clínicas
- **Precio publicado**: Pro $35.000/mes (1 profesional, pacientes ilimitados); Clínica $100.000/mes (multiprofesional, agenda por profesional); multisede a medida. Anual 2 meses gratis.
- **Riesgo de precio**: Precio medio; sin autogendamiento declarado, lo que reduce su valor para nuestro caso de uso.
- **Reserva online**: No evidenciado
- **Recordatorios**: Sí — soporte por WhatsApp
- **Puntaje**: Gestión de turnos y automatización: **2.0/5**, Funcionalidad odontológica clínica: **3.5/5**, Integraciones locales y WhatsApp: **2.5/5**, Administración, cobros y facturación: **3.0/5**, Experiencia del paciente: **1.5/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **3.0/5**
- **Total ponderado**: **2.42 / 5**
- **Evidencia**: Agenda de turnos semanal y diaria, ficha del paciente e historia clínica, odontograma y periodontograma digitales, consentimientos con firma digital. Finanzas (ingresos, egresos, resumen), control de inventario, tratamientos, especialidades y obras sociales. Acceso desde cualquier dispositivo y soporte por WhatsApp.
- **Notas**: Posicionamiento explícito contra el «software legacy» de servidor local.

### 13. Consultorio Digital

- **URL**: https://consultorio-digital.com.ar/
- **País · Segmento**: Argentina · consultorios individuales
- **Precio publicado**: No publicado.
- **Riesgo de precio**: Sin precio público; alcance funcional reducido (sin liquidaciones ni multiprofesional).
- **Reserva online**: Parcial — el paciente elige día y hora; el sistema crea el paciente si es nuevo
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **2.5/5**, Funcionalidad odontológica clínica: **3.5/5**, Integraciones locales y WhatsApp: **1.0/5**, Administración, cobros y facturación: **3.0/5**, Experiencia del paciente: **2.5/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **2.35 / 5**
- **Evidencia**: Agenda de turnos donde el paciente elige día y hora y el sistema crea el paciente si es nuevo. Odontograma por caras en notación FDI con cada cambio fechado; lo pendiente arma solo el plan de tratamiento y pasa a azul al atender. Control de stock de materiales con descuento automático, gastos y resumen mensual de ingresos y resultado.
- **Notas**: Muy orientado al flujo de consulta: stock, odontograma y cobro integrados en un solo toque. El más pequeño en alcance.

### 14. Dentalink

- **URL**: https://softwaredentalink.com/
- **País · Segmento**: Argentina · consultorios (producto comercializado por contenido)
- **Precio publicado**: No publicado.
- **Riesgo de precio**: Sin precio público.
- **Reserva online**: Sí — agenda online
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **2.5/5**, Funcionalidad odontológica clínica: **3.0/5**, Integraciones locales y WhatsApp: **1.0/5**, Administración, cobros y facturación: **2.5/5**, Experiencia del paciente: **3.0/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **2.23 / 5**
- **Evidencia**: Según su propio blog: agenda online, historia clínica, odontograma interactivo, presupuestos y cobros en cuotas desde un mismo lugar. Publicó una guía sobre sistemas de turnos online el 08/07/2026, de autoría de Ana Fernández (CEO y fundadora).
- **Notas**: Se comercializa principalmente vía contenido SEO y captación de leads. Alcance normativo argentino: no evidenciado. Órbita declara integración con Dentalink.

### 15. DenPro

- **URL**: https://www.denpro.ar/
- **País · Segmento**: España (soporte +34, enfoque GDPR) · orientado al mercado argentino
- **Precio publicado**: $19.900/mes plan Basic (1 usuario); $29.900/mes plan Team (usuarios ilimitados). Anual −15 %. Prueba de 30 días.
- **Riesgo de precio**: Origen aparentemente no argentino: soporte en España y enfoque GDPR; no menciona ARCA, obras sociales ni nomenclador argentino.
- **Reserva online**: No evidenciado
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **2.5/5**, Funcionalidad odontológica clínica: **3.0/5**, Integraciones locales y WhatsApp: **0.5/5**, Administración, cobros y facturación: **1.5/5**, Experiencia del paciente: **1.0/5**, Seguridad, exportación y trazabilidad: **4.0/5**, Precio y facilidad de adopción: **3.5/5**
- **Total ponderado**: **2.20 / 5**
- **Evidencia**: Turnos y calendario, pacientes, odontograma FDI, recetas e historia clínica. Planes Basic/Team con 30 días de prueba. Soporte telefónico +34 672 182 743 (España) y declaración de cifrado AES-256 con datacentros ISO 27001 en la UE y cumplimiento de GDPR.
- **Notas**: Buena declaración de seguridad, pero sin integración normativa argentina. Autogendamiento del paciente: no evidenciado.

### 16. UDENTIVA

- **URL**: https://udentiva.com/pt-ar
- **País · Segmento**: Argentina (versión en español y pesos) · clínicas con turismo de salud
- **Precio publicado**: No publicado. «Consulte». Ofrece «Comence Gratis».
- **Riesgo de precio**: Sin precio público; información pública escasa.
- **Reserva online**: No evidenciado
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **1.5/5**, Funcionalidad odontológica clínica: **2.0/5**, Integraciones locales y WhatsApp: **2.0/5**, Administración, cobros y facturación: **2.5/5**, Experiencia del paciente: **2.0/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **1.82 / 5**
- **Evidencia**: Plataforma de gestión de clínicas odontológicas con gestión de pacientes, consultas, finanzas, turismo de salud y operaciones impulsadas por IA. Versión para Argentina con precios en ARS, selector de moneda y video de presentación.
- **Notas**: El turismo de salud (paciente internacional que viaja a Argentina) tiene necesidades distintas: coordinación de viajes, CUIT de extranjero y pagos internacionales. No es comparable con nuestro segmento objetivo.

### 17. TurnosUno

- **URL**: https://turnosuno.com/
- **País · Segmento**: Argentina · profesionales de la salud
- **Precio publicado**: Profesional AR$6.000/mes (100 turnos/mes, 2 profesionales, 1 usuario interno); Institucional AR$10.000/mes (500 turnos, 10 profesionales); AR$20.000 (2.000 turnos, 15 profesionales). Promo 80 % OFF de lanzamiento, 14 días de prueba.
- **Riesgo de precio**: El precio publicado es de promoción de lanzamiento, no un precio de lista estable; el volumen de turnos está topado por plan.
- **Reserva online**: Sí — página pública de reservas con cancelación y reprogramación online
- **Recordatorios**: Sí — avisos automáticos por correo (sin WhatsApp declarado)
- **Puntaje**: Gestión de turnos y automatización: **3.0/5**, Funcionalidad odontológica clínica: **0.0/5**, Integraciones locales y WhatsApp: **0.5/5**, Administración, cobros y facturación: **0.5/5**, Experiencia del paciente: **3.5/5**, Seguridad, exportación y trazabilidad: **1.0/5**, Precio y facilidad de adopción: **4.5/5**
- **Total ponderado**: **1.57 / 5**
- **Evidencia**: Página pública de reservas, agenda y pacientes, avisos automáticos por correo, cancelación y reprogramación online. Sin historia clínica ni odontograma: es puramente agenda.
- **Notas**: El más barato del relevamiento y el único que segmenta por volumen de turnos. Es la cota inferior de precio para agenda online sin clínica.

### 18. Benty

- **URL**: https://benty.com.ar/
- **País · Segmento**: Argentina · consultorios
- **Precio publicado**: 1 mes bonificado; resto no publicado.
- **Riesgo de precio**: Información pública muy escasa: sin ficha técnica, sin precios ni funcionalidades detalladas.
- **Reserva online**: No evidenciado
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **2.0/5**, Funcionalidad odontológica clínica: **2.0/5**, Integraciones locales y WhatsApp: **1.0/5**, Administración, cobros y facturación: **1.0/5**, Experiencia del paciente: **1.0/5**, Seguridad, exportación y trazabilidad: **0.5/5**, Precio y facilidad de adopción: **1.5/5**
- **Total ponderado**: **1.43 / 5**
- **Evidencia**: Agenda, pacientes e historia clínica en una sola plataforma, con acompañamiento en la puesta en marcha y contacto por WhatsApp.
- **Notas**: No permite una evaluación sólida más allá del posicionamiento. No evidenciado: autogendamiento, odontograma, obras sociales, aplicación móvil. Órbita declara integración con Benty.

### 19. Turnos Online BB (R.E.B @nline)

- **URL**: https://turnosonlinebb.com/
- **País · Segmento**: Argentina · profesionales y centros de salud
- **Precio publicado**: No publicado.
- **Riesgo de precio**: Sin precio público; producto mínimo.
- **Reserva online**: Sí — obtener o cancelar turno de forma gratuita
- **Recordatorios**: No evidenciado
- **Puntaje**: Gestión de turnos y automatización: **2.0/5**, Funcionalidad odontológica clínica: **0.0/5**, Integraciones locales y WhatsApp: **0.0/5**, Administración, cobros y facturación: **0.0/5**, Experiencia del paciente: **2.5/5**, Seguridad, exportación y trazabilidad: **0.0/5**, Precio y facilidad de adopción: **1.0/5**
- **Total ponderado**: **0.80 / 5**
- **Evidencia**: Software de turnos online contratado por profesionales y centros de salud. El paciente o potencial paciente puede obtener o cancelar un turno médico de forma gratuita. Los turnos pueden ser modificados por decisión exclusiva de los profesionales de la salud.
- **Notas**: Producto mínimo y de tecnología aparentemente antigua. Útil como línea de base de la categoría «agenda online básica», que ya existía antes de la ola actual.