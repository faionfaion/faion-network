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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-negotiation.py` | Validate negotiation artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[selling-ideas]]
- [[stakeholder-communication]]
- [[conflict-resolution]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. Gates on BATNA concreteness, ZOPA sign, and presence of objective criteria. Failure at any gate halts or routes to the corresponding repair rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/negotiation-prep.txt`

```text
# Negotiation Preparation Template

## My Side

### Position
What I am asking for: [SPECIFIC]

### Interests
Why I want this:
1. [Interest 1]
2. [Interest 2]
3. [Interest 3]

### BATNA
If no deal: [My best alternative]
Walk-away point: [Minimum acceptable]

---

## Their Side (Predicted)

### Position
What they will likely ask for: [PREDICTION]

### Interests
Why they likely want it:
1. [Predicted interest 1]
2. [Predicted interest 2]

### BATNA
If no deal, they likely: [Their alternative]
Their urgency level: [High / Medium / Low — reason]

---

## ZOPA Analysis

My walk-away:    [VALUE]
Their walk-away: [VALUE]
Overlap exists:  [Yes / No / Unknown]

---

## Creative Options (mutual gain)
Ways to meet both parties' interests:
1. [Option 1]
2. [Option 2]
3. [Option 3]

## Objective Criteria
Standards both parties can reference:
- [Market rate source]
- [Industry standard]
- [Precedent from similar deal]

## Opening Move
First offer: [VALUE]
Rationale: [Why this anchors favorably without being insulting]
```

### `templates/zopa-calculator.py`

```python
def zopa(my_walk_away: float, their_walk_away: float, i_am_buyer: bool = True):
    """
    Compute the Zone of Possible Agreement (ZOPA).

    Args:
        my_walk_away:     the worst deal I will accept
        their_walk_away:  the worst deal they will accept (estimated)
        i_am_buyer:       True if I am buying (my_walk_away is a max price),
                          False if I am selling (my_walk_away is a min price)

    Returns:
        (low, high) tuple if ZOPA exists, None if no deal is possible.

    Notes:
        - If None is returned, creative options or BATNA improvement are needed
          before entering negotiation.
        - Values are monetary but the function works for any numeric scale.
    """
    if i_am_buyer:
        low = their_walk_away   # seller's minimum
        high = my_walk_away     # buyer's maximum
    else:
        low = my_walk_away      # seller's minimum
        high = their_walk_away  # buyer's maximum

    if low <= high:
        return (low, high)
    return None  # no ZOPA — negotiation cannot close at current positions


# Usage examples:
#
# Salary negotiation (I am the candidate = seller of labor):
# result = zopa(my_walk_away=80_000, their_walk_away=105_000, i_am_buyer=False)
# print(result)  # (80000, 105000) — deal possible, aim for top of range
#
# Vendor purchase (I am the buyer):
# result = zopa(my_walk_away=50_000, their_walk_away=45_000, i_am_buyer=True)
# print(result)  # (45000, 50000) — deal possible
#
# result = zopa(my_walk_away=40_000, their_walk_away=60_000, i_am_buyer=True)
# print(result)  # None — no overlap, need creative options
```
