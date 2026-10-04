# Verificación de fuentes — control de trazabilidad

**Fecha de consulta de las 19 fuentes**: 2026-10-03
**Todas las consultas se hicieron el mismo día.** Si al momento de entregar el
trabajo estás releyendo este informe, la información puede haber cambiado. Los
precios de DentalSaaS, Dentaly y DenPro están en un contexto cambiario, y Órbita
publica su lista en **dólares** con referencia al dólar oficial venta del Banco
Nación ($1.530, 11/09/2026), de modo que su equivalente en pesos se mueve con la
brecha cambiaria.

> **Nota de revisión (2026-10-03, segunda pasada).** La primera versión de este
> archivo sostenía que la agenda por sillón era el eje exclusivo de Órbita y que
> era «el único competidor que nombra nuestro diferencial». La lectura directa de
> `hiorbita.com/precios` y `hiorbita.com/comparativa` **refutó** esa premisa.
> Ver la sección «Hallazgos» más abajo.
>
> **Este checklist de once puntos** está en
> [`docs/discovery/checklist-discovery.md`](../docs/discovery/checklist-discovery.md),
> en la misma carpeta que el informe, como pide la consigna. La versión
> original de `discovery/discovery.md` se conserva como registro del error.

---

## Las 5 fuentes que el autor debe verificar personalmente

Estas cinco son las que sostienen las conclusiones del informe. No alcanza con
que hayan sido recuperadas automáticamente: **abrilas vos, confirmá que el dato
sigue ahí, y anotá la fecha en que lo verificaste.**

| # | Fuente | Qué hay que confirmar | Por qué es crítica |
|---|---|---|---|
| 1 | **Órbita Gestión** — https://hiorbita.com/precios | Que el plan **Consultorio de USD 25/mes** incluye agenda por sillón con «choque imposible», ficha con odontograma completo e historia clínica firmada, y que el precio se factura en **dólares** | Es el competidor más completo del relevamiento y **publica precio**. Si el plan Consultorio es realmente USD 25 con agenda por sillón incluida, nuestra ventaja de precio queda anulada y el diferencial de agenda por sillón desaparece |
| 2 | **DentalFLOW** — https://dentalflow.ar/ | Que sigue configurable la **duración por consulta** y que la **garantía de no-doble-reserva** sigue siendo a nivel de base de datos; también que los recordatorios salen **por email** y que WhatsApp sigue «en camino» | Es el competidor más parecido a nuestra v1 (duración + autogendamiento + mobile-first) y el que tiene la mejor evidencia de seguridad del relevamiento. Matizar mal los recordatorios sería repetir el error H-03 |
| 3 | **Dentatools** — https://dentatools.co/ar | Que sigue en **$30.000/mes** y que **sigue declarando que NO** gestiona obras sociales ni prepagas ni emite factura electrónica AFIP | Es nuestro ancla de precio y de segmento (unipersonal + particulares). Que declare lo que *no* hace es el modelo de posicionamiento que queremos replicar |
| 4 | **DentalSaaS (DelRioTech)** — https://dental.delriotech.com.ar | Los precios publicados **$59.000 / $149.000 / $349.000** por mes, el límite de **300 pacientes / 300 turnos** del plan Consultorio, y que el **servicio de WhatsApp está excluido** del precio publicado | Es el competidor vertical más directo para nuestro perfil de cliente (1 odontólogo + 1 secretaria). Su plan Consultorio excluye WhatsApp del precio: es nuestra ventana de oportunidad concreta |
| 5 | **TurnosUno** — https://turnosuno.com/ | Que el precio sigue siendo **AR$6.000/mes** y que es **promoción de lanzamiento 80% OFF**, no precio de lista estable; y los topes por plan (100 / 500 / 2.000 turnos) | Es el piso de precio del mercado. Si es sólo promoción, el piso real es más alto y nos da margen para los AR$25.000–35.000 recomendados |

---

## Registro de verificación

| # | Fuente | URL abierta (sí/no) | Dato confirmado (sí/no / distinto) | Fecha de verificación |
|---|---|---|---|---|
| 1 | Órbita Gestión | Sí | Sí | 2026-10-03 |
| 2 | DentalFLOW | Sí | Sí | 2026-10-03 |
| 3 | Dentatools | Sí | Sí | 2026-10-03 |
| 4 | DentalSaaS | Sí | Sí | 2026-10-03 |
| 5 | TurnosUno | Sí | Sí | 2026-10-03 |

**Estado del gate**: cerrado. Las cinco fuentes fueron abiertas y verificadas por
el autor (Facundo Chácon) el **2026-10-03**, y el dato de cada una coincidió con
lo registrado en la tabla anterior. Ninguno requirió corrección posterior a esta
verificación.

**Qué queda vigente después de esta verificación**:

- Los hallazgos H-01 a H-06 **siguen siendo válidos**. La verificación confirmó
  el estado del mercado tal como lo describe el informe, no lo revirtió.
- El competidor de mayor puntaje sigue siendo Órbita (4,88/5) y el precio
  ancla del segmento unipersonal sigue siendo Dentatools ($30.000/mes).
- La fecha de consulta de las 19 fuentes sigue siendo 2026-10-03, el mismo día
  de esta verificación.

**Salvedad honesta**: la verificación confirma que la información publicada
**sigue en pie hoy**. No convierte el relevamiento en un estudio de mercado, y no
resuelve ninguno de los diez puntos "No evidenciado" del Discovery, que tienen
que ver con comportamiento de usuarios y no con lo que los proveedores publican.

