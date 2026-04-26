# Agent Integration — ELK Stack Logging

## When to use
- Centralizing logs from a heterogeneous fleet (apps, hosts, containers, network gear) into a searchable store with dashboards.
- Building compliance / audit log archives with retention tiers (hot-warm-cold or frozen).
- Setting up SIEM-lite use cases — alerting on log patterns, correlating security signals.
- Kubernetes log aggregation with Filebeat or Fluent Bit → Logstash/Elastic.
- Replacing brittle grep-on-prod workflows for SREs.

## When NOT to use
- Pure metrics workloads — use Prometheus/Mimir/Datadog metrics, not Elasticsearch.
- Distributed tracing — use Tempo/Jaeger; Elastic APM is fine but a different methodology.
- Tiny single-node apps — `journalctl` + `lnav` or Loki is cheaper.
- Cost-sensitive cloud-native shops — Loki + Grafana is dramatically cheaper at petabyte scale.
- Hard-real-time queries (sub-100ms log lookup) — Elasticsearch refresh interval and shard cost make this expensive.

## Where it fails / limitations
- Cluster ops are non-trivial: shard sizing, JVM heap (50% RAM, max ~31GB), cold-warm-hot tiering. Operators get surprised by node OOMs.
- License/distro split: post-2021 Elastic license vs OpenSearch (AWS fork). Tooling diverges; templates that assume one may break the other.
- Cardinality explosions in fields like `pod_name`, `request_id` blow up index size; mapping discipline matters.
- Logstash JVM is heavy — most pipelines should use Beats → Elasticsearch directly, or Fluent Bit → Elasticsearch.
- Kibana RBAC and saved-objects management is fiddly across spaces and roles.
- Upgrades across major versions (7→8→9) require breaking-change reviews; agents that auto-bump versions break dashboards.

## Agentic workflow
Treat ELK as two layers: ingestion (Beats/Fluent Bit/Logstash) and storage/UX (Elasticsearch/Kibana). Agents are most useful authoring (1) ingestion configs (Filebeat inputs, Logstash pipelines, ECS-compliant field mappings), (2) index templates + ILM policies, (3) Kibana saved searches/dashboards as JSON. Never let an agent run cluster-mutating APIs (`_close`, `_delete_by_query`, `_reindex`) without a human approval and a tested rollback plan. Use Elastic Cloud or ECK in production; agents work better against a managed control plane.

### Recommended subagents
- `faion-sdd-executor-agent` — implement pipeline + dashboard changes with quality gates.
- Custom `ecs-mapping-author` — converts an unstructured log sample into ECS-compliant index mapping + Logstash filter.
- Custom `kibana-dashboard-builder` — generates Kibana saved-objects JSON from a metric brief.
- `password-scrubber-agent` — strips secrets from sample logs before they're shared with LLM context.

### Prompt pattern
"You are an ECS-compliant log-pipeline author. Input: 5-line sample of `nginx access logs`. Output: (1) Filebeat module config or `parsers` stanza, (2) Logstash filter using `dissect` or `grok` with named captures mapped to ECS fields (`url.path`, `http.response.status_code`, `client.ip`), (3) Elasticsearch index template with appropriate `keyword` vs `text` typing. Do NOT use `grok %{COMBINEDAPACHELOG}` — explicit ECS mapping required."

"You are an ILM policy author. Input: `{retention_days: 90, hot_days: 7, warm_days: 30, frozen: true}`. Output ILM JSON for hot-warm-cold-delete with `min_age` and `actions.rollover` at 50GB or 1d, whichever first."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `elasticsearch-curl` / `curl` to `_cat`, `_cluster`, `_ilm` APIs | Cluster ops | https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html |
| `eck-diagnostics` | Snapshot ECK state for support | https://github.com/elastic/eck-diagnostics |
| `filebeat`, `metricbeat`, `auditbeat` | Beats CLI tests, modules | https://www.elastic.co/beats/ |
| `fluent-bit` | Lightweight ingestion | https://docs.fluentbit.io/ |
| `vector` | Modern log/metric/trace pipeline (often replaces Logstash) | https://vector.dev/ |
| `elastdump` / `multielasticdump` | Index export/import | https://github.com/elasticsearch-dump/elasticsearch-dump |
| `esrally` | Benchmarking ES clusters | https://esrally.readthedocs.io/ |
| `kbn` (saved-objects API) | Kibana saved-object import/export | https://www.elastic.co/guide/en/kibana/current/saved-objects-api.html |
| `drain3` | Log clustering for high-cardinality logs | https://github.com/IBM/Drain3 |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Elastic Cloud | SaaS | Yes — REST API | Easiest production path |
| Elastic Cloud on Kubernetes (ECK) | OSS operator | Yes — CRDs | Self-managed K8s-native |
| OpenSearch (AWS) | OSS / SaaS | Yes — REST API | Apache 2 fork; tooling slightly diverges from Elastic 8/9 |
| Amazon OpenSearch Service | SaaS | Yes — REST + IAM | AWS-managed |
| Logstash / Vector | OSS | Yes — config-as-code | Vector recommended for new pipelines |
| Filebeat / Fluent Bit | OSS | Yes | Beats simpler, Fluent Bit lighter footprint |
| Grafana Loki | OSS / SaaS | Yes | Cheaper alternative; LogQL not Lucene |
| Datadog Logs | SaaS | Yes — API | Drop-in replacement; expensive at scale |
| Splunk | SaaS | Yes — REST | Enterprise standard, costly |
| Sematext / Logz.io / Logit.io | SaaS | Yes | Hosted ELK/OpenSearch, lower ops burden |

