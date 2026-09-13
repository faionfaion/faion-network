#!/usr/bin/env python3
"""validate-ai-llm-workload-architecture.py

Validate the artefact produced by the ai-llm-workload-architecture methodology against the JSON
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
  "$id": "faion://ai-llm-workload-architecture/output.schema.json",
  "title": "AI LLM workload architecture spec",
  "type": "object",
  "required": [
    "feature_name",
    "eval_set",
    "scoring",
    "baseline_run",
    "metrics",
    "regression_gate",
    "production_model_id",
    "budgets",
    "untrusted_input_channels",
    "degradation",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "pinned_model_id": {
      "type": "string",
      "minLength": 3,
      "pattern": "(\\d{4}-\\d{2}-\\d{2}|\\d{8}|@\\d+|:\\d+|-v\\d+(\\.\\d+)*$)",
      "not": {
        "pattern": "(?i)(^|[-:@/_])latest$"
      },
      "description": "dated (YYYYMMDD / YYYY-MM-DD) or explicitly versioned (@N, :N, -vN); never an alias"
    },
    "sha256": {
      "type": "string",
      "pattern": "^sha256:[0-9a-f]{64}$"
    },
    "case_ids": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "minLength": 1
      }
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "feature_name": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "pattern": "^[a-z-]+:[a-z0-9._-]+$"
    },
    "eval_set": {
      "type": "object",
      "required": [
        "path",
        "ref",
        "case_count",
        "contamination_check_passed"
      ],
      "additionalProperties": False,
      "properties": {
        "path": {
          "type": "string",
          "minLength": 3,
          "not": {
            "pattern": "\\.ipynb$"
          }
        },
        "ref": {
          "type": "string",
          "pattern": "^([0-9a-f]{7,40}|sha256:[0-9a-f]{64})$",
          "description": "git ref or content hash - the eval_set_ref input"
        },
        "case_count": {
          "type": "integer",
          "minimum": 1
        },
        "contamination_check_passed": {
          "type": "boolean",
          "const": True
        },
        "contamination_check_job": {
          "type": "string"
        }
      }
    },
    "scoring": {
      "type": "object",
      "required": [
        "kind"
      ],
      "additionalProperties": False,
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "exact-match",
            "regex",
            "json-schema",
            "unit-assertion",
            "llm-judge"
          ]
        },
        "judge": {
          "type": "object",
          "required": [
            "model_id",
            "temperature",
            "prompt_hash",
            "noise_floor"
          ],
          "additionalProperties": False,
          "properties": {
            "model_id": {
              "$ref": "#/definitions/pinned_model_id"
            },
            "temperature": {
              "type": "number",
              "const": 0
            },
            "prompt_hash": {
              "$ref": "#/definitions/sha256"
            },
            "noise_floor": {
              "type": "number",
              "minimum": 0,
              "description": "max score delta between two runs at the same commit"
            }
          }
        }
      },
      "if": {
        "properties": {
          "kind": {
            "const": "llm-judge"
          }
        }
      },
      "then": {
        "required": [
          "judge"
        ]
      }
    },
    "baseline_run": {
      "type": "object",
      "required": [
        "url",
        "commit"
      ],
      "additionalProperties": False,
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        },
        "commit": {
          "type": "string",
          "pattern": "^[0-9a-f]{7,40}$"
        },
        "run_at": {
          "type": "string",
          "format": "date"
        }
      }
    },
    "metrics": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "baseline",
          "tolerance",
          "threshold",
          "direction"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "minLength": 2
          },
          "baseline": {
            "type": "number"
          },
          "tolerance": {
            "type": "number",
            "description": "signed allowance from baseline; negative for higher-is-better metrics"
          },
          "threshold": {
            "type": "number",
            "description": "baseline plus tolerance"
          },
          "direction": {
            "type": "string",
            "enum": [
              "higher-is-better",
              "lower-is-better"
            ]
          }
        }
      }
    },
    "regression_gate": {
      "type": "object",
      "required": [
        "ci_job",
        "blocks_merge",
        "watched_paths",
        "prompts_in_version_control"
      ],
      "additionalProperties": False,
      "properties": {
        "ci_job": {
          "type": "string",
          "minLength": 2
        },
        "blocks_merge": {
          "type": "boolean",
          "const": True
        },
        "watched_paths": {
          "type": "array",
          "minItems": 2,
          "items": {
            "type": "string",
            "minLength": 2
          },
          "description": "prompts, model config, retrieval config, tool schemas"
        },
        "prompts_in_version_control": {
          "type": "boolean",
          "const": True
        },
        "prompt_hash_logged_at_startup": {
          "type": "boolean"
        }
      }
    },
    "production_model_id": {
      "$ref": "#/definitions/pinned_model_id"
    },
    "budgets": {
      "type": "object",
      "required": [
        "p95_latency_ms",
        "per_request",
        "measured_in_eval_run"
      ],
      "additionalProperties": False,
      "properties": {
        "p95_latency_ms": {
          "type": "integer",
          "minimum": 1
        },
        "per_request": {
          "type": "object",
          "additionalProperties": False,
          "properties": {
            "tokens": {
              "type": "integer",
              "minimum": 1
            },
            "cost_usd": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "anyOf": [
            {
              "required": [
                "tokens"
              ]
            },
            {
              "required": [
                "cost_usd"
              ]
            }
          ]
        },
        "measured_in_eval_run": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "untrusted_input_channels": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "channel",
          "kind",
          "injection_case_ids"
        ],
        "additionalProperties": False,
        "properties": {
          "channel": {
            "type": "string",
            "minLength": 2
          },
          "kind": {
            "type": "string",
            "enum": [
              "retrieval-source",
              "tool-output",
              "user-turn"
            ]
          },
          "injection_case_ids": {
            "$ref": "#/definitions/case_ids"
          }
        }
      }
    },
    "degradation": {
      "type": "object",
      "required": [
        "retry",
        "fallback",
        "user_message"
      ],
      "additionalProperties": False,
      "properties": {
        "retry": {
          "type": "object",
          "required": [
            "max_attempts",
            "backoff",
            "base_delay_ms"
          ],
          "additionalProperties": False,
          "properties": {
            "max_attempts": {
              "type": "integer",
              "minimum": 0,
              "maximum": 10
            },
            "backoff": {
              "type": "string",
              "enum": [
                "exponential-with-jitter",
                "exponential",
                "fixed"
              ]
            },
            "base_delay_ms": {
              "type": "integer",
              "minimum": 1
            },
            "triggers": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "timeout",
                  "429",
                  "5xx"
                ]
              }
            }
          }
        },
        "fallback": {
          "type": "object",
          "required": [
            "kind",
            "eval_case_ids"
          ],
          "additionalProperties": False,
          "properties": {
            "kind": {
              "type": "string",
              "enum": [
                "secondary-pinned-model",
                "cached-answer",
                "explicit-refusal"
              ]
            },
            "model_id": {
              "$ref": "#/definitions/pinned_model_id"
            },
            "eval_case_ids": {
              "$ref": "#/definitions/case_ids"
            }
          },
          "if": {
            "properties": {
              "kind": {
                "const": "secondary-pinned-model"
              }
            }
          },
          "then": {
            "required": [
              "model_id"
            ]
          }
        },
        "user_message": {
          "type": "string",
          "minLength": 10
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
  "feature_name": "support-ticket summariser",
  "owner": "swe:alice",
  "eval_set": {
    "path": "evals/summariser/cases.jsonl",
    "ref": "a1b2c3d4e5f",
    "case_count": 142,
    "contamination_check_passed": True,
    "contamination_check_job": "ci/eval-contamination-grep"
  },
  "scoring": {
    "kind": "llm-judge",
    "judge": {
      "model_id": "claude-sonnet-4-5-20250929",
      "temperature": 0,
      "prompt_hash": "sha256:fc97a67bbfa1c1d346e731e6ef96eab3c1df8690b53a58d814792cf5bffe218c",
      "noise_floor": 0.01
    }
  },
  "baseline_run": {
    "url": "https://ci.example.com/evals/summariser/run/4410",
    "commit": "7c9e2f1a3b",
    "run_at": "2026-03-04"
  },
  "metrics": [
    {
      "name": "answer_accuracy",
      "baseline": 0.89,
      "tolerance": -0.02,
      "threshold": 0.87,
      "direction": "higher-is-better"
    },
    {
      "name": "hallucination_rate",
      "baseline": 0.03,
      "tolerance": 0.01,
      "threshold": 0.04,
      "direction": "lower-is-better"
    },
    {
      "name": "injection_resistance",
      "baseline": 1.0,
      "tolerance": 0.0,
      "threshold": 1.0,
      "direction": "higher-is-better"
    }
  ],
  "regression_gate": {
    "ci_job": "eval-summariser",
    "blocks_merge": True,
    "watched_paths": [
      "prompts/summariser/",
      "config/models.yaml",
      "config/retrieval.yaml",
      "tools/schemas/"
    ],
    "prompts_in_version_control": True,
    "prompt_hash_logged_at_startup": True
  },
  "production_model_id": "claude-sonnet-4-5-20250929",
  "budgets": {
    "p95_latency_ms": 2500,
    "per_request": {
      "tokens": 6000,
      "cost_usd": 0.02
    },
    "measured_in_eval_run": True
  },
  "untrusted_input_channels": [
    {
      "channel": "ticket body (retrieval)",
      "kind": "retrieval-source",
      "injection_case_ids": [
        "inj-ticket-001",
        "inj-ticket-002"
      ]
    },
    {
      "channel": "kb-search tool output",
      "kind": "tool-output",
      "injection_case_ids": [
        "inj-kb-001"
      ]
    },
    {
      "channel": "agent user turn",
      "kind": "user-turn",
      "injection_case_ids": [
        "inj-user-001"
      ]
    }
  ],
  "degradation": {
    "retry": {
      "max_attempts": 3,
      "backoff": "exponential-with-jitter",
      "base_delay_ms": 500,
      "triggers": [
        "timeout",
        "429",
        "5xx"
      ]
    },
    "fallback": {
      "kind": "secondary-pinned-model",
      "model_id": "claude-haiku-4-5-20251001",
      "eval_case_ids": [
        "deg-429-001",
        "deg-timeout-001"
      ]
    },
    "user_message": "Summary temporarily unavailable; showing the ticket as filed."
  },
  "evidence": [
    "https://ci.example.com/evals/summariser/run/4410",
    "https://ci.example.com/evals/summariser/run/4411",
    "https://github.com/acme/support/pull/2210"
  ]
}

BAD = {
  "feature_name": "support-ticket summariser",
  "owner": "swe:alice",
  "eval_set": {
    "path": "notebooks/eval-playground.ipynb",
    "ref": "a1b2c3d4e5f",
    "case_count": 40,
    "contamination_check_passed": True
  },
  "scoring": {
    "kind": "llm-judge",
    "judge": {
      "model_id": "claude-latest",
      "temperature": 0.7,
      "prompt_hash": "sha256:fc97a67bbfa1c1d346e731e6ef96eab3c1df8690b53a58d814792cf5bffe218c",
      "noise_floor": 0.06
    }
  },
  "baseline_run": {
    "url": "https://ci.example.com/evals/summariser/run/4410",
    "commit": "7c9e2f1a3b"
  },
  "metrics": [
    {
      "name": "answer_accuracy",
      "baseline": 0.89,
      "tolerance": -0.02,
      "threshold": 0.87,
      "direction": "higher-is-better"
    }
  ],
  "regression_gate": {
    "ci_job": "eval-summariser",
    "blocks_merge": False,
    "watched_paths": [
      "prompts/summariser/"
    ],
    "prompts_in_version_control": True
  },
  "production_model_id": "gpt-4o-latest",
  "budgets": {
    "p95_latency_ms": 2500,
    "per_request": {
      "tokens": 6000
    },
    "measured_in_eval_run": False
  },
  "untrusted_input_channels": [
    {
      "channel": "ticket body (retrieval)",
      "kind": "retrieval-source",
      "injection_case_ids": []
    }
  ],
  "degradation": {
    "retry": {
      "max_attempts": 100,
      "backoff": "fixed",
      "base_delay_ms": 100
    },
    "fallback": {
      "kind": "explicit-refusal",
      "eval_case_ids": []
    },
    "user_message": "Error"
  },
  "evidence": [
    "https://ci.example.com/evals/summariser/run/4410"
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
        prog="validate-ai-llm-workload-architecture.py",
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
