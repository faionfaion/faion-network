# Agent Integration — Monolith Architecture

## When to use
- Greenfield product with team ≤10 and unclear domain boundaries — default to a (modular) monolith and let agents help structure it.
- "Should we go microservices?" investor/team debate — use agents to produce a Monolith-First counter-proposal grounded in this methodology + measured cost.
- Existing monolith hitting scale pain (deploy time, merge conflicts, hot-spot scaling) — agent runs a triage pass and recommends modular monolith refactor or selective extraction.
- Strangler-fig migration planning: rank candidate boundaries to extract, with cost + risk per boundary.
- Solo founder building MVP — agent scaffolds the standard Django/FastAPI/Rails monolith from `templates.md` to remove blank-page friction.

## When NOT to use
- Latency-critical or massively concurrent component (real-time game server, video transcoder, ML inference farm) — these justify dedicated services even at small scale.
- Multi-tenant systems with hard regulatory isolation (HIPAA per-tenant DBs, PCI scope reduction) — service boundary is a compliance requirement, not an architecture preference.
- Existing org with 50+ engineers and persistent merge-conflict pain — methodology already says it's time to extract; agents should switch to microservices/modular tooling.
- Pure batch/data-pipeline workloads — DAG orchestrator (Airflow, Dagster, Temporal) is a better baseline than a monolith.

## Where it fails / limitations
- **"Modular" is wishful:** without import-linter / ArchUnit / deptry enforcement, any monolith degrades into a Big Ball of Mud within ~12 months. The methodology mentions this but rarely automated.
- **Database coupling:** the doc recommends schema-per-module on one DB. In practice teams skip schemas, share tables, and lose all extraction options later. No tool listed enforces it.
- **Deploy risk:** a single artifact means a single failure mode. Blue-green/canary advice exists but presumes a CI/CD platform that solo teams often don't have set up.
- **Scaling axes:** vertical scaling has a clean cost ceiling that's not modeled. Agents tend to recommend "scale up" past the point where horizontal would be cheaper.
- **Tech-stack lock-in:** real cost is migration tax, not technology preference; the README understates it.
- **Feature-flag debt:** combining trunk-based + feature flags + canary requires lifecycle hygiene; without it, dead flags accumulate and become security/perf risks.

## Agentic workflow
Drive monolith design as a three-stage agent pipeline: (1) a **scaffolder agent** generates the project layout (cmd/internal/apps depending on stack) plus CI, lint config (`import-linter`, `deptry`, `ArchUnit`), and a `docs/adr/` folder pre-populated with an "ADR-0001 monolith-first" decision; (2) a **boundary-checker agent** runs on every PR — reads import-linter contracts and blocks cross-module imports, flags shared DB tables; (3) a **scaling-coach agent** runs weekly against perf/SLO metrics and proposes one of `vertical-scale | add-cache | add-replica | extract-service` with a cost estimate. Persist decisions as ADRs (link methodology: `architecture-decision-records/`).

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts the monolith checklist (12 phases) into SDD `todo/` tasks; one task per module boundary.
- `faion-research-agent` (`skills/faion-knowledge/knowledge/pro/research/researcher/`) — gathers comparable scaling data (Shopify, GitHub, Basecamp) when justifying a Monolith-First ADR to skeptics.
- A **module-boundary-linter agent** (purpose-built, worth creating): runs `import-linter` / `deptry` and explains every violation in plain language with the suggested public-API alternative.
- A **strangler-fig planner agent** (purpose-built): given a monolith repo + traffic logs, ranks candidates for extraction by `(scaling-need × team-coupling) / extraction-cost`.

### Prompt pattern
Scaffold:
```
You are a senior backend architect. Generate a Python/FastAPI modular
monolith for <product brief>. Modules: <list>. Each module owns its
schema and exposes only `public_api.py`. Include: pyproject.toml,
import-linter contracts blocking cross-module imports, Dockerfile,
docker-compose with PostgreSQL+Redis, GitHub Actions CI running
ruff + import-linter + pytest. No microservices. Reference
monolith-architecture/templates.md.
```

