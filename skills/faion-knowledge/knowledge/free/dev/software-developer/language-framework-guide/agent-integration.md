# Agent Integration — Language & Framework Selection Guide

## Note on scope
The methodology README is intentionally minimal (a small selection table + format/test commands). It serves as a tier-0 router for early project decisions, not a deep how-to. The agent-integration notes here are correspondingly compact.

## When to use
- Day-zero greenfield: agent must propose a stack for a project brief and justify it.
- A spec asks the agent to "use the right tool" — this guide is the canonical default mapping.
- Generating boilerplate format/lint/test commands for a CI scaffolding step.
- Sanity-check: the agent has chosen Python+Django for a 50ms-latency edge service — wrong fit, push back.

## When NOT to use
- The team has a strong existing stack mandate; this guide is a default, not a directive.
- Domains with non-obvious constraints (regulatory, hardware, specific cloud lock-in) — use a richer architectural decision record (ADR) flow instead.
- Picking between equally valid options for a small experiment — coin-flip is faster than a methodology page.

## Where it fails / limitations
- The list is short on purpose (Python, TS, Go, Rust + 4 frameworks); real selection includes 20+ candidate stacks (Elixir/Phoenix, Kotlin/Ktor, Java/Spring, .NET/ASP.NET, Ruby/Rails, etc.). Use this as a starter, not an exhaustive matrix.
- Doesn't capture cost, hiring market, or team familiarity — all dominant in real decisions.
- Format commands are out of date: most Python projects have moved from black+isort to ruff (`ruff format` + `ruff check`); JS toolchains are migrating to biome.
- No guidance on monorepo tooling (turborepo, nx, bazel) which is often a bigger decision than the language itself.

## Agentic workflow
Use a brief "stack-picker" subagent invocation: input is the spec (latency, scale, team size, hosting target); output is a one-line recommendation with two alternatives and the rationale. The orchestrator then emits scaffolding commands appropriate to the chosen stack. Do NOT have the same agent both pick the stack and implement it — separation forces explicit justification.

### Recommended subagents
- `faion-brainstorm` — diverge/converge over candidate stacks for non-trivial decisions.
- A custom `stack-picker` subagent — input: spec excerpt; output: recommendation + 2 alternatives + ADR stub.
- `faion-sdd-execution` — once stack is chosen, runs the SDD lifecycle with stack-specific quality gates.

### Prompt pattern
```
Spec: <one-paragraph project description>.
Recommend a primary stack from {Python+Django, Python+FastAPI, TS+Next.js, Go, Rust}, plus 2 alternatives.
For each: (a) one-line fit summary, (b) one risk, (c) one alternative scenario where the alternative wins.
Output ADR stub (Status, Context, Decision, Consequences).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Replaces black+isort+flake8 for Python | https://docs.astral.sh/ruff |
| `biome` | Replaces prettier+eslint for many JS projects | https://biomejs.dev |
| `prettier` | Format JS/TS/JSON/MD where biome is overkill | https://prettier.io |
| `eslint` | Lint JS/TS | https://eslint.org |
| `gofmt` / `goimports` | Format Go (built-in) | go.dev |
| `staticcheck` / `golangci-lint` | Lint Go | https://golangci-lint.run |
| `cargo fmt` / `clippy` | Format + lint Rust | rust-lang.org |
| `pytest` / `vitest` / `go test` / `cargo test` | Test runners per language | (each language site) |
| `cookiecutter` / `degit` / `create-*` CLIs | Template scaffolders | varies |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| stackshare.io | SaaS | yes | Reference for "what other companies use for X" — agent can cite. |
| GitHub Trends API | SaaS | yes | Sanity-check on language/framework popularity over the last year. |
| Astro / Next.js / Nuxt CLIs | OSS | yes | Stack-specific scaffolders the agent invokes after decision. |
| Cookiecutter Django / Cookiecutter PyPackage | OSS | yes | Opinionated templates encoding many of these defaults. |
| asdf / mise | OSS | yes | Multi-language version manager — agents pin per project. |

## Templates & scripts
The README already contains the format/test commands; no duplicate inline. For an ADR stub the picker subagent fills in:

```markdown
# ADR-NNN: Stack selection for <project>

Status: Proposed
Date: <YYYY-MM-DD>

## Context
<2–3 sentences on requirements>

## Decision
<chosen stack>

## Alternatives considered
- <alt 1>: rejected because <reason>
- <alt 2>: rejected because <reason>

## Consequences
- Positive: <bullets>
- Negative: <bullets>
- Neutral: <bullets>
```

## Best practices
- Force the picker to output two alternatives, not just one — eliminates "I picked X because X" reasoning.
- Anchor language choice to where the team is strongest unless there's a hard technical mismatch.
- Treat framework choice as cheaper to change than language choice — bias for popular frameworks within the chosen language.
- For solo/founder projects, prefer Python (FastAPI/Django) or TypeScript (Next.js) — biggest LLM training-data coverage means agents are most productive there.
- Prefer ruff over black+isort+flake8 for any new Python project; bias toward modern toolchains the agent knows well.

## AI-agent gotchas
- Agents pick the stack the prompt mentioned most recently, not the one that fits — randomize prompt order.
- LLM training cutoffs lag: an agent will pick last-year's "default" (e.g., CRA, webpack) over current best (Vite, Bun). Anchor prompts to the current year.
- The selection table here is not authoritative for niche domains (ML, embedded, blockchain, games). Don't let agents apply it outside its lane.
- Format/test commands in the README assume a project layout (`src/` for Python, top-level for JS). Agents copy verbatim into projects with different structure and break.
- Human-in-loop: stack decisions for any project that will live > 6 months should have human sign-off; agents are bad at long-tail considerations (compliance, hiring, vendor lock-in).
- Don't bake stack picks into reusable prompts — they become legacy fast.

## References
- https://docs.astral.sh/ruff — modern Python toolchain
- https://biomejs.dev — modern JS/TS toolchain
- https://github.com/joelparkerhenderson/architecture-decision-record — ADR templates
- https://stackshare.io — community stack inspiration
- https://2024.stateofjs.com / https://lp.jetbrains.com/python-developers-survey-2024 — annual popularity surveys
- https://thoughtworks.com/radar — Tech Radar for trend signals
