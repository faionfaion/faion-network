---
slug: inc-postmortem-auto-draft-no-publish
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: AI agent assembles a postmortem first draft (timeline, contributing factors, action item placeholders) within 2h of incident close; humans review and only humans publish.
content_id: "f64a38309f06d564"
complexity: medium
produces: report
est_tokens: 4400
tags: [incident, postmortem, ai-drafting, human-review, sdlc-ai]
---
# Auto-Draft Postmortem, No Auto-Publish

## Summary

**One-sentence:** AI agent assembles a postmortem first draft (timeline, contributing factors, action item placeholders) within 2h of incident close; humans review and only humans publish.

**One-paragraph:** AI agents are excellent at synthesising incident-channel transcripts, alerts, dashboards, and rollback PRs into a postmortem first draft — and terrible at deciding what's politically safe to publish. This methodology lets the agent assemble the draft within 2 hours of incident close, mark every claim with its evidence source, surface contributing factors as candidates, and STOP. Humans review, edit, and publish. Output is a draft postmortem with a hard `published=false` flag until a named human signs off.

**Ефективно для:**

- Team runs incident response with structured channels (PagerDuty + Slack + dashboards + rollback PRs).
- Postmortems are required for SEV2+ incidents and the writing burden is a blocker to publication.
- There is appetite for AI assistance with human-in-the-loop control.

## Applies If (ALL must hold)

- Team runs incident response with structured channels (PagerDuty + Slack + dashboards + rollback PRs).
- Postmortems are required for SEV2+ incidents and the writing burden is a blocker to publication.
- There is appetite for AI assistance with human-in-the-loop control.

## Skip If (ANY kills it)

- Incident lacks structured artifacts (no on-call log, no chat archive) — agent has nothing to synthesise.
- Team has no postmortem culture / no SEV definitions — install the culture first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident channel archive | json | Slack export / Teams archive |
| PagerDuty timeline | json | PD incident API |
| Dashboards URLs | yaml | Service catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-inc-postmortem-auto-draft-no-publish` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/postmortem-draft.md` | Draft skeleton with placeholders + flags |
| `templates/draft-metadata.json` | JSON metadata sibling to draft |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inc-postmortem-auto-draft-no-publish.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
