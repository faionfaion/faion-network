# Employee Value Proposition (EVP)

## Summary

**One-sentence:** Five-pillar EVP (Compensation / Benefits / Career / Work Environment / Culture-Purpose), each pillar backed by ≥3 named proof points before external publication.

**One-paragraph:** Five-pillar EVP (Compensation / Benefits / Career / Work Environment / Culture-Purpose), each pillar backed by ≥3 named proof points before external publication. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- annual or quarterly EVP refresh — survey + exit data + benchmark.
- ≥3 proof points (program, budget, data) per pillar — no aspirational fluff.
- DEI numbers — UNVERIFIED placeholder, fill from HRIS only.
- post-pass scrub generic clichés («innovative», «passionate»).
- segmented messaging engineering / sales / ops замість one-size-fits-all.

## Applies If (ALL must hold)

- company has 50+ employees and inconsistent narrative across careers page, JDs, recruiter outreach, and offer letters.
- offer-acceptance rate is dropping or post-decline surveys cite 'didn't understand what makes you different.'
- annual employer brand refresh: synthesize survey data, exit interviews, competitor pages into a draft EVP.
- localizing or segmenting EVP for different audiences (engineering vs. sales, EU vs. US).

## Skip If (ANY kills it)

- pre-PMF startup (<20 people): EVP will change in three months — premature.
- acute reputation crisis (layoffs, scandal): fix the underlying issue first.
- one-off role hiring with no brand intent: a well-written JD suffices.
- company offers below-market compensation and refuses to address it — no narrative compensates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/employee-value-proposition.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-employee-value-proposition.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[employer-branding]]
- [[interview-methods]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
