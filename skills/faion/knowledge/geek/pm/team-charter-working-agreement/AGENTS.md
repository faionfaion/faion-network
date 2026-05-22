---
slug: team-charter-working-agreement
tier: geek
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "194a41a24e76350a"
complexity: medium
produces: spec
est_tokens: 3000
summary: Produces a 1-page team charter (mission, decision rights, working hours, AI-tool policy, code-review SLA, on-call rotation) so a product team scaling past 5 people stops re-litigating norms every sprint.
tags: [pm, geek, team-charter, working-agreement, decision-rights, scaling]
---
# Team Charter Working Agreement

## Summary

**One-sentence:** Produces a 1-page, versioned, owner-signed team charter (mission, decision rights, working hours, AI-tool usage policy, code-review SLA, on-call rotation) so a product-dev team scaling past 5 people stops re-litigating norms every sprint.

**One-paragraph:** `team-development` literature covers Tuckman stages but ships no concrete artefact teams can actually adopt. The single most-cited missing doc on YC / HN threads about scaling product teams past 5 people is a one-page working agreement covering mission, decision rights, working hours, AI-tool usage policy, code-review SLA, and on-call rotation. This methodology pins that artefact's shape: bounded single-instance scope (per team, per chapter), typed inputs with source citations, a named human owner, semver + last_reviewed, and every section anchored to the specific gap it closes. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans consume without re-deriving rationale.

**Ефективно для:** tech lead / EM, який скейлить продуктову команду з 5 до 15 людей і вже втомився відповідати на питання "як ми тут вирішуємо" вдесяте.

## Applies If (ALL must hold)

- Team is scaling past 5 people OR multiple chapters need an aligned baseline.
- Operator has the artefacts named in Prerequisites before starting.
- Output will be consumed by a downstream agent or human reviewer (not discarded).
- A named human owner exists for the charter.

## Skip If (ANY kills it)

- The team already maintains a working team charter — replace, do not duplicate.
- The change is a greenfield prototype with no production users.
- Regulatory / compliance context overrides in-methodology guidance (defer to legal).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Recent context for the scaling decision | doc / retro notes | last 30 days team channel |
| Write-access to the artefact store | repo / wiki | team SDD space |
| Named owner | role + person | team roster |
| Existing tribal norms (verbal) | interview notes | onboarding shadow sessions |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | Provides operating context for the charter's decision-rights section. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; charter lives in the team's SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound-scope, typed-input, named-owner, versioned, grounded-in-rationale | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Single-instance gate + ownership branch | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation. |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/team-charter-working-agreement.json` | JSON schema for the charter output contract. |
| `templates/team-charter-working-agreement.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-charter-working-agreement.py` | Enforce charter output contract (owner is a person, version is semver, every section cites the gap it closes). | After subagent returns, before downstream consumer reads. |

## Related

- [[ramp-task-difficulty-ladder]] — peer operating artefact for the same scaling team.
- [[vendor-risk-assessment-template]] — sibling versioned-artefact methodology that shares the same envelope.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks single-instance scope and a named human owner. If the team is batching multiple unrelated norm decisions → split first. If owner is "team" or empty → block until a person is named. Otherwise → emit the charter using the rule set.
