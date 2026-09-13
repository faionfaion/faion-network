#!/usr/bin/env python3
"""validate-architectural-impact-pr-ranking.py

Validate the artefact produced by the architectural-impact-pr-ranking methodology against the JSON
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
  "$id": "faion://architectural-impact-pr-ranking/output.schema.json",
  "title": "Architectural impact PR ranking report",
  "type": "object",
  "required": [
    "window",
    "repositories",
    "session",
    "weights",
    "dependency_kind_weights",
    "signals_from_diff_only",
    "review_threshold",
    "ranked",
    "deferred",
    "exclusions",
    "merged_without_review",
    "previous_precision",
    "weights_changed",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "datetime": {
      "type": "string",
      "format": "date-time"
    },
    "handle": {
      "type": "string",
      "pattern": "^[a-z-]+:[a-z0-9._-]+$"
    },
    "pr_ref": {
      "type": "string",
      "pattern": "^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\\d+$",
      "description": "owner/repo#number"
    },
    "weights": {
      "type": "object",
      "required": [
        "modules_touched",
        "public_api_delta",
        "dependency_changes",
        "contract_changes",
        "infra_or_config_changes"
      ],
      "additionalProperties": False,
      "properties": {
        "modules_touched": {
          "type": "number",
          "minimum": 0
        },
        "public_api_delta": {
          "type": "number",
          "minimum": 0
        },
        "dependency_changes": {
          "type": "number",
          "minimum": 0
        },
        "contract_changes": {
          "type": "number",
          "minimum": 0
        },
        "infra_or_config_changes": {
          "type": "number",
          "minimum": 0
        }
      }
    },
    "signals": {
      "type": "object",
      "required": [
        "modules_touched",
        "public_api_delta",
        "dependency_changes",
        "contract_changes",
        "infra_or_config_changes"
      ],
      "additionalProperties": False,
      "properties": {
        "modules_touched": {
          "type": "integer",
          "minimum": 0
        },
        "public_api_delta": {
          "type": "integer",
          "minimum": 0
        },
        "dependency_changes": {
          "type": "number",
          "minimum": 0
        },
        "contract_changes": {
          "type": "integer",
          "minimum": 0
        },
        "infra_or_config_changes": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "scored_pr": {
      "type": "object",
      "required": [
        "pr",
        "score",
        "signals",
        "changed_lines",
        "read_minutes"
      ],
      "properties": {
        "pr": {
          "$ref": "#/definitions/pr_ref"
        },
        "title_context": {
          "type": "string"
        },
        "score": {
          "type": "number",
          "minimum": 0
        },
        "signals": {
          "$ref": "#/definitions/signals"
        },
        "changed_lines": {
          "type": "integer",
          "minimum": 0
        },
        "read_minutes": {
          "type": "integer",
          "minimum": 1
        }
      }
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "window": {
      "type": "object",
      "required": [
        "from",
        "to",
        "state_filter"
      ],
      "additionalProperties": False,
      "properties": {
        "from": {
          "$ref": "#/definitions/datetime"
        },
        "to": {
          "$ref": "#/definitions/datetime"
        },
        "state_filter": {
          "type": "string",
          "const": "opened-or-merged-in-window"
        }
      }
    },
    "repositories": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "has_public_api_list"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "pattern": "^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$"
          },
          "has_public_api_list": {
            "type": "boolean"
          },
          "public_api_paths_config": {
            "type": "string",
            "minLength": 3
          }
        },
        "if": {
          "properties": {
            "has_public_api_list": {
              "const": True
            }
          }
        },
        "then": {
          "required": [
            "public_api_paths_config"
          ]
        }
      }
    },
    "session": {
      "type": "object",
      "required": [
        "slot",
        "time_box_minutes",
        "top_n",
        "summed_read_minutes"
      ],
      "additionalProperties": False,
      "properties": {
        "slot": {
          "type": "string",
          "minLength": 3
        },
        "time_box_minutes": {
          "type": "integer",
          "minimum": 1
        },
        "top_n": {
          "type": "integer",
          "minimum": 1
        },
        "summed_read_minutes": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "weights": {
      "$ref": "#/definitions/weights"
    },
    "dependency_kind_weights": {
      "type": "object",
      "required": [
        "new_dependency",
        "major_bump",
        "minor_bump",
        "patch_bump",
        "removal",
        "lockfile_only"
      ],
      "additionalProperties": False,
      "properties": {
        "new_dependency": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "major_bump": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "minor_bump": {
          "type": "number",
          "minimum": 0
        },
        "patch_bump": {
          "type": "number",
          "minimum": 0,
          "maximum": 0.5
        },
        "removal": {
          "type": "number",
          "minimum": 0
        },
        "lockfile_only": {
          "type": "number",
          "const": 0
        }
      }
    },
    "signals_from_diff_only": {
      "type": "boolean",
      "const": True
    },
    "review_threshold": {
      "type": "number",
      "minimum": 0
    },
    "ranked": {
      "type": "array",
      "minItems": 1,
      "items": {
        "allOf": [
          {
            "$ref": "#/definitions/scored_pr"
          },
          {
            "type": "object",
            "required": [
              "rank",
              "outcome"
            ],
            "properties": {
              "rank": {
                "type": "integer",
                "minimum": 1
              },
              "outcome": {
                "type": "string",
                "enum": [
                  "hit",
                  "miss",
                  "pending"
                ]
              }
            }
          }
        ]
      }
    },
    "deferred": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/scored_pr"
      }
    },
    "exclusions": {
      "type": "object",
      "required": [
        "population_total",
        "bot_authors",
        "reverts",
        "docs_only",
        "generated_files"
      ],
      "additionalProperties": False,
      "properties": {
        "population_total": {
          "type": "integer",
          "minimum": 0
        },
        "bot_authors": {
          "type": "integer",
          "minimum": 0
        },
        "reverts": {
          "type": "integer",
          "minimum": 0
        },
        "docs_only": {
          "type": "integer",
          "minimum": 0
        },
        "generated_files": {
          "type": "integer",
          "minimum": 0
        },
        "below_threshold": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "merged_without_review": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "pr",
          "score",
          "merged_at",
          "merged_by"
        ],
        "additionalProperties": False,
        "properties": {
          "pr": {
            "$ref": "#/definitions/pr_ref"
          },
          "score": {
            "type": "number",
            "minimum": 0
          },
          "merged_at": {
            "$ref": "#/definitions/datetime"
          },
          "merged_by": {
            "$ref": "#/definitions/handle"
          }
        }
      }
    },
    "previous_precision": {
      "type": [
        "object",
        "None"
      ],
      "required": [
        "hits",
        "n",
        "value"
      ],
      "additionalProperties": False,
      "properties": {
        "hits": {
          "type": "integer",
          "minimum": 0
        },
        "n": {
          "type": "integer",
          "minimum": 1
        },
        "value": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      }
    },
    "weights_changed": {
      "type": "boolean"
    },
    "weight_change": {
      "type": "object",
      "required": [
        "previous_weights",
        "precision_weeks_cited",
        "precision_values"
      ],
      "additionalProperties": False,
      "properties": {
        "previous_weights": {
          "$ref": "#/definitions/weights"
        },
        "precision_weeks_cited": {
          "type": "integer",
          "minimum": 4
        },
        "precision_values": {
          "type": "array",
          "minItems": 4,
          "items": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
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
  },
  "if": {
    "properties": {
      "weights_changed": {
        "const": True
      }
    }
  },
  "then": {
    "required": [
      "weight_change"
    ]
  }
}

OK = {
  "window": {
    "from": "2026-09-01T00:00:00Z",
    "to": "2026-09-08T00:00:00Z",
    "state_filter": "opened-or-merged-in-window"
  },
  "repositories": [
    {
      "name": "acme/orders",
      "has_public_api_list": True,
      "public_api_paths_config": ".arch/public-api-paths.yaml"
    },
    {
      "name": "acme/billing",
      "has_public_api_list": True,
      "public_api_paths_config": ".arch/public-api-paths.yaml"
    },
    {
      "name": "acme/payments",
      "has_public_api_list": False
    }
  ],
  "session": {
    "slot": "Monday 10:00",
    "time_box_minutes": 45,
    "top_n": 4,
    "summed_read_minutes": 41
  },
  "weights": {
    "modules_touched": 1.0,
    "public_api_delta": 4.0,
    "dependency_changes": 2.0,
    "contract_changes": 4.0,
    "infra_or_config_changes": 1.5
  },
  "dependency_kind_weights": {
    "new_dependency": 3.0,
    "major_bump": 2.0,
    "minor_bump": 0.5,
    "patch_bump": 0.1,
    "removal": 1.0,
    "lockfile_only": 0
  },
  "signals_from_diff_only": True,
  "review_threshold": 8.0,
  "ranked": [
    {
      "rank": 1,
      "pr": "acme/orders#4412",
      "title_context": "small refactor of order status",
      "score": 27.5,
      "signals": {
        "modules_touched": 5,
        "public_api_delta": 2,
        "dependency_changes": 0,
        "contract_changes": 3,
        "infra_or_config_changes": 1
      },
      "changed_lines": 640,
      "read_minutes": 16,
      "outcome": "pending"
    },
    {
      "rank": 2,
      "pr": "acme/billing#902",
      "title_context": "add stripe-sdk",
      "score": 14.0,
      "signals": {
        "modules_touched": 2,
        "public_api_delta": 0,
        "dependency_changes": 3.0,
        "contract_changes": 1,
        "infra_or_config_changes": 2
      },
      "changed_lines": 310,
      "read_minutes": 10,
      "outcome": "pending"
    },
    {
      "rank": 3,
      "pr": "acme/orders#4398",
      "title_context": "BREAKING: rename test helper",
      "score": 9.5,
      "signals": {
        "modules_touched": 3,
        "public_api_delta": 0,
        "dependency_changes": 0,
        "contract_changes": 1,
        "infra_or_config_changes": 1
      },
      "changed_lines": 220,
      "read_minutes": 8,
      "outcome": "pending"
    },
    {
      "rank": 4,
      "pr": "acme/payments#77",
      "title_context": "migration: split ledger table",
      "score": 8.5,
      "signals": {
        "modules_touched": 4,
        "public_api_delta": 0,
        "dependency_changes": 0,
        "contract_changes": 1,
        "infra_or_config_changes": 1
      },
      "changed_lines": 190,
      "read_minutes": 7,
      "outcome": "pending"
    }
  ],
  "deferred": [
    {
      "pr": "acme/orders#4405",
      "score": 8.2,
      "signals": {
        "modules_touched": 6,
        "public_api_delta": 0,
        "dependency_changes": 0.5,
        "contract_changes": 0,
        "infra_or_config_changes": 1
      },
      "changed_lines": 1450,
      "read_minutes": 36
    }
  ],
  "exclusions": {
    "population_total": 143,
    "bot_authors": 31,
    "reverts": 2,
    "docs_only": 17,
    "generated_files": 4,
    "below_threshold": 84
  },
  "merged_without_review": [
    {
      "pr": "acme/billing#899",
      "score": 11.0,
      "merged_at": "2026-09-04T22:41:00Z",
      "merged_by": "swe:dpark"
    }
  ],
  "previous_precision": {
    "hits": 3,
    "n": 4,
    "value": 0.75
  },
  "weights_changed": False,
  "evidence": [
    "https://ci.example.com/arch-rank/run/2026-09-08",
    "https://github.com/acme/orders/blob/main/.arch/public-api-paths.yaml",
    "https://wiki.example.com/arch-review/2026-09-01"
  ]
}

BAD = {
  "window": {
    "from": "2026-09-01T00:00:00Z",
    "to": "2026-09-08T00:00:00Z",
    "state_filter": "open-only"
  },
  "repositories": [
    {
      "name": "acme/orders",
      "has_public_api_list": True
    },
    {
      "name": "acme/payments",
      "has_public_api_list": False
    }
  ],
  "session": {
    "slot": "Monday 10:00",
    "time_box_minutes": 45,
    "top_n": 10,
    "summed_read_minutes": 190
  },
  "weights": {
    "modules_touched": 1.0,
    "public_api_delta": 4.0,
    "dependency_changes": 2.0,
    "contract_changes": 4.0
  },
  "dependency_kind_weights": {
    "new_dependency": 1.0,
    "major_bump": 1.0,
    "minor_bump": 1.0,
    "patch_bump": 1.0,
    "removal": 1.0,
    "lockfile_only": 1.0
  },
  "signals_from_diff_only": False,
  "review_threshold": 8.0,
  "ranked": [
    {
      "rank": 1,
      "pr": "acme/orders#4398",
      "title_context": "BREAKING: rename test helper",
      "score": 30.0,
      "signals": {
        "modules_touched": 3,
        "public_api_delta": 0,
        "dependency_changes": 0,
        "contract_changes": 1,
        "infra_or_config_changes": 1
      },
      "changed_lines": 220,
      "read_minutes": 8
    },
    {
      "rank": 2,
      "pr": "acme/orders#4412",
      "score": 12.0,
      "signals": {
        "modules_touched": 5,
        "public_api_delta": 2,
        "dependency_changes": 0,
        "contract_changes": 3,
        "infra_or_config_changes": 1
      },
      "outcome": "pending"
    }
  ],
  "deferred": [],
  "exclusions": {
    "population_total": 143,
    "bot_authors": 0,
    "reverts": 2,
    "docs_only": 17,
    "generated_files": 4
  },
  "previous_precision": None,
  "weights_changed": True,
  "weight_change": {
    "previous_weights": {
      "modules_touched": 1.0,
      "public_api_delta": 3.0,
      "dependency_changes": 2.0,
      "contract_changes": 4.0,
      "infra_or_config_changes": 1.5
    },
    "precision_weeks_cited": 1,
    "precision_values": [
      0.5
    ]
  },
  "evidence": [
    "https://ci.example.com/arch-rank/run/2026-09-08"
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
        prog="validate-architectural-impact-pr-ranking.py",
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
