# Verification Rung Placement Rule

## Summary

**One-sentence:** Produces a Rung Placement Record that routes every check to the cheapest instrument able to detect its defect — rung 1 static lint at zero tokens, rung 2 trigger evals scored mechanically, rung 3 a pairwise judge, rung H a person reading — and rejects any placement that cannot justify itself against the rung below.

**One-paragraph:** The whole of verification collapses into one operational question: for this specific failure, what is the cheapest instrument that can detect it? The rungs are not novel and they are not a maturity model — you do not graduate from rung 1 to rung 3. Their value is that they forbid the expensive mistake everyone makes, which is reaching for a model to catch a defect a regex would have caught for free. Our own live example: 528 broken reference slugs across 5,744 published files were being found by a review agent, at rung-3 prices, for a defect a twenty-line validator catches on every commit at zero cost. Placement also constrains what each rung is allowed to do once a check lands there — exact rules may block and heuristics may only flag, rung 3 is pairwise and capped at fifteen scenarios because the best debiased judge tested still only reaches κ=0.549, and rung H is a legitimate gate whose cost is founder-hours and whose job is to discover new checks rather than to repeat old ones.

**Ефективно для:**

- Deciding where a newly discovered defect class should be caught, before writing anything.
- Auditing an existing suite that is green and has never caught a real regression.
- Any team about to build an eval harness or a judge before it has a referential-integrity check.
- Solopreneurs deciding what to automate first when attention is the scarce resource.

## Applies If (ALL must hold)

- More than one verification instrument is available — at minimum, code and a person.
- Defects are recurring often enough that where they get caught matters.
- Someone is paying for the current instrument, in tokens, in wall-clock, or in their own hours.

## Skip If (ANY kills it)

- Only one instrument exists and there is nothing to route between.
- The question is what a gate should do when it breaks, not which gate to build — see `gate-fail-closed-rule`.
- The question is whether a phase may be promoted rather than which instrument verifies a check — see `quality-gates-confidence`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | R1 places the check by three questions. R2 is the discipline: a check may live on a rung only if it cannot live on the rung below. R3-R6 govern blocking, judge shape, manual review, and cadence. |
| `content/02-output-contract.xml` | The Rung Placement Record: per-check fields, the answer-to-rung mapping, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six misplacement modes with the live instance of each, including plumbing suites that are green by construction. |
| `content/06-decision-tree.xml` | The three-question tree plus four overlays that constrain a check once it has landed. |
| `scripts/validate-verification-rung-placement-rule.py` | Validates a record; catches rung inflation mechanically by checking rung against the placement answer. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rung-placement-record.yaml` | Worked eight-check record over the faion corpus and CLI. Ships valid against the contract. |
| `templates/rung-placement-record-single-check.yaml` | Everyday one-check triage after a manual review catch. Ships valid against the contract. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- `gate-fail-closed-rule` — what a gate must do when it cannot evaluate. Placement decides the instrument; that decides its behaviour on failure.
- `lint-autofix-vs-flag-decision-rule` — what to do with a finding once produced; this routes which instrument found it.
- `lint-precommit-floor` — the hook carries rung 1 only; this is the rule that says why.
- `eval-driven-development-tdd-for-ai` — when to write an eval; this decides whether an eval is the right tool at all.
- `agent-eval-cost-budget-policy` — cadence and spend inside rungs 2 and 3, once placement has put a check there.
- `judge-calibration-protocol` — rung 3's entry requirement: no judge without a measured κ.
- `quality-gates-confidence` — phase-promotion gates; orthogonal, and each of its levels still needs its checks placed.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rung-placement-record.yaml`

