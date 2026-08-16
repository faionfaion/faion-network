# Adobe Firefly Creative Cloud Integration

## Summary

**One-sentence:** Produces an Adobe Firefly + Creative Cloud integration with structured prompt rules and brand-compliance auditing, scoped to the UX/UI designer's CC pipeline.

**One-paragraph:** UX/UI designers running Firefly inside Creative Cloud need a structured prompt taxonomy and brand-compliance audit layer so generated assets stay on-system. This methodology produces a Firefly Services client wired into the CC pipeline, a prompt-rule YAML (brand voice + forbidden + required), and a CI audit job that scans Firefly outputs for brand violations before they enter the asset library. Distinct from the UI-designer methodology by its CC pipeline integration + designer-driven workflow.

**Ефективно для:** UX/UI designer на CC pipeline, що потребує structured prompts + brand audit перед публікацією asset library.

## Applies If (ALL must hold)

- Designer-driven workflow inside Adobe Creative Cloud (Photoshop, Illustrator, InDesign).
- Assets entering a shared library must pass brand audit.
- Firefly Services credentials available.

## Skip If (ANY kills it)

- Workflow is non-designer (engineering batch) — use ui-designer/adobe-firefly-integration.
- Single ad-hoc image — desktop UI is faster.
- Brand audit not required.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Firefly Services API creds | secret | secrets manager |
| Brand voice spec | YAML | brand team |
| Asset library destination | URI | ops |
| CC pipeline config | JSON | design ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[ai-design-assistant-patterns]] | Pattern catalogue for designer-facing AI surfaces. |
| [[ai-enhanced-design-systems]] | DS automation context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-code` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/brand-audit-rules.yaml` | Brand audit rules skeleton (logo / forbidden / colour adherence). |
| `templates/_smoke-test.yaml` | Filled editorial-portrait prompt example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-adobe-firefly-integration.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-design-assistant-patterns]]
- [[ai-enhanced-design-systems]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the code; mis-routing leads to producing the wrong artefact shape.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/brand-audit-rules.yaml`

```yaml
# brand-audit-rules.yaml — Adobe Firefly Creative Cloud Integration
# Fill per task; validator: scripts/validate-adobe-firefly-integration.py

designer_id: design-team:viktoria
prompt: Editorial portrait of older couple in soft daylight, neutral background, brand-token palette.
prompt_taxonomy: {"subject": "older-couple", "style": "editorial", "lighting": "soft-daylight", "composition": "neutral-bg"}
brand_audit_passed: true
library_destination: ccx://library/longlife/2026-05
provenance: {"prompt_hash": "sha256:abc...", "model_version": "v3.2.1", "designer_id": "design-team:viktoria"}
```

### `templates/_smoke-test.yaml`

```yaml
# _smoke-test.yaml — Adobe Firefly Creative Cloud Integration
# Fill per task; validator: scripts/validate-adobe-firefly-integration.py

designer_id: design-team:viktoria
prompt: Editorial portrait of older couple in soft daylight, neutral background, brand-token palette.
prompt_taxonomy: {"subject": "older-couple", "style": "editorial", "lighting": "soft-daylight", "composition": "neutral-bg"}
brand_audit_passed: true
library_destination: ccx://library/longlife/2026-05
provenance: {"prompt_hash": "sha256:abc...", "model_version": "v3.2.1", "designer_id": "design-team:viktoria"}
```
