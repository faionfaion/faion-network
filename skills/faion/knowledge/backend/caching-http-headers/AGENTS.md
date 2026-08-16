# HTTP Caching Headers (Cache-Control, ETag, Vary, CDN)

## Summary

**One-sentence:** Produces a per-endpoint HTTP-caching spec: `Cache-Control` directives, `ETag`/`Vary` rules, `s-maxage`, `stale-while-revalidate`, private vs public, and CDN surrogate-key plan.

**Ефективно для:**

- REST / GraphQL endpoints fronted by a CDN (Cloudflare, Fastly, Akamai, CloudFront).
- High-read-low-write resources (catalog, listings, public pages).
- API responses that must invalidate on entity write events.
- Private user data that must NEVER hit shared caches.

**One-paragraph:** HTTP caching is the highest-leverage cache layer: correct `Cache-Control` eliminates origin hits for eligible responses, dropping latency and offloading ~90% of traffic to CDN edges. Four critical headers — `Cache-Control` (freshness policy), `ETag` (conditional revalidation), `Vary` (cache key dimensions), `Surrogate-Key`/`Cache-Tag` (CDN group invalidation) — must be set deliberately per endpoint, not by framework defaults.

## Applies If (ALL must hold)

- Endpoint serves a response cacheable for ≥1s.
- CDN or shared cache is in front of origin.
- Response varies by language / device / auth (Vary needed).
- Edge or browser revalidation is cheaper than recomputing the body.

## Skip If (ANY kills it)

- Streaming endpoints (chunked / SSE / WS) — caching headers don't apply.
- Always-personal endpoints with secrets in body — disable shared caching outright.
- Frequent writes (>1/s) — invalidation chatter exceeds cache win.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Endpoint inventory | OpenAPI spec | team |
| CDN feature matrix | vendor doc | SRE |
| Per-endpoint write rate + read rate | telemetry | SRE |
| PII / auth classification per endpoint | policy doc | security |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-endpoint` | haiku | PII vs public vs auth — bounded enum. |
| `draft-headers` | sonnet | Picks max-age / s-maxage / SWR per workload. |
| `audit-cdn-plan` | sonnet | Cross-checks invalidation tags against entity model. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-http-headers.json` | JSON Schema for the HTTP Caching Headers (Cache-Control, ETag, Vary, CDN) output contract |
| `templates/caching-http-headers.md.j2` | Markdown skeleton with the required fields |
| `templates/caching-http-headers.md` | Markdown skeleton with the required fields Generated from `templates/caching-http-headers.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a caching-http-headers record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a caching-http-headers record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-http-headers.py` | Enforce the HTTP Caching Headers (Cache-Control, ETag, Vary, CDN) output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[caching-invalidation]]
- [[caching-stampede-prevention]]
- [[caching-write-patterns]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/caching-http-headers.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/caching-http-headers.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^hch\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
