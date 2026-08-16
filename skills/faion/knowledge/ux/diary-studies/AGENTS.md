# Diary Studies

## Summary

**One-sentence:** Produces a diary-study report from longitudinal self-recorded entries over days/weeks with daily-and-event-triggered prompts + reminder cadence + analysis.

**One-paragraph:** Longitudinal UX research where participants self-record experiences in the moment across days or weeks. Two entry modes: daily-reflection (fixed time) and event-triggered (after specific actions). Reminder cadence is critical — without scheduled nudges, participation drops 40-60% by day 3. Analysis groups entries by participant + theme; output is a longitudinal report tracking behaviour change + breakdown patterns over time.

**Ефективно для:**

- Behaviour change over time (3-30 днів) — lab session не покаже.
- Real-world context для habit/sleep/exercise/medication products.
- Capture episodic 'aha moments' що зникають з memory before next interview.
- Mobile-first продукти де момент-of-use є critical.

## Applies If (ALL must hold)

- Study period 3-30 days where behaviour changes or accumulates context.
- Participants can self-record in their daily flow (mobile app / SMS / web form).
- Reminder infrastructure available (push notifications, SMS).

## Skip If (ANY kills it)

- Single-session insight — use interviews instead.
- Behaviour-sensitive contexts (mental health journaling, safety) — diary changes the behaviour.
- Need quantitative significance — diaries are qualitative; use surveys.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recruitment plan | criteria + n>=8 per segment | research |
| Entry templates | daily + event-triggered | this methodology template |
| Reminder schedule | cron-like cadence | this methodology |
| Consent + data-retention agreement | PDF | legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[contextual-inquiry]] | Alternative when on-site observation is feasible |
| [[personas]] | Diary themes refine personas |

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
| `templates/study-plan.md.j2` | Diary study plan template covering recruitment, prompts, cadence, analysis |
| `templates/study-plan.md` | Diary study plan template covering recruitment, prompts, cadence, analysis Generated from `templates/study-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/entry-daily.md` | Daily reflection entry template |
| `templates/entry-event.md.j2` | Event-triggered entry template |
| `templates/entry-event.md` | Event-triggered entry template Generated from `templates/entry-event.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/diary-reminders.py` | Python reminder scheduler emitting push + SMS based on participant timezone |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-diary-studies.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[contextual-inquiry]]
- [[focus-groups]]
- [[personas]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/diary-reminders.py`

```python
"""diary-reminders.py — schedule push + SMS reminders per participant timezone."""
from __future__ import annotations
import datetime
import json
from pathlib import Path

def schedule(participants_path: str) -> None:
    participants = json.loads(Path(participants_path).read_text())
    for p in participants:
        # 22:00 local push + 23:30 SMS fallback if no entry by then
        print(f"schedule push {p['id']} @22:00 {p['tz']}")
        print(f"schedule sms-fallback {p['id']} @23:30 {p['tz']}")

if __name__ == "__main__":
    import sys
    schedule(sys.argv[1])
```
