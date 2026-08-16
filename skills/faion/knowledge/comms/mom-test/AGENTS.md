# The Mom Test

## Summary

**One-sentence:** Generates a Mom-Test interview script + post-call signal classifier that distinguishes commitment signals (time/money/referral) from compliments.

**One-paragraph:** The Mom Test (Rob Fitzpatrick, 2013) is a customer discovery interview protocol with three rules: talk about their life not your idea; ask about past specifics not future hypotheticals; talk less than 20% of the time. This methodology turns those rules into two artefacts — a per-call script (≤8 questions, all past-tense or current-spend) and a post-call signal classifier that scores responses on the commitment ladder (time / reputation / money) versus the compliment band.

**Ефективно для:**

- Pre-funding customer-discovery sprints where false positives kill a roadmap.
- Validating a pricing hypothesis by measuring current spend on the pain.
- Coaching a non-PM founder away from leading questions.
- Auditing recorded interviews to score the interviewer's compliment-to-commitment ratio.

## Applies If (ALL must hold)

- Running customer-discovery interviews before committing build effort.
- Pivoting after a vanity-validated launch and need real signal.
- Onboarding a junior interviewer who keeps leading the prospect.
- Building a case study where the buyer's current spend matters.

## Skip If (ANY kills it)

- Sales call where the goal is closing, not learning — different protocol.
- Quantitative survey at scale — Mom Test is interview-only.
- Pure usability test of an existing product — Nielsen heuristics apply, not Mom Test.
- Post-mortem of a churned customer — use exit-interview methodology instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hypothesis | one-sentence problem + persona | founder / PM |
| Target list | 5-10 contacts with reach-out path | CRM / network |
| Recording consent | yes/no per contact | compliance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[active-listening]] | RASA discipline applied during the call |
| [[stakeholder-communication]] | mode selection upstream — Mom Test is the Interview mode for discovery |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: about-their-life, past-specifics, current-spend, commitment-ladder, listen-80-20 | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for interview script + signal classifier output + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (frame → script → run → classify → decide) | 700 |
| `content/05-examples.xml` | essential | Worked example: B2B inventory pain interview + classifier output | 400 |
| `content/06-decision-tree.xml` | essential | Routes by call stage (pre/during/post) and signal type to a rule | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `script-generation` | sonnet | Light judgment on past-tense phrasing + assumption checks. |
| `signal-classification` | haiku | Mechanical ladder mapping on transcript snippets. |
| `synthesis-go-no-go` | sonnet | Cross-call synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-template.md.j2` | Pre-filled Mom-Test interview script with question slots |
| `templates/interview-template.md` | Pre-filled Mom-Test interview script with question slots Generated from `templates/interview-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/prompt-question-gen.txt` | Prompt to generate past-tense, current-spend questions for a hypothesis |
| `templates/prompt-transcript-analysis.txt` | Prompt to classify a transcript on the commitment ladder |
| `templates/signal-classifier.py` | Python classifier: tags utterances as compliment / fact / commitment |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mom-test.py` | Validate Mom-Test script JSON against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[active-listening]]
- [[stakeholder-communication]]
- [[feedback]]
- [[selling-ideas]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts with stage (pre-call script vs post-call analysis), routes by hypothesis maturity, and lands on either a past-tense rule, a current-spend rule, or a commitment-ladder rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-question-gen.txt`

```text
Generate 10 customer discovery interview questions using The Mom Test methodology.
Problem hypothesis: <HYPOTHESIS>
Rules — each question must:
- Ask about past behavior and specific experiences only
- NOT ask for opinions ("Do you think...", "Do you like...")
- NOT use future hypotheticals ("Would you...", "Could you imagine...")
- NOT be leading (no embedded assumptions about the problem)
Output: numbered list of questions only. No preamble.
Review each question against the three Mom Test rules before including it.
```

### `templates/prompt-transcript-analysis.txt`

```text
Classify each statement from this interview transcript.
Categories: PROBLEM_SIGNAL | CURRENT_SOLUTION | COMMITMENT | RED_FLAG | COMPLIMENT
Format: [CATEGORY] "exact quote"
Transcript: <TRANSCRIPT>

Rules:
- Use exact quotes — never paraphrase
- A statement can have multiple categories
- RED_FLAG = hypothetical language ("would", "might", "probably")
- COMPLIMENT = positive but no commitment of time, money, or reputation
- Require 3+ independent PROBLEM_SIGNAL mentions across interviews before treating a problem as validated
```

### `templates/signal-classifier.py`

```python
"""
Keyword-based signal classifier for post-interview note processing.
Input: list of statement strings from interview notes.
Output: list of dicts with statement and matched signal types.

Signal types:
  PROBLEM       — interviewee describes pain or friction
  CURRENT_SOL   — interviewee describes what they use now
  COMMITMENT    — interviewee offers time, reputation, or money
  RED_FLAG      — hypothetical language, predicts unreliable signal
  COMPLIMENT    — positive but non-committal (discard for validation)
"""

SIGNAL_KEYWORDS: dict[str, list[str]] = {
    "PROBLEM": ["struggle", "hard", "frustrating", "pain", "waste", "annoying", "broken", "hate"],
    "CURRENT_SOL": ["I use", "we use", "currently", "right now", "we pay", "we spend", "we rely"],
    "COMMITMENT": ["introduce", "pilot", "deposit", "beta", "send you", "schedule", "sign", "prepay"],
    "RED_FLAG": ["would", "might", "probably", "I think I'd", "generally", "usually I'd"],
}


def classify_statement(statement: str) -> list[str]:
    lower = statement.lower()
    matched = [
        signal
        for signal, keywords in SIGNAL_KEYWORDS.items()
        if any(kw in lower for kw in keywords)
    ]
    return matched if matched else ["COMPLIMENT"]


def classify_interview(statements: list[str]) -> list[dict]:
    return [
        {"statement": s, "signals": classify_statement(s)}
        for s in statements
    ]
```
