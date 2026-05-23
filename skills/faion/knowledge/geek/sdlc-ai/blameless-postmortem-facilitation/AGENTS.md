---
slug: blameless-postmortem-facilitation
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Facilitation playbook for blameless postmortems: timeline reconstruction, contributing-factor analysis, action items with owners + deadlines, distributed-only language enforcement.
content_id: "43f7b5395884835e"
complexity: deep
produces: report
est_tokens: 4800
tags: [incident, postmortem, blameless, sre, sdlc-ai]
---
# Blameless Postmortem Facilitation

## Summary

**One-sentence:** Facilitation playbook for blameless postmortems: timeline reconstruction, contributing-factor analysis, action items with owners + deadlines, distributed-only language enforcement.

**One-paragraph:** Most postmortems devolve into either blame-the-individual or vague-platitudes. Blameless postmortems are a discipline: facilitator-guided, evidence-led, with a strict language convention (no 'should have', no individual names in cause text, contributing factors not root causes). This methodology codifies the facilitation script — timeline from observed events, contributing-factor tree, action items with owner + deadline + verifier, language-lint pass — and emits a report that audit can trust without a re-litigation cycle.

**Ефективно для:**

- Incident severity is SEV2 or worse, or customer impact is sustained ≥30 min.
- Team operates a no-blame culture (or wants to install one and has leadership backing).
- An on-call responder owns the postmortem and a separate facilitator runs the session.

## Applies If (ALL must hold)

- Incident severity is SEV2 or worse, or customer impact is sustained ≥30 min.
- Team operates a no-blame culture (or wants to install one and has leadership backing).
- An on-call responder owns the postmortem and a separate facilitator runs the session.

## Skip If (ANY kills it)

- Incident was a planned drill / chaos game-day — different framing applies.
- Severity is SEV4+ self-healing — handled by async note, not full postmortem.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident timeline raw | json | PagerDuty / on-call log + chat archive |
| Service catalog | yaml | Team `services.yaml` |
| Postmortem template | md | Repo at `docs/postmortem-template.md` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-blameless-postmortem-facilitation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/postmortem.md` | Postmortem markdown skeleton |
| `templates/language-lint-rules.txt` | Forbidden phrase list |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blameless-postmortem-facilitation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
