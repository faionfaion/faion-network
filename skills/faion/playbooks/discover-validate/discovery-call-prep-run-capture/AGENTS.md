# Discovery call prep + run + capture

**Persona:** P3 Technical Freelancer · **Tier:** solo · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

30-min prospect call: walk in with a hypothesis, walk out with enough signal to draft a proposal OR a clean disqualify. Done = call notes saved, fit score recorded, next-step email sent within 24h.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Prep

**Intent:** Walk into the call with hypothesis, agenda, and disqualifiers.

**Tasks**
- Research prospect (company, role, public artefacts)
- Write 3 hypotheses about their pain
- Draft an agenda with explicit disqualifiers

**Outputs**
- Pre-call note
- Hypotheses doc
- Agenda + disqualifiers

**Decision gate**

Advance only with prep notes in writing. Winging it bias kills signal.

### Stage 2 — Run

**Intent:** Run a 30-min call: listen, capture signal, avoid pitching.

**Tasks**
- Open with prospect's context, not yours
- Use Mom Test questions; avoid yes/no leading
- End with explicit next step

**Outputs**
- Live call recording / notes

**Decision gate**

Call closes only when next step is verbally agreed.

### Stage 3 — Capture

**Intent:** Save notes, score fit, send next-step within 24h.

**Tasks**
- Transcribe key quotes within 4h
- Score fit on rubric
- Send next-step email with proposal/decline within 24h

**Outputs**
- Call notes file
- Fit score
- Next-step email sent

**Decision gate**

Cycle closes only when fit score recorded + next-step sent.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelancer-discovery-call-template` (stage 2) — Stage 2 (Run) references this; no methodology exists yet.
- `solo-lead-qualification-rubric` (stage 3) — Stage 3 (Capture) references this; no methodology exists yet.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a medium-complexity atomic-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

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
