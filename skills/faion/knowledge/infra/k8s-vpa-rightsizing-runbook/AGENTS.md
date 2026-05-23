# K8s VPA Rightsizing Runbook

## Summary

**One-sentence:** Runs the VPA recommend → soak → HPA-reconcile → canary → full-rollout → recompute cycle and produces a per-cluster cost-reduction report with audit trail.

**One-paragraph:** Runs the VPA recommend → soak → HPA-reconcile → canary → full-rollout → recompute cycle and produces a per-cluster cost-reduction report with audit trail. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Кластер з 20+ workloads і HPA на 30%+ сервісах — потрібен керований переїзд на нові requests/limits.
- Місячна хмарна оплата кластера >=$1k — економія від rightsizing відбиває витрати на runbook.
- Команда вже зловила хоча б один OOMKill або throttling інцидент через неправильні requests.
- VPA controller встановлено; команда готова витримати 7+ днів soak і canary на 10% перед full rollout.

## Applies If (ALL must hold)

- cluster has >=20 long-running workloads (Deployment / StatefulSet)
- VPA controller installed OR can be installed safely
- HPA used on >=30% of workloads
- cluster cost >=$1k / month (saving floor for the runbook overhead)

## Skip If (ANY kills it)

- cluster is < 20 workloads — manual rightsizing cheaper than VPA infra
- workloads are batch / short-lived jobs only — VPA recommendations meaningless
- regulated environment requires fixed-resource pinning (no autoscaling allowed)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/report.md` | working skeleton matching the `produces=report` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-k8s-vpa-rightsizing-runbook.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is VPA controller installed and at least 20 long-running workloads with HPA in scope?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
