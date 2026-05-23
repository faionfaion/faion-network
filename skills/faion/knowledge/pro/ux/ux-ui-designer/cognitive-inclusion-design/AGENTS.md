---
slug: cognitive-inclusion-design
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a cognitive-inclusion spec covering chunking, predictability, progress indicators, focus mode, dyslexia font, reduced motion, and extended time limits for users with ADHD, autism, dyslexia, dyscalculia, anxiety, low literacy, and aging cognition.
content_id: "b624b9cb2ede6877"
complexity: medium
produces: spec
est_tokens: 4400
tags: [accessibility, cognitive, inclusion, adhd, autism, dyslexia]
---
# Cognitive Inclusion Design

## Summary

**One-sentence:** Produces a cognitive-inclusion spec covering chunking, predictability, progress indicators, focus mode, dyslexia font, reduced motion, and extended time limits for users with ADHD, autism, dyslexia, dyscalculia, anxiety, low literacy, and aging cognition.

**One-paragraph:** Cognitive inclusion is a design discipline that reduces working-memory load and adapts UI for neurodiverse users via structural patterns (chunking, predictability, progress indicators, escape hatches) and optional user settings (focus mode, dyslexia font, reduced motion, extended time limits, simplified language). The spec lists every pattern and every setting with its WCAG SC mapping and a measurable adoption metric.

**Ефективно для:**

- Продукти з критичним онбордингом / long forms — chunking + progress.
- ADHD/autism/dyslexia/low-literacy аудиторії — opt-in адаптації.
- Уникнути silent timeout / sudden motion — extended-time + reduced-motion.
- Plain-language переключувач для регульованих індустрій (health/finance/gov).

## Applies If (ALL must hold)

- Product surfaces a flow with >3 sequential steps, deadlines, or sustained attention.
- Audience includes users with ADHD, autism, dyslexia, dyscalculia, anxiety, or low literacy.
- Designer has authority to add user settings (not just visual polish).

## Skip If (ANY kills it)

- Single-shot transactional UI (e.g. one-button payment) — patterns unnecessary.
- B2B power-user tool where 'verbose simplification' would slow expert workflows.
- Embedded widget with no settings surface — different methodology applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Flow inventory | step list | product brief |
| Audience cognitive profile | personas with traits | research |
| Plain-language reading-level target | Flesch-Kincaid grade | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[accessibility-first-design]] | Visual contrast/motion tokens this builds on |
| [[personas]] | Cognitive profile sourced from research personas |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cognitive-inclusion-spec.md` | Surface-by-surface cognitive inclusion spec with patterns + settings + WCAG mapping |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cognitive-inclusion-design.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[accessibility-first-design]]
- [[wcag-22-compliance]]
- [[error-handling-in-vui]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