Boundary review:
```
Read <PR diff>. Identify any imports that cross module boundaries
defined in .importlinter. For each violation: file, offending import,
the *public_api* function the code should call instead, and a 1-line
fix. Output as markdown table; do not propose code changes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `import-linter` (Python) | Enforce architecture/import contracts in CI | `pip install import-linter` |
| `deptry` (Python) | Find unused/missing/transitive deps in monolith | `pip install deptry` |
| `ArchUnit` (Java/Kotlin) | JVM equivalent of import-linter | https://www.archunit.org |
| `dependency-cruiser` (TS/JS) | Module boundary rules in JS monoliths | `npm i -g dependency-cruiser` |
| `madge` | Visualize JS module graph, detect cycles | `npm i -g madge` |
| `pyreverse` (pylint) | Generate UML/dep graphs from Python monolith | included with `pylint` |
| `gh` CLI | Drive PR-based ADR review for monolith decisions | https://cli.github.com |
| `pgbouncer` | Connection pooling — required when scaling Python monolith horizontally | https://www.pgbouncer.org |
| `Unleash` / `Flagsmith` CLI | Feature-flag lifecycle (paired with trunk-based) | https://www.getunleash.io / https://flagsmith.com |
| `flyctl` / `kamal` / `caprover` | Solo-friendly deploy targets for monoliths | https://fly.io / https://kamal-deploy.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Render / Railway / Fly.io | SaaS PaaS | API yes | Best-in-class for solo monoliths; agents can deploy via CLI/API. |
| Heroku | SaaS PaaS | API yes | Classic monolith host; expensive but extremely stable. |
| Kamal (37signals) | OSS deploy | yes | Docker-based, made *for* monoliths; agent-driven via CLI. |
| AWS Elastic Beanstalk / ECS | SaaS | API yes | Defensible enterprise default; more ops cost than Fly/Render. |
| LaunchDarkly / Unleash / Flagsmith | SaaS / OSS feature flags | API yes | Required combo with trunk-based monolith; agents can read flag state to gate rollouts. |
| PgBouncer | OSS | n/a | Connection pooler — non-negotiable when scaling monolith pods. |
| Datadog APM / New Relic | SaaS APM | API yes | Single-process tracing is trivial — solo monolith gets 80% of value with 20% of microservice obs setup. |
| Sentry | SaaS errors | API yes | Best ROI tool for monolith reliability; agent-callable for triage. |
| GitHub Actions / GitLab CI | SaaS / OSS | yes | Build/test/deploy single-artifact pipeline; agents can scaffold from `templates.md`. |
| Shopify Engineering blog | n/a | n/a | Reference: real production modular monolith at scale. |

## Templates & scripts

`templates.md` already ships Django/FastAPI/Docker/nginx/CI templates. The missing piece is a stub `.importlinter` contract that enforces module boundaries declared in the methodology. Inline drop-in (≤50 lines):

```ini
# .importlinter — enforce modular monolith boundaries.
# Place at repo root, run: lint-imports
[importlinter]
root_packages =
    apps

[importlinter:contract:no-cross-module-imports]
name = Modules talk only via public_api
type = forbidden
source_modules =
    apps.users.internal
    apps.orders.internal
    apps.payments.internal
forbidden_modules =
    apps.users.internal
    apps.orders.internal
    apps.payments.internal
ignore_imports =
    apps.*.public_api -> apps.*.public_api

[importlinter:contract:layered-monolith]
name = Layered architecture
type = layers
layers =
    apps.*.api
    apps.*.domain
    apps.*.infrastructure
containers =
    apps.users
    apps.orders
    apps.payments
```
Wire `lint-imports` into pre-commit + CI; the boundary-checker agent reads this file for what's allowed.

## Best practices
- Pick modular monolith over plain monolith from day 1; the marginal cost is one config file plus discipline.
- Schema-per-module on a single Postgres instance — never share tables across modules; cross-module reads go through `public_api`.
- Pin "no microservices until [explicit metric]" in ADR-0001 (deploy time > 30 min, OR sustained 50+ engineers, OR one feature needs 10× resources).
- Wire `import-linter` / `deptry` / `ArchUnit` into pre-commit hook; methodology mentions them but adoption is the failure point.
- Keep `cmd/` (Go) or `manage.py` style entrypoints thin — orchestration, not logic.
- Pair monolith with trunk-based + feature flags from week 1; monoliths without flags become release-day disasters.
- Track build time + p95 deploy time as first-class SLIs — they are the leading indicators that monolith is outgrowing the team.

## AI-agent gotchas
- Default LLM bias is to over-recommend microservices. Force the agent to read `monolith-architecture/README.md` first and answer "why NOT microservices for this team size?" before any architecture proposal.
- Scaffolding agents tend to skip the `internal/` vs `public_api.py` split. Inspect generated trees and reject any module that exposes its model layer directly.
- Cross-module imports are the #1 silent failure: a one-line "from apps.orders.models import Order" in user code defeats the architecture. Always run `import-linter` after agent edits.
- Agents recommending "extract this to a service" should be required to attach a cost-of-extraction estimate (DB split, cross-service auth, distributed tx) — otherwise the suggestion is cheap talk.
- Long monolith codebases overflow context windows. Use `pyreverse`/`madge` to feed agents module graphs instead of full source.
- Human-in-loop checkpoints: (1) ADR-0001 monolith-first signed by tech lead, (2) any "extract service" PR, (3) any change to schema-ownership rules — these are not reversible without months of work.

## References
- Martin Fowler — Monolith First — https://martinfowler.com/bliki/MonolithFirst.html
- Shopify — Deconstructing the Monolith — https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity
- AWS — Strangler Fig Pattern — https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/strangler-fig.html
- ABP — Modular Monolith Architecture — https://abp.io/architecture/modular-monolith
- import-linter — https://import-linter.readthedocs.io
- ArchUnit — https://www.archunit.org
- Kamal — https://kamal-deploy.org
- Local methodology: `monolith-architecture/README.md`, `templates.md`, `checklist.md`, `examples.md`
