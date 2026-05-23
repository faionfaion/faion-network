# Okr Cascade Team To Company

## Summary

**One-sentence:** Produces a one-page-per-team OKR cascade (company KR → team OBJ → team KRs + contribution map + dependencies + alignment sign-off) ready for quarterly review.

**One-paragraph:** Produces a one-page-per-team OKR cascade (company KR → team OBJ → team KRs + contribution map + dependencies + alignment sign-off) ready for quarterly review. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у 8-10 особової продуктової команди — щоб OKR не залишався театром, а ставав маршрутом до company KR.

## Applies If (ALL must hold)

- Team has 8-10 people across ≥2 roles (PM + Eng + Design + Data or similar).
- Company has a published set of OKRs the team can map to.
- Quarterly cadence is the planning rhythm.
- Team lead OR PM owns the cascade and presents at leadership alignment review.

## Skip If (ANY kills it)

- Team < 5 people — KR overhead exceeds value; use direct goal-setting.
- Company has no published OKRs — cascade has nothing to attach to.
- Org uses a different framework (V2MOM, Hoshin Kanri) — adapt to that framework instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Company OKRs | doc/Notion | leadership |
| Team roster + roles | HR export | HRIS |
| Baseline metric values | BI tool / dashboard | data team |
| Cross-team dependency declarations | list | program PMs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/dependency-graph-reasoning` | Cross-team dependency graph the cascade declares against. |
| `geek/pm/project-manager/cross-role-handoff-protocol` | Contribution map handoff stages. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-cascade-page` | haiku | Template fill from company OKR list. |
| `contribution-quantification` | sonnet | Per-KR judgement: 'moves company KR X by Y' band. |
| `alignment-narrative` | opus | Cross-team synthesis for leadership review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | One-page cascade skeleton: company KR + team OBJ + 3-5 team KRs (baseline / target / measure) + contribution map + depends-on + alignment sign-off line. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-okr-cascade-team-to-company.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[dependency-graph-reasoning]]
- [[cross-role-handoff-protocol]]
- [[ai-assisted-velocity-anomaly-detection]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run the cascade (8-10 team + company OKRs + scheduled alignment), block (no company OKRs), or skip (small team). Run before the quarter-start planning week.
