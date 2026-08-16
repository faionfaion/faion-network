# Survey Design

## Summary

**One-sentence:** Designs a bias-linted survey: <=12 questions, no leading/double-barreled/loaded wording, mandatory open-text for top 2 themes, sample-size N>=120 per segment for 90% CI +/-9%.

**One-paragraph:** Survey-authoring methodology producing a survey doc + bias-lint pass + sample-size checklist. Caps at 12 questions per survey, enforces bias linting (no leading, double-barreled, loaded, or assumes-prior-knowledge wording), requires open-text fields for the top 2 themes, and demands N>=120 responses per segment for 90% CI +/-9% before publishing any conclusion.

**Ефективно для:**

- Quantitative validation після qualitative interviews.
- Pricing willingness-to-pay survey.
- NPS / CSAT квартальний пульс.
- Feature-prioritisation MaxDiff survey.
- Persona segmentation: підтвердити hypothesis по >=120 респондентах.

## Applies If (ALL must hold)

- Quantitative validation after qualitative interviews.
- Willingness-to-pay (pricing) survey.
- Quarterly NPS / CSAT pulse.
- Feature-prioritisation MaxDiff or Kano survey.
- Persona segmentation validation across >=120 respondents.

## Skip If (ANY kills it)

- Pre-interview exploration; do qualitative first.
- Open-ended discovery; use interviews + observation.
- Single-question pulse via SMS / popup (not a survey).
- Compliance-mandated survey with fixed wording (no design freedom).
- Sample < 30 (no statistical interpretation possible).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hypothesis to test | 1 sentence | PM / researcher |
| Target segment list | persona doc | persona-building |
| Distribution channel + expected reach | estimate | GTM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[persona-building]] | supplies the segments and minimum sample-size targets |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-questions` | sonnet | Compose <=12 questions ordered easy -> hard -> demographics. |
| `bias-lint` | haiku | Mechanical regex + pattern check for leading/double-barreled/loaded. |
| `sample-size-calc` | haiku | Compute required N per segment for CI target. |
| `pilot-and-iterate` | sonnet | Run pilot N=10; rewrite questions with confusion signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-design-doc.md.j2` | Survey doc skeleton (hypothesis + questions + sample plan) |
| `templates/survey-design-doc.md` | Survey doc skeleton (hypothesis + questions + sample plan) Generated from `templates/survey-design-doc.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/question-bank.md.j2` | Pre-vetted question phrasings by survey type |
| `templates/question-bank.md` | Pre-vetted question phrasings by survey type Generated from `templates/question-bank.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/bias-linter.py` | Lint questions for leading/double-barreled/loaded patterns |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-survey-design.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[user-research-at-scale]]
- [[persona-building]]
- [[continuous-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/bias-linter.py`

```python
#!/usr/bin/env python3
"""
bias_linter.py — deterministic pre-filter for survey question drafts.
Run before LLM bias-review pass to catch patterns the LLM rationalizes away.

Usage:
    cat questions.json | python bias_linter.py
    python bias_linter.py < questions.json

Input (stdin): JSON array of {"text": "question string"} objects.
Output (stdout): JSON array of flagged items with {q, text, flags}.
Exit code: 0 if clean, 1 if any flags found.
"""
import re
import sys
import json

LEADING = re.compile(
    r"\b(don't you (think|agree)|isn't it|wouldn't you say|how amazing|how awful)\b",
    re.IGNORECASE,
)
DOUBLE = re.compile(r"\b(and|or)\b.*\?")  # crude double-barrel heuristic
HYPOTHETICAL = re.compile(
    r"\b(would you|will you|do you plan to|how often will)\b",
    re.IGNORECASE,
)
ABSOLUTIST = re.compile(
    r"\b(always|never|every time|all of the time)\b",
    re.IGNORECASE,
)
MAX_WORDS = 28


def lint(items: list[dict]) -> list[dict]:
    out = []
    for i, q in enumerate(items, 1):
        text = q.get("text", "")
        flags = []
        if LEADING.search(text):
            flags.append("leading")
        if HYPOTHETICAL.search(text):
            flags.append("hypothetical")
        if ABSOLUTIST.search(text):
            flags.append("absolutist-anchor")
        if "?" in text and DOUBLE.search(text) and len(text.split()) > 8:
            # rough check: long question with "and/or" before the "?"
            if "satisf" in text.lower() or "engag" in text.lower():
                flags.append("possible-double-barrel")
        if len(text.split()) > MAX_WORDS:
            flags.append("too-long")
        if flags:
            out.append({"q": i, "text": text, "flags": flags})
    return out


if __name__ == "__main__":
    data = json.load(sys.stdin)  # [{"text": "..."}]
    results = lint(data)
    json.dump(results, sys.stdout, indent=2)
    print()
    if results:
        sys.exit(1)
```
