# Productize a recurring engagement into a fixed-scope offer

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** deep · **Angle:** synthesis

## Why this playbook exists

Take one repeatedly-sold engagement (e.g. 'Stripe integration audit', 'Next.js perf pass', 'CI pipeline setup') and convert it into a named, fixed-price productized service with a public landing page, SOP, intake form, and a delivery checklist that lets you book it without a discovery call.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Mine the pattern

**Intent:** Pull a candidate from past invoices.

**Tasks**
- Tag last 12 months of engagements by type
- Find the most repeated, highest-margin pattern
- Validate it's still in demand by 3 prospect calls

**Outputs**
- Engagement tag report
- Demand validation note

**Decision gate**

Advance only when one pattern is dominant AND validated by external prospects.

### Stage 2 — Scope + price

**Intent:** Fixed scope + fixed price + clear upsell ladder.

**Tasks**
- Write 1-page scope (what's IN, what's OUT)
- Set fixed price + scope-cap + upsell tier prices
- Draft pre-qualifying intake form

**Outputs**
- Scope doc
- Pricing ladder
- Intake form

**Decision gate**

Advance only when intake form weeds out obvious bad fits.

### Stage 3 — Build the surface

**Intent:** Landing page + booking flow + delivery checklist live.

**Tasks**
- Build landing page from template
- Wire booking flow to intake form
- Write delivery SOP / checklist

**Outputs**
- Landing live
- Booking flow
- Delivery SOP

**Decision gate**

Advance only when end-to-end booking works without your manual intervention.

### Stage 4 — Soft-launch

**Intent:** Sell to 3-5 past clients; harvest case studies.

**Tasks**
- Send tailored offer to past clients fitting the pattern
- Deliver against SOP; refine based on friction
- Publish 1-page case studies from soft-launch deliveries

**Outputs**
- 3-5 paid soft-launch deliveries
- Case studies live

**Decision gate**

Advance only with ≥3 paid deliveries + ≥2 published case studies.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `engagement-pattern-mining-from-past-invoices` (stage 1) — Stage 1 (Mine the pattern) references this; no methodology exists yet.
- `productized-service-candidate-selection` (stage 1) — Stage 1 (Mine the pattern) references this; no methodology exists yet.
- `scope-cap-and-upsell-laddering` (stage 2) — Stage 2 (Scope + price) references this; no methodology exists yet.
- `pre-qualifying-intake-form` (stage 2) — Stage 2 (Scope + price) references this; no methodology exists yet.
- `productized-service-landing-page-template` (stage 3) — Stage 3 (Build the surface) references this; no methodology exists yet.
- `productized-service-launch` (stage 4) — Stage 4 (Soft-launch) references this; no methodology exists yet.
- `past-client-soft-launch-sequence` (stage 4) — Stage 4 (Soft-launch) references this; no methodology exists yet.
- `single-page-case-study-generation` (stage 4) — Stage 4 (Soft-launch) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a deep-complexity synthesis-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

## Anti-patterns to avoid

- Running the stages out of order because one feels more urgent. Order encodes risk: skipping earlier stages usually means absorbing risk in a later stage where the cost is higher.
- Treating outputs as optional. Every stage requires a written artifact — that artifact is what makes the next decision-gate verifiable.
- Letting the client write your scope, your timeline, or your contract clauses. The whole point of this playbook is that *you* run a deterministic pipeline; the client engages with the pipeline, not the other way around.
- Skipping the closure / retro step. The compounding value of running this playbook many times is in the lessons captured at the end. Without retros, you re-learn the same expensive lessons every quarter.

## Agent prompt hints

If you are routing this playbook through `faion get-content` for an agent:

- Ask the agent to produce *each* stage's outputs as named files before moving to the next stage. Reject hand-wave outputs.
- Have the agent state the decision-gate condition out loud after producing outputs, and pass the gate before continuing.
- For any gap in the methodology chain (see *Gaps in the methodology chain* above), the agent should explicitly mark its substitute approach so you can backfill the missing methodology later.
