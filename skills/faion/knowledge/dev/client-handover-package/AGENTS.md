# Client Handover Package

## Summary

**One-sentence:** Produces a sign-off-gated handover package at engagement end: runbook, credentials transfer log, open items, training plan, and a 30-day support window definition — the artefact the client confirms before payment closes.

**One-paragraph:** Solo dev / outsource engagement ends fail predictably in three ways: client cannot run the system without you, credentials remain in your password manager, and "I'll send the docs Monday" never happens. This methodology pins the close: 7 sections of the handover package, each with a checkbox the client signs off. Includes a runbook (start / stop / debug), credential transfer log with rotation evidence, open items list with risk per item, 30-day support window terms, and a knowledge-transfer record (recordings / sessions / docs). Output is a versioned report committed to the client repo (or shared drive) — the artefact a future audit can read to understand what was delivered.

**Ефективно для:**

- Solo dev / outsource lead closing a client engagement and avoiding "what about X?" pings three months later.
- Multi-client agency standardising close — same artefact shape regardless of client.
- Liability protection: signed handover record evidences scope-completion for invoice + dispute defense.
- Knowledge transfer to a successor consultant — the package is their day-1 read.

## Applies If (ALL must hold)

- An engagement is ending OR a major handoff is happening (e.g. consultant rotation).
- The client has named a successor (in-house engineer OR new consultant).
- Working credentials, runbook fragments, and open-items list are available to capture.
- The engagement length warrants the handover overhead (typically ≥4 weeks).

## Skip If (ANY kills it)

- Single PR fix engagement — no system to hand over.
- Client refuses successor identification — escalate; close without handover is high risk.
- Existing handover record &lt; 30 days old.
- System being decommissioned — different closeout methodology applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Engagement scope record | doc | client + consultant |
| Working credentials list | secrets vault | consultant |
| Runbook draft | Markdown | consultant |
| Open items list | tracker | consultant |
| Successor name + email | string | client |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/client-conventions-intake` | Sibling: the intake record at engagement start. |
| `solo/dev/ci-quality-gate-design` | CI design is one of the handover sections. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: 7 sections, credential transfer evidence, open items with risk, named successor, signed sign-off, 30-day window, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for handover package + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vague runbook, untransferred secrets, open items hidden, no successor | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: draft → transfer secrets → review → sign-off → archive | 700 |
| `content/06-decision-tree.xml` | essential | Tree: sections complete? secrets transferred? successor named? signed? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `runbook-from-repo` | sonnet | Compose start/stop/debug runbook from CI + deploy scripts. |
| `open-items-risk` | sonnet | Score each open item: severity + effort + blast radius. |
| `transfer-checklist` | haiku | Mechanical: per-credential transfer line items. |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-handover-package.json` | JSON Schema for the handover artefact. |
| `templates/handover-package.md` | Markdown skeleton with the 7 sections. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-handover-package.py` | Validate handover JSON against schema + sign-off rule. | End of engagement, before final invoice. |

## Related

- [[client-conventions-intake]] — engagement-start sibling.
- [[ci-quality-gate-design]] — CI design is one section of the handover.
- [[changelog-automation-conventional-commits]] — release history at handover.

## Decision tree

See `content/06-decision-tree.xml`. The tree checks 7-section completeness, credential transfer evidence (rotated + acknowledged), open items each with risk score, named successor, and signed sign-off by both consultant and client. Leaves emit `archive-and-close`, `block-missing-sections`, `block-secrets-not-transferred`, `block-no-successor`, or `block-no-signoff`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/client-handover-package.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/client-handover-package.json",
  "type": "object",
  "required": [
    "artefact_id",
    "client",
    "engagement_end",
    "sections",
    "credentials",
    "open_items",
    "successor_email",
    "support_window",
    "signoff",
    "verdict",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^chp-[a-z0-9-]{6,}$"
    },
    "client": {
      "type": "string",
      "minLength": 1
    },
    "engagement_end": {
      "type": "string",
      "format": "date"
    },
    "sections": {
      "type": "object",
      "required": [
        "scope_summary",
        "runbook",
        "architecture",
        "ops_surface"
      ],
      "properties": {
        "scope_summary": {
          "type": "string",
          "minLength": 50
        },
        "runbook": {
          "type": "string",
          "minLength": 100
        },
        "architecture": {
          "type": "string",
          "minLength": 100
        },
        "ops_surface": {
          "type": "string",
          "minLength": 50
        }
      }
    },
    "credentials": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "vault_path",
          "rotation_date",
          "acknowledged_by",
          "acknowledged_at"
        ],
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1
          },
          "vault_path": {
            "type": "string",
            "minLength": 1
          },
          "rotation_date": {
            "type": "string",
            "format": "date"
          },
          "acknowledged_by": {
            "type": "string",
            "format": "email"
          },
          "acknowledged_at": {
            "type": "string",
            "format": "date"
          }
        }
      }
    },
    "open_items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "title",
          "severity",
          "effort",
          "blast_radius",
          "next_step"
        ],
        "properties": {
          "title": {
            "type": "string",
            "minLength": 5
          },
          "severity": {
            "enum": [
              "high",
              "medium",
              "low"
            ]
          },
          "effort": {
            "enum": [
              "S",
              "M",
              "L"
            ]
          },
          "blast_radius": {
            "enum": [
              1,
              3,
              5
            ]
          },
          "next_step": {
            "type": "string",
            "minLength": 5
          }
        }
      }
    },
    "successor_email": {
      "type": "string",
      "format": "email"
    },
    "support_window": {
      "type": "object",
      "required": [
        "days",
        "scope",
        "sla_hours",
        "channel",
        "after_window"
      ],
      "properties": {
        "days": {
          "type": "integer",
          "minimum": 7,
          "maximum": 90
        },
        "scope": {
          "type": "string"
        },
        "sla_hours": {
          "type": "number",
          "minimum": 0,
          "maximum": 168
        },
        "channel": {
          "type": "string"
        },
        "after_window": {
          "type": "string"
        }
      }
    },
    "signoff": {
      "type": "object",
      "required": [
        "consultant_signed_by",
        "consultant_signed_at",
        "client_signed_by",
        "client_signed_at"
      ],
      "properties": {
        "consultant_signed_by": {
          "type": "string",
          "format": "email"
        },
        "consultant_signed_at": {
          "type": "string",
          "format": "date"
        },
        "client_signed_by": {
          "type": "string",
          "format": "email"
        },
        "client_signed_at": {
          "type": "string",
          "format": "date"
        }
      }
    },
    "verdict": {
      "enum": [
        "archive-and-close",
        "block-missing-sections",
        "block-secrets-not-transferred",
        "block-no-successor",
        "block-no-signoff"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```
