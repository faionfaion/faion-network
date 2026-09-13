# Freelancer Rate Raise Letter Template

## Summary

**One-sentence:** Battle-tested raise-announcement letter for retainer clients with grace-period framing — not a generic 'difficult-conversations' lecture.

**One-paragraph:** Battle-tested raise-announcement letter for retainer clients with grace-period framing — not a generic 'difficult-conversations' lecture. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- quarterly rate review для retainer client.
- grace period framing замість «effective immediately».
- ціна обґрунтована value delta, не CPI.
- letter ships with churn-risk classifier (stay / negotiate / churn).
- post-letter follow-up на T+7 з конкретним path вперед.

## Applies If (ALL must hold)

- The client is on a retainer or recurring engagement with a signed contract whose rate-change notice clause can be read.
- At least one measurable value delta since the current rate was set exists in the engagement log (deliverable, metric moved, scope added, capability the client depends on).
- No rate change has been applied to this client in the last 12 months, or a material scope change since then is documented.
- The freelancer knows the client's share of trailing-12-month revenue and can name the client's realistic alternatives.

## Skip If (ANY kills it)

- The only available justification is inflation, CPI or the freelancer's own costs; the letter would be a cost-line note procurement caps.
- The client is above 30% of revenue, would likely churn, and no replacement-revenue pipeline exists yet; defer until it does.
- A rate change already took effect for this client inside the last 12 months with no documented scope change.
- The engagement is project-based with a fixed quote and no recurring rate to raise; reprice at the next quote instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Retainer contract with the rate-change notice clause and billing cycle | contract PDF with clause numbers | contract store |
| Engagement log since the current rate was set: deliverables, metrics before and after, scope added | dated log or ticket export | engagement file |
| Trailing-12-month revenue by client | spreadsheet or accounting export | finance |
| In-flight signed SOWs, accepted quotes and prepaid retainer periods | list with references and end dates | contract store / invoicing |
| Client feedback or NPS, payment history, renewal date | notes + invoice ledger | engagement file, bank |
| Banned-phrase list for the tone check | the list in `content/01-core-rules.xml` r-business-notice-tone-no-apology | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: 30-day grace period, value delta not CPI, single new rate, signed work honoured, no concession in letter, churn-risk classified, T+7 follow-up, business-notice tone | 2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: one rate with old, new and %, effective date >=30 days and >=1 cycle, at most one raise per 12 months, value deltas citing inputs_used, in-flight work protected, letter checks (250 words, banned phrases, no concession), churn class with evidence and replacement plan over 30%, T+7 follow-up paths, acknowledgement gate; valid + invalid examples, forbidden patterns | ~4200 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 950 |
| `content/04-procedure.xml` | essential | 8 steps: pin inputs, classify churn and cover concentration, set one number and the effective date, pull value deltas, list in-flight work, write the letter and hold the concession, schedule T+7 and send, apply the rate only on written acknowledgement | ~1800 |
| `content/05-examples.xml` | recommended | Complete artefact for a EUR 6,000 retainer raised 12% with 62 days' notice, the 196-word letter, a note per non-obvious value, and a bad artefact with the validator output | ~2500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-rate-raise-letter-template.md.j2` | Working spec skeleton with 5-line header |
| `templates/freelancer-rate-raise-letter-template.md` | Working spec skeleton with 5-line header Generated from `templates/freelancer-rate-raise-letter-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in version for smoke testing |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-rate-raise-letter-template.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[freelancer-payment-chase-script-library]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
