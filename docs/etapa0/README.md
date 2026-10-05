# Etapa 0 — Evidencia del instalador

La consigna pide **dos capturas** (PDF, línea 78):

> Evidencia: una captura del instalador finalizado y de la lista de harnesses instalados.

## Estado

| # | Archivo | Qué debe verse | Estado |
|---|---|---|---|
| 1 | `01-instalador-full.png` | El instalador **finalizado**, con el modo **Full** visible | ✅ hecho |
| 2 | `02-harnesses.png` | La lista de harnesses que imprime el instalador | ✅ hecho |
| — | `harnesses-instalados.md` | Inventario generado del estado real de la máquina | ✅ hecho |

Las dos capturas están en el repo, agregadas en el commit `3399abd`
(`docs(etapa0): agrega las capturas del instalador en modo Full`).

## Corrección aplicada el 2026-10-05 (H-10)

Este archivo decía que las dos capturas faltaban y que no podían generarse
automáticamente. **Eso era inexacto**: los dos PNG existían en `docs/etapa0/`
desde el commit `3399abd`, con 1359×715 y 1359×718 px y ~170 KB y ~220 KB
respectivamente. La tabla de estado y el párrafo introductorio se actualizaron
para reflejar el estado real.

Se conserva el procedimiento de captura porque sigue siendo válido para
rehacerlas si cambia el estado de la máquina.

**Límite de esta verificación:** se comprobó la existencia, el tamaño y las
dimensiones de los archivos. No se verificó visualmente que la captura del
instalador muestre el modo **Full**, porque la sesión de auditoría no puede
leer imágenes. Si el auditor exige esa comprobación, abrir
`docs/etapa0/01-instalador-full.png` a ojo.

## Procedimiento para rehacer las capturas

### 1. Clonar y construir

```powershell
cd $env:USERPROFILE
git clone https://github.com/Group-Active-IA/active-stack
cd active-stack
.\build.bat
```

### 2. Correr el instalador en modo Full

Elegí **Full**. No Lite: la consigna pide Full de forma explícita.

### 3. Capturar

Desde la raíz de este repo (`turnos-odontologia`), con el instalador visible:

```powershell
.\capturar-evidencia.ps1 "docs\etapa0\01-instalador-full.png"
.\capturar-evidencia.ps1 "docs\etapa0\02-harnesses.png"
```

El script captura la pantalla completa y crea la carpeta si no existe.
Si la ventana del instalador se cierra al terminar, correr el comando con
`-RetardoSegundos 5` para llegar a tiempo.

Sin el script: `Win + Shift + S`, y guardar en `docs/etapa0\` con esos nombres.

### 4. Verificar

```powershell
python C:\Users\Usuario\AppData\Local\Temp\opencode\audit_etapas.py
```

Debe pasar de `67 OK, 1 faltante` a `68 OK, 0 faltantes`.

## Nota sobre el estado actual del repo

Las carpetas `.opencode/` y `.claude/` existen y están completas, pero fueron
**reproducidas a mano**, no generadas por el instalador. Este límite sigue
vigente: las capturas acreditan que el instalador corrió, no que estas dos
carpetas hayan salido de él.
