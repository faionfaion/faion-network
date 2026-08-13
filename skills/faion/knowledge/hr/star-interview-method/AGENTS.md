# STAR Interview Method

## Summary

**One-sentence:** STAR method playbook step: how to probe Situation/Task/Action/Result completeness in real time and produce evidence-anchored notes.

**One-paragraph:** STAR method playbook step: how to probe Situation/Task/Action/Result completeness in real time and produce evidence-anchored notes. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Реальний run behavioral round з probing на STAR completeness.
- Збір evidence-anchored нотаток для debrief, а не general impressions.
- Кілька competencies в одному 45-60 хв slot.

## Applies If (ALL must hold)

- Interviewer is conducting a behavioral round.
- Notes must be evidence-anchored for downstream debrief.
- Multiple competencies will be probed in a single 45-60 minute session.

## Skip If (ANY kills it)

- Round is purely technical / coding — STAR adds noise.
- Candidate has <2 years of experience to draw stories from — fall back to hypothetical scenarios.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Calibrated STAR scorecard | markdown | star-interview-framework |
| Question seeds per competency | markdown | star-interview-examples |
| Note-taking template | markdown | interview lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[star-interview-framework]] | Provides the scorecard the notes will populate |
| [[structured-interview-design]] | Interview kit defines the round structure this step lives inside |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/star-playbook-step.md` | Per-question STAR probing playbook with probe prompts + note-slots |
| `templates/star-scorecard.md` | Per-question scorecard with STAR evidence rows + competency rating |
| `templates/hiring-manager-guide.md` | Hiring-manager-facing summary of the STAR method |
| `templates/star-completeness.py` | Helper to score STAR completeness from a transcript |
| `templates/_smoke-test.md` | Filled-in playbook for a single competency × question |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-star-interview-method.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[star-interview-framework]]
- [[star-interview-examples]]
- [[structured-interview-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/star-completeness.py`

```python
#!/usr/bin/env python3
"""
star-completeness.py — Deterministic STAR component detection.
Flags missing components and "we"-only answers before LLM transcript analysis.
Run BEFORE any LLM scoring pass to gate on completeness.

Input (stdin): JSON array
  [{"question": "Tell me about a time...", "answer": "..."}, ...]

Output (stdout): JSON array
  [{"q": "...", "S": bool, "T": bool, "A": bool, "R": bool,
    "pronoun_we_only": bool, "complete": bool}, ...]

Usage:
  python3 star-completeness.py < interview.json
  cat qa.json | python3 star-completeness.py | jq '.[] | select(.complete == false)'
"""
import sys
import json
import re

CUES: dict[str, list[str]] = {
    "S": [
        r"\b(when|at the time|context was|background|last (year|quarter|month|week))\b",
        r"\b(20\d\d|in (january|february|march|april|may|june|july|august|september|october|november|december))\b",
        r"\b(while i was|during my time at|at my (previous|last|current) (job|company|role))\b",
    ],
    "T": [
        r"\b(my (role|responsibility|task|goal|job|objective))\b",
        r"\b(i was (responsible|asked|tasked|expected|required) (for|to))\b",
        r"\b(it was (up to|my job) to)\b",
    ],
    "A": [
        r"\bi (decided|did|built|wrote|led|created|negotiated|shipped|coded|hired|coached|designed|implemented|fixed|resolved|managed|organized|proposed|initiated)\b",
        r"\bmy (approach|first step|solution|decision) was\b",
        r"\bso i (reached out|set up|drafted|called|scheduled|reviewed|analyzed)\b",
    ],
    "R": [
        r"\b(\d+\s*%|\$\s*\d+[kmb]?)\b",
        r"\b(reduced|increased|improved|grew|saved|cut|delivered|achieved|exceeded|reached|completed) (by|to|from)?\b",
        r"\b(the (result|outcome|impact|effect) was)\b",
        r"\b(as a result|in the end|ultimately|we (ended up|achieved|hit|delivered))\b",
    ],
}


def check(answer: str) -> dict:
    flags: dict[str, bool] = {}
    for component, patterns in CUES.items():
        flags[component] = any(re.search(p, answer, re.IGNORECASE) for p in patterns)

    text_lower = " " + answer.lower() + " "
    has_we = bool(re.search(r"\bwe\b", text_lower))
    has_i = bool(re.search(r"\bi\b", text_lower))
    flags["pronoun_we_only"] = has_we and not has_i
    flags["complete"] = all(flags[k] for k in "STAR")
    return flags


if __name__ == "__main__":
    data = json.load(sys.stdin)
    output = [{"q": item["question"], **check(item["answer"])} for item in data]
    json.dump(output, sys.stdout, indent=2)
    print()

    incomplete = [o for o in output if not o["complete"]]
    if incomplete:
        print(f"\n{len(incomplete)} answer(s) missing STAR components:", file=sys.stderr)
        for o in incomplete:
            missing = [c for c in "STAR" if not o[c]]
            print(f"  Q: {o['q'][:60]}... → missing: {missing}", file=sys.stderr)
        sys.exit(1)
```
