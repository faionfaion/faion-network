# Value Stream Management

## Summary

Map the end-to-end flow from customer request to customer value, measure it with Flow Metrics (Lead Time, Cycle Time, Throughput, WIP, %C/A) and DORA (Deployment Frequency, Change Lead Time, Change Failure Rate, MTTR), identify the constraint per Theory of Constraints, and run targeted experiments to elevate that constraint. Instrument with telemetry first — a VSM workshop without data decays into a poster within months.

## Why

AI productivity gains and DevOps automation frequently fail to improve customer-visible delivery time because the bottleneck lies outside the software team (product spec, design review, compliance gate, support queue). Flow Metrics expose end-to-end flow; DORA measures only DevOps efficiency. Used together they locate where value actually stalls, preventing teams from optimizing the wrong stage.

## When To Use

- Engineering org has shipped DevOps automation but customer-visible lead time has not improved
- Cross-functional bottleneck suspected across product → design → eng → release → support
- Quarterly OKR cycle wants to move from output metrics to flow metrics
- DORA metrics are already in place but not improving — need upstream view via Flow Metrics
- Org adopting SAFe, FAST Agile, or the Project-to-Product model

## When NOT To Use

- Single-team, single-product startup pre-PMF — premature optimization
- Org without telemetry baseline (no commit timestamps, no deploy log) — instrument first
- Pure cost-cutting context — VSM exposes inefficiencies but is not a layoff lever
- Teams with no shared ownership across the stream — VSM names the bottleneck but cannot move it

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | VSM metrics, DORA four-tuple, Flow + DORA combination, implementation steps |
| `content/02-workflow.xml` | Agentic instrumenter and bottleneck-analyzer pipeline, prompt patterns, AI-agent gotchas |
| `content/03-tools-and-references.xml` | CLI tools, SaaS services, best practices, key references |

## Templates

| File | Purpose |
|------|---------|
| `templates/dora-quick.sh` | Bash script: compute last-30-day DORA from git log + deploy.log |
| `templates/flow-item.yaml` | Schema for a single traced work item across VSM stages |
