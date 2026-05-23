# SDD Workflows Navigation Hub

## Summary

**One-sentence:** Generates a phase-route record locating a feature in the SDD lifecycle and pointing to the next phase methodology to apply.

**One-paragraph:** Reads the current state of a feature directory (which docs exist, what their frontmatter status says) and emits a route record naming the current SDD phase (Spec / Design / Execution) plus the next methodology to dispatch. Routes only — does not author spec / design / plan content itself; that work belongs to `workflow-spec-phase`, `workflow-design-phase`, and `writing-implementation-plans` respectively. This file is the dispatcher.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'SDD phase routing' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A feature directory exists under `.aidocs/features/<status>/<feature>/`.
- The caller does not yet know which SDD phase is active and needs routing.
- The caller will dispatch the next-phase methodology after receiving the route.
- The feature is not a single-file bugfix that bypasses SDD entirely.

## Skip If (ANY kills it)

- Caller already knows the phase and target methodology — go directly to it.
- Looking for document templates — use `template-spec`, `template-design`, or `template-task`.
- Feature is too small for SDD (single-file fix, typo, docs-only) — bypass routing.
- Bootstrapping a brand-new project with no `.aidocs/` structure yet — initialize first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature directory path | filesystem path | `.aidocs/features/<status>/<feature>/` |
| Listing of docs in that dir | directory listing | filesystem |
| Frontmatter status fields of each doc | yaml | each `.md` in the dir |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/workflow-spec-phase` | Target methodology when phase resolves to Spec. |
| `solo/sdd/sdd-planning/workflow-design-phase` | Target methodology when phase resolves to Design. |
| `solo/sdd/sdd-planning/writing-implementation-plans` | Target methodology when phase resolves to Plan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the route record + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 4-step procedure: list docs → read statuses → compute phase → emit route | ~600 |
| `content/05-examples.xml` | medium | Worked example: a feature with spec Accepted and no design yet → route to Design | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `list-feature-docs` | sonnet | Mechanical directory enumeration. |
| `read-frontmatter-statuses` | sonnet | Bounded yaml extraction. |
| `compute-route` | sonnet | Phase decision-tree application. |

## Templates

| File | Purpose |
|------|---------|
| `templates/route-record.md` | Canonical phase-route record with current phase, next methodology, and blockers. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-workflows.py` | Validate the route record against the schema in `content/02-output-contract.xml`. | After subagent emits the route, before the caller dispatches the next phase. |

## Related

- [[workflow-spec-phase]]
- [[workflow-design-phase]]
- [[writing-implementation-plans]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (which docs exist, what their statuses are) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about which SDD phase to dispatch.
