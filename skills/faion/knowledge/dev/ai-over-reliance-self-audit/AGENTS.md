# AI Over-Reliance Self-Audit

## Summary

**One-sentence:** Solo-dev quarterly self-audit checklist that surfaces over-reliance on AI pairing (skill decay, copy-paste-without-reading, unsupervised commits) before it ships broken code.

**One-paragraph:** AI pairing is a force multiplier until it isn't. Solo devs hit silent skill decay (can't write the loop without autocomplete), context collapse (accept a refactor without reading the diff), and supervision drift (auto-applied agent commits without review). The checklist is 8-12 binary items run every cycle (sprint, month, quarter) with a target score; failed audits route to remediation drills. Output is the filled audit conforming to the schema. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- AI Over-Reliance Self-Audit — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `ai-over-reliance-self-audit` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Operator is a solo dev relying on AI pairing daily for ≥2 weeks.
- Operator wants a recurring audit cadence rather than ad-hoc self-checks.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- AI pairing usage is <1 hour/week — overhead exceeds signal.
- Operator works inside a team with peer-review already covering the same risks.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-pairing-decision-tree]] | Decides when AI pairing fits; this audit measures whether the discipline held |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-ai-over-reliance-self-audit-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-ai-over-reliance-self-audit.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-over-reliance-self-audit.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[ai-pairing-decision-tree]]
- [[ai-prompt-as-commit-artifact]]
- [[ai-prompt-patterns-test-ideation]]

## Decision tree

See `content/06-decision-tree.xml`. Maps score vs threshold onto pass / remediate / escalate-pause-pairing. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
