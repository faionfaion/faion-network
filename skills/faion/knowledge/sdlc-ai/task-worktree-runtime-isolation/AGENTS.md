# One Task → One Branch → One Worktree → One Agent (Runtime-Isolated)

## Summary

**One-sentence:** Map every parallel agent run to one git worktree + one branch + one file-ownership scope + one runtime sandbox (ports, DB, cache, secrets) so collisions surface at merge, never at edit or boot.

**One-paragraph:** Each parallel agent run gets its own git worktree, its own feature branch, its own scoped file-ownership manifest, AND its own runtime sandbox: distinct ports, database name, cache namespace, and secret bundle. The mapping is exactly one task → one branch → one worktree → one agent. The agent is forbidden from editing files outside its declared scope; collisions surface only at merge time, never at edit time. Crucially, worktrees alone do not isolate runtime — port and DB collisions are the documented 2026 failure mode — so the harness MUST allocate a runtime sandbox per worktree, not just a working directory.

**Ефективно для:**

- Parallel coding-agent fleet, де 3+ агенти бігають одночасно.
- Stateful apps (Postgres/Redis): port + DB collisions inakshe рвуть build.
- Trunk-based dev із багатьма concurrent feature branches.
- CI runners that must spin up isolated sandboxes per PR.

## Applies If (ALL must hold)

- More than one coding agent runs in parallel against the same repo.
- The project boots a long-running service (web/api/db) the agent must exercise.
- Shared infra (Postgres, Redis, ports < 65536) is otherwise contended.

## Skip If (ANY kills it)

- Single agent, single task, no parallel execution.
- Pure static-analysis or doc edits with no runtime boot.
- Mandatory shared singleton (e.g., system service that cannot be sandboxed) makes per-worktree runtimes impossible.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo with main branch | git | repo root |
| Service boot config | docker-compose / Procfile / env | repo |
| Port and DB allocation policy | Markdown | infra docs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wt-env.example` | Env-file template with placeholders for port range, DB namespace, cache prefix, secrets ref. |
| `templates/wt-spawn.sh` | Shell harness that allocates a slot and spawns an isolated worktree. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-worktree-runtime-isolation.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-plan-mode-locked-execution]]
- [[task-spec-kit-three-step]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
