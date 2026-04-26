# Agent Integration — Django Code Decision Tree

## When to use
- Adding new functionality to a Django app and an agent needs a deterministic answer to "where does this code go?"
- Refactoring a fat view or fat model into clean layers (views → services → utils → models).
- Code review: an agent diffs a PR and flags any business logic in views, ORM calls in utils, or HTTP-aware code in services.
- Onboarding a newly-spun-up agent (or human) into a Django project — the tree is read first to align on conventions.

## When NOT to use
- Tiny Django apps (single-file `views.py`, no business logic) — adding services/ and utils/ folders just for ceremony hurts clarity.
- Non-Django Python projects (FastAPI, Flask, plain CLIs) — the layer names mostly transfer but the rationale (DRF serializers, Django ORM coupling) does not.
- Projects already on a different convention (DDD with bounded contexts, hexagonal, Clean Arch) — converting partway leaves a mess; either fully adopt or leave alone.
- DRF-only API microservices where serializers double as use-cases — splitting services from serializers is overkill.

## Where it fails / limitations
- Boundary creep: an agent unsure between `services/` and `utils/` will put pure helpers in services because "it touches a model" — slows tests and balloons services into a god module.
- The tree is silent on cross-app dependencies. Two apps both importing each other's services produces import cycles the tree doesn't catch.
- Signals and Django middleware aren't represented well; agents tend to dump signal handlers into `signals.py` without thinking about reentrancy.
- The decision tree assumes one app == one bounded context. Large apps (`apps/orders/` with 30 models) need internal sub-decomposition the tree doesn't describe.
- When ORM access is unavoidable inside utils (e.g., a tax calculation that reads a Country row), the tree forces awkward signature passing of pre-loaded values.

## Agentic workflow
A planning agent maps each acceptance criterion to a layer (view/service/util/model). An implementation agent writes code per-layer with import constraints enforced (utils may not import models; services may not import views). A code-review agent runs `import-linter` or a custom AST walker to verify directionality and rejects the PR on violations. The decision tree itself is encoded as a `.aidocs/decisions/code-placement.md` constitution that every agent reads before mutating Django code.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the placement decision per-task; constitution.md anchors the rule set.
- A purpose-built `architecture-linter` subagent — runs after each commit, walks imports, enforces "views → services → utils" direction.
- `password-scrubber-agent` — orthogonal but useful: ensures no secrets land in service-layer code that gets logged.

### Prompt pattern
```
Use the Django decision tree (free/dev/software-developer/django-decision-tree).
For the change <summary>, list every new function and its target file path
(views/services/utils/models/serializers/tasks/integrations). Justify each.
Stop. Do not write code yet.
```
```
Audit <app>/. For each function: (1) which layer, (2) does it match the
decision tree, (3) if not, propose new path. Output: original_path,
proposed_path, reason.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `import-linter` | Enforce layer dependency direction | `pip install import-linter` · https://import-linter.readthedocs.io/ |
| `pydeps` | Generate import graphs | `pip install pydeps` |
| `tach` | Modular boundary enforcement (Rust-fast) | `pip install tach` · https://gauge-sh.github.io/tach/ |
| `ruff` | `flake8-tidy-imports` rules; `RUF` checks for layer hints | `pip install ruff` |
| `dependency-cruiser` (JS sibling) | If the project also has a JS frontend | `npm i -D dependency-cruiser` |
| `django-extensions` | `graph_models` for ORM diagrams | `pip install django-extensions` |
| `bandit` | Security checks per-layer (e.g., utils shouldn't shell out) | `pip install bandit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Run import-linter / tach on every PR. |
| Sourcegraph | SaaS | Yes | Cross-repo enforcement of layer rules; good for monorepos. |
| Sigrid / CodeScene | SaaS | Yes | Trend analysis — flag growing god services. |
| ArchUnit (Java sibling) | OSS | n/a | Inspiration for what import-linter should be. |

## Templates & scripts
See `templates.md` for full layer scaffolds. Inline import-linter contract:

```toml
# .importlinter
[importlinter]
root_package = apps

[[importlinter.contracts]]
name = "views must not be imported by services or utils"
type = "forbidden"
source_modules = [
  "apps.*.services",
  "apps.*.utils",
  "apps.*.tasks",
]
forbidden_modules = ["apps.*.views"]

[[importlinter.contracts]]
name = "utils must not import Django ORM"
type = "forbidden"
source_modules = ["apps.*.utils"]
forbidden_modules = ["django.db", "apps.*.models"]
```

## Best practices
- Make the tree a constitution doc the agent re-reads on every Django task; do not hope it remembers across sessions.
- Use a `services/` package (folder), not a single `services.py` — split per-domain (`orders.py`, `inventory.py`) so file size stays under 300 lines.
- Wrap multi-step service ops in `transaction.atomic`; agents that forget this produce partially-applied state on errors.
- Keep `utils/` 100% pure — no `models`, no `requests`, no `time.sleep`. Easier to test, easier for agents to refactor.
- `integrations/` for third-party API wrappers; never call `requests.post()` directly from `services/` — agents lose mockability.
- Views: only request parsing and response shaping. Push validation into serializers, business logic into services.
- Background work: any task that takes >100ms or has retries goes to `tasks/` (Celery / RQ / Dramatiq), not inline.
- Two apps that import each other → extract shared code to `core/` or `common/`. The tree's "Reusable across apps" branch is non-negotiable.
- Don't let the tree decay: encode it in `import-linter` and run on every PR.

## AI-agent gotchas
- LLMs default to fat views ("just put it in the view, simpler"). Override with system prompt: "All DB writes go to services/. Views are < 30 lines."
- "Service" is overloaded — agents will name a class `OrderService(models.Manager)` when really they want a function. Prefer module-level functions in services/ over service classes.
- Agents often drop `@transaction.atomic` on cross-model writes. Add a lint rule: any service function that calls `.objects.create()`/`.save()` ≥2 times must be `@atomic`.
- Cycle imports between `services/` and `models/` (when models call into services for derived fields). Push computation into `utils/` or use signals carefully.
- Helpers with side effects ("save user audit log") look pure but aren't — agents place them in utils, breaking the layering. Add a Bandit/Ruff rule against `utils/` importing the logger or DB.
- DRF serializers with `create()`/`update()` methods are services in disguise. Either keep them thin and delegate to services, or accept that serializers double as service-layer for that endpoint — pick one and document.
- `@override` is rarely used; agents inheriting from BaseModel/BaseService often shadow methods unintentionally. Use `mypy --strict` + `pyright` to catch shadowing.
- Decision-tree skew across apps: each app uses a different layout because no agent enforces the rule globally. Run `tach check` in CI.

## References
- https://import-linter.readthedocs.io/ — enforce dependency rules
- https://gauge-sh.github.io/tach/ — modern Rust-based variant
- https://docs.djangoproject.com/en/stable/topics/db/transactions/ — atomic semantics
- https://www.cosmicpython.com/ — "Architecture Patterns with Python" (Percival & Gregory) — the canonical book on this style
- https://martinfowler.com/eaaCatalog/serviceLayer.html — Fowler on Service Layer
- https://github.com/HackSoftware/Django-Styleguide — HackSoft's well-known Django service-layer style
