# LLM Observability Stack (2026)

## Summary

**One-sentence:** Integrates Langfuse (tracing), Helicone (cost analytics), Arize Phoenix (eval), and Braintrust (multi-agent tracing) behind a one-line SDK wrapper so each tool sees the same span tree.

**One-paragraph:** Production LLM apps need four observability planes: traces (Langfuse), cost analytics (Helicone), evaluation (Arize Phoenix), multi-agent tracing (Braintrust). Running them in silos forces redundant span emission and makes correlation impossible. This methodology defines a one-line SDK wrapper that emits OTEL-format spans consumed by all four tools, plus a hostable Langfuse + Phoenix self-host config when data-residency matters.

**Ефективно для:**

- Multi-agent product where one trace spans 5+ tool calls.
- Cost re-attribution audit (Helicone shines).
- Eval dashboard for stakeholders (Phoenix shines).
- Self-hosted observability for data-residency compliance.

## Applies If (ALL must hold)

- Pipeline runs ≥10 LLM calls per request OR multi-agent.
- Cost is non-trivial ($500/mo+).
- Team has bandwidth to wire OTEL exporters.

## Skip If (ANY kills it)

- Single-call pipeline — Helicone alone suffices.
- Spend < $100/mo — observability cost outweighs value.
- Closed-API only with provider dashboard sufficient.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OTEL exporter | library | Already in stack or being added |
| Tool accounts | API keys | Provider signup |
| Data-residency rules | policy | Legal |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wrapper_author` | sonnet | One-line SDK wrapper emitting OTEL spans. |
| `config_self_host` | sonnet | Langfuse + Phoenix self-host compose. |
| `dashboard_setup` | haiku | Default dashboards per tool. |

## Templates

| File | Purpose |
|------|---------|
| `templates/docker-compose.yml` | Self-host Langfuse + Phoenix compose |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-observability-stack-2026.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llm-cost-basics]]
- [[evaluation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is data residency required (EU)? Branches route to a rule id from `content/01-core-rules.xml` (self-host-when-residency, one-span-tree, pii-redaction-edge, ...) so every leaf is traceable to a testable statement.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/docker-compose.yml`

```yaml
# docker-compose for llm-observability-stack-2026 self-host skeleton
version: '3.8'
services:
  app:
    image: example/llm-observability-stack-2026:latest
    environment:
      - LOG_LEVEL=info
    ports:
      - '8080:8080'
```
