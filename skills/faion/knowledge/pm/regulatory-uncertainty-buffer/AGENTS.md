# Regulatory Uncertainty Buffer

## Summary

**One-sentence:** A typed decision rule that converts regulatory uncertainty (EU AI Act, GDPR, DSA, MiCA, US state privacy laws) into a numeric buffer — engineering hours + budget contingency + go/no-go thresholds — backed by recorded-call evidence per decision.

**One-paragraph:** Regulatory uncertainty is treated as "we'll figure it out" until the engagement is mid-delivery and a regulator finding lands. This methodology pins inputs + published thresholds: each regulation produces a `RegulatoryBuffer` record with (a) named jurisdiction + regulation + signal, (b) numeric threshold (e.g., "high-risk AI per Annex III" → +30% engineering buffer), (c) default action (proceed / pause / escalate to legal), (d) recorded-call evidence anchor (transcript, regulator letter, counsel opinion), (e) review_on_failure trigger so every miss updates the rule. Outputs are versioned and feed downstream cost models + sponsor conversations.

**Ефективно для:**

- Fixed-price vs T&M estimation for AI / GDPR / DSA / MiCA-touching engagements.
- Sponsor conversation: "we add X% buffer because thresholds A/B fire".
- Quarterly review: misses update thresholds; hits prune unused ones.
- Recording defensible decisions for legal audit.

## Applies If (ALL must hold)

- Project touches regulated material (PII, AI, payments, health, content moderation).
- Counsel access exists (in-house, external, or association).
- PM has authority to set + apply buffer in estimates.
- Recorded-call infrastructure exists (transcripts / signed memos).

## Skip If (ANY kills it)

- Out-of-scope: pure internal tools with no PII / regulated flow.
- Regulator-mandated framework already in place — adopt it.
- < 3 regulated projects per year — bespoke memos cheaper than rule-driven.
- No counsel access — escalate to legal first, methodology second.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Regulation register | YAML | counsel |
| Counsel opinions / regulator letters | PDF / Markdown | legal |
| Recorded-call evidence | transcript URL | meeting tool |
| Previous quarter buffer outcomes | JSON | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rag-policy-thresholds]] | Regulatory signals feed amber/red colour transitions. |
| [[proposal-red-team-checklist]] | Buffers feed the `Estimation & Buffers` pause-point. |
| [[rpo-rto-negotiation-guide]] | Regulated systems often mandate RPO/RTO floor; buffer applies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named inputs, published thresholds, default action, recorded call, review on failure | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `RegulatoryBuffer` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, example-text leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: identify regulations → set thresholds → record evidence → apply buffer → quarterly review | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: jurisdiction + signal vs threshold → buffer % / pause / escalate-to-legal | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `regulation-identifier` | sonnet | Jurisdiction + scope judgment. |
| `threshold-setter` | sonnet | Per-regulation numeric buffer with counsel evidence. |
| `apply-buffer` | haiku | Mechanical addition to estimate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | RegulatoryBuffer skeleton with default jurisdictions |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `RegulatoryBuffer` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-regulatory-uncertainty-buffer.py` | Validate `RegulatoryBuffer`: named inputs, numeric thresholds, recorded-call evidence, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag policies whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[rag-policy-thresholds]]
- [[proposal-red-team-checklist]]
- [[rpo-rto-negotiation-guide]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps jurisdiction + signal to buffer % / pause / escalate-to-legal. Every leaf references a rule from `01-core-rules.xml`.
