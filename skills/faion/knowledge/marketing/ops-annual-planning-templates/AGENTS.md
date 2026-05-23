# Annual Planning Templates

## Summary

**One-sentence:** Annual planning template pack spec: Annual Plan, Quarterly Review, Annual Review, Monthly Plan, OKR template, Year-in-Review — content scaffolds that agents fill only with grounded data.

**One-paragraph:** Annual Planning Templates pins the discipline that turns this workflow from tribal knowledge into a reviewable, owned, version-controlled operating artefact. The methodology constrains input shape, output shape, evidence anchors, and named ownership; the JSON Schema in `content/02-output-contract.xml` drives a stdlib validator at commit time. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without a named owner are tagged stale. The artefact lives in the team's versioned space and is refreshed on a stated cadence.

## Applies If (ALL must hold)

- The team operates the system the methodology targets (`ops-annual-planning-templates` scope).
- A named human owner is available to sign the artefact.
- The artefact lives in a version-controlled or wiki-style space with diff history.
- Tier ≥ pro (gated by tier-manifest).

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- A regulator or contract mandates a different shape — use the mandated template.
- No named owner is available — anonymous artefacts rot; defer until ownership resolved.

**Ефективно для:**

- Заповнення річних і квартальних шаблонів без винаходу нової структури кожного разу.
- OKR-сесій, де baseline + target + initiatives повинні бути explicit.
- Year-in-Review з даними з реальних трекерів, а не з пам'яті.
- Onboarding нового оператора: один пакет шаблонів замість усної традиції.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workflow spec | Markdown | team |
| Named owner | Person + role | team / RACI |
| Versioned space for artefact | Git / wiki with history | team |
| Trigger event | Event / threshold / schedule | operating cadence |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist` | Parent skill — provides go-to-market operating context for this methodology. |
| `pro/marketing/growth-marketer` | Peer skill — supplies adjacent growth-marketing methodology that may consume or produce inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source; includes skip-this-methodology guard | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end with decision gates | 800 |
| `content/05-examples.xml` | essential | One worked example from inputs to validated artefact | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: pick correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-annual-planning-templates.md` | Working skeleton for the `ops-annual-planning-templates` artefact with required fields and `not_applicable: <reason>` markers per row. |
| `templates/_smoke-test.md` | Minimum viable filled artefact used by the validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-annual-planning-templates.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only; supports `--help` and `--self-test`. | CI on artefact change; pre-commit. |

## Related

- [[gtm-strategist]]
- [[growth-marketer]]
- [[ops-pricing-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, owner presence, trigger naming, evidence presence) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
