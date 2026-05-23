# Project Closure

## Summary

**One-sentence:** Formal termination process: written deliverable acceptance, resource release, contract closure, lessons captured, documents archived, transition to operations.

**One-paragraph:** Formal termination process: written deliverable acceptance, resource release, contract closure, lessons captured, documents archived, transition to operations. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-project-closure.py` enforces the output contract.

**Ефективно для:**

- Capital projects with sponsor sign-off requirement.
- Vendor engagements requiring contract closure + final invoice.
- Programs handing over to ops / BAU teams.
- Compliance regimes requiring documented closure artefacts.

## Applies If (ALL must hold)

- Deliverables exist and are testable against acceptance criteria.
- Sponsor / customer is available for sign-off.
- Operations team is ready to receive handover.

## Skip If (ANY kills it)

- Project cancelled before delivery (use cancellation playbook instead).
- Ongoing program without natural end (use continuous review).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Acceptance criteria per deliverable | Markdown/CSV | PM + Sponsor |
| Lessons-learned capture | Markdown | PM + team |
| Archive destination | URL / folder | PMO |
| Handover doc | Markdown | PM + ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lessons-learned]] | closure feeds the lesson repository |
| [[benefits-realization]] | closure hands off to benefit tracking |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-acceptance` | sonnet | Judgement: evidence sufficiency per criterion. |
| `draft-handover` | sonnet | Judgement: what ops needs to operate. |
| `run-archive` | haiku | Mechanical archive walker + manifest. |

## Templates

| File | Purpose |
|------|---------|
| `templates/acceptance-form.md` | Acceptance form template: deliverable, criteria, evidence, sign-off |
| `templates/closeout-archive.sh` | Archive walker: copies artefacts to long-term store with manifest |
| `templates/closure-checklist.md` | Closure checklist template: acceptance, resources, contracts, lessons, archive, handover |
| `templates/final-report.md` | Final report template: scope delivered vs baseline, schedule + cost variance, lessons highlights |
| `templates/handover-doc.md` | Handover doc template: operating procedures, runbooks, support contacts |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-project-closure.py` | Validate the spec artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[lessons-learned]]
- [[benefits-realization]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

