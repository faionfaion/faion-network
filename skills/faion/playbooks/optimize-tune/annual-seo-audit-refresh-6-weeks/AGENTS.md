# Annual SEO Audit & Refresh (6 weeks)

A 9-stage playbook for the global angle. Tier: **geek**. Complexity: **deep**.

## Context

Full technical + content SEO audit, AI-overview readiness review, refresh of top-30 pages, cannibalization cleanup, internal-link rewiring, and 12-month forward plan. 'Done' = audit report delivered, refresh sprint executed for top-30 pages, AI-overview adaptation merged across the priority cluster, and the next-year SEO plan is in roadmap with quarterly OKRs.

## Outcome

A complete delivery cycle from frame to decision: artifacts shipped, metrics flowing, a written continue/pivot/kill verdict that next quarter's planning can act on.

## Steps

### 1. Frame

Lock the goal, owner, success metric, and time-box.

Tasks:
- Draft a one-paragraph charter with goal, owner, success metric, time-box
- List explicit non-goals so scope cannot creep
- Identify stakeholders and their decision rights

Methodologies:
- `geek/marketing/seo-manager/google-ai-overviews-optimization`
- `solo/marketing/seo-manager/seo-techniques`

Outputs:
- Charter doc (1 page)

Decision gate: Advance only with a written charter that all stakeholders read and signed off.

### 2. Discover

Talk to real users / stakeholders / sales — kill assumptions before they enter the plan.

Tasks:
- Run 5-10 short interviews tied to the charter goal
- Capture verbatim quotes, not paraphrases
- Update the charter if discovery contradicts an assumption

Methodologies:
- `geek/marketing/seo-manager/technical-seo-for-ai`
- `solo/marketing/seo-manager/topical-authority`

Outputs:
- Discovery notes with quotes

Decision gate: Advance only when discovery either confirms the charter or forces a documented re-charter.

### 3. Research

Gather the inputs needed to plan: data, prior work, competitors, constraints.

Tasks:
- Pull the relevant data extract / dashboards / prior decks
- Scan competitors and prior internal attempts
- Document constraints (legal, tech, brand) up front

Methodologies:
- `pro/marketing/growth-marketer/north-star-metric`
- `solo/marketing/seo-manager/zero-click-search-adaptation`

Outputs:
- Research brief with sources

Decision gate: Advance once research surfaces no blocker; otherwise loop with stakeholders.

### 4. Plan

Convert the charter + research into a sequenced plan with owners.

Tasks:
- Break the work into 3-7 phases with explicit exit-criteria
- Assign an owner per phase
- Wire metrics + dashboards before execution starts

Methodologies:
- `pro/marketing/growth-marketer/ops-metrics-basics`

Outputs:
- Plan doc with Gantt or phase table

Decision gate: Advance only when each phase has a named owner and exit-criterion.

### 5. Produce

Create the core artifacts: assets, content, code, campaigns, configs.

Tasks:
- Build the core deliverables per phase plan
- Hold a draft review with the named owner before publish
- Track WIP visibly so blockers surface fast

Methodologies:
- `pro/marketing/gtm-strategist/ops-annual-planning-process`

Outputs:
- Drafts of all core artifacts

Decision gate: Advance when drafts pass internal review against the charter, not personal taste.

### 6. Ship

Push live: deploy, publish, launch the campaign, flip the switch.

Tasks:
- Run the launch checklist (dependencies, tracking, comms)
- Publish on schedule; do not pre-leak
- Confirm tracking is flowing in real-time on a dashboard

Methodologies:
- `pro/marketing/gtm-strategist/ops-annual-planning-templates`

Outputs:
- Launch evidence (URLs / receipts)

Decision gate: Advance only with tracking visibly flowing; otherwise hold launch.

### 7. Stabilize

Make the new thing not collapse the moment attention moves elsewhere.

Tasks:
- Document the runbook for whoever inherits this
- Set alarms on the success metric so silent drift surfaces
- Hand off ownership formally if not staying with you

Methodologies:
- `solo/marketing/content-marketer/growth-content-marketing`

Outputs:
- Runbook + ownership transfer

Decision gate: Advance only after the next owner can run this from the runbook without you.

### 8. Measure

Read the metrics against the plan; separate noise from signal.

Tasks:
- Compare actuals vs charter success metric
- Split cohort/segment/channel to find what drove the result
- Document confounders before drawing conclusions

Methodologies:
- `solo/marketing/seo-manager/growth-seo-link-building`

Outputs:
- Measurement readout (1 page)

Decision gate: Advance when readout passes a peer sniff-test against confounders.

### 9. Iterate-or-close

Decide: continue, kill, or hand off to BAU.

Tasks:
- Hold the retro on what shipped vs what was planned
- Decide continue / pivot / kill / hand-off in writing
- If continue: define next 30-day milestone with metrics

Methodologies:
- `solo/marketing/seo-manager/seo`

Outputs:
- Decision doc with next steps

Decision gate: Required output: a written decision; no "let's see".

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/geek/marketing/seo-manager/google-ai-overviews-optimization`
- `knowledge/geek/marketing/seo-manager/technical-seo-for-ai`
- `knowledge/pro/marketing/growth-marketer/north-star-metric`
- `knowledge/pro/marketing/growth-marketer/ops-metrics-basics`
- `knowledge/pro/marketing/gtm-strategist/ops-annual-planning-process`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
