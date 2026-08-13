# Working Backwards PR/FAQ

## Summary

**One-sentence:** Produces a PRFAQ Record — a one-page launch press release plus two separately-audienced FAQ banks — run as five phases that end in a `proceed / revise / kill` judgement before a single line of spec is written.

**One-paragraph:** Amazon's Working Backwards inverts the order of product work: write the launch announcement first, for a named customer, in the past tense, and build only if the announcement is one somebody would want to read. The value is not the document — it is that the document is allowed to come back `kill`. A concept gate that has never killed anything is decoration, so this methodology makes `kill` a first-class successful outcome and refuses to emit a numeric score, because a number invites negotiation where a judgement demands a decision. Five phases run in order — customer and problem, press release, customer FAQ, internal FAQ, verdict — and any of them may terminate the review early. There is no software dependency anywhere in it. The `{concept_type}` switch re-points two things per run — the success measure and the party the internal FAQ interrogates — so the same five phases serve a commercial product, an internal platform, an open-source release, a nonprofit programme, a service business, a creative work and a physical good without a second methodology.

**Ефективно для:**

- Anyone about to write `spec.md` for something no customer has been named for.
- Solo founders whose validation is that the idea still sounds good to them a week later.
- Internal platform work, where the customer is a colleague who is not allowed to decline.
- Open-source releases where the real cost is maintenance nobody has priced.
- Any concept that has survived three conversations without anyone stating what would kill it.

## Applies If (ALL must hold)

- A concept exists that would consume real build effort if accepted.
- No spec, design or code has been committed to it yet.
- A customer can in principle be named — even if naming them turns out to be the hard part.

## Skip If (ANY kills it)

- The work is already committed and the open question is how, not whether — write a spec, not a gate.
- It is a bug fix, a chore, a dependency bump or a legally mandated change; there is no whether to gate.
- The customer is you and the build is one evening — the gate would cost more than the thing.
- You are exploring options rather than judging one — diverge first; this instrument only converges.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | The five phases and seven testable rules, one section per phase. R1 and R7 are the two gates. |
| `content/02-output-contract.xml` | The PRFAQ Record: every field, the early-stop condition, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six ways a concept gate stops gating, with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from what the review actually produced to `proceed` / `revise` / `kill`. |
| `scripts/validate-working-backwards-prfaq.py` | Validates a record; enforces the early stop, the score ban, the past-tense press release and the `{concept_type}` coupling. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prfaq-record.yaml` | Fill-in record for a completed five-phase review; ships valid against the contract. |
| `templates/prfaq-record-kill.yaml` | The early-stop record — a kill at phase 1, which is the cheapest correct outcome. |

## Related

- `kill-or-keep-criteria` — thresholds for a product line that already exists; this gate runs before one does.
- `what-you-dont-know-about-launch-pre-mortem` — launch-time risk; the PR/FAQ is concept-time, and a pre-mortem on a concept that should have been killed is wasted.
- `product-discovery` — what `proceed` authorises you to start.
- `architecture-decision-records` — the PRFAQ Record is a decision record with a fixed schema; log it the same way.

## Sourcing note

The structural anchors (announcement-first, past tense, the separate FAQ banks, the narrative rather than slides) come from Bryar & Carr, *Working Backwards*, St. Martin's Press, 2021, and from Amazon's 2004 internal narrative-memo mandate as re-described in the 2018 Amazon shareholder letter. No live Amazon specification was reachable at authoring time (2026-08-04); nothing here is presented as a quoted Amazon standard, and no adoption or success statistic is claimed for the practice.
