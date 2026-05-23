---
slug: xp-extreme-programming
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an XP-readiness checklist scoring a team / repo on the 12 XP practices (TDD, pair programming, CI, small releases, YAGNI, refactor, collective ownership, simple design, sustainable pace, metaphor, planning game, on-site customer).
content_id: "09561b55db549aca"
complexity: medium
produces: checklist
est_tokens: 3700
tags: [extreme-programming, agile, tdd, pair-programming, continuous-integration]
---
# Extreme Programming (XP)

## Summary

**One-sentence:** Scores a team / repo against the 12 XP practices and emits a readiness checklist with per-practice fixes; the "Done" rule (tests pass, no TODOs, CHANGELOG updated) becomes a mechanical gate.

**One-paragraph:** XP packages a coherent set of agile practices that compose well — TDD pairs with refactor; pair programming substitutes for async code review; CI makes small releases safe. Adopting XP partially often fails (TDD without CI yields broken trunk; pair without sustainable pace burns out the pair). This methodology scores each of the 12 practices, surfaces the missing pillars, and proposes a phased adoption order: tests + CI first (substrate), then small releases + refactor, then pair + collective ownership. Output: a readiness checklist artefact + a Done-definition that the team's PR template enforces.

**Ефективно для:**

- Solo dev / small team pitching XP adoption against a "just ship" culture.
- Outsource lead introducing XP into a new client engagement.
- AI-pair coding teams — pair programming subsumes async code review when the pair is human+AI.
- Engineering manager scoring "are we actually agile" against a known framework.

## Applies If (ALL must hold)

- Team / solo dev wants to adopt agile practices coherently rather than piecemeal.
- Test + CI substrate exists OR will be built first.
- Release cadence can be weekly or better.
- Team is colocated, async-disciplined, OR pair-pair-program with AI.

## Skip If (ANY kills it)

- Heavily regulated env mandating a different process (FDA, aviation) — defer to regulator's framework.
- Long-cycle research project where small releases don't make sense.
- Hostile-to-process culture — escalate organisational issue first.
- Adoption has been tried + rolled back in last 12 months — investigate why first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test coverage report | report | CI |
| CI pipeline definition | YAML | repo |
| Release cadence | doc | team handbook |
| Sprint / iteration structure | doc | team handbook |
| Pair-programming logistics (or AI-pair) | doc | team handbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-dev-principles` | TBD is the branching substrate for XP's small releases. |
| `solo/dev/ci-quality-gate-design` | CI gates that enforce the Done rule. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ rules: 12 practices, Done definition, phased adoption, sustainable pace, no piecemeal, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the readiness checklist + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: cargo-cult-pair, TDD-without-CI, no-sustainable-pace, missing-Done | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: assess → adopt-substrate → adopt-flow → adopt-craft → review | 700 |
| `content/06-decision-tree.xml` | essential | Tree: substrate ready? → adopt phase 1/2/3 → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-practice` | sonnet | Per-practice judgment based on repo + handbook signals. |
| `phase-recommendation` | sonnet | Pick next-phase practice given the score vector. |
| `done-gate-wiring` | haiku | Mechanical CI gate matching the Done rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/xp-extreme-programming.json` | JSON Schema for the readiness checklist. |
| `templates/done-definition.md` | Done rule snippet for PR template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-xp-extreme-programming.py` | Validate readiness JSON against schema + adoption-phase rule. | After scoring; quarterly review. |

## Related

- [[trunk-based-dev-principles]] — TBD is the branching substrate XP small-releases depends on.
- [[ci-quality-gate-design]] — Done gate joins the CI design.
- [[characterization-test-recipes]] — TDD on legacy = characterization tests first.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks substrate (tests + CI + release cadence). If substrate missing → phase 1 only (build substrate). If substrate present → phase 2 (flow: small releases, refactor, YAGNI). If flow stable → phase 3 (craft: pair programming, collective ownership, metaphor). Leaves emit `phase-1`, `phase-2`, `phase-3`, `block-substrate-missing`, or `block-org-hostile`. Each leaf references a rule in `01-core-rules.xml`.
