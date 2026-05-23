<!-- __faion_header_v1__ -->
<!-- purpose: Markdown checklist mirroring the rule set. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: checklist; depends-on: content/01-core-rules.xml#r1-fits-execution-limits -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Markdown checklist mirroring the rule set.","consumes":"see content/02-output-contract.xml","produces":"checklist","depends_on":"content/01-core-rules.xml#r1-fits-execution-limits","token_budget_impact":"~150 tokens when loaded"}} -->
# Serverless Foundations Checklist

| # | Item                                                                                            | Verdict |
|---|-------------------------------------------------------------------------------------------------|---------|
| 1 | Workload is short-lived (< 15min) and fits FaaS execution limits.                               |         |
| 2 | Functions are stateless; persistent state lives in managed services (DB / KV / object store).   |         |
| 3 | Each function has a single trigger and a single responsibility.                                 |         |
| 4 | Cold-start tolerance and PC strategy are decided.                                               |         |
| 5 | Per-invocation idempotency design exists for async triggers.                                    |         |
| 6 | Observability (logs + metrics + traces with correlation id) is wired.                           |         |
| 7 | Secrets live in a managed provider (Vault / Secrets Manager / Key Vault).                       |         |
| 8 | IaC template (SAM / CDK / Serverless Framework / Pulumi / Terraform) defines all resources.     |         |
| 9 | Vendor lock-in is acknowledged with documented exit cost.                                       |         |
| 10| Cost ceiling and break-even-vs-containers RPS are recorded.                                     |         |
