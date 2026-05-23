# AI-Assisted Accessibility

## Summary

**One-sentence:** Use a Haiku subagent to run axe-playwright/pa11y + filter noise + rank by impact; a Sonnet subagent generates code fixes per issue; human a11y experts validate every AI output before dev tickets are created.

**One-paragraph:** AI accelerates WCAG auditing by automating scan execution, false-positive filtering, fix suggestion generation, and bulk alt text creation — reducing audit time by 60–75%. A Haiku subagent runs axe-playwright or pa11y, filters noise, and ranks issues by impact. A Sonnet subagent generates code fixes per issue. Human experts validate all AI output before developer tickets are created.

**Ефективно для:**

- Quarterly WCAG audits — 60-75% audit-time reduction.
- Stack із axe-playwright / pa11y підтримкою.
- Org із dedicated a11y expert для validation.
- Bulk fix proposals: Sonnet codes, expert sign-off, dev queue.

## Applies If (ALL must hold)

- Org runs a recurring (≥ quarterly) WCAG audit cycle.
- Both Haiku-class and Sonnet-class models are available.
- Human accessibility expert is in the loop to validate output.

## Skip If (ANY kills it)

- One-off audit with no recurring cycle.
- No human a11y expert available — AI fixes cannot be validated.
- Stack lacks axe/pa11y compatibility (rare in 2026 web stacks).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| axe-playwright or pa11y installed | deps | test infra |
| Haiku + Sonnet model access | API keys | ops |
| Human accessibility expert | role | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-a11y-gate.sh` | CI script invoking axe + pa11y and pushing artifacts to the Haiku filter. |
| `templates/pa11yci.json` | pa11y-ci config covering critical paths. |
| `templates/prompt-generate-fix.txt` | Prompt for the Sonnet fix-generator with WCAG citation enforcement. |
| `templates/prompt-triage-issues.txt` | Prompt for the Haiku filter + ranker. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-accessibility.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[ai-accessibility-automation-2026]]
- [[test-self-healing-locators-audited]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