## Templates & scripts
See `templates.md` for index templates, ILM policies, Filebeat modules. Inline cluster health gate:

```bash
#!/usr/bin/env bash
# es-pre-deploy.sh — refuse risky deploys when cluster isn't green
set -euo pipefail
ES=${ES_URL:?https://es.example:9200}
AUTH=${ES_AUTH:?user:pass}
HEALTH=$(curl -sSu "$AUTH" "$ES/_cluster/health" | jq -r '.status')
[[ "$HEALTH" == "green" ]] || { echo "ES status: $HEALTH (refuse)"; exit 2; }
PENDING=$(curl -sSu "$AUTH" "$ES/_cluster/pending_tasks" | jq '.tasks | length')
[[ "$PENDING" -lt 5 ]] || { echo "Pending tasks: $PENDING"; exit 3; }
JVM=$(curl -sSu "$AUTH" "$ES/_nodes/stats/jvm" | jq '[.nodes[].jvm.mem.heap_used_percent] | max')
[[ "$JVM" -lt 80 ]] || { echo "Heap pressure: ${JVM}%"; exit 4; }
echo "ES ready (status=$HEALTH heap=${JVM}%)"
```

## Best practices
- ECS (Elastic Common Schema) field names everywhere; reject pipelines that ship raw app fields.
- Index templates with explicit mappings — never auto-detect on production indices; cardinality bombs hide there.
- ILM with rollover at size + age; hot tier on SSD, warm on HDD, frozen on object storage.
- Beats → Elasticsearch direct when possible; introduce Logstash/Vector only when you need parsing/enrichment beyond Beat modules.
- JVM heap = 50% of node RAM, max ~31GB (compressed oops boundary).
- Separate node roles: master-only, data, ingest, coordinating; in tiny clusters combine but never under load.
- TLS on all transport + HTTP; certificates rotated via cert-manager or Elastic Cloud.
- RBAC with role mappings tied to SSO; avoid local users.
- Snapshot to S3/GCS via SLM (snapshot lifecycle management) — not just relying on replicas.
- Loki/Vector pilot before committing to ELK at high volume — cost difference is order-of-magnitude.

## AI-agent gotchas
- LLMs emit `grok` patterns that look right but match too greedily; require `dissect` first or test against samples in CI.
- Mapping suggestions tend to use `text` everywhere — search aggregations need `keyword` subfields; force `multi_fields`.
- ILM hot/warm/cold templates copy-paste from outdated docs (pre-7.x); pin Elastic version in prompt.
- Auto-detected timezones: agents default to UTC but app logs may be local — assert `@timestamp` is ISO-8601 with offset.
- Wildcard queries (`*foo*`) destroy performance; agent-suggested Kibana searches need linting.
- Re-indexing prompts: LLMs propose `_reindex` for trivial schema changes — ILM rollover with new template is usually cleaner.
- Sample-log leakage: developers paste raw logs (with tokens, emails) into agent context; route through scrubber.
- License confusion: agent recommends Elastic-only feature on an OpenSearch cluster (Watcher → use OpenSearch Alerting).

## References
- Elastic docs: https://www.elastic.co/guide/index.html
- ECS schema: https://www.elastic.co/guide/en/ecs/current/index.html
- ILM concepts: https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html
- ECK: https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html
- OpenSearch: https://opensearch.org/docs/latest/
- Vector: https://vector.dev/docs/
- Fluent Bit: https://docs.fluentbit.io/
- Drain3 (log clustering): https://github.com/IBM/Drain3
