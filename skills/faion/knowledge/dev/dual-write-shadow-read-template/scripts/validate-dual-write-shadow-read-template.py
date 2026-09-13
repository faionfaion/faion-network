#!/usr/bin/env python3
"""validate-dual-write-shadow-read-template.py

Validate the artefact produced by the dual-write-shadow-read-template methodology against the JSON
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
  "$id": "faion://dual-write-shadow-read-template/output.schema.json",
  "title": "Dual-write + shadow-read migration runbook",
  "type": "object",
  "required": [
    "migration_name",
    "kind",
    "old_store",
    "new_store",
    "entity_types",
    "dual_write",
    "reconciliation",
    "backfill",
    "shadow_read",
    "flags",
    "cutover",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "handle": {
      "type": "string",
      "pattern": "^[a-z-]+:[a-z0-9._-]+$"
    },
    "flag_name": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_.-]*$"
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "migration_name": {
      "type": "string",
      "minLength": 3
    },
    "kind": {
      "type": "string",
      "enum": [
        "postgres-major-upgrade",
        "monolith-to-service-split",
        "schema-rewrite",
        "datastore-swap",
        "other"
      ]
    },
    "old_store": {
      "type": "string",
      "minLength": 2
    },
    "new_store": {
      "type": "string",
      "minLength": 2
    },
    "entity_types": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "primary_key",
          "version_field",
          "parity_excluded_fields",
          "gate"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "minLength": 2
          },
          "primary_key": {
            "type": "string",
            "minLength": 1
          },
          "version_field": {
            "type": "string",
            "minLength": 1,
            "description": "row version, updated_at, or log sequence number"
          },
          "parity_excluded_fields": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "gate": {
            "type": "object",
            "required": [
              "mismatch_ratio_max",
              "window_hours",
              "min_comparisons"
            ],
            "additionalProperties": False,
            "properties": {
              "mismatch_ratio_max": {
                "type": "number",
                "minimum": 0,
                "exclusiveMaximum": 1
              },
              "window_hours": {
                "type": "integer",
                "minimum": 1
              },
              "min_comparisons": {
                "type": "integer",
                "minimum": 1
              }
            }
          }
        }
      }
    },
    "dual_write": {
      "type": "object",
      "required": [
        "upsert_kind",
        "compare_and_set_on_version",
        "outside_old_store_transaction",
        "failure_fails_user_request",
        "retry_queue",
        "failure_metric",
        "alert_threshold"
      ],
      "additionalProperties": False,
      "properties": {
        "upsert_kind": {
          "type": "string",
          "const": "version-guarded-upsert"
        },
        "compare_and_set_on_version": {
          "type": "boolean",
          "const": True
        },
        "outside_old_store_transaction": {
          "type": "boolean",
          "const": True
        },
        "failure_fails_user_request": {
          "type": "boolean",
          "const": False
        },
        "retry_queue": {
          "type": "string",
          "minLength": 2
        },
        "failure_metric": {
          "type": "string",
          "const": "dual_write_failures_total"
        },
        "alert_threshold": {
          "type": "number",
          "exclusiveMinimum": 0
        }
      }
    },
    "reconciliation": {
      "type": "object",
      "required": [
        "job_name",
        "cadence",
        "max_repairs_per_run",
        "metric",
        "declared_before_dual_write"
      ],
      "additionalProperties": False,
      "properties": {
        "job_name": {
          "type": "string",
          "minLength": 2
        },
        "cadence": {
          "type": "string",
          "enum": [
            "every-5-minutes",
            "hourly",
            "every-6-hours",
            "daily",
            "weekly"
          ]
        },
        "max_repairs_per_run": {
          "type": "integer",
          "minimum": 0
        },
        "metric": {
          "type": "string",
          "const": "reconciliation_repairs_total"
        },
        "declared_before_dual_write": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "backfill": {
      "type": "object",
      "required": [
        "starts_after_dual_write",
        "uses_same_upsert",
        "per_partition_counts_match",
        "checksum_match",
        "completed_before_shadow_parity"
      ],
      "additionalProperties": False,
      "properties": {
        "starts_after_dual_write": {
          "type": "boolean",
          "const": True
        },
        "uses_same_upsert": {
          "type": "boolean",
          "const": True
        },
        "per_partition_counts_match": {
          "type": "boolean",
          "const": True
        },
        "checksum_match": {
          "type": "boolean",
          "const": True
        },
        "completed_before_shadow_parity": {
          "type": "boolean",
          "const": True
        },
        "partitions": {
          "type": "integer",
          "minimum": 1
        }
      }
    },
    "shadow_read": {
      "type": "object",
      "required": [
        "comparator",
        "returns_old_store_result",
        "candidate_timeout_ms",
        "old_store_p99_ms",
        "exceptions_swallowed_and_counted",
        "sampling_flag",
        "sampling_percent_initial",
        "mismatch_metric",
        "mismatch_samples_retained"
      ],
      "additionalProperties": False,
      "properties": {
        "comparator": {
          "type": "string",
          "const": "normalising"
        },
        "returns_old_store_result": {
          "type": "boolean",
          "const": True
        },
        "candidate_timeout_ms": {
          "type": "integer",
          "minimum": 1
        },
        "old_store_p99_ms": {
          "type": "integer",
          "minimum": 1
        },
        "exceptions_swallowed_and_counted": {
          "type": "boolean",
          "const": True
        },
        "sampling_flag": {
          "$ref": "#/definitions/flag_name"
        },
        "sampling_percent_initial": {
          "type": "number",
          "minimum": 0,
          "exclusiveMaximum": 100
        },
        "mismatch_metric": {
          "type": "string",
          "const": "shadow_read_mismatch_ratio"
        },
        "mismatch_samples_retained": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "flags": {
      "type": "object",
      "required": [
        "dual_write_on",
        "shadow_read_on",
        "read_from_new_on",
        "write_to_old_off",
        "runtime_flippable",
        "reverse_order",
        "retention_window_days",
        "read_flipback_rehearsed_before_write_off"
      ],
      "additionalProperties": False,
      "properties": {
        "dual_write_on": {
          "$ref": "#/definitions/flag_name"
        },
        "shadow_read_on": {
          "$ref": "#/definitions/flag_name"
        },
        "read_from_new_on": {
          "$ref": "#/definitions/flag_name"
        },
        "write_to_old_off": {
          "$ref": "#/definitions/flag_name"
        },
        "runtime_flippable": {
          "type": "boolean",
          "const": True
        },
        "reverse_order": {
          "type": "array",
          "minItems": 4,
          "maxItems": 4,
          "uniqueItems": True,
          "items": {
            "type": "string",
            "enum": [
              "write_to_old_off",
              "read_from_new_on",
              "shadow_read_on",
              "dual_write_on"
            ]
          }
        },
        "retention_window_days": {
          "type": "integer",
          "minimum": 1
        },
        "read_flipback_rehearsed_before_write_off": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "cutover": {
      "type": "object",
      "required": [
        "gate_declared_before_shadow",
        "read_from_new_approver",
        "write_to_old_off_approver"
      ],
      "additionalProperties": False,
      "properties": {
        "gate_declared_before_shadow": {
          "type": "boolean",
          "const": True
        },
        "gate_evaluation_url": {
          "type": "string",
          "format": "uri"
        },
        "read_from_new_flipped": {
          "type": "boolean"
        },
        "read_from_new_approver": {
          "$ref": "#/definitions/handle"
        },
        "write_to_old_off_approver": {
          "$ref": "#/definitions/handle"
        }
      },
      "if": {
        "properties": {
          "read_from_new_flipped": {
            "const": True
          }
        }
      },
      "then": {
        "required": [
          "gate_evaluation_url"
        ]
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
  "migration_name": "orders-db Postgres 13 to 16 with partitioned ledger",
  "kind": "postgres-major-upgrade",
  "old_store": "pg13.orders",
  "new_store": "pg16.orders",
  "entity_types": [
    {
      "name": "order",
      "primary_key": "order_id",
      "version_field": "row_version",
      "parity_excluded_fields": [
        "updated_at",
        "search_vector"
      ],
      "gate": {
        "mismatch_ratio_max": 0.001,
        "window_hours": 72,
        "min_comparisons": 50000
      }
    },
    {
      "name": "ledger_entry",
      "primary_key": "entry_id",
      "version_field": "lsn",
      "parity_excluded_fields": [
        "inserted_at"
      ],
      "gate": {
        "mismatch_ratio_max": 0.0001,
        "window_hours": 72,
        "min_comparisons": 200000
      }
    },
    {
      "name": "customer_note",
      "primary_key": "note_id",
      "version_field": "updated_at",
      "parity_excluded_fields": [
        "updated_at",
        "tsv"
      ],
      "gate": {
        "mismatch_ratio_max": 0.005,
        "window_hours": 168,
        "min_comparisons": 2000
      }
    }
  ],
  "dual_write": {
    "upsert_kind": "version-guarded-upsert",
    "compare_and_set_on_version": True,
    "outside_old_store_transaction": True,
    "failure_fails_user_request": False,
    "retry_queue": "sqs.orders-dual-write-retry",
    "failure_metric": "dual_write_failures_total",
    "alert_threshold": 50
  },
  "reconciliation": {
    "job_name": "orders-reconcile-keywalk",
    "cadence": "hourly",
    "max_repairs_per_run": 20,
    "metric": "reconciliation_repairs_total",
    "declared_before_dual_write": True
  },
  "backfill": {
    "starts_after_dual_write": True,
    "uses_same_upsert": True,
    "per_partition_counts_match": True,
    "checksum_match": True,
    "completed_before_shadow_parity": True,
    "partitions": 64
  },
  "shadow_read": {
    "comparator": "normalising",
    "returns_old_store_result": True,
    "candidate_timeout_ms": 45,
    "old_store_p99_ms": 48,
    "exceptions_swallowed_and_counted": True,
    "sampling_flag": "orders.shadow_read_percent",
    "sampling_percent_initial": 5,
    "mismatch_metric": "shadow_read_mismatch_ratio",
    "mismatch_samples_retained": True
  },
  "flags": {
    "dual_write_on": "orders.dual_write_on",
    "shadow_read_on": "orders.shadow_read_on",
    "read_from_new_on": "orders.read_from_new_on",
    "write_to_old_off": "orders.write_to_old_off",
    "runtime_flippable": True,
    "reverse_order": [
      "write_to_old_off",
      "read_from_new_on",
      "shadow_read_on",
      "dual_write_on"
    ],
    "retention_window_days": 14,
    "read_flipback_rehearsed_before_write_off": True
  },
  "cutover": {
    "gate_declared_before_shadow": True,
    "gate_evaluation_url": "https://grafana.example.com/d/orders-parity?from=2026-09-01&to=2026-09-04",
    "read_from_new_flipped": True,
    "read_from_new_approver": "arch:nkovacs",
    "write_to_old_off_approver": "dba:marta"
  },
  "evidence": [
    "https://grafana.example.com/d/orders-reconciliation",
    "https://ci.example.com/orders/backfill-verify/run/77",
    "https://grafana.example.com/d/orders-parity?from=2026-09-01&to=2026-09-04",
    "https://wiki.example.com/orders/flipback-rehearsal-2026-09-05"
  ]
}

BAD = {
  "migration_name": "orders-db Postgres 13 to 16",
  "kind": "postgres-major-upgrade",
  "old_store": "pg13.orders",
  "new_store": "pg16.orders",
  "entity_types": [
    {
      "name": "order",
      "primary_key": "order_id",
      "version_field": "row_version",
      "parity_excluded_fields": [],
      "gate": {
        "mismatch_ratio_max": 1,
        "window_hours": 0,
        "min_comparisons": 0
      }
    }
  ],
  "dual_write": {
    "upsert_kind": "plain-insert",
    "compare_and_set_on_version": False,
    "outside_old_store_transaction": False,
    "failure_fails_user_request": True,
    "retry_queue": "",
    "failure_metric": "errors",
    "alert_threshold": 0
  },
  "reconciliation": {
    "job_name": "none",
    "cadence": "weekly",
    "max_repairs_per_run": 0,
    "metric": "reconciliation_repairs_total",
    "declared_before_dual_write": False
  },
  "backfill": {
    "starts_after_dual_write": False,
    "uses_same_upsert": False,
    "per_partition_counts_match": True,
    "checksum_match": False,
    "completed_before_shadow_parity": False
  },
  "shadow_read": {
    "comparator": "raw",
    "returns_old_store_result": False,
    "candidate_timeout_ms": 5000,
    "old_store_p99_ms": 48,
    "exceptions_swallowed_and_counted": False,
    "sampling_flag": "orders.shadow_read_percent",
    "sampling_percent_initial": 100,
    "mismatch_metric": "shadow_read_mismatch_ratio",
    "mismatch_samples_retained": False
  },
  "flags": {
    "dual_write_on": "orders.migrated",
    "shadow_read_on": "orders.migrated",
    "read_from_new_on": "orders.migrated",
    "write_to_old_off": "orders.migrated",
    "runtime_flippable": False,
    "reverse_order": [
      "write_to_old_off"
    ],
    "retention_window_days": 0,
    "read_flipback_rehearsed_before_write_off": False
  },
  "cutover": {
    "gate_declared_before_shadow": False,
    "read_from_new_flipped": True,
    "read_from_new_approver": "team:data",
    "write_to_old_off_approver": "team:data"
  },
  "evidence": [
    "https://grafana.example.com/d/orders-parity"
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
        prog="validate-dual-write-shadow-read-template.py",
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
