---
slug: idea-validated-mvp-launch
tier: solo
group: solo-saas
persona: P1
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Solo founder takes one raw idea from notebook to a paid landing page + working MVP with first 5 paying users; exit when a written go/no-go decision is in hand backed by problem evidence, scoped spe...
content_id: 5f17afc6db77e538
methodology_refs:
  - mom-test
  - growth-reddit-marketing
  - spec-writing
  - value-proposition-design
  - decision-tree-tech-stack
  - growth-landing-page-design
  - product-analytics
  - writing-implementation-plans
  - feature-flags
  - growth-hacker-news-launch
  - idea-generation
  - logging-patterns
  - growth-indiehackers-strategy
  - naming-and-domains
  - trunk-based-development
  - growth-product-hunt-launch
  - niche-evaluation
  - backup-recovery
  - continuous-discovery
  - jobs-to-be-done
  - cloudflare-domain-dns
  - micro-mvps
  - pain-point-research
  - health-checks-autoheal
  - mvp-scoping
  - problem-validation-2026
  - ssl-tls-management
  - product-launch
  - user-interviews
---

# Idea → Validated MVP launch

## Intent

Solo founder takes one raw idea from notebook to a paid landing page + working MVP with first 5 paying users; exit when a written go/no-go decision is in hand backed by problem evidence, scoped spec, shipped product, and at least 5 paying customers (or a clean kill).

## Scope

Solo founder takes one raw idea from notebook to a paid landing page + working MVP with first 5 paying users; exit when a written go/no-go decision is in hand backed by problem evidence, scoped spec, shipped product, and at least 5 paying customers (or a clean kill).

## Stages

### 1. Discovery

From multiple raw ideas to one chosen problem with documented JTBD.

Tasks:
- Generate 5-10 idea variants from your domain pain
- Score each on founder-market fit and pain frequency
- Write a JTBD statement for the top candidate

Outputs:
- Idea brief (1 page)
- JTBD statement
- Founder-market fit score

Decision gate: Advance if top idea scores >=7/10 on founder fit AND pain frequency. Else pick the next candidate.

### 2. Problem validation

Confirm the pain is real and severe before any build commitment.

Tasks:
- Recruit 10 prospects from cold + warm channels
- Run Mom-test-style problem interviews (no pitch)
- Tag each transcript with severity and frequency

Outputs:
- 10 interview notes
- Severity/frequency tally
- Top-3 painpoint quotes

Decision gate: Advance if >=7/10 confirm pain is top-3 in their workflow. Pivot variant if 4-6. Kill if <=3.

### 3. Willingness to pay

Get specific pricing commitments before code.

Tasks:
- Run 5 follow-up calls with the top-pain segment
- Ask would you pay $X today with a concrete number
- Capture verbatim pricing reactions

Outputs:
- 5 willingness-to-pay quotes
- Pricing hypothesis with 3 tiers
- Value-prop canvas

Decision gate: Advance if >=3/5 say yes at $X today with a concrete number. Re-price if vague. Kill if every call softens.

### 4. Spec

Smallest possible build scope with explicit cuts.

Tasks:
- Write a 1-page spec covering only the validated workflow
- List explicit non-goals and cuts
- Define acceptance criteria per feature

Outputs:
- spec.md (1 page)
- Non-goals list
- Acceptance criteria table

Decision gate: Advance if spec fits on one page AND every feature maps to an acceptance criterion.

### 5. Build

Working MVP that delivers the validated value, nothing more.

Tasks:
- Implement spec items in dependency order
- Deploy to a real URL daily, however ugly
- Skip anything not blocking first payment

Outputs:
- Working URL with end-to-end flow
- Implementation log (shipped vs cut)
- CI green on main

Decision gate: Advance when a stranger can complete the workflow without help.

### 6. Beta

5 friendly users run the MVP under real conditions.

Tasks:
- Invite 5 prospects from Discovery
- Observe usage without pre-explaining
- Log every confusion point and bug

Outputs:
- 5 session notes
- Bug + confusion log
- Activation rate

Decision gate: Advance if >=3/5 reach the value moment unaided. Iterate UX if 1-2. Re-spec if 0.

### 7. Launch

Paid landing page live; first paying users converted.

Tasks:
- Build paid landing with Stripe checkout
- Convert beta users to paying customers
- Open public sign-up and ship to 2 channels

Outputs:
- Live paid landing URL
- First 5 paid invoices
- Initial traffic source mix

Decision gate: Advance if >=5 paying customers within 14 days post-launch.

### 8. Decide

Written go/no-go backed by evidence.

Tasks:
- Compile evidence trail (interviews + metrics + paying-user feedback)
- Write explicit continue/pivot/kill decision
- If continue, define the next 30-day milestone

Outputs:
- Decision doc with evidence
- Next-30-days plan OR kill rationale

Decision gate: Required output is a written decision - no maybe, no see how it goes.

### 9. Reflexion

Capture lessons into pattern + mistake memory.

Tasks:
- Write 1-page reflexion on what worked and what did not
- Update pattern memory with reusable assets
- Update mistake memory with traps to avoid next cycle

Outputs:
- Reflexion doc
- Pattern memory delta
- Mistake memory delta

Decision gate: Cycle closes when reflexion is committed and memories updated.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
