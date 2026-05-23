# Decision Options Memo Template

## Summary

**One-sentence:** A standardised options memo BAs use to escalate decisions with cost-value-risk per option, recommendation, dissent acknowledgement, and a decision-required-by date.

**One-paragraph:** Decisions that linger because there is no forcing function rot the program. Options-memo gives the decision a deadline, frames the options, captures dissent, and lands on a recommendation. Output: a Markdown memo attached to the decision record + escalated through the agreed channel.

**Ефективно для:**

- Cross-functional decisions where no one owns the call.
- Architectural decisions that cross team boundaries.
- Re-baselining decisions where stakes are high.
- Vendor selection decisions.

## Applies If (ALL must hold)

- ≥2 viable options exist
- named decision-maker exists
- decision-required-by date is agreed
- the BA / PM has standing to escalate

## Skip If (ANY kills it)

- decision can be made by a single role inline — no memo needed
- no viable options — escalate as 'no-option' memo
- decision-maker absent — escalate to next-up first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| decision context | MD | BA / PM |
| ≥2 viable options | MD | BA |
| named decision-maker + deadline | calendar | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cr-options-matrix-template]] | CR-specific specialisation of this pattern. |
| [[decision-rationale-capture]] | Captures the resulting rationale. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: ≥2 options, scored on cost-value-risk, named decision-maker, decision-required-by date, dissent acknowledged | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for options memo: options[], scores, recommendation, dissent, decision_maker, deadline | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: single-option theatre, anonymous decision-maker, missing deadline, dissent suppressed, post-hoc rationale | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: frame options → score → capture dissent → recommend + escalate | 600 |
| `content/05-examples.xml` | essential | Worked example: vendor-selection memo with 3 options, dissent noted, recommendation | 500 |
| `content/06-decision-tree.xml` | essential | Tree on option count + decision-maker availability + dissent presence | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-option scoring + recommendation. |
| `review_for_compliance` | opus | High-stakes architectural / vendor decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-options-memo-template.json` | JSON skeleton for the options memo. |
| `templates/decision-options-memo-template.md` | Markdown skeleton with required fields. |
| `templates/_smoke-test.md` | Minimum viable options memo. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-options-memo-template.py` | Validates the options memo against the JSON Schema. | Before escalation; pre-commit. |

## Related

- [[decision-rationale-capture]]
- [[cr-options-matrix-template]]
- [[cr-impact-memo-template]]
- [[definition-of-done-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
