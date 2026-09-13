#!/usr/bin/env python3
"""validate-govtech-foia-ba-pack.py

Validate the artefact produced by the govtech-foia-ba-pack methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only, self-contained:
`faion get-content` ships this file alone, so the schema and the checker live
here rather than in a shared module.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid / invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "faion://govtech-foia-ba-pack/output.schema.json",
  "title": "GovTech FOIA / records-retention BA pack",
  "type": "object",
  "required": [
    "system_name",
    "jurisdiction",
    "access_request_clock_working_days",
    "record_classes",
    "data_stores",
    "exemption_map",
    "staff_channels",
    "accessibility_audit",
    "clause_review_log",
    "public_notice",
    "records_officer",
    "access_request_officer",
    "schedule_approved_on",
    "launch_date",
    "blocking_findings"
  ],
  "additionalProperties": False,
  "definitions": {
    "handle": {
      "type": "string",
      "pattern": "^[a-z-]+:[a-z0-9._-]+$"
    },
    "date": {
      "type": "string",
      "format": "date",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    },
    "clause_entries": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "clause_id",
          "design_decision",
          "status",
          "evidence"
        ],
        "additionalProperties": False,
        "properties": {
          "clause_id": {
            "type": "string",
            "minLength": 2
          },
          "design_decision": {
            "type": "string",
            "minLength": 10
          },
          "status": {
            "type": "string",
            "enum": [
              "met",
              "open",
              "waived"
            ]
          },
          "waived_by": {
            "$ref": "#/definitions/handle"
          },
          "evidence": {
            "type": "string",
            "format": "uri"
          }
        },
        "if": {
          "properties": {
            "status": {
              "const": "waived"
            }
          }
        },
        "then": {
          "required": [
            "waived_by"
          ]
        }
      }
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "system_name": {
      "type": "string",
      "minLength": 3
    },
    "jurisdiction": {
      "type": "string",
      "enum": [
        "us-federal",
        "us-state",
        "uk",
        "eu",
        "ca-federal",
        "ca-provincial"
      ]
    },
    "access_request_clock_working_days": {
      "type": "integer",
      "minimum": 1,
      "maximum": 60
    },
    "record_classes": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "retention_period",
          "disposition",
          "schedule_item"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "minLength": 3
          },
          "retention_period": {
            "type": "string",
            "pattern": "^P(\\d+Y)?(\\d+M)?(\\d+D)?$",
            "description": "ISO-8601 duration, e.g. P7Y; never open-ended"
          },
          "disposition": {
            "type": "string",
            "enum": [
              "destroy",
              "transfer-to-archives"
            ]
          },
          "schedule_item": {
            "type": "string",
            "minLength": 5,
            "description": "NARA GRS item, agency schedule, PRA 1958 body schedule, state or provincial archives item"
          },
          "stores": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    },
    "data_stores": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "export_path",
          "export_lead_time_working_days"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "minLength": 2
          },
          "export_path": {
            "type": "object",
            "required": [
              "tool",
              "query",
              "owner"
            ],
            "additionalProperties": False,
            "properties": {
              "tool": {
                "type": "string",
                "minLength": 2
              },
              "query": {
                "type": "string",
                "minLength": 2
              },
              "owner": {
                "$ref": "#/definitions/handle"
              }
            }
          },
          "export_lead_time_working_days": {
            "type": "integer",
            "minimum": 0
          },
          "notes": {
            "type": "string"
          }
        }
      }
    },
    "exemption_map": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "field",
          "category",
          "statutory_basis",
          "redaction"
        ],
        "additionalProperties": False,
        "properties": {
          "field": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+\\.[A-Za-z0-9_.-]+$",
            "description": "store.field"
          },
          "category": {
            "type": "string",
            "enum": [
              "personal-privacy",
              "law-enforcement",
              "deliberative",
              "commercial-confidentiality",
              "security",
              "other-statutory"
            ]
          },
          "statutory_basis": {
            "type": "string",
            "minLength": 5,
            "description": "e.g. 5 U.S.C. §552(b)(6); UK FOIA 2000 s.40"
          },
          "redaction": {
            "type": "string",
            "enum": [
              "field-driven",
              "structural-split-required",
              "manual-review"
            ]
          },
          "manual_review_cost_estimate": {
            "type": "string",
            "minLength": 5
          }
        },
        "if": {
          "properties": {
            "redaction": {
              "const": "manual-review"
            }
          }
        },
        "then": {
          "required": [
            "manual_review_cost_estimate"
          ]
        }
      }
    },
    "staff_channels": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "channel",
          "capture_mechanism",
          "auto_delete"
        ],
        "additionalProperties": False,
        "properties": {
          "channel": {
            "type": "string",
            "minLength": 2
          },
          "capture_mechanism": {
            "type": "string",
            "minLength": 5
          },
          "auto_delete": {
            "type": "boolean"
          },
          "non_official_copy_within_days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 20,
            "description": "44 U.S.C. §2911 for us-federal"
          }
        }
      }
    },
    "accessibility_audit": {
      "type": "object",
      "required": [
        "wcag_version",
        "level",
        "flows",
        "launch_gate",
        "accessibility_statement_required"
      ],
      "additionalProperties": False,
      "properties": {
        "wcag_version": {
          "type": "string",
          "enum": [
            "2.1",
            "2.2"
          ]
        },
        "level": {
          "type": "string",
          "const": "AA"
        },
        "standard_reference": {
          "type": "string",
          "enum": [
            "section-508",
            "en-301-549",
            "uk-psbar-2018",
            "aoda",
            "other"
          ]
        },
        "flows": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "flow",
              "automated_tool",
              "manual_tests",
              "remediation_owner"
            ],
            "additionalProperties": False,
            "properties": {
              "flow": {
                "type": "string",
                "minLength": 3
              },
              "automated_tool": {
                "type": "string",
                "minLength": 2
              },
              "manual_tests": {
                "type": "array",
                "minItems": 3,
                "uniqueItems": True,
                "items": {
                  "type": "string",
                  "enum": [
                    "screen-reader",
                    "keyboard-only",
                    "zoom-200"
                  ]
                }
              },
              "remediation_owner": {
                "$ref": "#/definitions/handle"
              }
            }
          }
        },
        "launch_gate": {
          "type": "string",
          "const": "no-critical-or-serious-failure"
        },
        "accessibility_statement_required": {
          "type": "boolean"
        },
        "accessibility_statement_url": {
          "type": "string",
          "format": "uri"
        }
      },
      "if": {
        "properties": {
          "accessibility_statement_required": {
            "const": True
          }
        }
      },
      "then": {
        "required": [
          "accessibility_statement_url"
        ]
      }
    },
    "clause_review_log": {
      "type": "object",
      "required": [
        "data_residency",
        "security_authorisation",
        "source_code_escrow_and_ip",
        "open_source_licence",
        "subcontractor_flow_down",
        "accessibility_warranty",
        "records_transfer_on_termination"
      ],
      "properties": {
        "data_residency": {
          "$ref": "#/definitions/clause_entries"
        },
        "security_authorisation": {
          "$ref": "#/definitions/clause_entries"
        },
        "source_code_escrow_and_ip": {
          "$ref": "#/definitions/clause_entries"
        },
        "open_source_licence": {
          "$ref": "#/definitions/clause_entries"
        },
        "subcontractor_flow_down": {
          "$ref": "#/definitions/clause_entries"
        },
        "accessibility_warranty": {
          "$ref": "#/definitions/clause_entries"
        },
        "records_transfer_on_termination": {
          "$ref": "#/definitions/clause_entries"
        }
      },
      "additionalProperties": {
        "$ref": "#/definitions/clause_entries"
      }
    },
    "public_notice": {
      "type": "object",
      "required": [
        "assessed",
        "required"
      ],
      "additionalProperties": False,
      "properties": {
        "assessed": {
          "type": "boolean",
          "const": True
        },
        "required": {
          "type": "boolean"
        },
        "regime": {
          "type": "string",
          "enum": [
            "pra",
            "state-apa",
            "uk-consultation",
            "eu-consultation",
            "other"
          ]
        },
        "buffer_days": {
          "type": "integer",
          "minimum": 90
        },
        "notices_filed": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "notice",
              "date"
            ],
            "additionalProperties": False,
            "properties": {
              "notice": {
                "type": "string",
                "enum": [
                  "60-day-federal-register",
                  "30-day-federal-register",
                  "omb-submission",
                  "consultation-open",
                  "consultation-close",
                  "other"
                ]
              },
              "date": {
                "$ref": "#/definitions/date"
              }
            }
          }
        },
        "omb_control_number": {
          "type": "string",
          "pattern": "^\\d{4}-\\d{4}$"
        }
      },
      "if": {
        "properties": {
          "required": {
            "const": True
          }
        }
      },
      "then": {
        "required": [
          "regime",
          "buffer_days",
          "notices_filed"
        ]
      }
    },
    "records_officer": {
      "$ref": "#/definitions/handle"
    },
    "access_request_officer": {
      "$ref": "#/definitions/handle"
    },
    "schedule_approved_on": {
      "$ref": "#/definitions/date"
    },
    "launch_date": {
      "$ref": "#/definitions/date"
    },
    "blocking_findings": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 10
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "jurisdiction": {
            "enum": [
              "us-federal",
              "uk"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "access_request_clock_working_days": {
            "const": 20
          },
          "data_stores": {
            "items": {
              "properties": {
                "export_lead_time_working_days": {
                  "maximum": 20
                }
              }
            }
          }
        }
      }
    }
  ]
}

OK = {
  "system_name": "State benefits intake portal",
  "jurisdiction": "us-state",
  "access_request_clock_working_days": 10,
  "record_classes": [
    {
      "name": "citizen benefit applications",
      "retention_period": "P7Y",
      "disposition": "destroy",
      "schedule_item": "State Archives GRS 4-100 item 12",
      "stores": [
        "postgres.applications",
        "s3.uploads"
      ]
    },
    {
      "name": "caseworker notes",
      "retention_period": "P7Y",
      "disposition": "destroy",
      "schedule_item": "State Archives GRS 4-100 item 14",
      "stores": [
        "postgres.case_notes"
      ]
    },
    {
      "name": "audit logs",
      "retention_period": "P3Y",
      "disposition": "destroy",
      "schedule_item": "State Archives GRS 1-200 item 3",
      "stores": [
        "cloudwatch.audit"
      ]
    },
    {
      "name": "program policy decisions",
      "retention_period": "P10Y",
      "disposition": "transfer-to-archives",
      "schedule_item": "State Archives GRS 2-050 item 1",
      "stores": [
        "sharepoint.policy"
      ]
    }
  ],
  "data_stores": [
    {
      "name": "postgres.applications",
      "export_path": {
        "tool": "pg_dump + redaction script",
        "query": "SELECT * FROM applications WHERE applicant_id = ANY($1)",
        "owner": "dba:marta"
      },
      "export_lead_time_working_days": 2
    },
    {
      "name": "postgres.case_notes",
      "export_path": {
        "tool": "records-export CLI",
        "query": "records-export notes --case",
        "owner": "dba:marta"
      },
      "export_lead_time_working_days": 2
    },
    {
      "name": "s3.uploads",
      "export_path": {
        "tool": "aws s3 sync by applicant prefix",
        "query": "s3://intake-uploads/<applicant_id>/",
        "owner": "sre:dmitri"
      },
      "export_lead_time_working_days": 1
    },
    {
      "name": "cloudwatch.audit",
      "export_path": {
        "tool": "CloudWatch Logs Insights",
        "query": "fields @timestamp, actor, action | filter subject_id = <id>",
        "owner": "sre:dmitri"
      },
      "export_lead_time_working_days": 3
    },
    {
      "name": "sharepoint.policy",
      "export_path": {
        "tool": "SharePoint eDiscovery",
        "query": "site:policy-decisions",
        "owner": "records:jlee"
      },
      "export_lead_time_working_days": 5
    }
  ],
  "exemption_map": [
    {
      "field": "postgres.applications.ssn",
      "category": "personal-privacy",
      "statutory_basis": "State Public Records Act s.6254(c); 5 U.S.C. §552(b)(6) analogue",
      "redaction": "field-driven"
    },
    {
      "field": "postgres.applications.bank_account",
      "category": "personal-privacy",
      "statutory_basis": "State Public Records Act s.6254(c)",
      "redaction": "field-driven"
    },
    {
      "field": "postgres.case_notes.fraud_referral_detail",
      "category": "law-enforcement",
      "statutory_basis": "State Public Records Act s.6254(f)",
      "redaction": "structural-split-required"
    },
    {
      "field": "postgres.case_notes.body",
      "category": "personal-privacy",
      "statutory_basis": "State Public Records Act s.6254(c)",
      "redaction": "manual-review",
      "manual_review_cost_estimate": "about 4 minutes per note; 600 notes per request average = 40 reviewer hours"
    }
  ],
  "staff_channels": [
    {
      "channel": "agency email (Exchange)",
      "capture_mechanism": "journaling to records archive",
      "auto_delete": False
    },
    {
      "channel": "Teams caseworker chat",
      "capture_mechanism": "Purview retention policy, 7 years, auto-delete disabled",
      "auto_delete": False
    },
    {
      "channel": "vendor ticket tool (Zendesk)",
      "capture_mechanism": "nightly export to postgres.case_notes via API",
      "auto_delete": False
    }
  ],
  "accessibility_audit": {
    "wcag_version": "2.1",
    "level": "AA",
    "standard_reference": "section-508",
    "flows": [
      {
        "flow": "apply for benefits",
        "automated_tool": "axe-core in CI",
        "manual_tests": [
          "screen-reader",
          "keyboard-only",
          "zoom-200"
        ],
        "remediation_owner": "fe:priya"
      },
      {
        "flow": "upload supporting documents",
        "automated_tool": "axe-core in CI",
        "manual_tests": [
          "screen-reader",
          "keyboard-only",
          "zoom-200"
        ],
        "remediation_owner": "fe:priya"
      },
      {
        "flow": "check application status",
        "automated_tool": "axe-core in CI",
        "manual_tests": [
          "screen-reader",
          "keyboard-only",
          "zoom-200"
        ],
        "remediation_owner": "fe:priya"
      }
    ],
    "launch_gate": "no-critical-or-serious-failure",
    "accessibility_statement_required": True,
    "accessibility_statement_url": "https://benefits.example.gov/accessibility"
  },
  "clause_review_log": {
    "data_residency": [
      {
        "clause_id": "C-4.2",
        "design_decision": "All stores in us-west-2 and us-east-1 only; no cross-border replication",
        "status": "met",
        "evidence": "https://git.example.gov/intake/infra/pull/88"
      }
    ],
    "security_authorisation": [
      {
        "clause_id": "C-7.1",
        "design_decision": "StateRAMP Moderate authorisation for the hosting vendor before go-live",
        "status": "open",
        "evidence": "https://tickets.example.gov/SEC-311"
      }
    ],
    "source_code_escrow_and_ip": [
      {
        "clause_id": "C-12",
        "design_decision": "State owns the code; repository mirrored to the state GitLab weekly",
        "status": "met",
        "evidence": "https://git.example.gov/intake/mirror"
      }
    ],
    "open_source_licence": [
      {
        "clause_id": "C-12.3",
        "design_decision": "No AGPL dependencies; SBOM scanned in CI",
        "status": "met",
        "evidence": "https://git.example.gov/intake/app/-/jobs/4410"
      }
    ],
    "subcontractor_flow_down": [
      {
        "clause_id": "C-15",
        "design_decision": "Identity-proofing subcontractor signed the same residency and security terms",
        "status": "met",
        "evidence": "https://contracts.example.gov/idp-flowdown.pdf"
      }
    ],
    "accessibility_warranty": [
      {
        "clause_id": "C-9",
        "design_decision": "WCAG 2.1 AA warranted; audit report attached to acceptance",
        "status": "met",
        "evidence": "https://tickets.example.gov/A11Y-20"
      }
    ],
    "records_transfer_on_termination": [
      {
        "clause_id": "C-21",
        "design_decision": "Records exported as CSV plus PDF/A with schedule metadata within 30 days of termination",
        "status": "waived",
        "waived_by": "procurement:hwong",
        "evidence": "https://contracts.example.gov/waiver-c21.pdf"
      }
    ]
  },
  "public_notice": {
    "assessed": True,
    "required": True,
    "regime": "state-apa",
    "buffer_days": 120,
    "notices_filed": [
      {
        "notice": "consultation-open",
        "date": "2026-03-02"
      },
      {
        "notice": "consultation-close",
        "date": "2026-04-16"
      }
    ]
  },
  "records_officer": "records:jlee",
  "access_request_officer": "pra-officer:tnguyen",
  "schedule_approved_on": "2026-02-20",
  "launch_date": "2026-07-01",
  "blocking_findings": [
    "clause C-7.1 security_authorisation is open: StateRAMP Moderate letter not yet issued for the hosting vendor"
  ]
}

BAD = {
  "system_name": "Federal grant application portal",
  "jurisdiction": "us-federal",
  "access_request_clock_working_days": 20,
  "record_classes": [
    {
      "name": "grant applications",
      "retention_period": "P7Y",
      "disposition": "retain indefinitely",
      "schedule_item": "NARA GRS 1.2 item 020"
    }
  ],
  "data_stores": [
    {
      "name": "kafka.intake-events",
      "export_path": {
        "tool": "ask engineering",
        "query": "custom consumer, not written",
        "owner": "eng:platform"
      },
      "export_lead_time_working_days": 45
    }
  ],
  "exemption_map": [
    {
      "field": "postgres.applications.notes",
      "category": "personal-privacy",
      "statutory_basis": "5 U.S.C. §552(b)(6)",
      "redaction": "manual-review"
    }
  ],
  "staff_channels": [
    {
      "channel": "Slack #grants-review",
      "capture_mechanism": "",
      "auto_delete": True
    }
  ],
  "accessibility_audit": {
    "wcag_version": "2.1",
    "level": "A",
    "flows": [
      {
        "flow": "submit application",
        "automated_tool": "axe-core",
        "manual_tests": [
          "keyboard-only"
        ],
        "remediation_owner": "fe:priya"
      }
    ],
    "launch_gate": "post-launch-review",
    "accessibility_statement_required": True
  },
  "clause_review_log": {
    "data_residency": [
      {
        "clause_id": "H.4",
        "design_decision": "US regions only",
        "status": "met",
        "evidence": "https://git.example.gov/grants/infra/pull/3"
      }
    ]
  },
  "public_notice": {
    "assessed": True,
    "required": True,
    "regime": "pra",
    "buffer_days": 30,
    "notices_filed": []
  },
  "records_officer": "records:jlee",
  "access_request_officer": "foia:delegate",
  "schedule_approved_on": "2026-02-20",
  "launch_date": "2026-05-01",
  "blocking_findings": []
}

_FORMATS = {
    "date-time": re.compile(
        r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
        r"(?:Z|[+-]\d{2}:?\d{2})?$"
    ),
    "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "email": re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"),
    "uri": re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:\S*$"),
    "uri-reference": re.compile(r"^\S+$"),
}

_PY_TYPES = {"object": dict, "array": list, "string": str, "null": type(None)}


def _type_ok(value, declared) -> bool:
    names = declared if isinstance(declared, list) else [declared]
    for name in names:
        if name == "integer":
            ok = isinstance(value, int) and not isinstance(value, bool)
        elif name == "number":
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        elif name == "boolean":
            ok = isinstance(value, bool)
        elif name in _PY_TYPES:
            ok = isinstance(value, _PY_TYPES[name])
        else:
            ok = True
        if ok:
            return True
    return False


def _label(path: str) -> str:
    return path or "<root>"


def _resolve(ref: str):
    """Local `#/definitions/<name>` references only (draft-07 `$ref` replaces its siblings)."""
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported $ref: {ref}")
    node = SCHEMA
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _valid(value, schema) -> bool:
    errs: list[str] = []
    _check(value, schema, "", errs)
    return not errs


def _check(value, schema, path: str, errs: list) -> None:
    """Draft-07 subset: required, type, enum, const, pattern, format, minimum /
    maximum (+exclusive), minLength / maxLength, minItems / maxItems,
    uniqueItems, items, properties, additionalProperties, allOf / anyOf /
    oneOf / not, if / then / else, local $ref."""
    if schema is True or schema == {}:
        return
    if schema is False:
        errs.append(f"{_label(path)}: schema forbids any value here")
        return
    if "$ref" in schema:
        schema = _resolve(schema["$ref"])
    declared = schema.get("type")
    if declared is not None and not _type_ok(value, declared):
        errs.append(f"{_label(path)}: expected type {declared}, got {type(value).__name__}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{_label(path)}: {value!r} not in allowed enum {schema['enum']!r}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{_label(path)}: {value!r} is not the required const {schema['const']!r}")

    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errs.append(f"{_label(path)}: {value!r} does not match pattern {pattern!r}")
        rx = _FORMATS.get(schema.get("format"))
        if rx is not None and not rx.match(value):
            errs.append(f"{_label(path)}: {value!r} is not a valid {schema['format']}")
        low, high = schema.get("minLength"), schema.get("maxLength")
        if isinstance(low, int) and len(value) < low:
            errs.append(f"{_label(path)}: length {len(value)} is under minLength {low}")
        if isinstance(high, int) and len(value) > high:
            errs.append(f"{_label(path)}: length {len(value)} is over maxLength {high}")

    if isinstance(value, list):
        low, high = schema.get("minItems"), schema.get("maxItems")
        if isinstance(low, int) and len(value) < low:
            errs.append(f"{_label(path)}: {len(value)} items is under minItems {low}")
        if isinstance(high, int) and len(value) > high:
            errs.append(f"{_label(path)}: {len(value)} items is over maxItems {high}")
        if schema.get("uniqueItems"):
            seen = [json.dumps(v, sort_keys=True) for v in value]
            if len(set(seen)) != len(seen):
                errs.append(f"{_label(path)}: items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, element in enumerate(value):
                _check(element, item_schema, f"{_label(path)}[{i}]", errs)
        elif isinstance(item_schema, list):
            for i, (element, sub) in enumerate(zip(value, item_schema)):
                _check(element, sub, f"{_label(path)}[{i}]", errs)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        for key, test, word in (
            ("minimum", lambda v, b: v < b, "is below minimum"),
            ("maximum", lambda v, b: v > b, "is above maximum"),
            ("exclusiveMinimum", lambda v, b: v <= b, "is not above exclusiveMinimum"),
            ("exclusiveMaximum", lambda v, b: v >= b, "is not below exclusiveMaximum"),
        ):
            bound = schema.get(key)
            if isinstance(bound, (int, float)) and test(value, bound):
                errs.append(f"{_label(path)}: {value} {word} {bound}")

    if isinstance(value, dict):
        props = schema.get("properties") or {}
        for key in schema.get("required") or []:
            if key not in value:
                errs.append(f"{_label(path)}: missing required field: {key}")
        extra = schema.get("additionalProperties", True)
        for key in value:
            if key in props:
                continue
            if extra is False:
                errs.append(f"{_label(path)}: unknown field {key!r} (additionalProperties: false)")
            elif isinstance(extra, dict):
                _check(value[key], extra, f"{path}.{key}" if path else key, errs)
        for key, sub in props.items():
            if key in value and isinstance(sub, (dict, bool)):
                _check(value[key], sub, f"{path}.{key}" if path else key, errs)

    for sub in schema.get("allOf") or []:
        _check(value, sub, path, errs)
    any_of = schema.get("anyOf")
    if any_of and not any(_valid(value, s) for s in any_of):
        errs.append(f"{_label(path)}: matches none of the anyOf alternatives")
    one_of = schema.get("oneOf")
    if one_of:
        hits = sum(1 for s in one_of if _valid(value, s))
        if hits != 1:
            errs.append(f"{_label(path)}: matches {hits} oneOf alternatives, need exactly 1")
    if "not" in schema and _valid(value, schema["not"]):
        errs.append(f"{_label(path)}: matches the forbidden `not` schema")
    if "if" in schema:
        branch = "then" if _valid(value, schema["if"]) else "else"
        if branch in schema:
            _check(value, schema[branch], path, errs)


def validate(obj: object) -> list[str]:
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    errs: list[str] = []
    _check(obj, SCHEMA, "", errs)
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-govtech-foia-ba-pack.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
