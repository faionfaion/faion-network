<!-- purpose: filled-in canonical PHI data-flow design for calibration (careportal-api) -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: design instance that MUST validate via scripts/validate-hipaa-phi-data-flow-design.py -->
<!-- depends-on: templates/output.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~1200 tokens -->

# Hipaa Phi Data Flow Design — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-hipaa-phi-data-flow-design.py --self-test` runs it.

```json
{
  "system": "careportal-api",
  "hops": [
    {
      "id": "hop-api",
      "name": "careportal-api (FastAPI)",
      "kind": "service",
      "operations": [
        "processes",
        "transmits"
      ],
      "external": false,
      "identifier_classes": [
        "names",
        "dates_except_year",
        "medical_record_numbers",
        "email_addresses"
      ],
      "fields": [
        {
          "name": "patient.name",
          "justification": "shown on the encounter screen the clinician is authorised to view"
        },
        {
          "name": "patient.mrn",
          "justification": "record lookup key"
        },
        {
          "name": "encounter.date",
          "justification": "encounter timeline"
        },
        {
          "name": "patient.email",
          "justification": "appointment reminders"
        }
      ],
      "purpose": "serve clinician encounter views and appointment scheduling",
      "deidentified": false,
      "access": {
        "roles": [
          {
            "role": "clinician",
            "operations": [
              "read",
              "write"
            ]
          },
          {
            "role": "scheduler",
            "operations": [
              "read"
            ]
          }
        ],
        "shared_accounts": false,
        "auto_logoff_minutes": 15,
        "break_glass": {
          "documented_at": "runbooks/break-glass.md",
          "audit_alert": "pagerduty:phi-break-glass"
        }
      },
      "retention": {
        "period_days": 0,
        "deletion_mechanism": "stateless; no PHI persisted in the service"
      }
    },
    {
      "id": "hop-postgres",
      "name": "patients PostgreSQL (RDS)",
      "kind": "database",
      "operations": [
        "stores"
      ],
      "external": false,
      "identifier_classes": [
        "names",
        "dates_except_year",
        "medical_record_numbers",
        "email_addresses",
        "phone_numbers"
      ],
      "fields": [
        {
          "name": "patients.*",
          "justification": "system of record for the patient chart"
        }
      ],
      "purpose": "system of record",
      "deidentified": false,
      "encryption_at_rest": {
        "enabled": true,
        "standard": "NIST SP 800-111",
        "kms": "aws-kms:alias/careportal-phi",
        "key_rotation_enabled": true
      },
      "access": {
        "roles": [
          {
            "role": "api-service-principal",
            "operations": [
              "read",
              "write",
              "delete"
            ]
          },
          {
            "role": "dba",
            "operations": [
              "admin"
            ]
          }
        ],
        "shared_accounts": false,
        "auto_logoff_minutes": 10,
        "break_glass": {
          "documented_at": "runbooks/break-glass.md",
          "audit_alert": "pagerduty:phi-break-glass"
        }
      },
      "retention": {
        "period_days": 2190,
        "deletion_mechanism": "nightly job deletes rows past retention and on patient deletion request; cascades to encounters"
      }
    },
    {
      "id": "hop-backup",
      "name": "RDS snapshots to S3",
      "kind": "backup",
      "operations": [
        "stores"
      ],
      "external": false,
      "identifier_classes": [
        "names",
        "dates_except_year",
        "medical_record_numbers",
        "email_addresses",
        "phone_numbers"
      ],
      "fields": [
        {
          "name": "full snapshot",
          "justification": "disaster recovery of the system of record"
        }
      ],
      "purpose": "disaster recovery",
      "deidentified": false,
      "encryption_at_rest": {
        "enabled": true,
        "standard": "NIST SP 800-111",
        "kms": "aws-kms:alias/careportal-phi",
        "key_rotation_enabled": true
      },
      "access": {
        "roles": [
          {
            "role": "sre",
            "operations": [
              "read",
              "admin"
            ]
          }
        ],
        "shared_accounts": false,
        "auto_logoff_minutes": 10,
        "break_glass": {
          "documented_at": "runbooks/break-glass.md",
          "audit_alert": "pagerduty:phi-break-glass"
        }
      },
      "retention": {
        "period_days": 35,
        "deletion_mechanism": "S3 lifecycle rule expires snapshots at 35 days; deletion requests replay against restored snapshots per runbooks/deletion.md"
      }
    },
    {
      "id": "hop-error-tracker",
      "name": "Sentry (Business plan, HIPAA add-on)",
      "kind": "error_tracker",
      "operations": [
        "stores",
        "processes"
      ],
      "external": true,
      "identifier_classes": [
        "medical_record_numbers"
      ],
      "fields": [
        {
          "name": "request.path with mrn",
          "justification": "needed to reproduce failures on a specific record; body and headers scrubbed"
        }
      ],
      "purpose": "error triage",
      "deidentified": false,
      "baa": {
        "executed": true,
        "vendor": "Sentry",
        "plan": "Business",
        "covered_service": "Error Monitoring with PII scrubbing enabled",
        "link": "contracts/sentry-baa-2026-01.pdf",
        "executed_on": "2026-01-14"
      },
      "encryption_at_rest": {
        "enabled": true,
        "kms": "vendor-managed per BAA section 4",
        "key_rotation_enabled": true
      },
      "access": {
        "roles": [
          {
            "role": "on-call-engineer",
            "operations": [
              "read"
            ]
          }
        ],
        "shared_accounts": false,
        "auto_logoff_minutes": 30,
        "break_glass": {
          "documented_at": "runbooks/break-glass.md",
          "audit_alert": "pagerduty:phi-break-glass"
        }
      },
      "retention": {
        "period_days": 30,
        "deletion_mechanism": "vendor retention set to 30 days; per-event deletion API called on deletion request"
      }
    },
    {
      "id": "hop-embeddings",
      "name": "Hosted embeddings API for note search",
      "kind": "llm_or_embeddings_api",
      "operations": [
        "processes"
      ],
      "external": true,
      "identifier_classes": [],
      "fields": [
        {
          "name": "note.text_deidentified",
          "justification": "semantic search over clinical notes; all 18 identifiers removed before the call"
        }
      ],
      "purpose": "semantic search over clinical notes",
      "deidentified": true,
      "deidentification_method": "safe_harbor_164_514_b_2",
      "access": {
        "roles": [
          {
            "role": "search-service-principal",
            "operations": [
              "write"
            ]
          }
        ],
        "shared_accounts": false,
        "auto_logoff_minutes": 5,
        "break_glass": {
          "documented_at": "runbooks/break-glass.md",
          "audit_alert": "pagerduty:phi-break-glass"
        }
      },
      "retention": {
        "period_days": 0,
        "deletion_mechanism": "vendor zero-retention endpoint; nothing persisted"
      }
    }
  ],
  "links": [
    {
      "from": "hop-api",
      "to": "hop-postgres",
      "tls_version": "1.2",
      "tls_terminates_at": "RDS endpoint (rds.force_ssl=1)",
      "identifier_classes": [
        "names",
        "dates_except_year",
        "medical_record_numbers",
        "email_addresses",
        "phone_numbers"
      ]
    },
    {
      "from": "hop-postgres",
      "to": "hop-backup",
      "tls_version": "1.2",
      "tls_terminates_at": "S3 endpoint",
      "identifier_classes": [
        "names",
        "dates_except_year",
        "medical_record_numbers",
        "email_addresses",
        "phone_numbers"
      ]
    },
    {
      "from": "hop-api",
      "to": "hop-error-tracker",
      "tls_version": "1.3",
      "tls_terminates_at": "sentry.io ingest",
      "identifier_classes": [
        "medical_record_numbers"
      ]
    },
    {
      "from": "hop-api",
      "to": "hop-embeddings",
      "tls_version": "1.3",
      "tls_terminates_at": "vendor API gateway",
      "identifier_classes": []
    }
  ],
  "audit_log": {
    "store": "CloudWatch Logs group /careportal/phi-audit with retention lock",
    "append_only": true,
    "contains_phi_field_values": false,
    "retention_years": 7,
    "event_fields": [
      "identity",
      "timestamp",
      "record_id",
      "action",
      "originating_system"
    ],
    "bulk_access_alert": "CloudWatch alarm: >200 distinct record_ids read by one identity in 10 minutes -> pagerduty:phi-bulk-access"
  },
  "log_scrubbing": {
    "allow_list_scrubber_at": "careportal/logging/scrubber.py (allow-list of 14 safe keys)",
    "phi_in_urls_or_query_strings": false,
    "synthetic_record_test": {
      "path": "tests/compliance/test_no_phi_in_logs.py",
      "covers_every_request_path": true,
      "asserts_no_identifier_in_logs_errors_traces": true,
      "runs_in_ci": true
    }
  },
  "deletion_propagation": [
    {
      "trigger": "patient deletion request or retention expiry in hop-postgres",
      "propagates_to": [
        "hop-backup",
        "hop-error-tracker"
      ],
      "mechanism": "deletion job writes a tombstone; backup restore replays tombstones (runbooks/deletion.md); Sentry per-event deletion API by mrn"
    }
  ],
  "media_disposal_procedure": "runbooks/media-disposal.md: NIST SP 800-88 purge for any drive or device that held PHI; cloud volumes are KMS-encrypted and keys are destroyed on decommission",
  "review": {
    "status": "ready_for_review",
    "security_officer": "security-officer@careportal.example",
    "approved_by_agent": false
  }
}
```
