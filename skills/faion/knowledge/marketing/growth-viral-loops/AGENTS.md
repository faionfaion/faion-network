# Growth Viral Loops

## Summary

**One-sentence:** Generates a viral-loop spec: invitation moment, K-factor target, cycle time, projected growth curve, friction-removal experiments.

**One-paragraph:** Generates a viral-loop spec: invitation moment, K-factor target, cycle time, projected growth curve, friction-removal experiments. Use it when product має natural sharing moment (collaborative / multiplayer / messaging). The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Product має natural sharing moment (collaborative / multiplayer / messaging).
- Instrumentation per share + per accepted invite.
- Existing K-factor >=0.4 — є шанс довести до >1 з оптимізацією.
- Cycle time відстежуваний (від send до accept).

## Applies If (ALL must hold)

- The product has a named event where a user shares, invites or sends to another person as part of getting their own value (collaboration, messaging, publishing, splitting a bill).
- invite_shown, invite_sent, invite_opened, invite_accepted and invitee_activated exist or can be added, each carrying an invite_id and the inviter's user_id so i, c and cycle time can be joined per invite.
- At least two full loop cycles of joined event data are available, so K can be decomposed into invites per active user and accept rate per invite and cycle time can be measured from timestamps.
- Current measured K is at least 0.4 if the sponsor expects a self-sustaining target; otherwise the team accepts a K-increment target anchored to a named benchmark.
- Invitee and organic D30 retention can be reported separately, and any reward can be triggered on an activation milestone rather than signup.

## Skip If (ANY kills it)

- No inherent sharing moment exists and the only candidate is a post-signup invite modal or a /refer page: run an activation or acquisition methodology, or design the sharing feature first.
- invite_sent and invite_accepted cannot be joined on an invite_id: the first deliverable is instrumentation, not a loop spec, and no K target is set until then.
- The sponsor wants a K above 1.0 written into the spec from a baseline below 0.4 or from no baseline at all.
- The loop's growth engine is a contact-list import that emails addresses without consent, and the team will not change it: the spec is not shippable under CASL, GDPR and the FTC guides.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Joined loop events | per-invite rows: invite_id, inviter_user_id, timestamps for invite_shown, invite_sent, invite_opened, invite_accepted, invitee_activated | product analytics warehouse |
| K components | invites per active user and accept rate per invite, each with window in days and sample size, over at least two cycles | warehouse query over the joined events |
| Cycle-time distribution | median days from the inviter's send event to the invitee's first send event | warehouse query |
| Invitee path conversions | measured drop-off at each step from first exposure to activated account, at most three steps | funnel query |
| Category K benchmark | range with a named source (templates/loop-projection.py lists consumer 0.10-0.30, B2B SaaS 0.05-0.20) | published practitioner benchmarks |
| `templates/loop-anatomy.md.j2`, `templates/referral-program.md.j2`, `templates/loop-projection.py` | anatomy worksheet, incentive design worksheet with the compliance checklist, projection model | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: K decomposed as i x c, cycle time measured and projected, K target anchored to baseline, inherent share moment, friction capped at 3 steps, five joinable loop events, reward on activation, consent and disclosure | 2450 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the viral-loop spec: inherent share event with an optional secondary incentivised loop, K as i x c with windows and samples, cycle time from timestamps, churn-free projection reproduced by loop-projection.py, K target anchored to baseline and benchmark, invitee path of at most 3 steps with friction experiments per step, five joinable events, invitee vs organic D30, activation-triggered incentive with caps and self-referral block, consent and disclosure; valid and invalid specs; 8 forbidden patterns | 4800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 950 |
| `content/04-procedure.xml` | essential | 8 steps: name the inherent share event, instrument the five joinable events, decompose K over two cycles, measure cycle time and run the projection, anchor the K target, map the invitee path and friction experiments, design any incentive on activation, clear consent and disclosure and validate | 1650 |
| `content/05-examples.xml` | recommended | Complete spec for a board-collaboration loop (board_shared, K 0.648 from 1.8 x 0.36, 6-day cycle, 1,000 to 2,838 users in 90 days, target 0.8 as an increment against a 0.05-0.20 benchmark, three-step invitee path, two friction experiments, invitee D30 0.41 vs 0.38, no incentive) with a note per value, plus a bolt-on referral page spec and what the validator prints | 2150 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-growth-viral-loops.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-viral-loops.spec.md.j2` | Markdown spec skeleton with 5-line header |
| `templates/growth-viral-loops.spec.md` | Markdown spec skeleton with 5-line header Generated from `templates/growth-viral-loops.spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-viral-loops.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |
| `templates/loop-anatomy.md.j2` | Viral loop anatomy worksheet — loop type, fit argument, action/artifact/distribution/motivation/friction breakdown, K-factor estimate, events to instrument. |
| `templates/loop-anatomy.md` | Viral loop anatomy worksheet — loop type, fit argument, action/artifact/distribution/motivation/friction breakdown, K-factor estimate, events to instrument. Generated from `templates/loop-anatomy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/referral-program.md.j2` | Referral program design worksheet — value proposition, reward mechanics, offer ladder, fraud rules, tracking, compliance checklist. |
| `templates/referral-program.md` | Referral program design worksheet — value proposition, reward mechanics, offer ladder, fraud rules, tracking, compliance checklist. Generated from `templates/referral-program.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-viral-loops.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
