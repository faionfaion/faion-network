# Business Analysis Planning

## Summary

**One-sentence:** Produces five BABOK KA1 task artefacts (T1-T5) with named approvers, cadences, and lifecycles seeding all downstream BA work.

**One-paragraph:** Produces five BABOK KA1 task artefacts (T1-T5) with named approvers, cadences, and lifecycles seeding all downstream BA work. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Програма починає планову delivery-фазу і потребує п'ять окремих artefact'ів (T1-T5) з названими approver'ами та різною каденцією review.
- Гібридний plan-driven + change-driven engagement, де відсотки фіксуються per-artefact (70/30, 50/50), а не глобально.
- Активація суміжних ba-core методологій — KA1 сеть seeding-церемонія для stakeholder-analysis, requirements-lifecycle, ba-governance.
- Запуск BA performance loop з ≥3 метриками з null-baselines на першому циклі.

## Applies If (ALL must hold)

- A new initiative crosses from discovery to planned delivery and needs an explicit BA approach, stakeholder map, governance, information management, and performance plan.
- Program must demonstrate BABOK conformance to certifying bodies or internal QA (CCBA/CBAP, IIBA-aligned PMOs).
- Hybrid plan-driven + change-driven engagement where per-artefact baselined-vs-living declarations are needed.
- Sibling ba-core methodologies (stakeholder-analysis, ba-governance, requirements-lifecycle, elicitation-techniques) are about to be activated — KA1 is their prerequisite.
- Introducing BA performance metrics (rework rate, requirement defect density, elicitation throughput).

## Skip If (ANY kills it)

- Solo MVP, prototype, or research spike — five KA1 tasks are heavier than the work itself; use a one-page lean canvas.
- Pure backlog-driven Scrum where the Definition of Ready already encodes the BA approach.
- Continuous-discovery context where requirements churn weekly — KA1 baselines go stale faster than they can be reviewed.
- Sponsor refuses to name a governance approver — KA1 governance becomes decorative.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Initiative brief | Markdown / Confluence page | sponsor |
| Org chart | CSV / HRIS export | people-ops |
| Existing methodology decision (Agile / Waterfall / hybrid) | ADR / steering memo | PMO |
| Tooling inventory (Jira / Confluence / GitHub) | list | operations |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-analysis]] | downstream consumer of T2 stakeholder list |
| [[ba-governance]] | downstream consumer of T3 governance plan |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-t1-t5` | sonnet | Apply BABOK KA1 template across five artefacts; deterministic structure with judgement on approach percentages. |
| `score-cadence` | haiku | Mechanical mapping of artefact type to review-cadence-days. |
| `review-coherence` | opus | Cross-check T2-T5 dependency chain against T1 approach declaration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-approach-document.md.j2` | T1 plan-BA-approach skeleton with stakeholders, elicitation plan, deliverables, governance. |
| `templates/ba-approach-document.md` | T1 plan-BA-approach skeleton with stakeholders, elicitation plan, deliverables, governance. Generated from `templates/ba-approach-document.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ka1-bundle-skeleton.md.j2` | Bundle index linking T1-T5 artefacts in dependency order. |
| `templates/ka1-bundle-skeleton.md` | Bundle index linking T1-T5 artefacts in dependency order. Generated from `templates/ka1-bundle-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ka1_check.py` | Helper that verifies the 5 KA1 artefacts exist and are within review cadence; emits JSON. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[stakeholder-analysis]]
- [[ba-governance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ka1_check.py`

```python
"""ka1_check.py — verify the 5 BABOK KA1 artifacts are present and within review cadence.
Usage: python ka1_check.py <directory with T1-T5 markdown files>
"""
from __future__ import annotations

import sys
import json
import datetime as dt
import pathlib

try:
    import yaml
except ImportError:
    print(json.dumps({"error": "pyyaml not installed: pip install pyyaml"}))
    sys.exit(2)

TASKS = {
    "T1": "plan_ba_approach",
    "T2": "plan_stakeholder_engagement",
    "T3": "plan_ba_governance",
    "T4": "plan_ba_information_management",
    "T5": "identify_ba_performance_improvements",
}
REQUIRED_FIELDS = {"task_id", "version", "approver", "last_reviewed", "baselined"}
CADENCE_DAYS = {"T1": 30, "T2": 14, "T3": 30, "T4": 30, "T5": 7}


def load_frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing YAML frontmatter (must start with ---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{path}: malformed frontmatter")
    return yaml.safe_load(parts[1]) or {}


def main(root_str: str) -> int:
    root = pathlib.Path(root_str)
    errors: list[str] = []
    found: dict[str, dict] = {}

    for tid, slug in TASKS.items():
        candidates = list(root.glob(f"{tid}-*.md"))
        if not candidates:
            errors.append(f"{tid} ({slug}): no artifact found (expected {tid}-*.md)")
            continue

        fm = load_frontmatter(candidates[0])
        missing = REQUIRED_FIELDS - set(fm)
        if missing:
            errors.append(f"{tid}: missing frontmatter fields: {sorted(missing)}")

        approver = fm.get("approver", "")
        if not approver or approver in {"leadership", "management", "product team"}:
            errors.append(f"{tid}: approver must be a named person, got: '{approver}'")

        last = fm.get("last_reviewed")
        if isinstance(last, (dt.date, dt.datetime)):
            last_d = last if isinstance(last, dt.date) else last.date()
            age = (dt.date.today() - last_d).days
            if age > CADENCE_DAYS[tid]:
                errors.append(
                    f"{tid} stale: last_reviewed={last_d}, age={age}d > cadence={CADENCE_DAYS[tid]}d"
                )
        elif last is not None:
            errors.append(f"{tid}: last_reviewed is not a date: {last!r}")

        found[tid] = fm

    result = {
        "ok": not errors,
        "tasks_found": sorted(found),
        "tasks_missing": [t for t in TASKS if t not in found],
        "errors": errors,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
```
