---
slug: tracker-ai-triage-classify-route
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a six-step triage pipeline (classify → severity → dedupe → label → CODEOWNERS-route → load-balance) that pre-processes inbound issues before any human picks them up.
content_id: "764955b90b9e20ad"
complexity: deep
produces: config
est_tokens: 4200
tags: [triage, issue-tracker, ai-agent, classification, routing]
---
# AI Triage, Classify, and Route Inbound Issues

## Summary

**One-sentence:** Pipe every inbound bug or request through a six-step triage agent: classify type, score severity with SLA, dedupe by cosine similarity, apply /area/component/lang labels, route to CODEOWNERS team, assign least-loaded engineer.

**One-paragraph:** Pipe every inbound bug or request through a six-step triage agent before any human picks it up: classify type (bug/story/epic/task/spike), score severity with an attached SLA timer (blocker/critical/major/minor), dedupe against the last 1000 issues by title+body cosine similarity, apply `/area/*`, `/component/*`, `/lang/*` labels, route to the CODEOWNERS-derived team, and assign to the least-loaded engineer on that team. Severity = blocker MUST require an on-call confirmation before the SLA timer arms; everything else is auto-routed. The agent emits a single comment listing every classification it applied so the assignee can dispute any field with one reaction.

**Ефективно для:**

- High-volume tracker, де human triage стає bottleneck.
- Multi-team monorepo з CODEOWNERS as source-of-truth.
- Compliance: SLA timers + audit comment per issue.
- Load-balancing fleet of engineers — fair assignment.

## Applies If (ALL must hold)

- Issue tracker with ≥ 100 open issues and ongoing inbound volume.
- CODEOWNERS file exists and is maintained.
- Team has an on-call rotation for confirming blocker severity.

## Skip If (ANY kills it)

- Tiny project with < 20 issues — triage by hand is faster.
- No CODEOWNERS / team mapping available.
- Cultural resistance to AI-applied labels (review burden outweighs throughput gain).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CODEOWNERS file | text | repo root |
| On-call schedule API | REST endpoint | Opsgenie / PagerDuty |
| Engineer load metric source | API | internal dashboard |

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
| `templates/triage-pipeline.yaml` | YAML config for the six-step triage pipeline (classify/severity/dedupe/label/route/assign). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tracker-ai-triage-classify-route.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-agent-fixable-triage-gate]]
- [[tracker-github-copilot-workspace]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
