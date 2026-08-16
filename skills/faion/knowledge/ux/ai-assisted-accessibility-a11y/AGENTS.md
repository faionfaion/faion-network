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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-accessibility-automation-2026]]
- [[test-self-healing-locators-audited]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ci-a11y-gate.sh`

```bash
#!/usr/bin/env bash
# ci-a11y-gate.sh — Run pa11y-ci against a list of URLs; fail build on critical issues.
# Usage: ./ci-a11y-gate.sh [urls-file] [threshold]
#   urls-file: path to file with one URL per line (default: urls.txt)
#   threshold: max allowed errors before failure (default: 0 = fail on any error)
set -euo pipefail

URLS_FILE="${1:-urls.txt}"
THRESHOLD="${2:-0}"

pa11y-ci \
  --config .pa11yci.json \
  --threshold "$THRESHOLD" \
  $(cat "$URLS_FILE" | tr '\n' ' ')
```

### `templates/pa11yci.json`

```json
{
  "standard": "WCAG2AA",
  "runners": [
    "axe",
    "htmlcs"
  ],
  "ignore": [
    "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail"
  ],
  "chromeLaunchConfig": {
    "args": [
      "--no-sandbox"
    ]
  }
}
```

### `templates/prompt-generate-fix.txt`

```text
SYSTEM:
You are an accessibility engineer. Generate concrete code fixes for WCAG violations.
Rules:
(1) Never suggest overlay or widget-based fixes.
(2) Explain why the fix satisfies the WCAG criterion in one sentence.
(3) Provide one alternative fix if multiple valid approaches exist.
(4) Flag dynamic/AJAX content fixes for manual review.

USER:
WCAG violation: [criterion name, e.g., 1.1.1 Non-text Content]
Element selector: [CSS selector]
Current code:
[paste code snippet]
Framework: [React / HTML / Vue / Angular]

Generate a concrete code fix. Format:
- Primary fix (code)
- Why this satisfies [criterion] (one sentence)
- Alternative fix (if applicable)
- Manual review needed: yes/no — reason
```

### `templates/prompt-triage-issues.txt`

```text
SYSTEM:
You are an accessibility engineer. Triage axe-core scan results.
Rules:
(1) Never suggest overlay or widget-based fixes.
(2) Filter likely false positives: violations where element is aria-hidden or display:none.
(3) Rank remaining issues by user impact: Critical / High / Medium / Low.
(4) Group related issues by component type.

USER:
Given the following axe-core JSON scan results, triage the issues:

[paste axe-core JSON output]

Output a ranked issue list as JSON array with fields:
{ id, wcag_criterion, impact, element_selector, description, suggested_fix, false_positive: true/false }

Group Critical and High issues at the top.
Flag any issues related to dynamic/AJAX content for manual review rather than automated fix.
```
