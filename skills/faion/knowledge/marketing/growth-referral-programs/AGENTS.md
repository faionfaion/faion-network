# Growth Referral Programs

## Summary

**One-sentence:** Generates a referral-program spec: trigger event, incentive structure, K-factor projection, fraud guard, lifecycle emails, landing pages.

**One-paragraph:** Generates a referral-program spec: trigger event, incentive structure, K-factor projection, fraud guard, lifecycle emails, landing pages. Use it when product має nps >= 30 (users готові рекомендувати). The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Product має NPS >= 30 (users готові рекомендувати).
- Unit economics дозволяють double-sided incentive.
- Fraud detection адекватний для self-referral abuse.
- Lifecycle email + landing infra може приймати referral params.

## Applies If (ALL must hold)

- An NPS or willingness-to-recommend survey on active users from the last 90 days exists with its sample size and date, and the score is at least 30.
- The product has an instrumented value event (first successful outcome, activation milestone) and the share of users reaching it is known; the prompt will fire there, not at sign-up.
- Blended paid CAC and first-order gross margin or expected LTV are known, so a double-sided reward can be sized at or below both.
- Sign-up and checkout expose payment instrument, device fingerprint, IP and email so self-referral can be matched, and reward fulfilment can be keyed on (referrer_id, referee_id, qualifying_event).
- The landing page and lifecycle email infrastructure accept a referral parameter and the account-creation path can persist the referrer link server-side.

## Skip If (ANY kills it)

- No NPS measurement exists or the score is below 30: measure it first; an incentive below the threshold pays detractors to send lukewarm invitations.
- The only reward the team will fund is one-sided or releases on account creation, and they will not change it.
- The landing page or email stack cannot carry a per-user referral parameter and attribution would rest on utm_source or the referrer's word.
- Fewer than 500 invites and 50 referrers are available or plannable before a K-factor is demanded, and the sponsor wants a viral growth curve written into the spec anyway.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| NPS or willingness-to-recommend survey | score, sample size, population (active users), survey date within 90 days | product analytics or survey tool |
| Value-event reach | instrumented event name and the share of sign-ups reaching it | product analytics |
| Unit economics | blended paid CAC, average first order, first-order gross margin or expected LTV | finance / growth model |
| Beta or first-cycle referral counts | invites sent, referee sign-ups, active referrers, trigger-to-qualifying timestamps (at least 500 invites, 50 referrers) | referral event log |
| Refund and chargeback windows | days | payments / finance |
| `templates/k_factor.py`, `templates/emails.md.j2`, `templates/landing-page.md.j2`, `templates/growth-referral-programs.spec.md.j2` | K computation, lifecycle copy, landing copy, spec skeleton | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: NPS 30 gate, trigger at value moment, reward on qualifying event, double-sided within unit economics, self-referral fraud guard and idempotent rewards, K-factor on 500+ invites, server-side attribution, lifecycle sequence, disclosure and terms | 2500 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the referral-programme spec: NPS gate (active users, 90 days, at least 30), trigger event with reach, qualifying event with minimum order value stated on page and emails, double-sided incentive whose cost is at or below paid CAC and a share of margin or LTV, four-signal fraud guard with hold and idempotency tuple, K on 500+ invites and 50+ referrers as i x c with cycle time and the 1/(1-K) multiplier, server-side attribution, announcement / one reminder / two-sided confirmation, disclosure and terms; valid and invalid specs; 9 forbidden patterns | 6050 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 1150 |
| `content/04-procedure.xml` | essential | 8 steps: measure the NPS gate, name the trigger event, define the qualifying event, size the double-sided incentive against CAC and margin, build the fraud guard, wire server-side attribution, compute K on 500 invites with k_factor.py, write lifecycle, landing page and terms and validate | 1900 |
| `content/05-examples.xml` | recommended | Complete spec for a B2B SaaS exporting tool (NPS 42, prompt on first_successful_export, reward on a 50 USD first order, 20 + 20 USD against CAC 95 and margin 126, K 0.741 on 4,200 invites as a 3.86x multiplier, 14-day reminder, published terms) with a note per value, plus a pay-on-signup spec and what the validator prints | 2550 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-growth-referral-programs.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-referral-programs.spec.md.j2` | Markdown spec skeleton with 5-line header |
| `templates/growth-referral-programs.spec.md` | Markdown spec skeleton with 5-line header Generated from `templates/growth-referral-programs.spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-referral-programs.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |
| `templates/emails.md.j2` | Two-email referral-program lifecycle sequence — announcement + no-referrals-yet reminder. |
| `templates/emails.md` | Two-email referral-program lifecycle sequence — announcement + no-referrals-yet reminder. Generated from `templates/emails.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/landing-page.md.j2` | Referral-program landing page copy — headline, how-it-works, live stats, FAQ. |
| `templates/landing-page.md` | Referral-program landing page copy — headline, how-it-works, live stats, FAQ. Generated from `templates/landing-page.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-referral-programs.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
