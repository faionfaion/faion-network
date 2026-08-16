# CD Pipelines and Deployment Strategies

## Summary

**One-sentence:** Concrete CD pipeline YAML: discrete build → integration → staging → E2E → production jobs with a chosen deployment strategy (rolling, blue-green, canary) and DORA events.

**One-paragraph:** Concrete CD pipeline YAML: discrete build → integration → staging → E2E → production jobs with a chosen deployment strategy (rolling, blue-green, canary) and DORA events. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- CD prerequisites in place (CI + tests + flags + IaC) — see cd-basics.
- Stack runs on GitHub Actions or equivalent declarative CI runner.
- Need to operationalise blue-green or canary deployments with health checks and rollback.
- Output produces `config` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- CD prerequisites in place (CI + tests + flags + IaC) — see cd-basics.
- Stack runs on GitHub Actions or equivalent declarative CI runner.
- Need to operationalise blue-green or canary deployments with health checks and rollback.

## Skip If (ANY kills it)

- CD prerequisites missing — solve cd-basics first.
- Service is run-to-completion (batch) rather than long-running — pipeline shape differs.
- On-prem with no orchestrator and no IaC — adopt orchestrator first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| cd-basics output | audited prereqs + stage plan | cd-basics methodology |
| Health check endpoint | /healthz returning 200 when ready | service |
| Deployment strategy choice | rolling / blue-green / canary | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cd-basics]] | principles and prereq audit upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-yaml` | sonnet | Generate workflow YAML from stage plan + strategy. |
| `write-rollback-runbook` | sonnet | Document rollback steps + decision criteria. |
| `dora-emitter` | haiku | Boilerplate event emit step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cd.yml` | GitHub Actions CD pipeline: build → unit → integration → staging → e2e → production (manual) |
| `templates/rollback_runbook.md.j2` | Rollback runbook: criteria, commands, comms |
| `templates/rollback_runbook.md` | Rollback runbook: criteria, commands, comms Generated from `templates/rollback_runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cd-pipelines.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[cd-basics]]
- [[continuous-delivery]]
- [[trunk-based-ci-gates]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are cd-basics prereqs in place AND is the workload long-running?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cd.yml`

```yaml
# faion_header_json: {"__faion_header__":{"purpose":"GitHub Actions CD pipeline: build \u2192 unit \u2192 integration \u2192 staging \u2192 e2e \u2192 production (manual)","consumes":"see content/02-output-contract.xml","produces":"config","depends_on":"content/01-core-rules.xml#discrete-stages","token_budget_impact":"~150 tokens when loaded"}}
name: cd
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/build.sh
  unit:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/unit.sh
  integration:
    needs: unit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/integration.sh
  staging:
    needs: integration
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh staging
  e2e:
    needs: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/e2e.sh staging
  production:
    needs: e2e
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh production --strategy canary --steps 5,25,50,100
      - run: ./scripts/dora-emit.sh
```
