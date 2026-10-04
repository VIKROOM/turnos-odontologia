# Etapa 0 — Evidencia pendiente

La consigna pide **dos capturas** (PDF, línea 78):

> Evidencia: una captura del instalador finalizado y de la lista de harnesses instalados.

Ninguna de las dos se puede generar automáticamente: dependen de correr el
instalador de Active Stack en modo **Full**.

## Estado

| # | Archivo | Qué debe verse | Estado |
|---|---|---|---|
| 1 | `01-instalador-full.png` | El instalador **finalizado**, con el modo **Full** visible | ❌ falta |
| 2 | `02-harnesses.png` | La lista de harnesses que imprime el instalador | ❌ falta |
| — | `harnesses-instalados.md` | Inventario generado del estado real de la máquina | ✅ hecho |

`harnesses-instalados.md` cubre la **segunda** evidencia de forma parcial y
verificable: prueba qué harnesses hay, pero **no** que el instalador se haya
ejecutado. Está escrito para que quede claro ese límite.

## Procedimiento

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

Debe passar de `67 OK, 1 faltante` a `68 OK, 0 faltantes`.

## Nota sobre el estado actual del repo

Las carpetas `.opencode/` y `.claude/` existen y están completas, pero fueron
**reproducidas a mano**, no generadas por el instalador. Por eso la captura del
instalador no se puede reconstruir: hay que ejecutarlo.