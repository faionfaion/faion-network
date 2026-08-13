# Elicitation Techniques

## Summary

**One-sentence:** Produces a technique-to-session mapping selecting interview / workshop / survey / observation / document-analysis per information type and stakeholder count.

**One-paragraph:** Produces a technique-to-session mapping selecting interview / workshop / survey / observation / document-analysis per information type and stakeholder count. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Discovery-sprint з mix-stakeholder'ів (SME + user + ops), де треба differentiate technique per group.
- Compliance/audit context, де треба evidence trail як requirement'и зібрані.
- BA-onboarding на новий продукт — мапінг who-to-talk-to + what-to-extract.
- Conflict-heavy initiative, де треба workshop facilitation, а не серії 1:1 interview'ів.

## Applies If (ALL must hold)

- New scope or feature requires structured stakeholder input — not just standup chatter.
- Stakeholder population is mixed (SMEs + users + ops + regulators) and needs technique differentiation.
- Time-boxed discovery sprint with explicit deliverables per session.
- Compliance or audit requires evidence trail of how requirements were sourced.

## Skip If (ANY kills it)

- Solo dev with no external stakeholders.
- Reactive bug-fix work — no requirements elicitation needed.
- Trust gap is so wide that any elicitation will surface theatre, not truth.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder list | Output of stakeholder-analysis | BA |
| Information-need list | Markdown | BA / PM |
| Time-box and budget for discovery | calendar | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-analysis]] | stakeholder list drives technique selection |
| [[ba-planning]] | elicitation plan plugs into T1 approach |

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
| `score-info-types` | haiku | Mechanical classification per information-need into deep/group/broad. |
| `map-techniques` | sonnet | Pick technique per info-need + stakeholder cluster. |
| `draft-session-plan` | sonnet | Sequence sessions with logistics + facilitator. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | 1:1 interview guide skeleton with open + probing questions. |
| `templates/workshop-agenda.md` | Multi-stakeholder workshop agenda with facilitation cues. |
| `templates/technique-selector.py` | CLI selector mapping (info_type, stakeholder_count) → technique. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[stakeholder-analysis]]
- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/technique-selector.py`

```python
#!/usr/bin/env python3
"""technique-selector.py — map (info_type, stakeholder_count) to elicitation technique."""
from __future__ import annotations
import sys

MATRIX = {
    ('sme-deep', 1): 'interview', ('sme-deep', 2): 'interview', ('sme-deep', 3): 'interview',
    ('consensus-needs', 4): 'workshop', ('consensus-needs', 8): 'workshop',
    ('broad-preference', 15): 'survey', ('broad-preference', 100): 'survey',
    ('process-observe', 1): 'observation',
    ('artefact-analysis', 0): 'document-analysis',
}

def pick(info_type: str, count: int) -> str:
    for (it, n), tech in MATRIX.items():
        if it == info_type and count >= n: return tech
    return 'interview'

if __name__ == '__main__':
    print(pick(sys.argv[1], int(sys.argv[2])))
```
