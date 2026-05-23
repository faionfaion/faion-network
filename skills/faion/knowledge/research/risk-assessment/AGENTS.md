# Risk Assessment

## Summary

**One-sentence:** Builds a 1-page risk register: top 7 risks with P10/P50/P90 likelihood, severity, mitigation owner, trigger, and a decision gate; rejects vague 'medium' likelihood values.

**One-paragraph:** Risk register methodology producing a 1-page artefact: top 7 product/business risks scored on P10/P50/P90 likelihood plus severity, each carrying a named mitigation owner, an observable trigger (input X drops below Y), and a decision gate (escalate / accept / mitigate). Rejects vague 'medium' / 'high' descriptors without numeric backing.

**Ефективно для:**

- Pre-launch або pre-release - треба зафіксувати risks перед публічним shipping.
- Investor / board update з 'top risks' секцією.
- Major architecture change (DB migration, infra swap).
- New geographic market launch.
- Compliance audit (GDPR, SOC 2, DSA).

## Applies If (ALL must hold)

- Pre-launch or pre-release: lock the top risks before public shipping.
- Investor / board update with a 'top risks' section.
- Major architecture change (DB migration, infra swap).
- New geographic market launch with new regulatory exposure.
- Compliance audit (GDPR, SOC 2, DSA).

## Skip If (ANY kills it)

- Hobby project with no users.
- Internal-only experiment.
- Day-to-day execution (use incident review instead).
- Risks already exhaustively covered in a SOC 2 / ISO control set.
- When stakeholders want one number ('rate the risk') - that is risk-scoring, not risk-assessment.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product spec | markdown | engineering / PM |
| Architecture diagram | diagram / markdown | engineering |
| Compliance scope | list of regulations | legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[competitor-analysis]] | supplies the market/competitive risks branch of the register |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-risks` | sonnet | Synthesise risks across product / market / regulatory / financial / operational. |
| `score-p-bands` | sonnet | Assign P10/P50/P90 likelihood + severity 1-5. |
| `assign-owner-trigger` | sonnet | Name owner + observable trigger + decision gate. |
| `prune-to-seven` | haiku | Cap to top 7; lower ones land in parked-risks.md. |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | 1-page risk register template |
| `templates/riskreg.sh` | Bash helper to print risk-register table from YAML |
| `templates/risk-register.yaml` | Authoring source (YAML) for risk-register.md |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-risk-assessment.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[competitor-analysis]]
- [[business-model-research]]
- [[frameworks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
