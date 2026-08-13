# AI Accessibility Automation 2026

## Summary

**One-sentence:** Wire axe-playwright into every deploy, an AI ranks/de-duplicates violations, code fixes are AI-suggested per issue, VPAT 2.5 drafts are AI-generated from scan summaries, alt-text + captions pipelines run on every media upload, and a human a11y lead gates every AI output.

**One-paragraph:** Full continuous accessibility automation pipeline for products with frequent deployments: axe-playwright scans every deploy, AI ranks and de-duplicates violations, code fixes are suggested per issue, VPAT 2.5 drafts are generated from scan summaries, and caption/alt-text pipelines run on every media upload. All AI outputs are gated by a human accessibility lead before entering the developer backlog.

**Ефективно для:**

- Continuous-deploy products з частими a11y regressions.
- VPAT-driven sales: AI drafts → human lead signs.
- Bulk alt-text generation для media-heavy sites.
- Org з human lead, що caps AI output backlog.

## Applies If (ALL must hold)

- Product deploys ≥ weekly (continuous integration required).
- Org carries a human accessibility lead with capacity to gate AI output.
- Media uploads (images / video) are common and need alt / caption pipelines.

## Skip If (ANY kills it)

- Static brochure site with one release per quarter — manual audit cheaper.
- No human a11y lead available — AI output cannot be gated.
- Product has no media uploads (alt/caption pipelines wasted).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Playwright + axe-playwright installed | deps | test infra |
| Human accessibility lead | role | team roster |
| Media upload pipeline | code | media service |

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
| `templates/ci-a11y-gate.sh` | Shell script wiring axe-playwright into CI as a deploy gate. |
| `templates/prompt-scan-triage.txt` | Prompt ranking + de-duplicating axe violations for the human lead. |
| `templates/prompt-vpat-draft.txt` | Prompt drafting a VPAT 2.5 section from scan summaries. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[ai-assisted-accessibility]]
- [[test-self-healing-locators-audited]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ci-a11y-gate.sh`

```bash
#!/usr/bin/env bash
# ci-a11y-gate.sh — Fail build if new Critical a11y violations introduced vs baseline.
# Usage: ./ci-a11y-gate.sh [baseline-file]
#   baseline-file: JSON from a previous axe scan (default: a11y-baseline.json)
#   Create initial baseline: run once and save output as a11y-baseline.json
set -euo pipefail

BASELINE="${1:-a11y-baseline.json}"
CURRENT="a11y-current.json"

npx axe-cli \
  --browser chrome \
  --tags wcag2a,wcag2aa \
  --reporter json \
  "$(cat urls.txt)" > "$CURRENT"

python3 - <<'EOF'
import json
import os
import sys

baseline = (
    json.load(open("a11y-baseline.json"))
    if os.path.exists("a11y-baseline.json")
    else {"violations": []}
)
current = json.load(open("a11y-current.json"))

baseline_ids = {v["id"] for v in baseline.get("violations", [])}
new_violations = [
    v for v in current.get("violations", [])
    if v["id"] not in baseline_ids and v["impact"] == "critical"
]

if new_violations:
    print(f"FAIL: {len(new_violations)} new Critical a11y violations introduced:")
    for v in new_violations:
        print(f"  - {v['id']}: {v['description']}")
    sys.exit(1)

print("PASS: No new Critical a11y violations.")
EOF
```

### `templates/prompt-scan-triage.txt`

```text
SYSTEM:
You are an accessibility automation engineer. Triage axe-core scan results and draft VPAT sections.
Rules:
(1) Never suggest overlay or widget-based fixes.
(2) Remove violations where element is aria-hidden or display:none (likely false positives).
(3) Do not invent issues not present in the scan data.
(4) Flag complex ARIA patterns (combobox, tree, grid) for senior human review.
(5) Mark all VPAT entries as DRAFT — human review required before external use.

USER:
Given this axe-core scan report (JSON):
[paste scan JSON]

Perform:
1. Remove likely false positives (aria-hidden, display:none elements)
2. Rank remaining: Critical (A failures affecting all users) / High (AA failures) / Medium (A with workarounds) / Low (AAA or minor)
3. Group by component type
4. For each Critical and High issue, generate a code fix in [framework]
5. Draft VPAT 2.5 conformance entries: Supports / Partially Supports / Does Not Support / Not Applicable

Output: { summary: {...}, issues: [...], fixes: {...}, vpat_draft: [...] }
All vpat_draft entries must include: "DRAFT — human review required before publication"
```

### `templates/prompt-vpat-draft.txt`

```text
SYSTEM:
You are drafting a VPAT 2.5 accessibility conformance report section.
Rules:
(1) Use only data from the provided scan summary — do not invent conformance claims.
(2) For each criterion, output exactly one of: Supports | Partially Supports | Does Not Support | Not Applicable
(3) Add a one-sentence note for each non-"Supports" entry explaining what fails.
(4) Mark every entry with "DRAFT — human review required before publication".
(5) Do not assess organizational processes or policies — only code-level evidence.

USER:
Draft VPAT 2.5 sections based on this scan summary:
[paste scan summary JSON]

Product: [product name]
Scan date: [date]
Standard: WCAG 2.2 Level AA

For each WCAG success criterion covered in the scan:
- Criterion number and name
- Conformance level: Supports | Partially Supports | Does Not Support | Not Applicable
- One-sentence explanation for non-Supports entries
- DRAFT watermark on all entries

Output as structured list. Note at top: "DRAFT — Requires legal/compliance review before any external use."
```
