# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

**Project**: SaaS Odontología (turnos-odontologia) — agenda por sillón para consultorio odontológico unipersonal
**Stack**: FastAPI 3.11 + PostgreSQL 15 + React 18 (Vite) + Docker Compose (DD-11)
**Generated**: 2026-10-05

## User Skills

All user-level skills live in `C:\Users\GERMAN\.config\opencode\skills\`. No project-level skill dirs exist (`.opencode/skills/`, `.claude/skills/`, `skills/` contain only `openspec-*` workflow skills — see Excluded below).

| Trigger | Skill | Path |
|---------|-------|------|
| `/active-orchestrator:init\|:kb\|:rules\|:openspec\|:devops\|:find-skill\|:registry` — or "start a new project from scratch using SDD/OpenSpec foundation flow" | active-orchestrator | `C:\Users\GERMAN\.config\opencode\skills\active-orchestrator\SKILL.md` |
| "crear/generar/actualizar AGENTS.md o CLAUDE.md", "armar las reglas del proyecto", "instrucciones para los agentes", after kb-creator + roadmap-generator | agents-md-generator (dir: `agent-instruction`) | `C:\Users\GERMAN\.config\opencode\skills\agent-instruction\SKILL.md` |
| Before declaring a task done — after implementing, after tests go green, "¿esto ya está?", "¿cumple lo pedido?" | criterios-aceptacion-check | `C:\Users\GERMAN\.config\opencode\skills\criterios-aceptacion-check\SKILL.md` |
| "find a skill for X", "is there a skill that can...", "how do I do X", "can you do X" | find-skills (dir: `find-skill`) | `C:\Users\GERMAN\.config\opencode\skills\find-skill\SKILL.md` |
| "crear base de conocimiento", "generar KB desde los docs", "documentar proyecto", build KB from .txt/.docx/.pdf | kb-creator | `C:\Users\GERMAN\.config\opencode\skills\kb-creator\SKILL.md` |
| "armar CHANGES", "armar roadmap", "crear mapa de changes", "generar plan de implementación", "qué changes necesito" | roadmap-generator | `C:\Users\GERMAN\.config\opencode\skills\roadmap-generator\SKILL.md` |
| Create a new skill, edit/optimize an existing skill, run evals, benchmark, optimize a skill's description for triggering | skill-creator | `C:\Users\GERMAN\.config\opencode\skills\skill-creator\SKILL.md` |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### criterios-aceptacion-check
- Run before saying "done/terminado/listo/hecho" — after implementing, after tests first go green, or when asked "¿cumple lo pedido?".
- Not for design or exploration (no implementation / no declared criteria yet).
- Step 0: locate the acceptance criteria source of truth (`design.md` / analyst's criteria doc). If no explicit list exists → STOP and ask for the criteria. Never invent criteria at close time.
- Copy each criterion verbatim into a traceability table (# | Criterio textual | Evidencia | Estado). Rewriting a criterion means verifying the wrong thing.
- Evidence must be reproducible by a third party: test name, command + output, file:line. Inspection-only criteria → mark ⚠️ and state explicitly that no test covers it.
- Default bias is "terminado"; this skill exists to counter it. When in doubt: ⚠️ before ✅. Verify the criterion, not code quality.
- Step 3 — always probe edge cases not in the criteria: out-of-range/zero/negative/null, double submit / retry / idempotency replay, information leaks in error messages (does an error reveal a patient/user exists?), concurrent access to the same row.
- Uncovered edge case = a finding for the analyst, not a test defect. Report it.
- Close with exactly one of three verdicts: ✅ APROBADO | ⚠️ APROBADO CON HALLAZGOS | ❌ RECHAZADO (a rejection without a repro — exact input, expected, obtained — is not a rejection). A finding not reported is a silent decision.

### kb-creator
- Output goes ONLY to `knowledge-base/` at project root — never mix with `docs/` (source docs).
- Mode A (silent/ingest): `docs/` has real source files (.txt/.docx/.pdf/.md non-README) → read all, generate the 10 canonical files + `README.md`, ask NOTHING. Ambiguities go to `10_preguntas_abiertas.md`; never invent a value.
- Mode B (interactive): no `docs/` sources and no `knowledge-base/` → act as strategic partner: summarize understanding, list 3-5 uncertainties, propose 2-3 approaches with pros/cons, ask 3-5 strategic questions, WAIT for answers before writing files.
- 10 mandatory files with exact names: 01_vision_y_objetivos, 02_descripcion_general, 03_actores_y_roles, 04_modelo_de_datos, 05_reglas_de_negocio, 06_funcionalidades, 07_flujos_principales, 08_arquitectura_propuesta, 09_decisiones_y_supuestos, 10_preguntas_abiertas + `knowledge-base/README.md` index.
- Optional extras `1X_`/`2X_kebab-case.md` (e.g. 11_pagos_mercadopago.md) complement, never replace, the 10.
- This project: KB already exists and is complete → do NOT re-run; edit individual files instead. State hook writes `state.kb` only (never `step`).

### roadmap-generator
- Pre-checks (fail → generate nothing): `knowledge-base/` exists, has the 10 canonicals, `openspec/` exists. Message + stop otherwise.
- Output: ONE file, `CHANGES.md` at project ROOT (not inside `openspec/`).
- Read always: 04_modelo_de_datos, 06_funcionalidades, 07_flujos_principales, 08_arquitectura_propuesta. Optionally: 03_actores_y_roles (auth/RBAC), 05_reglas_de_negocio, 10_preguntas_abiertas.
- Structure is a contract — do not add/remove top-level sections: Cómo usar este documento / Árbol de dependencias (ASCII tree with └── │) / Paralelismo por fase (GATE N) / Camino crítico / Plan óptimo con 3 agentes / FASE N sections.
- Change IDs `C-01`…`C-NN` (2-digit padding always), kebab-case name, NO `us-NNN-` prefix. Per change: Estado `[ ]`, Scope, Dependencias, Governance (BAJO/MEDIO/ALTO/CRITICO), Leer antes (3-5 KB files with `§section`).
- Dependency hierarchy (apply in order): infra/foundation first → core models → auth before protected resources → referenced entity before referencing → backend before coupled frontend → external integrations/payments/webhooks last → admin/dashboards last → visual refactors last.
- Scope bullets must be operational (what the agent will generate), not descriptive: ✅ `POST /api/auth/login — JWT access+refresh, rate limit 5/60s per IP+email`, ❌ "Sistema de autenticación completo".
- Fire-and-forget: no questions asked. State hook writes `state.roadmap` only (never `step`).
- This project: `CHANGES.md` already exists → for a single change, edit it directly instead of regenerating.

### agents-md-generator
- Pre-checks: `knowledge-base/` exists and `knowledge-base/02_descripcion_general.md` exists, else stop. Missing `CHANGES.md` → generate anyway but omit the Roadmap section and say so.
- Output: `AGENTS.md` AND `CLAUDE.md` at project ROOT, identical content (many harnesses read one or the other). Never inside `.claude/` or `openspec/`.
- Read `.atl/skill-registry.md` as the single source of truth for available skills — do NOT re-scan the filesystem. Fallback only if registry missing: scan `.claude/skills/` + `~/.claude/skills/`.
- Read `~/.claude/CLAUDE.md` (global) to AVOID duplicating universal rules (orchestrator, governance, engram, TDD). For each universal rule: if present in global → reference, don't repeat; if absent → include it here (else it falls in the void).
- Hard rules are stack-aware, never hardcoded to a language. Derive candidates from `knowledge-base/02_descripcion_general.md` (Go: gofmt/go vet, %w, no panic in libs; Python: snake_case, type hints, Pydantic extra='forbid' only if Pydantic; TS/React: PascalCase components, no `any`, strict tsconfig), then CONFIRM with the user via AskUserQuestion and STOP. Write only confirmed rules, as `NUNCA X → hacer Y`.
- If the user adds no project-specific rule, leaving just the reference line to the global is valid and desirable.
- DRY: AGENTS.md/CLAUDE.md only maps skill→agent role. Compact rules live ONLY here in the registry — add the literal reference line to `.atl/skill-registry.md`. Never invent skills that don't exist.
- Contract sections (don't remove): Stack Tecnológico / Base de Conocimiento / Skills Disponibles / Roadmap de Changes / Reglas Duras / Flujo de Trabajo.
- Don't use when: no `knowledge-base/` (run kb-creator first), or the user wants to edit one single rule (suggest editing the existing file).

### find-skills
- Check the leaderboard at https://skills.sh/ BEFORE running a CLI search — a well-known skill often already exists.
- CLI: `npx skills find <query> [--owner <owner>]`, `npx skills add <owner/repo@skill>`, `npx skills update`.
- Never recommend on search results alone. Verify: install count (prefer 1K+, cautious under 100), source reputation (`vercel-labs`, `anthropics`, `microsoft` over unknown authors), GitHub stars (<100 stars = treat with skepticism).
- Queries must be specific and multi-word: "react testing" > "testing"; try alternates if "deploy" misses ("deployment", "ci-cd").
- Present: skill name + what it does, install count, source, exact install command, skills.sh link.
- `-g` = global (user-level), `-y` = skip prompts. In this project the orchestrator owns installs: recommend only, never run `npx skills add` itself.
- No match → say so, offer to do the task directly, suggest `npx skills init`.

### skill-creator
- Anatomy: `skill-name/SKILL.md` (required) + optional `scripts/`, `references/`, `assets/`. Frontmatter `name` + `description` required.
- Progressive disclosure: metadata always in context (~100 words) → SKILL.md body when triggered (<500 lines) → bundled resources on demand. Over ~500 lines, add a layer of hierarchy with pointers instead of growing.
- The `description` is the ONLY triggering mechanism — put ALL "when to use" there, never in the body. Make it slightly "pushy" to counter under-triggering; name the concrete contexts/keywords.
- Prefer imperative instructions; explain the WHY rather than stacking ALL-CAPS MUSTs (heavy-handed rigidity is a yellow flag).
- No malware/exploit content; content must not surprise the user relative to its description.
- Test prompts to `evals/evals.json` (prompts first, assertions later). Evals must be substantive — simple one-step queries won't trigger skills regardless of description quality.
- Baseline for a new skill = no skill (`without_skill`); for an improved skill = snapshot of the original (`cp -r` to workspace before editing).
- Launch with-skill AND baseline runs in the SAME turn; results in `<skill-name>-workspace/iteration-N/eval-<id>/`.
- `grading.json` MUST use fields `text`, `passed`, `evidence` (the viewer depends on these exact names). Write scripts for programmatically checkable assertions rather than eyeballing.
- Use `eval-viewer/generate_review.py` — never custom HTML; headless/Cowork → `--static <path>`, feedback arrives as a downloaded `feedback.json`.
- Improving: generalize from feedback instead of overfitting, keep the prompt lean, explain the why, and bundle scripts when multiple runs independently re-invent the same helper.
- Description optimization: 20 realistic trigger evals (8-10 should-trigger with varied phrasings, 8-10 tricky near-miss should-NOT-trigger), then `scripts.run_loop --max-iterations 5`; pick `best_description` by TEST score, not train (avoids overfitting).

### active-orchestrator
- Thin coordinator ONLY: detect entrypoint, own `step` in `.active-orchestrator-state.json` (schema version 4), run `openspec init`, dispatch phases, hold a checkpoint at every boundary, degrade when a sub-skill is missing.
- NEVER reimplement a phase's logic, NEVER ask discovery questions (kb-creator's domain), NEVER write knowledge-base/, CHANGES.md, or CLAUDE.md.
- Phase order (frozen): openspec init → kb-creator (inline) → roadmap-generator (sub-agent) → find-skill (sub-agent, RECOMMEND-ONLY) → skill-registry (sub-agent) → agent-instruction (inline).
- Interactivity decides placement: phases that must ask the user run inline (`Skill`); mechanical phases go to `Agent` (they'd inflate context).
- NEVER chain phases without a checkpoint. After each phase show a one-line summary, then AskUserQuestion: Continuar / Ajustar (re-run same phase) / Parar. Advance `step` ONLY on explicit "Continuar".
- Never install autonomously: find-skill recommends, the user picks at the install gate, then the orchestrator installs only the picks.
- After `openspec init`, remove the redundant `.claude/skills/openspec-*` copies (they ship globally) — but NEVER touch `.claude/commands/opsx/`.
- Degrade gracefully if a sub-skill is missing: offer install → if declined, mark `{section: {skipped: true}}` and continue. Never abort the full flow.
- Commit/push and install project dependencies only when explicitly asked.

## Excluded — OpenSpec/SDD workflow skills (no compact rules)

These are SDD workflow skills, not coding/task skills. They are invoked via `/opsx:*` slash commands, not injected as rules. Listed so delegators don't re-scan for them. Duplicate copies exist in `.opencode/skills/` and `.claude/skills/` — `.opencode/skills/` wins for OpenCode.

| Skill | Path |
|-------|------|
| openspec-propose | `.opencode/skills/openspec-propose/SKILL.md` |
| openspec-apply-change | `.opencode/skills/openspec-apply-change/SKILL.md` |
| openspec-update-change | `.opencode/skills/openspec-update-change/SKILL.md` |
| openspec-sync-specs | `.opencode/skills/openspec-sync-specs/SKILL.md` |
| openspec-archive-change | `.opencode/skills/openspec-archive-change/SKILL.md` |
| openspec-explore | `.opencode/skills/openspec-explore/SKILL.md` |

## Project Conventions

No `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, or `copilot-instructions.md` exists at project root yet — Phase 5 (`agents-md-generator`) generates them. The files below are the current de-facto conventions and source of truth.

