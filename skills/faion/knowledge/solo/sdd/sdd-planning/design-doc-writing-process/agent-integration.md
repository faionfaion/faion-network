# Agent Integration — Design Document Writing Process

## When to use
- After spec.md is approved and before implementation-plan.md is created
- When codebase patterns need to be discovered before architecture decisions are made
- When the feature touches multiple subsystems and API contracts must be pinned
- Generating ADR-style decisions (AD-X) that executor agents will reference during coding

## When NOT to use
- Features with no new architecture (CRUD on existing model) — copy existing AD patterns directly without a full design process
- Hot-fixes where the solution is already known
- Before spec.md is approved — design without locked requirements causes rework

## Where it fails / limitations
- Phase 2 (codebase research) consumes 20–40k tokens; skipping it produces designs that conflict with existing patterns
- OpenAPI-style documentation in Phase 7 becomes stale quickly if generated early — write contracts after data models are finalized (Phase 6)
- The 7-phase process is sequential by design; agents that skip phases (especially Phase 3, the traceability matrix) produce designs where some FR-X have no implementing AD

## Agentic workflow
A design agent runs Phases 1–3 in a single pass (context loading + codebase research + traceability matrix), then pauses for human review of the FR coverage table. After approval, it runs Phases 4–7 to produce architecture decisions, file structure, data models, and API contracts. This two-turn structure prevents the agent from committing to contracts before understanding existing patterns.

The research in Phase 2 is the most valuable subagent task: it can run in parallel across multiple modules using Glob/Grep, then feed findings into the AD drafting pass.

### Recommended subagents
- `faion-sdd-executor-agent` — can execute Phase 2 (codebase research) as a standalone read-only pass before the design agent writes anything
- General Claude subagent (Opus) — for Phase 4 (architecture decisions) where trade-off reasoning matters
- General Claude subagent (Sonnet) — for Phase 5–7 (file structure, data models, API contracts) from established patterns

### Prompt pattern
```
Phase 1-3: Read constitution.md, spec.md, and existing done/ features.
Build a traceability matrix: every FR-X maps to at least one AD-X candidate.
Output only the matrix — do not write ADs yet.
```

```
Phase 4-7: Given this traceability matrix and codebase research,
write design.md sections: Architecture Decisions (ADR format), File Changes table,
Data Models (TypeScript types + SQL schema), API Contracts (OpenAPI-style).
Every AD must reference the FR-X it satisfies.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ripgrep` (`rg`) | Phase 2 pattern discovery across codebase | `apt install ripgrep` |
| `adr-tools` | Generate and index ADR files from command line | https://github.com/npryce/adr-tools |
| `openapi-generator` | Scaffold code from API contracts defined in Phase 7 | https://openapi-generator.tech |
| `schemaspy` | Visualize DB schema after Phase 6 models are defined | https://schemaspy.org |
| `sqlfluff` | Lint SQL migration scripts from Phase 6 | `pip install sqlfluff` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight | SaaS | Yes (REST API) | Design-first API; sync OpenAPI spec from Phase 7 |
| Swagger Hub | SaaS | Yes (REST API) | Host and validate OpenAPI contracts; free tier available |
| Structurizr | OSS/SaaS | Partial | C4 diagrams from code; useful for Phase 5 architecture visualization |
| dbdiagram.io | SaaS | No API | Manual input; useful for Phase 6 schema review with stakeholders |

## Templates & scripts
See `templates/README.md` → Constitution Template and Implementation Plan Template for the artifacts that design.md feeds into.

Phase 2 helper — find all service/handler patterns in a codebase:
```bash
#!/usr/bin/env bash
# find-patterns.sh SRC_DIR
SRC=${1:-.}
echo "=== Services ==="
rg --type ts --type py -l "class.*Service" "$SRC" | head -20
echo "=== Controllers/Handlers ==="
rg --type ts -l "class.*Controller|export.*Router|@app.route" "$SRC" | head -20
echo "=== Models ==="
rg --type py -l "class.*Model\)" "$SRC" | head -20
echo "=== Existing migrations ==="
find "$SRC" -name "*.sql" -o -name "*migration*" | head -20
```

## Best practices
- Always run Phase 2 (codebase research) before writing any AD — naming and structural decisions must match the existing codebase
- Each AD must declare its alternatives with explicit rejection reasons; future agents need to understand why a path was NOT taken
- Keep the traceability matrix (Phase 3) as a living section in design.md — update it when ADs are added
- API contracts (Phase 7) should include error responses for every 4xx and 5xx case; executor agents generate incomplete error handling when contracts are vague
- Separate concerns: data model decisions (AD-Data) and API contract decisions (AD-API) should be distinct ADs so they can be implemented in separate tasks

## AI-agent gotchas
- Agents skip Phase 2 when under context pressure — explicitly require a codebase research section in the design.md output or it will not happen
- "Alternatives Considered" tables are frequently fabricated; validate that alternatives listed were actually considered against real constraints
- Phase 7 API contracts generated without real validation rules (field types, lengths, required flags) produce executor tasks that implement incomplete validation
- Design docs written without reading `constitution.md` violate tech stack decisions — always load constitution first and cite it in ADs
- Human approval of design.md is required before creating TASK_*.md files — automatic continuation is a common agent failure mode

## References
- https://opensource.zalando.com/restful-api-guidelines/ — Zalando REST API guidelines
- https://refactoring.com/catalog/ — Martin Fowler refactoring catalog
- https://martinfowler.com/eaaCatalog/ — Patterns of Enterprise Application Architecture
- https://github.com/npryce/adr-tools — ADR tooling
- https://c4model.com — C4 model for software architecture diagrams
