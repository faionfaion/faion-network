# UAT Script Pattern

## Summary

**One-sentence:** Generates a repeatable UAT script — acceptance criteria → numbered steps → expected results → sign-off log — replacing ad-hoc Google Docs at release time.

**One-paragraph:** Generates a repeatable UAT script — acceptance criteria → numbered steps → expected results → sign-off log — replacing ad-hoc Google Docs at release time.

**Ефективно для:**

- Solo team running a major release QA cycle (regression + smoke + UAT).
- Pre-launch UAT against staging where stakeholders sign off.
- Release where regressions must be traceable to test steps.

## Applies If (ALL must hold)

- Release has ≥3 acceptance criteria.
- UAT will be performed by ≥1 named tester before sign-off.
- Sign-off is required (not auto-merge).
- Test results will be stored for ≥90 days.

## Skip If (ANY kills it)

- Continuous-deploy environment with full auto-coverage — UAT overhead exceeds value.
- Greenfield prototype with no users.
- Bug-fix release with one-line scope — smoke test only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AC list | yaml | spec.md acceptance-criteria block |
| Tester names | list | team roster |
| Staging URL | url | deploy environment |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| qa-test-pyramid-vs-trophy-decision | UAT lives at the e2e tier; its budget comes from the pyramid decision. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-ac-to-step-traceability, r2-numbered-steps, r3-expected-result-per-step, r4-named-tester, r5-sign-off-log | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the UAT Script Pattern artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: ad-hoc-doc, acceptance-criteria-drift, no-sign-off-record | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-uat-script-pattern` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-uat-script-pattern` | sonnet | Bounded structural check against the output contract. |
| `review-uat-script-pattern` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/uat-script-pattern.json` | JSON skeleton matching the output contract. |
| `templates/uat-script-pattern.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-uat-script-pattern.py` | Validate UAT Script Pattern output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[qa-test-pyramid-vs-trophy-decision]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
