# Serverless IaC and Templates

## Summary

**One-sentence:** IaC blueprint for a serverless stack: SAM / CDK / Serverless Framework / Pulumi / Terraform choice, parameterised template with env-aware stages, deployment pipeline, drift detection.

**One-paragraph:** IaC blueprint for a serverless stack: SAM / CDK / Serverless Framework / Pulumi / Terraform choice, parameterised template with env-aware stages, deployment pipeline, drift detection. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- New serverless project moving from prototype to production-ready IaC.
- Existing serverless stack with console drift or missing parameterisation.
- Multi-environment (dev / staging / prod) deployment about to be set up.
- Output produces `config` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- New serverless project moving from prototype to production-ready IaC.
- Existing serverless stack with console drift or missing parameterisation.
- Multi-environment (dev / staging / prod) deployment about to be set up.

## Skip If (ANY kills it)

- Throwaway experiment with no operational expectations.
- Single-function service already managed by an existing IaC pattern; no change in scope.
- Migration to containers / VMs already approved; IaC effort would be wasted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource inventory (functions, queues, tables, IAM) | list | team |
| Cloud provider account + region(s) | field | ops |
| Environment list (dev / staging / prod) + stage naming | doc | ops |
| Existing IaC tool standard (if any) | doc | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[serverless-foundations]] | Foundations checklist precedes IaC investment. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-tool` | sonnet | Bounded choice: SAM / CDK / Serverless Framework / Pulumi / Terraform. |
| `scaffold-template` | sonnet | Generate parameterised template with stage / env support. |
| `wire-pipeline` | sonnet | Author CI deployment pipeline + drift detection job. |

## Templates

| File | Purpose |
|------|---------|
| `templates/samconfig.toml` | SAM CLI configuration with multi-stage parameter overrides. |
| `templates/template.yaml` | SAM template skeleton parameterised by Environment. |
| `templates/deploy.yaml` | GitHub Actions deploy pipeline with drift detection. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serverless-iac-and-templates.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[serverless-foundations]]
- [[serverless-architecture-patterns]]
- [[serverless-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (inventory, account, environments, tool standard)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/samconfig.toml`

```toml
# faion_header_json: {"__faion_header__":{"purpose":"SAM CLI configuration with multi-stage parameter overrides.","consumes":"see content/02-output-contract.xml","produces":"config","depends_on":"content/01-core-rules.xml#r1-pick-tool-with-care","token_budget_impact":"~150 tokens when loaded"}}
version = 0.1

[default.deploy.parameters]
stack_name = "my-service"
region = "eu-west-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=dev"
confirm_changeset = false
resolve_s3 = true

[prod.deploy.parameters]
stack_name = "my-service-prod"
region = "eu-west-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=prod"
confirm_changeset = true
```

### `templates/template.yaml`

```yaml
# faion_header_json: {"__faion_header__":{"purpose":"SAM template skeleton parameterised by Environment.","consumes":"see content/02-output-contract.xml","produces":"config","depends_on":"content/01-core-rules.xml#r1-pick-tool-with-care","token_budget_impact":"~150 tokens when loaded"}}
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: my-service ${Environment}
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
Globals:
  Function:
    Runtime: python3.12
    Timeout: 10
    MemorySize: 512
    Tracing: Active
    Environment:
      Variables:
        ENVIRONMENT: !Ref Environment
        LOG_LEVEL: !If [IsProd, INFO, DEBUG]
Conditions:
  IsProd: !Equals [!Ref Environment, prod]
Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/api/
      Handler: app.lambda_handler
      Events:
        Api:
          Type: HttpApi
          Properties:
            Path: /items
            Method: GET
```

### `templates/deploy.yaml`

```yaml
# faion_header_json: {"__faion_header__":{"purpose":"GitHub Actions deploy pipeline with drift detection.","consumes":"see content/02-output-contract.xml","produces":"config","depends_on":"content/01-core-rules.xml#r1-pick-tool-with-care","token_budget_impact":"~150 tokens when loaded"}}
name: deploy
on:
  push:
    branches: [main]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
      - run: sam validate
      - run: sam build
  deploy:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111111111111:role/deploy
          aws-region: eu-west-1
      - uses: aws-actions/setup-sam@v2
      - run: sam deploy --no-confirm-changeset --config-env prod
  drift-detect:
    runs-on: ubuntu-latest
    steps:
      - run: aws cloudformation detect-stack-drift --stack-name my-service-prod
```
