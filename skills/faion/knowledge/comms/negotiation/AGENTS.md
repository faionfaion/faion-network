# Negotiation and Persuasion

## Summary

**One-sentence:** Generates a negotiation preparation brief: BATNA + ZOPA computation, principled-negotiation interest map, and Cialdini-aligned persuasion levers.

**One-paragraph:** A framework for interest-based negotiation that replaces positional bargaining with mutual-gain problem solving. Core models: Principled Negotiation (Fisher & Ury — separate people from problem, focus on interests, generate options, use objective criteria), BATNA/ZOPA analysis for leverage calculation, Cialdini's 6 Principles for persuasion copy. Tactical layer: anchoring, silence, bracketing, the flinch, the nibble. Output: a structured prep brief that scores leverage before the conversation.

**Ефективно для:**

- Pricing conversation for a contract or salary.
- Vendor negotiation with multiple terms in play.
- Investor term-sheet discussion.
- Cofounder equity / role split.

## Applies If (ALL must hold)

- Both parties want the deal (positive ZOPA likely).
- There is time to prepare (not a flash auction).
- Multiple terms are negotiable (not single-dimension).
- Author has decision authority on at least one term.

## Skip If (ANY kills it)

- Zero-sum mandatory rejection (regulatory ban) — no negotiation possible.
- Author has no BATNA — no leverage, plan one first.
- Counterparty is in crisis — manipulation risk.
- Decision is purely emotional — different methodology applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| BATNA | best alternative to negotiated agreement | author |
| Counterparty interests | what they want + why | research |
| Negotiable terms | list of dimensions | author |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[selling-ideas]] | SPIN before negotiation when pain not yet established |
| [[stakeholder-communication]] | mode selection before the conversation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interest-mapping` | sonnet | Judgment on the 'why' for both sides. |
| `zopa-calc` | haiku | Pure arithmetic. |
| `lever-selection` | sonnet | Honest tagging requires judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/negotiation-prep.txt` | Negotiation prep brief skeleton |
| `templates/zopa-calculator.py` | Compute ZOPA from reserves + render summary |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-negotiation.py` | Validate negotiation artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[selling-ideas]]
- [[stakeholder-communication]]
- [[conflict-resolution]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. Gates on BATNA concreteness, ZOPA sign, and presence of objective criteria. Failure at any gate halts or routes to the corresponding repair rule.
