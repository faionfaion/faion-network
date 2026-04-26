# SDLC + AI Methodologies

Geek-tier knowledge base of methodologies that wire AI coding agents (Claude Code, Cursor, Codex, aider, Windsurf) into the deterministic SDLC floor: language toolchains, lint/format, tests, trackers, knowledge bases, task lifecycle, merge automation, incident response, security, governance.

## Scope

Each methodology is a self-contained folder with `CLAUDE.md`, `AGENTS.md`, `content/*.xml`, optional `templates/` and `scripts/`. Routing is via the methodology `AGENTS.md` (under 80 lines, strict shape per `docs/skill-authoring.md`).

## Categories

| Prefix | Domain | Target |
|--------|--------|--------|
| `lang-` | Language / package mgmt / build | 10 |
| `lint-` | Linters, formatters, hooks | 6 |
| `test-` | Testing frameworks and tactics | 6 |
| `tracker-` | Issue trackers + agent integration | 5 |
| `kb-` | Knowledge base, docs, agent memory | 4 |
| `task-` | Task / spec / branch lifecycle | 5 |
| `mr-` | Merge request / PR review automation | 5 |
| `inc-` | Incident response, on-call | 4 |
| `sec-` | Supply chain + SAST + secrets | 3 |
| `gov-` | Governance, audit, identity | 4 |

## How To Use

1. Pick the category by the active task — language work → `lang-`, hook fix → `lint-`, etc.
2. List the matching methodology folders.
3. Read each candidate's `AGENTS.md` (cheap — under 80 lines).
4. Load only the `content/*.xml` files relevant to the decision.
5. Apply, then run the deterministic checks named in the methodology.

## Related

- Sibling: `geek/ai/ai-agents/` (agent-construction methodologies)
- Sibling: `geek/ai/llm-integration/semantic-xml-content/` (closed XML tag glossary)
- Spec: `docs/skill-authoring.md` (methodology folder structure)