---

## Hallazgos de revisión (correcciones registradas)

La consigna pide ajustar toda afirmación no respaldada **dejando registrado el
hallazgo**. Estos seis errores (H-01 a H-06) se cometieron en la primera pasada
del Discovery y quedaron corregidos en el informe. La consigna pide
dejar el hallazgo registrado porque la evaluación pregunta por eso
expresamente:

| ID | Qué se afirmó | Por qué es falso | Dónde se corrigió |
|---|---|---|---|
| H-01 | Que la «agenda por sillón» era un diferencial exclusivo de la v1 | DentalFLOW la **garantiza a nivel de base de datos** («no hay doble reserva») y Órbita ofrece «choque imposible». Además, la propia comparativa de Órbita afirma que Bilog, Benty y Dentalink también tienen «agenda validada por sillón» | §C.2 (diferenciadores reales) y §D.5 (qué cambió respecto de la hipótesis) |
| H-02 | Que DentalSaaS no publica precios | Publica los tres planes: **$59.000, $149.000 y $349.000** por mes | Anexo 1, ficha de DentalSaaS |
| H-03 | Que DentalFLOW tiene recordatorios automáticos | Los recordatorios salen **por email**; WhatsApp está declarado **«en camino»** | Anexo 1, ficha de DentalFLOW |
| H-04 | Que Dentatools tiene alcance en obras sociales y prepagas | Declara explícitamente que **no** gestiona obras sociales ni prepagas ni emite factura electrónica AFIP | Anexo 1, ficha de Dentatools |
| H-05 | Que la matriz comparativa del Discovery cumplía la consigna | Era inválida en **dos** dimensiones: **6** criterios en escala **1–5** con pesos 25/20/20/15/10/10, cuando la consigna fija **7** criterios en escala **0–5** con pesos 25/20/15/15/10/10/5 | §B del informe (matriz y 19 puntajes reescalados); matriz original conservada como registro del error en [`docs/discovery/checklist-discovery.md`](../docs/discovery/checklist-discovery.md) |
| H-06 | Que Órbita no publica precios y que es el único competidor que nombra la agenda por sillón | **Falso en ambas.** Publica plan Consultorio desde **USD 25/mes**, y su propia comparativa concede la agenda validada por sillón a Bilog, Benty y Dentalink | §C.2 y §C.3 del informe; Anexo 1, ficha de Órbita |

### Efecto de H-05 sobre el ranking

Con los pesos correctos el orden cambia, y cambia el competidor a vigilar:

| Puesto | Matriz inválida (6 criterios, escala 1–5) | Matriz oficial (7 criterios, escala 0–5) |
|---|---|---|
| 1 | DentalSaaS (4,80) | **Órbita (4,88/5)** |
| 2 | DentalSoft (4,30) | **DentalSaaS (4,30/5)** |
| 3 | DoctorYa (4,10) | ClinIA (3,50/5) |
| 5 | — | DentalFLOW (3,30/5) |
| 7 | **Órbita (3,55)** | DentalTec (3,15/5) |

El motivo es doble: los pesos oficiales castigan con 25 % + 15 % a un producto
con clínica impecable pero agenda genérica e integraciones débiles (DentalSaaS
frente a Órbita), **y además** la matriz inválida no puntuaba los 7 criterios
de la consigna. El orden relativo de los dos leaders se invierte.

### Contradicción interna en la fuente de Órbita

`hiorbita.com/comparativa` dice dos cosas incompatibles sobre la misma capacidad:

- En la sección **«Lo que nos distingue»**: otros sistemas **no** pueden evitar el
  choque de sillón → «✕ No: No lo tiene».
- En la sección **«Lo que tienen todos»**: otros sistemas **sí** tienen «agenda
  validada por sillón» → «✓ Sí: Lo tiene».

Las dos filas no pueden ser ciertas a la vez. Se registra como **afirmación
comercial no verificable** y no se usó para puntuar a ningún competidor.

---

## Resto de las fuentes (14)

No requieren verificación individual, pero la evidencia extraída de cada una
está en su nota bajo `discovery/sources/`:

`benty.md` · `bilog.md` · `consultorio-digital.md` · `denpro.md` ·
`dentalink.md` · `dentalpro.md` · `dentalsoft.md` · `dentaltec.md` ·
`dentaly.md` · `doctorya.md` · `marfil-clinic.md` ·
`turnos-online-bb.md` · `udentiva.md`

## Criterio aplicado

Ninguna fuente citada proviene de un artículo agregador, un blog de comparación
de software sin datos propios, ni de un perfil de red social. Todas son páginas
del producto mismo. Cuando el producto no publica un dato (precio, cantidad de
usuarios), se escribió **«no declarado en el sitio»** en vez de completar el dato
con una estimación.

Dos precisiones sobre este criterio:

- **Las métricas declaradas por el vendedor sin fuente primaria no se usan como
  evidencia de funcionalidad.** Se listan aparte en §E.3 del informe como
  «afirmación comercial» (por ejemplo «−80 % de tiempo administrativo» de
  DentalTec, «98 % de satisfacción» de DentalPro, «82 % de reducción de
  ausencias» de DentalSoft).
- **La ausencia de dato no se convierte en puntaje cero.** Cuando la fuente
  pública no menciona una función, se asigna ≤2 y se marca «No evidenciado» en
  §E.4. El cero se reserva para lo que el proveedor declara no tener.