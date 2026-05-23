---
slug: team-development
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Builds high-performing teams via Tuckman five-stage staging + co-authored charter + skills matrix + retro synthesis; produces a team-development report with stage diagnosis, gap plan, and named PM actions.
content_id: "72883bf0b8bfe630"
complexity: deep
produces: report
est_tokens: 4400
tags: [team, tuckman, charter, retrospectives, skills-matrix]
---
# Team Development

## Summary

**One-sentence:** Builds high-performing teams via Tuckman five-stage staging + co-authored charter + skills matrix + retro synthesis; produces a team-development report with stage diagnosis, gap plan, and named PM actions.

**One-paragraph:** Talented individuals do not automatically form effective teams: unaddressed Storming calcifies into permanent dysfunction, skills gaps surface mid-project, and retro themes repeat across sprints because nobody synthesises them. This methodology runs four sub-agents — team-charter-builder, retro-synthesiser, tuckman-coach, skills-matrix-analyzer — over named inputs (team list, project context, last-N retros, throughput signals) and emits a typed `TeamDevelopmentReport` with the current Tuckman stage + confidence + evidence, charter draft, skills-gap plan (training/pair/hire), and recurring themes (≥2-sprint evidence). The PM role shifts by stage: directive at Forming, mediating at Storming, delegating at Performing, celebrating at Adjourning.

**Ефективно для:**

- Forming a new team — produce charter, working agreements, RACI + skills matrix in one pass.
- Diagnosing a struggling team — Tuckman stage with confidence + evidence + concrete PM actions.
- Building a skills-gap plan — training vs pairing vs hire (in that order of preference).
- Cross-sprint retro synthesis — themes backed by ≥ 2 sprints, no individual names.

## Applies If (ALL must hold)

- Team size ≥ 2 and a project context with measurable throughput exists.
- The PM has authority to schedule rituals (charter workshop, retros, 1:1s) and act on signals.
- Last N (≥ 2) retro notes are available in markdown, OR a kickoff is happening so retros will start collecting from sprint 1.
- Sensitive content can be redacted before agent processing (no personal names in retro inputs).

## Skip If (ANY kills it)

- Single-person project — no team to develop.
- HR / performance-management decision (compensation, PIP, firing) — escalate to humans + HR system.
- Crisis intervention (harassment, mental health, layoffs) — agents must escalate immediately.
- Cross-cultural mediation where confidentiality dominates — automation backfires.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster | YAML / CSV (name, role, joined) | HR / kickoff sheet |
| Project context | charter.md or one-pager | PM |
| Last N retros | retro_*.md | retro tool export |
| Throughput / cycle-time signal | CSV or DORA report | Jira / Linear / git |
| Skills taxonomy | YAML list | role expectations |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[team-morale-pulse-survey]] | Provides eNPS / workload / clarity signal that feeds Tuckman staging. |
| [[value-stream-management]] | Throughput / cycle-time signals required for stage transition detection. |
| [[work-breakdown-structure]] | WBS supplies the deliverable map skill-matrix gaps map onto. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: confidence-scoring on Tuckman, co-authored charter, owner+deadline on retro actions, no individual naming, ≥2-sprint pattern evidence, training-before-hire | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `TeamDevelopmentReport` + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: "more-standups" reflex, phantom-3 skill scores, retro amnesia, hire-first bias | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: ingest signals → stage → charter → matrix → retro-synth → publish report | ~900 |
| `content/05-examples.xml` | medium | Full worked report: Storming team, charter + matrix + 3 themes + PM action set | ~600 |
| `content/06-decision-tree.xml` | essential | Tree on observable signals (size, signal availability, conflict-shape) → action + rule ref | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `team-charter-builder` | sonnet | Light judgment, structured fill from roster + context. |
| `retro-synthesiser` | sonnet | Cross-sprint pattern judgment, evidence selection. |
| `tuckman-coach` | sonnet | Stage diagnosis with confidence + evidence (multi-signal). |
| `skills-matrix-analyzer` | sonnet | Gap-plan judgment training vs pair vs hire. |
| `redact-individuals` | haiku | Mechanical name stripping before synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/team-charter.md` | Charter skeleton: mission, members, working agreements, cadence, success metrics. |
| `templates/skills-matrix.md` | Role × skill grid (1–4 scale, `?` for unknown) with Gap-Action column. |
| `templates/retro.md` | Went-well / didn't-go-well / ideas / action items (owner + sprint deadline). |
| `templates/_smoke-test.json` | Minimum-viable filled `TeamDevelopmentReport` for validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-development.py` | Validate a `TeamDevelopmentReport` against the JSON Schema | Pre-commit on every report change |

## Related

- [[team-morale-pulse-survey]]
- [[value-stream-management]]
- [[wbs-creation]]
- [[work-breakdown-structure]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (team size, retro corpus depth, throughput shape, conflict signal) to a concrete action — Forming workshop, Storming mediation, gap plan, or escalation — each leaf referencing a rule from `01-core-rules.xml`. Use the tree before deciding which sub-agent to invoke first.
