<!--
purpose: Per-round scorecard template tied to the design doc competencies
consumes: see AGENTS.md Prerequisites
produces: Structured Interview Design spec
depends-on: content/02-output-contract.xml schema
token-budget-impact: ~400 tokens when filled
variables:
  - name: candidate_name
    type: string
    required: true
    sensitive: true
    placeholder: "__FAION_CANDIDATE_NAME__"
    description: The candidate's name as they wrote it. Declared sensitive so it never leaves your machine - this is an evaluative record about an identified person and the assembler has no business holding it.
  - name: role_title
    type: string
    required: true
    description: The role exactly as advertised, not the internal level code. The competencies scored below must be the ones in that advert, or this scorecard measures a different job than the one applied for.
  - name: interviewer_name
    type: string
    required: true
    description: Who ran this round and is accountable for the evidence in it. One name - a card filled in by a panel averages away the disagreement, which was the useful part.
  - name: date
    type: string
    required: true
    description: Date of the interview, ISO. Evidence decays: a scorecard read the same week is context, the same card read six months later is a rumour with a number attached.
  - name: round_label
    type: string
    required: true
    description: Which round this is and what it covered - "Round 2, systems design". Scores only combine across rounds if each round says what it was measuring.
  - name: competency_source
    type: path
    required: true
    description: Path to the interview design doc holding the competency list and weights. If the weights are not written down somewhere both interviewers read, the weighted score below is decoration.
-->

# Interview Scorecard

**Candidate:** {{candidate_name}}
**Role:** {{role_title}}
**Interviewer:** {{interviewer_name}}
**Date:** {{date}}
**Round:** {{round_label}}
**Competencies and weights from:** `{{competency_source}}`

---

## Competency Scores

| Competency | Score (1-5) | Evidence / Notes |
|------------|-------------|-----------------|
| | | |
| | | |
| | | |
| | | |

**Weighted Score:** [Calculate: sum of (score × weight) for each competency]

---

## Question-by-Question Notes

**Q1:** [Question text]

- S (Situation):
- T (Task):
- A (Action):
- R (Result):
- Score: [ ]
- Key evidence:

**Q2:** [Question text]

- S:
- T:
- A:
- R:
- Score: [ ]
- Key evidence:

**Q3:** [Question text]

- S:
- T:
- A:
- R:
- Score: [ ]
- Key evidence:

---

## Overall Assessment

**Strengths (cite specific evidence):**
1.
2.

**Concerns (cite specific evidence):**
1.
2.

**Questions for future rounds:**

---

## Hiring Recommendation

- [ ] Strong Hire — exceeds bar; would advocate strongly
- [ ] Hire — meets bar
- [ ] Lean Hire — meets bar with reservations (specify below)
- [ ] Lean No Hire — below bar with some positives (specify below)
- [ ] No Hire — does not meet bar
- [ ] Strong No Hire — clear no

**Rationale (must cite evidence; do not submit without this field):**
