# Deploy Notes Template with Rollback

## Summary

**One-sentence:** Pre-deploy spec capturing the change set, blast-radius, rollback recipe, and post-deploy verification steps so a single operator can recover without context; produces a deploy-notes artefact pinned to the deployable artifact id.

**One-paragraph:** Pre-deploy spec capturing the change set, blast-radius, rollback recipe, and post-deploy verification steps so a single operator can recover without context; produces a deploy-notes artefact pinned to the deployable artifact id. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Solo founders running production deploys without a co-on-call.
- Friday-afternoon hotfixes when memory and adrenaline make written context essential.
- DB schema changes where ordering of code + migration determines reversibility.
- Vendor-driven deploys (Stripe webhook update, OAuth migration) with rollback windows.

## Applies If (ALL must hold)

- A code change is about to be deployed to a production-equivalent environment.
- The deployable artifact has a stable identifier (SHA, image tag, version tag).
- Rollback is possible (previous artifact still pullable / DB migrations are reversible or guarded).
- A single named operator will run the deploy and hold ownership of the outcome.

## Skip If (ANY kills it)

- Pre-production environment (staging, dev) with throw-away data — overhead not justified.
- No previous artifact to roll back to (first-ever deploy) — use a launch checklist instead.
- Forward-only DB migration with no down-script — escalate to a migration-impact mapping first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[migration-impact-mapping]] | upstream context this methodology builds on |
| [[qa-rollback-trigger-canon]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-deploy-notes-template-with-rollback-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-deploy-notes-template-with-rollback.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-deploy-notes-template-with-rollback.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[migration-impact-mapping]]
- [[qa-rollback-trigger-canon]]
- [[blast-radius-scoring-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