| File | Path | Notes |
|------|------|-------|
| README.md | `README.md` | Project name/header only — thin, no real conventions |
| CHANGES.md | `CHANGES.md` | Master index of OpenSpec changes: dependency tree, parallelism gates, critical path, per-change scope/governance/"Leer antes". Read before any `/opsx:propose`. |
| Knowledge base index | `knowledge-base/README.md` | Index of the 10 canonical KB files |
| KB — vision | `knowledge-base/01_vision_y_objetivos.md` | Purpose, actors, scope/out-of-scope |
| KB — description | `knowledge-base/02_descripcion_general.md` | **Stack table source of truth**: FastAPI 3.11, PostgreSQL 15, React 18 + Vite, JWT httpOnly cookies, Docker Compose (DD-11) |
| KB — actors | `knowledge-base/03_actores_y_roles.md` | Roles, RBAC, public routes |
| KB — data model | `knowledge-base/04_modelo_de_datos.md` | Entities, ERD, seed data, `EXCLUDE USING gist` no-overlap constraint (DD-05) |
| KB — business rules | `knowledge-base/05_reglas_de_negocio.md` | RN-XX coded rules |
| KB — features | `knowledge-base/06_funcionalidades.md` | User stories / epics = unit of each change |
| KB — flows | `knowledge-base/07_flujos_principales.md` | End-to-end flows |
| KB — architecture | `knowledge-base/08_arquitectura_propuesta.md` | Patterns, dirs, security, env vars |
| KB — decisions | `knowledge-base/09_decisiones_y_supuestos.md` | DD-NN design decisions + inferred assumptions |
| KB — open questions | `knowledge-base/10_preguntas_abiertas.md` | Blocking inconsistencies + prioritized open questions |
| Orchestrator state | `.active-orchestrator-state.json` | Schema v4, `step: "roadmap"`. Sections owned by sub-skills. Not a convention doc — read for phase context. |
| OpenSpec config | `openspec/config.yaml` | OpenSpec project config |
| Discovery research | `docs/discovery/informe-discovery.md` | Original discovery report the KB was ingested from |
| Discovery verification | `discovery/verificacion-fuentes.md` | Manual verification of the 6 critical competitor URLs |
| Evidence capture script | `capturar-evidencia.ps1` | Screenshot/evidence capture helper |

Read the convention files listed above for project-specific patterns and rules. All referenced paths have been extracted — no need to read index files to discover more.