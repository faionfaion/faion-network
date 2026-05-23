# Vision Image Classification & Content Moderation

## Summary

**One-sentence:** Classifies images into predefined categories and detects unsafe content (violence, adult, hate) with severity levels, balancing VLM accuracy with cost on a managed-moderation-API fallback.

**One-paragraph:** Image classification labels images into N predefined categories; content moderation is a specialised classification that detects unsafe content with severity levels. This methodology selects between a managed moderation API (cheap, deterministic, low false-positive on common categories) and a VLM call (expensive, flexible, needed for nuanced categories like context-dependent hate symbols). Always cascade: managed API first, VLM fallback only when confidence is low or category is custom.

**Ефективно для:**

- UGC platforms with >1k uploads/day where 99% are benign and a cheap first pass is mandatory.
- Marketplace product-image classification (50+ custom categories).
- Brand-safety filters where category is context-dependent (hate symbol vs cultural icon).
- Compliance scenarios (CSAM detection) where a hashed-database check must run before any VLM call.

## Applies If (ALL must hold)

- Image stream volume exceeds 100/day.
- Output must be a category label (or unsafe/severity triple), not free-form text.
- False-positive cost is non-trivial (manual review queue exists).

## Skip If (ANY kills it)

- Free-form image description is needed — use vision-accessibility instead.
- Categories change daily — classification needs stable taxonomy.
- Single-image one-shot use — overkill; just call the VLM directly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Image stream | URL/bytes | Upload service or batch import |
| Category taxonomy | YAML | Trust & Safety team output |
| Severity thresholds | config | Policy team output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hash_check` | haiku | PhotoDNA / CSAI-Match lookup; deterministic. |
| `managed_api` | haiku | OpenAI / AWS Rekognition call. |
| `vlm_fallback` | sonnet | VLM only when managed confidence < threshold. |

## Templates

| File | Purpose |
|------|---------|
| `templates/moderation-config.yaml` | Cascade thresholds + category map skeleton |
| `templates/decision-record.md` | Per-image moderation decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-classification-moderation.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[vision-agentic-pipeline]]
- [[vision-document-extraction]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the image hash present in a CSAM database? Branches route to a rule id from `content/01-core-rules.xml` (hash-first, managed-first, vlm-on-low-confidence, ...) so every leaf is traceable to a testable statement.
