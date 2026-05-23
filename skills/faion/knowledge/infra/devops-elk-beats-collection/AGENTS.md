# Log Collection with Filebeat and Elastic Beats

## Summary

**One-sentence:** Produces a Filebeat config (DaemonSet on K8s, or per-host) with autodiscover, multiline + JSON parsing, fields_under_root=true, and shipping to Elasticsearch / Logstash.

**One-paragraph:** Filebeat is the lightweight log shipper: file tail + multiline handling + JSON parsing + Kubernetes metadata enrichment + autodiscover. The non-negotiables: deploy as DaemonSet on K8s (one pod per node), set fields_under_root=true on every input so fields are flat in Elasticsearch, enable autodiscover for K8s so new pods don't need config updates, and handle multiline events (Java/Python tracebacks) correctly. Output: Filebeat YAML + DaemonSet manifest + autodiscover provider config.

**Ефективно для:**

- Centralised logs з file sources на Linux / Windows hosts.
- K8s environments — all container stdout/stderr без modifying apps.
- Lightweight collection без Logstash JVM overhead.
- Dynamic envs з frequent service deploys — autodiscover handles config.

## Applies If (ALL must hold)

- Sources include log files OR K8s container stdout/stderr.
- Volume < 100k events/sec per node (Fluent Bit better above that).
- Existing Filebeat skills OR willingness to learn (community is large).

## Skip If (ANY kills it)

- Complex parsing (grok, translate, conditional routing) — Logstash or Fluentd more capable.
- Fluentd already deployed — adding Filebeat duplicates collection.
- Very high event rates (>100k events/sec/node) — Fluent Bit has lower per-event overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source map | list of file paths / containers per host | app team |
| Cluster endpoint | ES / Logstash URL + auth | platform team |
| Field schema | service / environment / log-type per source | log-modelling exercise |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-elk-architecture]] | Beats ship to the architected cluster |
| [[devops-elk-index-management]] | Index templates + ILM applied downstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: daemonset-on-k8s, fields-under-root, multiline-config, autodiscover, output-pinned, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for Filebeat config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: nested-fields, no-multiline, hostpath-instead-of-dsmount, output-on-bulk-error-retry-disabled | 800 |
| `content/04-procedure.xml` | essential | 5 steps: source enum → inputs + processors → autodiscover → output → deploy | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on substrate → DaemonSet / host-agent | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-inputs` | sonnet | Per-source input config with fields + multiline. |
| `write-autodiscover` | sonnet | K8s autodiscover provider rules. |
| `validate-fields` | haiku | Mechanical fields_under_root + service/env presence check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/filebeat.yml` | Filebeat YAML config with inputs + autodiscover + processors + output |
| `templates/filebeat-daemonset.yaml` | Kubernetes DaemonSet manifest for Filebeat (one pod per node) |
| `templates/_smoke-test.json` | Minimum config used by validate-devops-elk-beats-collection.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-elk-beats-collection.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-elk-architecture]]
- [[devops-elk-logstash-pipeline]]
- [[devops-elk-index-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when standing up log collection from K8s or hosts to ELK.
