# Idea → Validated MVP launch

A 7-stage chain for one founder taking one raw idea from notebook to a launched
MVP with first paying customers — or a clean kill backed by evidence.

## Intent

Raw idea in a notebook → paid landing page + working MVP with first 5 paying
users. The exit condition is a written go/no-go decision backed by problem
evidence, scoped spec, shipped product, and at least 5 paying customers (or
documented kill rationale).

## Scope

A solo founder takes one raw idea through Discovery, Validation, Spec, Build,
Beta, Launch, and Decide. The playbook is built for a single operator with no
team to delegate to and a small enough budget that "paid traffic" means tens of
dollars, not thousands. What's IN: customer interviews, paid landing tests,
spec compression, MVP build, beta with friendly users, launch with checkout,
and a written decision. What's OUT: hiring, fund-raising, multi-product
strategy, enterprise compliance. Done is reached when the Decide stage has
produced a written continue / pivot / kill document with evidence trail.

## Stages

### 1. Discovery

From multiple raw ideas to one chosen problem with documented Jobs-To-Be-Done.

Tasks:
- Generate idea variants and pick top 1–3 by founder-market fit.
- Define the Job-To-Be-Done and the painful workflow it replaces.
- Survey 10 prospects for problem severity and frequency.

Decision gate: advance if ≥7/10 interviews confirm the pain is top-3 in their
workflow; pivot to another idea variant if 4–6 confirm; kill if ≤3.

Methodologies (all resolve under `knowledge/solo/research/`):
- `solo/research/market-researcher/idea-generation`
- `solo/research/researcher/jobs-to-be-done`
- `solo/research/researcher/problem-validation`

Outputs: idea brief (1 page), JTBD statement, 10 problem-interview notes.

### 2. Validate

Confirm willingness-to-pay before any code is written.

Tasks:
- Define value proposition tied to the JTBD.
- Run 5 follow-up interviews focused on pricing signal.
- Identify minimum viable pricing tier.

Decision gate: advance if ≥3/5 prospects say "yes, I would pay $X today" with
a specific number; pivot pricing/scope if vague; kill if pricing softens on
every call.

Methodologies:
- `solo/research/researcher/value-proposition-design`
- `solo/research/researcher/pricing-research`
- `solo/research/researcher/user-interviews`

Outputs: value-prop canvas, pricing hypothesis with 3 tiers, 5
willingness-to-pay quotes.

### 3. Spec

Smallest possible build scope with explicit cuts.

Tasks:
- Write 1-page spec covering only the validated workflow.
- Cut anything not on the critical path to first payment.
- Define acceptance criteria per feature.

Decision gate: advance if spec fits on one page AND every feature maps to an
acceptance criterion. Iterate the spec if either fails.

Methodologies:
- `solo/sdd/sdd-planning/writing-specifications`
- `solo/sdd/sdd-planning/spec-structure`
- GAP — `mvp-scope-cutting-template` (see `gaps[]`).

Outputs: `spec.md` (1 page max), explicit non-goals list.

### 4. Build

Working MVP that delivers the validated value, nothing more.

Tasks:
- Implement only spec items in order of dependency.
- Skip features that don't block the first-payment flow.
- Deploy to a real URL daily, however ugly.

Decision gate: advance when a stranger can complete the validated workflow
without help; stay in Build if anyone needs hand-holding.

Methodologies:
- `solo/sdd/sdd-planning/writing-implementation-plans`
- `solo/sdd/sdd-planning/impl-plan-100k-rule`

Outputs: working URL with the validated workflow end-to-end, implementation
log (shipped vs cut).

### 5. Beta

5 friendly users run the MVP under real conditions.

Tasks:
- Invite 5 prospects from Discovery interviews.
- Observe usage; do not pre-explain features.
- Log every confusion point.

Decision gate: advance if ≥3/5 reach the value moment unaided; iterate UX if
1–2; re-spec if 0.

Methodologies:
- GAP — `beta-session-observation-protocol` (see `gaps[]`).
- `solo/research/researcher/user-interviews`

Outputs: 5 session-observation notes, bug + confusion log.

### 6. Launch

Paid landing page live; first paying users converted.

Tasks:
- Build paid landing with checkout.
- Convert beta users to paying customers.
- Open public sign-up.

Decision gate: advance if ≥5 paying customers in 14 days post-launch;
otherwise Decide.

Methodologies:
- GAP — `paid-landing-checkout-stack` (see `gaps[]`).

Outputs: live paid landing URL, first 5 paid invoices.

### 7. Decide

Written go/no-go backed by evidence.

Tasks:
- Compile evidence trail: interviews + metrics + paying-user feedback.
- Write explicit decision: continue / pivot / kill.
- If continue: define the next 30-day milestone.

Decision gate: required output is a written decision — no "maybe", no
"see how it goes".

Methodologies:
- GAP — `solo-go-no-go-decision-rubric` (see `gaps[]`).

Outputs: decision doc with evidence and next-30-days plan (or kill rationale).

## Common pitfalls

- Building before Validate — easy to confirmation-bias your way into code.
- Cutting Decide when the MVP feels "almost there" — that's exactly when it
  matters.
- Treating Discovery interviews as sales calls — kills signal.

## Quality checklist

- Can I show a stranger the decision doc and they understand WHY we shipped or
  killed?
- Did I actually cut something during Spec, or did I just rename items?
- Did the 5 paying users find me, or did I beg friends?

## Related playbooks

- `solo-landing-page-conversion`
- `solo-pricing-experiment`

## Gaps (status: draft until empty)

Five methodologies still missing — see `gaps[]` in `playbook.yaml`. This
playbook cannot move to `status: published` until each is authored under
`knowledge/solo/...` and the gap entry is removed.
