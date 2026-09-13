# Graceful Offboard Script

## Summary

**One-sentence:** Bad-fit offboarding script that ends a client engagement without damaging brand or referral pipeline — strategic move, not a confession.

**One-paragraph:** Bad-fit offboarding script that ends a client engagement without damaging brand or referral pipeline — strategic move, not a confession. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- QBR показує bad-fit client → agency-side offboard.
- frame як value alignment, не «ми не справляємось».
- handover plan + recommended-alternative агенція.
- referral pipeline не повинен бути зруйнованим.
- post-offboard NPS / testimonial запит, не silence.

## Applies If (ALL must hold)

- The QBR source of record shows at least two quantified bad-fit signals against stated targets (margin over two or more quarters, out-of-scope requests over the cap, days-to-pay over terms, hours over budget, satisfaction under threshold).
- The signed contract's termination clause (notice period, minimum term, cure period) is readable and the agency intends to honour it.
- The agency holds assets for the client (ad or analytics accounts, DNS, repositories, design files, documentation) that can be inventoried and transferred.
- A partner or alternative provider exists whose core matches where the client's needs are moving.
- The named account owner can hold a live conversation with the client sponsor.

## Skip If (ANY kills it)

- Only one bad-fit signal, or a single incident: that is an intervention (repricing, scope reset), not an exit; revisit at the next QBR.
- The client is terminating, not the agency; run the contract's termination-assistance clause instead of this script.
- The contract's termination clause cannot be read or the notice period cannot be honoured; the exit would become a breach.
- The relationship has already broken into a dispute or non-payment; that routes to collections or legal, not to a fit-framed offboard.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| QBR data for the account: gross margin by quarter, scope-change requests vs cap, days-to-pay, hours vs budget, satisfaction score | spreadsheet or dashboard export | QBR pack / finance |
| Signed contract with termination clause id, notice period, minimum term, work-product ownership and termination-assistance clauses | contract PDF with clause numbers | contract store |
| Prepaid or committed periods and their amounts | invoicing record | finance |
| Inventory of every system the agency touches for the client (ad, analytics, DNS, credentials, repos, design, content, docs) | list with owner and access level | account team / IT |
| The client's stated roadmap or upcoming needs | QBR notes | account owner |
| Partner network with a confirmed willingness to take introductions | contact list with confirmation dates | agency leadership |
| Banned-phrase list for the framing check | the list in `content/01-core-rules.xml` r-frame-as-fit-not-confession | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: two QBR bad-fit signals, fit framing not confession, exit date honours termination clause, handover asset inventory, confirmed alternative provider, live delivery then written, T+30 feedback request, root cause changes intake | 2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: two or more QBR signals with value and target, termination clause and last service date with prepaid disposition, fit framing with banned-phrase and criticism checks, per-asset handover inventory with transfer dates, confirmed alternative, live-then-written delivery within one business day, T+30 feedback with promoter and non-promoter actions, root cause and intake change; valid + invalid examples, forbidden patterns | ~4900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 1000 |
| `content/04-procedure.xml` | essential | 9 steps: evidence the bad fit, read the clause and set the date, build the asset inventory, confirm the alternative, write and check the script, schedule T+30 and deliver live, written follow-up within a business day, handover on schedule, internal record and feedback request | ~1850 |
| `content/05-examples.xml` | recommended | Complete offboard for a retail client at 11% margin for three quarters, the written follow-up text, a note per non-obvious value, and a bad artefact with the validator output | ~2800 |
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
| `templates/graceful-offboard-script.md.j2` | Working spec skeleton with 5-line header |
| `templates/graceful-offboard-script.md` | Working spec skeleton with 5-line header Generated from `templates/graceful-offboard-script.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in version for smoke testing |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graceful-offboard-script.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[freelancer-rate-raise-letter-template]]
- [[contractor-onboarding-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
