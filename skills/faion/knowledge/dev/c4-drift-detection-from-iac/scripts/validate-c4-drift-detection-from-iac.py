#!/usr/bin/env python3
"""validate-c4-drift-detection-from-iac.py

Validate the artefact produced by the c4-drift-detection-from-iac methodology against the JSON
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
  "$id": "faion://c4-drift-detection-from-iac/output.schema.json",
  "title": "C4 versus IaC drift report",
  "type": "object",
  "required": [
    "system_name",
    "c4_model",
    "iac_state",
    "comparison_level",
    "mapping_table",
    "allowlist",
    "run",
    "findings",
    "unmapped",
    "reconciliation",
    "escalated_finding_ids",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "sha": {
      "type": "string",
      "pattern": "^[0-9a-f]{7,40}$"
    },
    "date": {
      "type": "string",
      "format": "date",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    },
    "datetime": {
      "type": "string",
      "format": "date-time"
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
    "c4_model": {
      "type": "object",
      "required": [
        "format",
        "path",
        "commit"
      ],
      "additionalProperties": False,
      "properties": {
        "format": {
          "type": "string",
          "enum": [
            "structurizr-dsl",
            "structurizr-json",
            "likec4",
            "model-yaml",
            "model-json"
          ]
        },
        "path": {
          "type": "string",
          "minLength": 3
        },
        "commit": {
          "$ref": "#/definitions/sha"
        }
      }
    },
    "iac_state": {
      "type": "object",
      "required": [
        "tool",
        "source",
        "identity"
      ],
      "additionalProperties": False,
      "properties": {
        "tool": {
          "type": "string",
          "enum": [
            "terraform",
            "pulumi",
            "cloudformation"
          ]
        },
        "source": {
          "type": "string",
          "enum": [
            "terraform-show-json",
            "pulumi-stack-export",
            "cloudformation-describe-stack-resources"
          ]
        },
        "identity": {
          "type": "object",
          "additionalProperties": False,
          "properties": {
            "serial": {
              "type": "integer",
              "minimum": 0
            },
            "lineage": {
              "type": "string",
              "minLength": 8
            },
            "export_version": {
              "type": "integer",
              "minimum": 0
            },
            "stack_id": {
              "type": "string",
              "minLength": 8
            },
            "last_updated_at": {
              "$ref": "#/definitions/datetime"
            }
          }
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "tool": {
                "const": "terraform"
              }
            }
          },
          "then": {
            "properties": {
              "source": {
                "const": "terraform-show-json"
              },
              "identity": {
                "required": [
                  "serial",
                  "lineage"
                ]
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "tool": {
                "const": "pulumi"
              }
            }
          },
          "then": {
            "properties": {
              "source": {
                "const": "pulumi-stack-export"
              },
              "identity": {
                "required": [
                  "export_version"
                ]
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "tool": {
                "const": "cloudformation"
              }
            }
          },
          "then": {
            "properties": {
              "source": {
                "const": "cloudformation-describe-stack-resources"
              },
              "identity": {
                "required": [
                  "stack_id",
                  "last_updated_at"
                ]
              }
            }
          }
        }
      ]
    },
    "comparison_level": {
      "type": "string",
      "enum": [
        "container",
        "system-context"
      ]
    },
    "mapping_table": {
      "type": "object",
      "required": [
        "path",
        "commit"
      ],
      "additionalProperties": False,
      "properties": {
        "path": {
          "type": "string",
          "minLength": 3
        },
        "commit": {
          "$ref": "#/definitions/sha"
        }
      }
    },
    "allowlist": {
      "type": "object",
      "required": [
        "path",
        "commit",
        "hardcoded_skips_in_script",
        "suppressed"
      ],
      "additionalProperties": False,
      "properties": {
        "path": {
          "type": "string",
          "minLength": 3
        },
        "commit": {
          "$ref": "#/definitions/sha"
        },
        "hardcoded_skips_in_script": {
          "type": "boolean",
          "const": False
        },
        "suppressed": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "entry",
              "count"
            ],
            "additionalProperties": False,
            "properties": {
              "entry": {
                "type": "string",
                "minLength": 2
              },
              "count": {
                "type": "integer",
                "minimum": 0
              }
            }
          }
        }
      }
    },
    "run": {
      "type": "object",
      "required": [
        "trigger",
        "ran_at",
        "cadence",
        "post_apply_hook_wired"
      ],
      "additionalProperties": False,
      "properties": {
        "trigger": {
          "type": "string",
          "enum": [
            "post-apply",
            "schedule"
          ]
        },
        "ran_at": {
          "$ref": "#/definitions/datetime"
        },
        "cadence": {
          "type": "string",
          "enum": [
            "hourly",
            "daily",
            "weekly"
          ]
        },
        "post_apply_hook_wired": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "class",
          "iac_address",
          "c4_element_id",
          "description",
          "closure",
          "reports_open"
        ],
        "additionalProperties": False,
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^drift-\\d{4,}$"
          },
          "class": {
            "type": "string",
            "enum": [
              "added",
              "removed",
              "edge-changed"
            ]
          },
          "iac_address": {
            "type": "string",
            "minLength": 3
          },
          "c4_element_id": {
            "type": "string",
            "minLength": 2
          },
          "description": {
            "type": "string",
            "minLength": 10
          },
          "closure": {
            "type": "object",
            "required": [
              "kind"
            ],
            "additionalProperties": False,
            "properties": {
              "kind": {
                "type": "string",
                "enum": [
                  "model-commit",
                  "iac-change",
                  "accepted",
                  "open"
                ]
              },
              "commit": {
                "$ref": "#/definitions/sha"
              },
              "reason": {
                "type": "string",
                "minLength": 10
              },
              "expires_on": {
                "$ref": "#/definitions/date"
              }
            },
            "allOf": [
              {
                "if": {
                  "properties": {
                    "kind": {
                      "enum": [
                        "model-commit",
                        "iac-change"
                      ]
                    }
                  }
                },
                "then": {
                  "required": [
                    "commit"
                  ]
                }
              },
              {
                "if": {
                  "properties": {
                    "kind": {
                      "const": "accepted"
                    }
                  }
                },
                "then": {
                  "required": [
                    "reason",
                    "expires_on"
                  ]
                }
              }
            ]
          },
          "reports_open": {
            "type": "integer",
            "minimum": 1
          }
        }
      }
    },
    "unmapped": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "resource_type",
          "count"
        ],
        "additionalProperties": False,
        "properties": {
          "resource_type": {
            "type": "string",
            "minLength": 3
          },
          "count": {
            "type": "integer",
            "minimum": 1
          }
        }
      }
    },
    "reconciliation": {
      "type": "object",
      "required": [
        "state_resources_total",
        "allowlisted",
        "mapped",
        "unmapped"
      ],
      "additionalProperties": False,
      "properties": {
        "state_resources_total": {
          "type": "integer",
          "minimum": 0
        },
        "allowlisted": {
          "type": "integer",
          "minimum": 0
        },
        "mapped": {
          "type": "integer",
          "minimum": 0
        },
        "unmapped": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "escalated_finding_ids": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^drift-\\d{4,}$"
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
  "system_name": "orders-platform (prod)",
  "c4_model": {
    "format": "structurizr-dsl",
    "path": "docs/c4/workspace.dsl",
    "commit": "3f9a2c1d"
  },
  "iac_state": {
    "tool": "terraform",
    "source": "terraform-show-json",
    "identity": {
      "serial": 412,
      "lineage": "6c1f0b2e-8a3d-4f5e-9b7c-1d2e3f4a5b6c"
    }
  },
  "comparison_level": "container",
  "mapping_table": {
    "path": "docs/c4/iac-mapping.yaml",
    "commit": "3f9a2c1d"
  },
  "allowlist": {
    "path": "docs/c4/iac-allowlist.yaml",
    "commit": "3f9a2c1d",
    "hardcoded_skips_in_script": False,
    "suppressed": [
      {
        "entry": "aws_cloudwatch_log_group",
        "count": 14
      },
      {
        "entry": "aws_iam_role",
        "count": 22
      },
      {
        "entry": "aws_iam_role_policy_attachment",
        "count": 31
      },
      {
        "entry": "random_id",
        "count": 3
      },
      {
        "entry": "aws_route53_record (same host)",
        "count": 6
      }
    ]
  },
  "run": {
    "trigger": "post-apply",
    "ran_at": "2026-09-08T14:02:11Z",
    "cadence": "weekly",
    "post_apply_hook_wired": True
  },
  "findings": [
    {
      "id": "drift-0041",
      "class": "added",
      "iac_address": "aws_sqs_queue.orders_dlq",
      "c4_element_id": "expected:orders.dlq",
      "description": "Dead-letter queue applied on 2026-09-04; no container in the model",
      "closure": {
        "kind": "model-commit",
        "commit": "8b1e4d7a"
      },
      "reports_open": 1
    },
    {
      "id": "drift-0042",
      "class": "edge-changed",
      "iac_address": "aws_security_group_rule.api_to_ledger_5432",
      "c4_element_id": "orders.api -> ledger.db",
      "description": "Security group now allows orders-api to reach the ledger database directly; model shows access only via ledger-service",
      "closure": {
        "kind": "open"
      },
      "reports_open": 1
    },
    {
      "id": "drift-0037",
      "class": "removed",
      "iac_address": "aws_elasticache_cluster.session_cache",
      "c4_element_id": "orders.session-cache",
      "description": "Session cache still in the model; removed from state at serial 398",
      "closure": {
        "kind": "accepted",
        "reason": "Cache is being replaced by the token service in Q4; model updated when the replacement lands",
        "expires_on": "2026-10-06"
      },
      "reports_open": 2
    }
  ],
  "unmapped": [
    {
      "resource_type": "aws_msk_serverless_cluster",
      "count": 1
    }
  ],
  "reconciliation": {
    "state_resources_total": 131,
    "allowlisted": 76,
    "mapped": 54,
    "unmapped": 1
  },
  "escalated_finding_ids": [
    "drift-0037"
  ],
  "evidence": [
    "https://ci.example.com/c4-drift/orders-platform/run/2026-09-08",
    "https://github.com/acme/orders-infra/blob/3f9a2c1d/docs/c4/iac-mapping.yaml",
    "https://github.com/acme/orders-infra/blob/3f9a2c1d/docs/c4/iac-allowlist.yaml",
    "https://ci.example.com/c4-drift/orders-platform/run/2026-09-01"
  ]
}

BAD = {
  "system_name": "orders-platform (prod)",
  "c4_model": {
    "format": "png",
    "path": "docs/architecture.png",
    "commit": "3f9a2c1d"
  },
  "iac_state": {
    "tool": "terraform",
    "source": "terraform-show-json",
    "identity": {}
  },
  "comparison_level": "container",
  "mapping_table": {
    "path": "docs/c4/iac-mapping.yaml",
    "commit": "3f9a2c1d"
  },
  "allowlist": {
    "path": "docs/c4/iac-allowlist.yaml",
    "commit": "3f9a2c1d",
    "hardcoded_skips_in_script": True,
    "suppressed": []
  },
  "run": {
    "trigger": "schedule",
    "ran_at": "2026-09-08T14:02:11Z",
    "cadence": "weekly",
    "post_apply_hook_wired": False
  },
  "findings": [
    {
      "id": "drift-0041",
      "class": "added",
      "iac_address": "aws_sqs_queue.orders_dlq",
      "c4_element_id": "expected:orders.dlq",
      "description": "Dead-letter queue with no container in the model",
      "closure": {
        "kind": "model-commit"
      },
      "reports_open": 1
    },
    {
      "id": "drift-0037",
      "class": "removed",
      "iac_address": "aws_elasticache_cluster.session_cache",
      "c4_element_id": "orders.session-cache",
      "description": "Cache still in the model",
      "closure": {
        "kind": "accepted",
        "reason": "known, ignore"
      },
      "reports_open": 3
    },
    {
      "id": "drift-0043",
      "class": "diagram-stale",
      "iac_address": "",
      "c4_element_id": "",
      "description": "The diagram is a bit out of date",
      "closure": {
        "kind": "open"
      },
      "reports_open": 1
    }
  ],
  "unmapped": [],
  "reconciliation": {
    "state_resources_total": 131,
    "allowlisted": 0,
    "mapped": 54,
    "unmapped": 0
  },
  "escalated_finding_ids": [],
  "evidence": [
    "https://ci.example.com/c4-drift/orders-platform/run/2026-09-08"
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
        prog="validate-c4-drift-detection-from-iac.py",
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
