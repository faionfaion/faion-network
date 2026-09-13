# Freelancer Payment Chase Script Library

## Summary

**One-sentence:** Escalation ladder of payment-chase emails (polite → firm → legal-mention) tuned to preserve the relationship while collecting.

**One-paragraph:** Escalation ladder of payment-chase emails (polite → firm → legal-mention) tuned to preserve the relationship while collecting. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned checklist artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- invoice прострочений, але relationship хочеш зберегти.
- ladder: polite (T+3) → firm (T+10) → legal-mention (T+30).
- кожен крок — typed input (invoice id, amount, contract clause).
- log send + response → дані для повторного аудиту контракту.
- stop-conditions: client paid OR ladder exhausted → handoff to legal.

## Applies If (ALL must hold)

- An invoice is past the due date printed on it, and its number, amount, invoice date, due date and payment-terms clause can be copied from the invoicing system and the signed contract.
- The client relationship is worth keeping: the freelancer wants the next engagement, not only this payment.
- A finance or accounts-payable contact at the client can be identified for the firm rung.
- The freelancer can read the bank or payment-processor ledger before each send to check for payment.

## Skip If (ANY kills it)

- The client has raised a written dispute about the invoice or the work; that routes to dispute handling, not to a chase ladder.
- The invoice or the contract cannot be reached in the system of record; a chase drafted from memory is worse than silence.
- The freelancer has already decided to end the relationship and go straight to collections or a claim; the ladder's relationship-preserving rungs have no purpose.
- Fewer than 3 days have passed since the due date; nothing may be sent yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| The invoice: number, amount with currency, invoice date, due date, PDF or link | invoice record + PDF | invoicing system |
| The signed contract: payment-terms clause id, late-interest or fee clause (if any), suspension or IP clauses, written-notice channel | contract PDF with clause numbers | contract store |
| Governing-law late-payment statute where the contract is silent (UK: Late Payment of Commercial Debts (Interest) Act 1998; EU: Directive 2011/7/EU) | act name and current rate | legislation site |
| Both parties' full legal names and addresses; client sponsor and finance / accounts-payable contacts | contact record | contract front page, client onboarding notes |
| Bank or payment-processor ledger for the invoice | statement or dashboard | bank / processor |
| Named legal or collections contact for the handoff when the ladder is exhausted | name + email | freelancer's adviser or agency |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: three rungs clocked from due date, invoice facts on every rung, fees only from contract or statute, polite rung assumes oversight, firm rung deadline, formal letter before action, stop on payment or dispute, send log feeds renewal terms | 2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for one invoice's ladder: six invoice facts, parties, fee basis (clause / statute / none), exactly three rungs at T+3 / T+10 / T+30 with per-rung constraints (120 words, pay-by within 7 days, 7-14 day final deadline), stop state, send log, renewal terms change; valid + invalid examples, forbidden patterns | ~4300 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 950 |
| `content/04-procedure.xml` | essential | 8 steps: pin invoice facts and parties, source the fee basis and notice channel, schedule three rungs from the due date, check stop conditions before every send, polite rung, firm rung, formal notice, handoff and renewal terms | ~1800 |
| `content/05-examples.xml` | recommended | Complete ladder for a GBP 4,800 net-15 invoice paid after the polite rung, the three rung texts, a note per non-obvious value, and a bad ladder with the validator output | ~2450 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-payment-chase-script-library.md.j2` | Working checklist skeleton with 5-line header |
| `templates/freelancer-payment-chase-script-library.md` | Working checklist skeleton with 5-line header Generated from `templates/freelancer-payment-chase-script-library.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-payment-chase-script-library.py` | Validate the checklist artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[freelancer-rate-raise-letter-template]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