```yaml
#
# Validate:  validate-verification-rung-placement-rule.py rung-placement-record.yaml
#
# Worked example: the faion knowledge corpus and the search CLI over it.
# Read the `answers` column first — it, not preference, decides the rung.

system: "faion knowledge corpus and the search CLI over it"

# Hard cap is 15, ever. Past that you have a slow rung-2 suite with an RNG in it.
rung3_budget: 5

checks:
  # --- RUNG 1: bytes only, 0 tokens, pre-commit + every CI run ---
  - id: refs-resolve
    defect: "a methodology_refs or playbook_refs entry points at a slug that does not exist"
    answers: bytes            # bytes | mechanical | judgement | none
    rung: 1
    instrument: "scripts/validate-refs.py (~20 lines, resolves against tier-manifest.json)"
    exact: true
    action: block
    cadence: pre-commit
    # Measured 2026-08-04: 528 broken refs across 5,744 MDX files, 18,107 refs
    # checked, 69 phantom slugs — previously found by a review agent at rung-3 prices.

  - id: description-length
    defect: "frontmatter description falls outside the 140-160 character window"
    answers: bytes
    rung: 1
    instrument: "scripts/check-structural.py"
    exact: true
    action: block
    cadence: pre-commit

  - id: ai-tell-density
    defect: "prose reads as machine-written because em-dash or hedging density is off"
    answers: bytes
    rung: 1
    instrument: "scripts/check-ai-tells.py"
    exact: false              # heuristic -> may only flag (r3)
    action: flag
    cadence: ci

  - id: tier-gate-coverage
    defect: "a content path is ungated, double-gated, or gated to a tier nobody owns"
    answers: bytes
    rung: 1
    instrument: "scripts/regen-tier-manifest.py --dry-run"
    exact: true
    action: block
    cadence: ci

  # --- RUNG 2: real system runs, answer compared with == ---
  - id: retrieval-recall-at-5
    defect: "a prompt edit, corpus addition or model pin drops the correct methodology out of the top 5"
    answers: mechanical
    rung: 2
    instrument: "evals/queries.yaml q001-q030, binary relevance, scored outside the model"
    cannot_live_below: "the ranking only exists once the real system has run; no amount of byte reading produces it"
    cadence: nightly

  - id: tier-leak-rate
    defect: "a result set includes an item above the caller's tier"
    answers: mechanical
    rung: 2
    instrument: "evals/queries.yaml, tier-labelled rows; must be exactly 0"
    cannot_live_below: "rung 1 checks the shape of one response; only a real query mix shows the leak happening"
    cadence: on-change

  # --- RUNG 3: judgement, no ground truth, pairwise only, budgeted ---
  - id: why-still-explanatory
    defect: "the why field degrades into tautology after a prompt refactor"
    answers: judgement
    rung: 3
    instrument: "champion-challenger scenario S1, formatting normalised, order swapped"
    cannot_live_below: "no mechanical ground truth exists for whether an explanation actually explains"
    pairwise: true            # absolute scores are not a gate at kappa 0.549 (r4)
    cadence: pre-release

  # --- RUNG H: a person, reading. Highest judgement ceiling, zero repeatability. ---
  - id: new-domain-sanity
    defect: "a newly added domain reads as plausible but is subtly wrong about its own subject"
    answers: none
    rung: H
    instrument: "operator read-through before the domain is published"
    cannot_live_below: "nobody has enumerated what would be wrong yet, so no check can be written until it is"
    cadence: on-demand

# Required whenever a rung-H check exists. This is the field that makes manual
# review compound instead of repeat: every catch names the rung it moved to.
manual_review_log:
  - found: "writers inventing methodology slugs that do not exist"
    pushed_down_to: refs-resolve
  - found: "translated descriptions expanding past the 160-char cap"
    pushed_down_to: description-length
  - found: "a domain summary that was fluent and factually thin"
    pushed_down_to: "accepted-risk — no repeatable signal identified; re-read on each new domain"
```

### `templates/rung-placement-record-single-check.yaml`

```yaml
#
# Validate:  validate-verification-rung-placement-rule.py rung-placement-record-single-check.yaml
#
# Ask the three questions in order and stop at the first yes:
#   Q1 decidable from the artefact's bytes?           -> answers: bytes      -> rung 1
#   Q2 needs the real system, answer compares with ==? -> answers: mechanical -> rung 2
#   Q3 judgement, and you would re-read it anyway?     -> answers: judgement  -> rung 3
#   otherwise                                          -> answers: none       -> rung H
# The validator rejects any rung that disagrees with the answer, which is how
# rung inflation gets caught before it costs anything.

system: "single-check triage after a manual review catch"
rung3_budget: 0

checks:
  - id: replace-me
    defect: "describe what goes wrong, observably — not what the check does"
    answers: bytes
    rung: 1
    instrument: "scripts/validate-<thing>.py"
    exact: true               # false if it decides by threshold or density
    action: block             # must be flag whenever exact is false
    cadence: pre-commit
    # cannot_live_below: required only when rung is 2, 3 or H — one line on why
    # the rung below provably cannot decide this. "Easier to write" is rejected.
```
