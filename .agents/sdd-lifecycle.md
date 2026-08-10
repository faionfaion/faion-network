# SDD Lifecycle

Full directory documentation: [../docs/directory-structure.md](../docs/directory-structure.md).

**Feature lifecycle:** `backlog/ → todo/ → in-progress/ → done/`
**Task lifecycle (inside a feature):** `todo/ → in-progress/ → done/`

## Document types

- **constitution.md** — tech decisions, standards, architecture. Declares the per-project `project-spec/` location.
- **roadmap.md** — feature timeline, releases, success metrics.
- **project-spec/** — per-project source-of-truth folder (domain, business rules, data model, deploy, invariants). See the `project-spec-structure` methodology.
- **spec.md** — what to build (requirements, success criteria); delta-only when `project-spec/` exists.
- **plan.md** — merged design + implementation plan; exactly two H2 sections: `## Design` + `## Execution Plan`. See the `plan-md-structure` methodology.
- **user-flows.md** — per-feature, REQUIRED only when a user-facing flow exists. See `user-flows-template`.
- **ui-ux-design.md** — per-feature, REQUIRED only when UI is touched. See `ui-ux-design-template`.
- **readiness.md** — gate before moving a feature to `done/`. See `readiness-checklist`.

`project-spec/` location is declared per-project in that project's `constitution.md`.

The retired quartet — `design.md`, `test-plan.md`, `implementation-plan.md` alongside `spec.md` — is rejectable output. `plan.md` replaces design + implementation plan.

## CR / BUG side streams

- **crs/{todo,done}/CR0NN-slug.md** — change requests; lighter than features. See `cr-bug-tracking`.
- **bugs/{todo,in-progress,done}/BUG0NN-slug.md** — defects with repro + regression test. See `cr-bug-tracking`.

## No time estimates

Never state a duration for task execution in the SDD workflow.

- Not allowed: "This will take 2 hours", "Estimated duration: 3 days", "Should be done in 30 minutes".
- Allowed: "Task complexity: High" (qualitative), "Est. tokens: ~50k" (resource-based).

Why: time estimates are unreliable and create false expectations. Use complexity levels and token estimates instead.

In documents: `plan.md` carries no `estimated_duration` field; `TASK_*.md` uses token estimates only; `roadmap.md` uses phases and milestones rather than dates where possible.

## SDD memory

Project-local, not global:

```
.aidocs/memory/
├── patterns.md           # Learned patterns
├── mistakes.md           # Errors and solutions
├── decisions.md          # Key decisions
└── session.md            # Session state
```

Memory updates sync to the project `CLAUDE.md` automatically.

## Token efficiency

Symbols: `→` leads to · `⇒` transforms.
Abbreviations: `cfg` config · `impl` implementation · `perf` performance · `sec` security · `dep` dependency.
