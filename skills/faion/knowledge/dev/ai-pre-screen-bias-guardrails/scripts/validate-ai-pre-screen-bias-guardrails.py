#!/usr/bin/env python3
"""validate-ai-pre-screen-bias-guardrails.py

Validate the artefact produced by the ai-pre-screen-bias-guardrails methodology against the JSON
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
  "$id": "faion://ai-pre-screen-bias-guardrails/output.schema.json",
  "title": "AI pre-screen bias guardrail spec",
  "type": "object",
  "required": [
    "role_title",
    "candidate_jurisdictions",
    "redaction",
    "rubric",
    "proxy_review",
    "calibration",
    "adverse_impact",
    "human_of_record",
    "legal",
    "audit_log",
    "pinned_tuple",
    "evidence"
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
    "sha256": {
      "type": "string",
      "pattern": "^sha256:[0-9a-f]{64}$"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+(\\.\\d+)?$"
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "role_title": {
      "type": "string",
      "minLength": 3
    },
    "candidate_jurisdictions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "minLength": 2
      }
    },
    "redaction": {
      "type": "object",
      "required": [
        "version",
        "stripped_attributes",
        "unit_tested",
        "fixture_set_path",
        "human_sample_inspected_per_release"
      ],
      "additionalProperties": False,
      "properties": {
        "version": {
          "$ref": "#/definitions/version"
        },
        "stripped_attributes": {
          "type": "array",
          "minItems": 10,
          "uniqueItems": True,
          "items": {
            "type": "string",
            "enum": [
              "name",
              "photo",
              "email-handle",
              "date-of-birth-and-age",
              "graduation-years",
              "address-below-city",
              "gender-markers-and-pronouns",
              "nationality-and-visa-status",
              "marital-and-parental-status",
              "protected-class-associations"
            ]
          }
        },
        "unit_tested": {
          "type": "boolean",
          "const": True
        },
        "fixture_set_path": {
          "type": "string",
          "minLength": 3
        },
        "human_sample_inspected_per_release": {
          "type": "boolean",
          "const": True
        },
        "sample_size_per_release": {
          "type": "integer",
          "minimum": 1
        }
      }
    },
    "rubric": {
      "type": "object",
      "required": [
        "version",
        "hash",
        "written_before_first_score",
        "criteria"
      ],
      "additionalProperties": False,
      "properties": {
        "version": {
          "$ref": "#/definitions/version"
        },
        "hash": {
          "$ref": "#/definitions/sha256"
        },
        "written_before_first_score": {
          "type": "boolean",
          "const": True
        },
        "first_score_at": {
          "$ref": "#/definitions/date"
        },
        "criteria": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "name",
              "job_requirement",
              "anchors"
            ],
            "additionalProperties": False,
            "properties": {
              "name": {
                "type": "string",
                "minLength": 2
              },
              "job_requirement": {
                "type": "string",
                "minLength": 5
              },
              "anchors": {
                "type": "object",
                "required": [
                  "low",
                  "mid",
                  "high"
                ],
                "additionalProperties": False,
                "properties": {
                  "low": {
                    "type": "string",
                    "minLength": 10
                  },
                  "mid": {
                    "type": "string",
                    "minLength": 10
                  },
                  "high": {
                    "type": "string",
                    "minLength": 10
                  }
                }
              }
            }
          }
        }
      }
    },
    "proxy_review": {
      "type": "object",
      "required": [
        "reviewed_on",
        "reviewed_by",
        "proxy_terms_found",
        "evidence_url"
      ],
      "additionalProperties": False,
      "properties": {
        "reviewed_on": {
          "$ref": "#/definitions/date"
        },
        "reviewed_by": {
          "$ref": "#/definitions/handle"
        },
        "proxy_terms_found": {
          "type": "array",
          "maxItems": 0,
          "items": {
            "type": "string"
          }
        },
        "evidence_url": {
          "type": "string",
          "format": "uri"
        }
      }
    },
    "calibration": {
      "type": "object",
      "required": [
        "sample_source",
        "sample_size",
        "human_reviewers",
        "statistic",
        "threshold",
        "threshold_set_before_run",
        "result",
        "run_url",
        "passed"
      ],
      "additionalProperties": False,
      "properties": {
        "sample_source": {
          "type": "string",
          "const": "real-applicant-pool"
        },
        "sample_size": {
          "type": "integer",
          "minimum": 1
        },
        "human_reviewers": {
          "type": "integer",
          "minimum": 2
        },
        "statistic": {
          "type": "string",
          "enum": [
            "cohens-kappa",
            "weighted-kappa",
            "spearman"
          ]
        },
        "threshold": {
          "type": "number",
          "minimum": -1,
          "maximum": 1
        },
        "threshold_set_before_run": {
          "type": "boolean",
          "const": True
        },
        "result": {
          "type": "number",
          "minimum": -1,
          "maximum": 1
        },
        "run_url": {
          "type": "string",
          "format": "uri"
        },
        "passed": {
          "type": "boolean"
        },
        "run_at": {
          "$ref": "#/definitions/date"
        }
      }
    },
    "adverse_impact": {
      "type": "object",
      "required": [
        "self_id_store",
        "self_id_store_separate_from_scoring",
        "hold_threshold",
        "per_stage"
      ],
      "additionalProperties": False,
      "properties": {
        "self_id_store": {
          "type": "string",
          "minLength": 2
        },
        "self_id_store_separate_from_scoring": {
          "type": "boolean",
          "const": True
        },
        "hold_threshold": {
          "type": "number",
          "const": 0.8
        },
        "per_stage": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "stage",
              "groups",
              "min_ratio",
              "on_hold"
            ],
            "additionalProperties": False,
            "properties": {
              "stage": {
                "type": "string",
                "minLength": 2
              },
              "groups": {
                "type": "array",
                "minItems": 2,
                "items": {
                  "type": "object",
                  "required": [
                    "group",
                    "selection_rate"
                  ],
                  "additionalProperties": False,
                  "properties": {
                    "group": {
                      "type": "string",
                      "minLength": 1
                    },
                    "selection_rate": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1
                    }
                  }
                }
              },
              "min_ratio": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "lowest group rate divided by highest group rate"
              },
              "on_hold": {
                "type": "boolean"
              }
            },
            "if": {
              "properties": {
                "min_ratio": {
                  "exclusiveMaximum": 0.8
                }
              }
            },
            "then": {
              "properties": {
                "on_hold": {
                  "const": True
                }
              }
            }
          }
        },
        "table_url": {
          "type": "string",
          "format": "uri"
        }
      }
    },
    "human_of_record": {
      "type": "object",
      "required": [
        "auto_reject_filter_present",
        "decision_carries_role_handle",
        "reviewer_inputs"
      ],
      "additionalProperties": False,
      "properties": {
        "auto_reject_filter_present": {
          "type": "boolean",
          "const": False
        },
        "decision_carries_role_handle": {
          "type": "boolean",
          "const": True
        },
        "reviewer_inputs": {
          "type": "array",
          "minItems": 2,
          "uniqueItems": True,
          "items": {
            "type": "string",
            "enum": [
              "redacted-document",
              "score-with-reasons"
            ]
          }
        },
        "reviewers": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/handle"
          }
        }
      }
    },
    "legal": {
      "type": "object",
      "required": [
        "applicable_law"
      ],
      "additionalProperties": False,
      "properties": {
        "applicable_law": {
          "type": "string",
          "enum": [
            "nyc-ll-144",
            "illinois-aivi",
            "colorado-ai-act",
            "eu-ai-act",
            "other",
            "none"
          ]
        },
        "confirmed_by": {
          "$ref": "#/definitions/handle"
        },
        "notice_text_url": {
          "type": "string",
          "format": "uri"
        },
        "notice_lead_business_days": {
          "type": "integer",
          "minimum": 0
        },
        "bias_audit": {
          "type": "object",
          "required": [
            "conducted_on",
            "independent",
            "summary_url"
          ],
          "additionalProperties": False,
          "properties": {
            "conducted_on": {
              "$ref": "#/definitions/date"
            },
            "independent": {
              "type": "boolean",
              "const": True
            },
            "summary_url": {
              "type": "string",
              "format": "uri"
            },
            "auditor": {
              "type": "string"
            }
          }
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "applicable_law": {
                "const": "none"
              }
            }
          },
          "then": {
            "required": [
              "confirmed_by"
            ]
          },
          "else": {
            "required": [
              "notice_text_url",
              "bias_audit"
            ]
          }
        },
        {
          "if": {
            "properties": {
              "applicable_law": {
                "const": "nyc-ll-144"
              }
            }
          },
          "then": {
            "required": [
              "notice_lead_business_days"
            ],
            "properties": {
              "notice_lead_business_days": {
                "minimum": 10
              }
            }
          }
        }
      ]
    },
    "audit_log": {
      "type": "object",
      "required": [
        "fields",
        "retention_months",
        "queryable_per_candidate"
      ],
      "additionalProperties": False,
      "properties": {
        "fields": {
          "type": "array",
          "minItems": 7,
          "uniqueItems": True,
          "items": {
            "type": "string",
            "enum": [
              "submission_hash",
              "redacted_text",
              "model_id",
              "prompt_hash",
              "rubric_version",
              "score_with_reasons",
              "human_decision"
            ]
          }
        },
        "retention_months": {
          "type": "integer",
          "minimum": 12
        },
        "retention_basis": {
          "type": "string"
        },
        "queryable_per_candidate": {
          "type": "boolean",
          "const": True
        },
        "storage": {
          "type": "string"
        }
      }
    },
    "pinned_tuple": {
      "type": "object",
      "required": [
        "model_id",
        "prompt_hash",
        "rubric_version",
        "redaction_version"
      ],
      "additionalProperties": False,
      "properties": {
        "model_id": {
          "type": "string",
          "minLength": 3,
          "not": {
            "pattern": "(?i)(^|[-:@/_])latest$"
          }
        },
        "prompt_hash": {
          "$ref": "#/definitions/sha256"
        },
        "rubric_version": {
          "$ref": "#/definitions/version"
        },
        "redaction_version": {
          "$ref": "#/definitions/version"
        }
      }
    },
    "evidence": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "format": "uri"
      }
    }
  }
}

OK = {
  "role_title": "Senior backend engineer",
  "candidate_jurisdictions": [
    "US-NY",
    "US-CA",
    "DE"
  ],
  "redaction": {
    "version": "1.3.0",
    "stripped_attributes": [
      "name",
      "photo",
      "email-handle",
      "date-of-birth-and-age",
      "graduation-years",
      "address-below-city",
      "gender-markers-and-pronouns",
      "nationality-and-visa-status",
      "marital-and-parental-status",
      "protected-class-associations"
    ],
    "unit_tested": True,
    "fixture_set_path": "hiring/redaction/fixtures/",
    "human_sample_inspected_per_release": True,
    "sample_size_per_release": 20
  },
  "rubric": {
    "version": "2.1",
    "hash": "sha256:4c2a9b1e7f3d6a8c0b5e2f9d1a7c3e6b8f0d2a4c6e8b1d3f5a7c9e1b3d5f7a9c",
    "written_before_first_score": True,
    "first_score_at": "2026-02-10",
    "criteria": [
      {
        "name": "correctness",
        "job_requirement": "Ships services that pass the integration suite",
        "anchors": {
          "low": "Solution fails the provided test cases or does not run",
          "mid": "Passes the provided tests; misses at least one stated edge case",
          "high": "Passes provided tests and handles every stated edge case with tests of its own"
        }
      },
      {
        "name": "design clarity",
        "job_requirement": "Designs modules other engineers can extend",
        "anchors": {
          "low": "Single function with mixed concerns; no explanation of trade-offs",
          "mid": "Reasonable separation; trade-offs partly explained",
          "high": "Clear module boundaries with the trade-offs and alternatives stated"
        }
      }
    ]
  },
  "proxy_review": {
    "reviewed_on": "2026-02-03",
    "reviewed_by": "dei:rkim",
    "proxy_terms_found": [],
    "evidence_url": "https://hr.example.com/reviews/rubric-2.1-proxy-review"
  },
  "calibration": {
    "sample_source": "real-applicant-pool",
    "sample_size": 30,
    "human_reviewers": 2,
    "statistic": "weighted-kappa",
    "threshold": 0.65,
    "threshold_set_before_run": True,
    "result": 0.71,
    "run_url": "https://hr.example.com/calibration/backend-2026-02",
    "passed": True,
    "run_at": "2026-02-07"
  },
  "adverse_impact": {
    "self_id_store": "hris.eeo_self_id",
    "self_id_store_separate_from_scoring": True,
    "hold_threshold": 0.8,
    "per_stage": [
      {
        "stage": "take-home forwarded to hiring manager",
        "groups": [
          {
            "group": "A",
            "selection_rate": 0.52
          },
          {
            "group": "B",
            "selection_rate": 0.47
          },
          {
            "group": "C",
            "selection_rate": 0.49
          }
        ],
        "min_ratio": 0.9,
        "on_hold": False
      },
      {
        "stage": "advanced to onsite",
        "groups": [
          {
            "group": "A",
            "selection_rate": 0.31
          },
          {
            "group": "B",
            "selection_rate": 0.27
          },
          {
            "group": "C",
            "selection_rate": 0.29
          }
        ],
        "min_ratio": 0.87,
        "on_hold": False
      }
    ],
    "table_url": "https://hr.example.com/adverse-impact/backend-2026-q1"
  },
  "human_of_record": {
    "auto_reject_filter_present": False,
    "decision_carries_role_handle": True,
    "reviewer_inputs": [
      "redacted-document",
      "score-with-reasons"
    ],
    "reviewers": [
      "em:jdoe",
      "em:apatel"
    ]
  },
  "legal": {
    "applicable_law": "nyc-ll-144",
    "notice_text_url": "https://careers.example.com/aedt-notice",
    "notice_lead_business_days": 10,
    "bias_audit": {
      "conducted_on": "2025-11-15",
      "independent": True,
      "summary_url": "https://careers.example.com/aedt-bias-audit-2025",
      "auditor": "Example Audit LLP"
    }
  },
  "audit_log": {
    "fields": [
      "submission_hash",
      "redacted_text",
      "model_id",
      "prompt_hash",
      "rubric_version",
      "score_with_reasons",
      "human_decision"
    ],
    "retention_months": 24,
    "retention_basis": "29 CFR 1602.14 one-year floor; company policy two years",
    "queryable_per_candidate": True,
    "storage": "hiring.screen_audit table, candidate_id index"
  },
  "pinned_tuple": {
    "model_id": "claude-sonnet-4-5-20250929",
    "prompt_hash": "sha256:8e1f0a3c5b7d9f2e4a6c8b0d1f3e5a7c9b1d3f5e7a9c2b4d6f8a0c1e3b5d7f9a",
    "rubric_version": "2.1",
    "redaction_version": "1.3.0"
  },
  "evidence": [
    "https://hr.example.com/calibration/backend-2026-02",
    "https://hr.example.com/reviews/rubric-2.1-proxy-review",
    "https://careers.example.com/aedt-bias-audit-2025",
    "https://hr.example.com/adverse-impact/backend-2026-q1"
  ]
}

BAD = {
  "role_title": "Senior backend engineer",
  "candidate_jurisdictions": [
    "US-NY"
  ],
  "redaction": {
    "version": "1.0",
    "stripped_attributes": [
      "name",
      "photo",
      "email-handle"
    ],
    "unit_tested": False,
    "fixture_set_path": "hiring/redaction/fixtures/",
    "human_sample_inspected_per_release": False
  },
  "rubric": {
    "version": "1.0",
    "hash": "sha256:4c2a9b1e7f3d6a8c0b5e2f9d1a7c3e6b8f0d2a4c6e8b1d3f5a7c9e1b3d5f7a9c",
    "written_before_first_score": False,
    "criteria": [
      {
        "name": "overall impression",
        "job_requirement": "rate 1-10",
        "anchors": {
          "low": "weak",
          "mid": "ok",
          "high": "strong"
        }
      }
    ]
  },
  "proxy_review": {
    "reviewed_on": "2026-02-03",
    "reviewed_by": "dei:rkim",
    "proxy_terms_found": [
      "culture fit",
      "recent graduate"
    ],
    "evidence_url": "https://hr.example.com/reviews/rubric-1.0-proxy-review"
  },
  "calibration": {
    "sample_source": "synthetic-cvs",
    "sample_size": 50,
    "human_reviewers": 1,
    "statistic": "cohens-kappa",
    "threshold": 0.6,
    "threshold_set_before_run": False,
    "result": 0.92,
    "run_url": "https://hr.example.com/calibration/backend-synthetic",
    "passed": True
  },
  "adverse_impact": {
    "self_id_store": "hris.eeo_self_id",
    "self_id_store_separate_from_scoring": True,
    "hold_threshold": 0.8,
    "per_stage": [
      {
        "stage": "take-home forwarded",
        "groups": [
          {
            "group": "A",
            "selection_rate": 0.6
          },
          {
            "group": "B",
            "selection_rate": 0.4
          }
        ],
        "min_ratio": 0.67,
        "on_hold": False
      }
    ]
  },
  "human_of_record": {
    "auto_reject_filter_present": True,
    "decision_carries_role_handle": False,
    "reviewer_inputs": [
      "score-with-reasons"
    ]
  },
  "legal": {
    "applicable_law": "nyc-ll-144",
    "notice_lead_business_days": 3
  },
  "audit_log": {
    "fields": [
      "model_id",
      "score_with_reasons"
    ],
    "retention_months": 3,
    "queryable_per_candidate": False
  },
  "pinned_tuple": {
    "model_id": "gpt-4o-latest",
    "prompt_hash": "sha256:8e1f0a3c5b7d9f2e4a6c8b0d1f3e5a7c9b1d3f5e7a9c2b4d6f8a0c1e3b5d7f9a",
    "rubric_version": "1.0",
    "redaction_version": "1.0"
  },
  "evidence": [
    "https://hr.example.com/calibration/backend-synthetic"
  ]
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
        prog="validate-ai-pre-screen-bias-guardrails.py",
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
