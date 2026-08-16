# Logstash Pipeline Configuration and Tuning

## Summary

**One-sentence:** Produces a Logstash pipeline (input → filter → output) with grok / JSON parsing, PII masking, multi-pipeline isolation, dead-letter queue, and tuned worker / batch settings.

**One-paragraph:** Raw log lines are unstructured strings. Logstash transforms them into typed documents (grok / json / date / geoip / useragent), masks PII (mutate gsub), normalises field names, and routes to multiple outputs. Multi-pipeline architecture isolates heavy processing (grok) from lightweight routing. Dead-letter queues capture parse failures for replay. Output: pipelines.yml + per-pipeline .conf + DLQ config + worker / batch tuning numbers. PII masking before indexing is mandatory for GDPR / PCI compliance.

**Ефективно для:**

- Сирі логи різних форматів — grok + json + syslog + custom.
- PII masking, field normalisation, GeoIP enrichment перед index.
- Heavy processing (grok / useragent) ізольоване від write path.
- Routing у різні ES indices з різними retention.
- Dead-letter queue — capture + replay parse failures.

## Applies If (ALL must hold)

- Sources produce multiple formats requiring different parsing.
- PII masking OR enrichment needed pre-index.
- Multi-stream routing with different retention.
- Volume justifies a Logstash JVM (≥10 events/sec/source).

## Skip If (ANY kills it)

- Simple JSON logs single app — Filebeat direct to ES is cheaper.
- K8s-native + Fluentd already deployed — adding Logstash creates duplicate.
- Throughput exceeds single-node Logstash AND horizontal scale constrained — put Kafka in front.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source format catalogue | list of log formats + sample lines | app team |
| PII mask list | regexes for credit cards, tokens, etc. | security / GRC |
| ES index targets | per-stream index name + retention | see index-management |
| Throughput budget | events/sec target + Logstash node count | platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[devops-elk-architecture]] | Where Logstash fits in the cluster |
| [[devops-elk-index-management]] | Output indices + ILM policies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pii-mask-before-index, multi-pipeline-isolation, dlq-enabled, worker-batch-tuned, grok-with-on-failure, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for pipeline config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: pii-leak, single-pipeline-bottleneck, dropped-on-parse-failure, default-worker-count | 800 |
| `content/04-procedure.xml` | essential | 5 steps: catalogue formats → pipelines.yml → per-format filter → PII mask → tune | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on format diversity + PII → single/multi pipeline | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-grok` | sonnet | Per-format grok pattern composition. |
| `design-pipelines-yml` | sonnet | Multi-pipeline split + dependency map. |
| `tune-workers` | haiku | Mechanical worker/batch math against CPU + heap. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pipelines.yml` | Multi-pipeline config: heavy / routing / pii |
| `templates/main.conf` | Pipeline: Beats input → grok + JSON + PII mask → Elasticsearch output |
| `templates/_smoke-test.json` | Minimum config used by validate-devops-elk-logstash-pipeline.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-elk-logstash-pipeline.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[devops-elk-architecture]]
- [[devops-elk-beats-collection]]
- [[devops-elk-index-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when wiring Logstash for mixed-format ingest or PII masking.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pipelines.yml`

```yaml
- pipeline.id: heavy
  path.config: "/etc/logstash/conf.d/heavy.conf"
  pipeline.workers: 4
  pipeline.batch.size: 250
  dead_letter_queue.enable: true

- pipeline.id: routing
  path.config: "/etc/logstash/conf.d/routing.conf"
  pipeline.workers: 2
  pipeline.batch.size: 500
  dead_letter_queue.enable: true
```

### `templates/main.conf`

```conf
input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key         => "/etc/logstash/certs/logstash.key"
  }
}

filter {
  if [log_type] == "nginx-access" {
    grok {
      match => { "message" => "%{COMBINEDAPACHELOG}" }
      tag_on_failure => ["_grokparsefailure"]
    }
    date { match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss Z"] }
    geoip { source => "clientip" }
  }

  if [log_type] == "app-json" {
    json {
      source => "message"
      tag_on_failure => ["_jsonparsefailure"]
    }
  }

  # PII masking — credit card numbers + bearer tokens
  mutate {
    gsub => [
      "message", "\b(?:\d[ -]*?){13,16}\b", "[REDACTED-CC]",
      "message", "Bearer\s+[A-Za-z0-9._\-]+", "Bearer [REDACTED-TOKEN]"
    ]
  }
}

output {
  if "_grokparsefailure" in [tags] or "_jsonparsefailure" in [tags] {
    # DLQ
    file { path => "/var/log/logstash/dlq/%{+yyyy-MM-dd}.log" }
  } else {
    elasticsearch {
      hosts => ["https://elasticsearch:9200"]
      ssl => true
      cacert => "/etc/logstash/certs/ca.crt"
      user => "${ES_USER}"
      password => "${ES_PASS}"
      index => "logs-write"
      action => "create"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "pipelines": [
    {
      "id": "heavy",
      "workers": 4,
      "batch_size": 250,
      "dlq_enabled": true
    }
  ],
  "pii_masking": [
    {
      "field": "message",
      "pattern": "credit-card",
      "replacement": "[REDACTED-CC]"
    }
  ],
  "outputs": [
    {
      "target": "elasticsearch",
      "tls": true,
      "auth": true
    }
  ]
}
```
