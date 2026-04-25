# SDLC+AI Methodologies — Research & Curation

**Goal:** Collect 50+ practical methodologies for building a modern AI-augmented SDLC.
Output: methodologies in `geek/sdlc-ai/` + matching site articles in `faion-net-fe/content/knowledge/sdlc/`.

## Scope

How to wire AI agents into the software-development lifecycle without losing rigor:

- **Without-AI hardening first** — linters, formatters, type checkers, autotests per language. AI builds on top of a solid floor.
- **Project KB for agents** — AGENTS.md / CLAUDE.md / .agents / .aidocs conventions; symbol indexes; vector retrieval over the codebase.
- **Task lifecycle with AI** — agents read a task tracker, investigate the code, draft tasks, get specialist approval, execute, open MRs.
- **Incident & error response** — agents that triage Sentry-style 500s and open MRs; playbook agents that run runbooks for incidents.
- **Governance** — approval gates, allowlists, sandboxes, audit trails.

## Files

| File | Purpose |
|------|---------|
| `state.json` | Counter, target, last-updated, current cycle, category buckets |
| `methodologies.jsonl` | One line per accepted methodology |
| `candidates.md` | Brainstorm queue |
| `sources.md` | Bibliography |
| `progress.md` | Append-only log |
| `loop-prompt.md` | The /loop tick prompt |
| `research/AGENT-NN.md` | One per research subagent |
| `brainstorm/CYCLE-NN.md` | Per-tick output |
| `project-mining/` | Tricks extracted from our own pipelines |
| `articles-published/MAP.md` | methodology → article-id |

## Categories (target distribution)

| Category | Target | Slug prefix |
|----------|--------|-------------|
| Per-language tooling (Py, JS/TS, Go, Rust, Java, Kotlin, Ruby, PHP, C#, Swift) | 10 | `lang-` |
| Linters/formatters/SAST (no-AI floor) | 6 | `lint-` |
| Test patterns (TDD, BDD, property, mutation, contract, E2E) | 6 | `test-` |
| Task-tracker integration | 5 | `tracker-` |
| Project KB for agents | 4 | `kb-` |
| Agent task-investigation flow | 5 | `task-` |
| MR automation (Sentry→PR, AutoPR, agent-as-author) | 5 | `mr-` |
| Incident & playbook agents | 4 | `inc-` |
| CI/CD security & secrets | 3 | `sec-` |
| Governance & approval gates | 4 | `gov-` |
| **Total** | **52** | |

## Acceptance criteria

1. Concrete, testable rule (not "use good practices")
2. At least one cited source OR a real example from our projects
3. Identifies *when to use* and *when NOT to*
4. Distinct from already-accepted methodologies
5. Maps to one of the 10 categories
