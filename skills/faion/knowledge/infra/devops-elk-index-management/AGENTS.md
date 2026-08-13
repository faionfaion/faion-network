# Elasticsearch Index Lifecycle Management and Templates

## Summary

**One-sentence:** Produces ES index management config: index templates (mappings + settings) + ILM policy (hot→warm→cold→delete via rollover) + write alias for time-series logs.

**One-paragraph:** Without ILM, engineers manually delete old indices, causing accidental data loss or cluster-red from disk exhaustion. Without index templates, each new index inherits ES defaults (too many shards + wrong field types). Rollover aliases decouple write target from physical index name. This methodology produces the three artefacts: component templates + index template, an ILM policy with hot/warm/cold/delete phases driven by max_age + max_size, and a write alias bound to the policy. Output replaces all manual index management.

**Ефективно для:**

- Production ES cluster з time-series logs + retention period.
- New log source — index growing beyond one index.
- Migration з daily-naming (logs-2025.01.15) → size-based rollover.
- Storage cost reduction — aging data → warm/cold tiers.

## Applies If (ALL must hold)

- Data is time-series (logs / metrics / traces with @timestamp).
- Retention policy is defined (days or storage cap).
- Cluster has multiple tiers (hot-warm-cold) OR plans to add them.

## Skip If (ANY kills it)

- Dev / throwaway cluster — plain indices simpler.
- Static dataset (imported once, never updated) — use snapshot/restore.
- Single-tier cluster + retention < 7 days — ILM overhead not justified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Retention policy | days per data stream | GRC / app team |
| Tier topology | hot/warm/cold node availability | see devops-elk-architecture |
| Index name pattern | logs-*, metrics-* etc. | naming convention |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-elk-architecture]] | Tier topology comes from there |
| [[devops-elk-beats-collection]] | Ingest agents write into the alias |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: index-template-before-data, ilm-policy-required, rollover-by-size-or-age, write-alias-bound, shard-count-bounded, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ILM + template config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: no-template-default-mapping, daily-index-without-rollover, no-ilm-manual-delete, oversharded-cluster | 800 |
| `content/04-procedure.xml` | essential | 5 steps: template → ILM policy → write alias → bootstrap first index → verify rollover | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on retention + volume → policy phases | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-template` | sonnet | Component + index template composition. |
| `design-ilm` | sonnet | Phase config + transitions. |
| `validate-shards` | haiku | Shard count math against best-practice. |

## Templates

| File | Purpose |
|------|---------|
| `templates/index-template.json` | Index template + component templates for logs-* |
| `templates/ilm-policy.json` | ILM policy: hot (rollover 50G or 7d) → warm 30d → cold 60d → delete 90d |
| `templates/bootstrap.sh` | Bootstrap script: create policy + template + initial index + write alias |
| `templates/_smoke-test.json` | Minimum config used by validate-devops-elk-index-management.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-elk-index-management.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-elk-architecture]]
- [[devops-elk-beats-collection]]
- [[devops-elk-logstash-pipeline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when wiring index management on a new ES cluster.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/index-template.json`

```json
{
  "index_patterns": [
    "logs-*"
  ],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs-write",
      "refresh_interval": "5s"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "service": {
          "type": "keyword"
        },
        "environment": {
          "type": "keyword"
        },
        "level": {
          "type": "keyword"
        },
        "message": {
          "type": "text"
        },
        "kubernetes.pod.name": {
          "type": "keyword"
        }
      }
    }
  },
  "data_stream": {}
}
```

### `templates/ilm-policy.json`

```json
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "7d"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "allocate": {
            "include": {
              "data_tier": "data_warm"
            }
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "s3-logs-cold"
          },
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### `templates/bootstrap.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
ES_URL="${ES_URL:?missing}"
AUTH=(-u "${ES_USER:?}:${ES_PASS:?}")

curl -sfX PUT "$ES_URL/_ilm/policy/logs-policy" "${AUTH[@]}" -H "Content-Type: application/json" --data-binary @ilm-policy.json
curl -sfX PUT "$ES_URL/_index_template/logs-template" "${AUTH[@]}" -H "Content-Type: application/json" --data-binary @index-template.json
curl -sfX PUT "$ES_URL/logs-000001" "${AUTH[@]}" -H "Content-Type: application/json" -d '{"aliases": {"logs-write": {"is_write_index": true}}}'
echo OK
```

### `templates/_smoke-test.json`

```json
{
  "index_pattern": "logs-*",
  "policy_name": "logs-policy",
  "phases": [
    "hot",
    "warm",
    "cold",
    "delete"
  ],
  "rollover": {
    "max_primary_shard_size": "50gb",
    "max_age_days": 7
  },
  "shard_count": 1,
  "replica_count": 1,
  "write_alias": "logs-write"
}
```
