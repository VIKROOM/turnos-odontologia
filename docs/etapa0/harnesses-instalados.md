# Harnesses instalados

> **Generated**: `2026-10-03` por inspeccion del estado real de la maquina. Este archivo **no** es una captura del instalador.

## Que prueba y que no prueba este archivo

| | |
|---|---|
| **Si prueba** | que los harnesses estan presentes en la maquina y con que contenido |
| **No prueba** | que el instalador de Active Stack se haya ejecutado en modo Full |

La consigna (Etapa 0) pide dos capturas: la del **instalador finalizado** y la de la
**lista de harnesses instalados**. La segunda se reemplaza por este archivo hasta que
se cargue la captura; la primera depende de correr el instalador.

## Harnesses detectados

| Harness | CLI | Version | Carpeta en el repo | Comandos | Skills | Rol |
|---|---|---|---|---|---|---|
| OpenCode | `opencode` | `1.18.34` | `.opencode` (si) | 6 | 6 | Agente de codigo con el que se esta corriendo esta sesion |
| Claude Code | `claude` | `2.1.221 (Claude Code)` | `.claude` (si) | 6 | 6 | Segundo agente de codigo, requerido por la consigna como alternativa |

## CLIs requeridos por la consigna

La consigna pide como herramientas previas Go, Git, Node y un agente de codigo
funcionando. Estado verificado:

| Herramienta | Estado | Version |
|---|---|---|
| `openspec` | instalada | `1.14.0` |
| `claude` | instalada | `2.1.221 (Claude Code)` |
| `opencode` | instalada | `1.18.34` |
| `go` | instalada | `go version go1.26.6 windows/amd64` |
| `git` | instalada | `git version 2.50.1.windows.1` |
| `node` | instalada | `v24.11.1` |
| `npm` | instalada | `11.6.2` |

## Estado del repositorio

- `.active-orchestrator-state.json` presente, `version` = `4`
- `step` = `kb`
- `gate_discovery` = `None`

## Pendiente (Etapa 0)

- [ ] `01-instalador-full.png` — captura del instalador en modo **Full** finalizado
- [ ] `02-harnesses.png` — captura de la lista de harnesses que imprime el instalador
- [ ] Reemplazar este inventario por la captura, o conservarlo como complemento

Ver `docs/etapa0/README.md` para el procedimiento.
