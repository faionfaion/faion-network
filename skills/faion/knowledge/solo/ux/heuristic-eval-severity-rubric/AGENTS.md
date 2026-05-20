---
slug: heuristic-eval-severity-rubric
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "37cfe6af0d64c638"
summary: "Heuristic Eval Severity Rubric — testable methodology for design, research, accessibility, severity. Nielsen's heuristics methodology lacks a 0–4 severity rubric with calibrated examples; without it, ratings drift between designers."
tags: [ux, solo, methodology]
---
# Heuristic Eval Severity Rubric

## Summary

**One-sentence:** Heuristic Eval Severity Rubric — testable methodology for design, research, accessibility, severity. Nielsen's heuristics methodology lacks a 0–4 severity rubric with calibrated examples; without it, ratings drift between designers.

**One-paragraph:** Heuristic Eval Severity Rubric closes a known gap in ux practice: Nielsen's heuristics methodology lacks a 0–4 severity rubric with calibrated examples; without it, ratings drift between designers. The methodology is anchored to the recurring activity 'Heuristic evaluation on a new screen (1hr) (role: role-ux-ui-designer)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Heuristic evaluation on a new screen (1hr) (role: role-ux-ui-designer)' shows up in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems, dashboards, or transcripts that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `heuristic_eval_severity_rubric_template_fill` | haiku | Template fill, no judgement |
| `heuristic_eval_severity_rubric_evidence_check` | sonnet | Bounded comparison + judgement |
| `heuristic_eval_severity_rubric_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `solo/ux/` (see neighbouring methodologies)
- triggering activity: `Heuristic evaluation on a new screen (1hr) (role: role-ux-ui-designer)`
- external: industry references cited inline in `content/01-core-rules.xml`
