#!/usr/bin/env python3
"""validate-claude-md-creation.py

Validate the artefact produced by the claude-md-creation methodology against the JSON
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
  "$id": "faion://claude-md-creation/output.schema.json",
  "title": "CLAUDE.md creation record",
  "type": "object",
  "required": [
    "repo",
    "layout",
    "template",
    "token_count",
    "commands",
    "secrets_scan",
    "structure",
    "key_files",
    "gotchas",
    "local_settings",
    "resync_check",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "path_with_purpose": {
      "type": "object",
      "required": [
        "path",
        "purpose"
      ],
      "additionalProperties": False,
      "properties": {
        "path": {
          "type": "string",
          "minLength": 1,
          "not": {
            "pattern": "(^|/)(node_modules|dist|build|\\.venv|__pycache__|\\.next|target)(/|$)"
          }
        },
        "purpose": {
          "type": "string",
          "minLength": 5
        },
        "exists": {
          "type": "boolean"
        }
      }
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "repo": {
      "type": "string",
      "pattern": "^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$"
    },
    "layout": {
      "type": "string",
      "enum": [
        "single",
        "monorepo"
      ]
    },
    "template": {
      "type": "string",
      "enum": [
        "minimal",
        "standard",
        "monorepo"
      ]
    },
    "token_count": {
      "type": "integer",
      "minimum": 1
    },
    "commands": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "command",
          "source",
          "comment",
          "ran_ok"
        ],
        "additionalProperties": False,
        "properties": {
          "command": {
            "type": "string",
            "minLength": 2
          },
          "source": {
            "type": "string",
            "enum": [
              "package.json",
              "Makefile",
              "pyproject.toml",
              "justfile",
              "other-manifest"
            ]
          },
          "comment": {
            "type": "string",
            "minLength": 3
          },
          "ran_ok": {
            "type": "boolean",
            "const": True
          }
        }
      }
    },
    "secrets_scan": {
      "type": "object",
      "required": [
        "tool",
        "clean",
        "env_vars_by_name_only",
        "env_example_referenced"
      ],
      "additionalProperties": False,
      "properties": {
        "tool": {
          "type": "string",
          "enum": [
            "gitleaks",
            "trufflehog",
            "host-builtin"
          ]
        },
        "clean": {
          "type": "boolean",
          "const": True
        },
        "env_vars_by_name_only": {
          "type": "boolean",
          "const": True
        },
        "env_example_referenced": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "structure": {
      "type": "array",
      "minItems": 1,
      "maxItems": 20,
      "items": {
        "$ref": "#/definitions/path_with_purpose"
      }
    },
    "key_files": {
      "type": "array",
      "items": {
        "allOf": [
          {
            "$ref": "#/definitions/path_with_purpose"
          },
          {
            "type": "object",
            "required": [
              "exists"
            ],
            "properties": {
              "exists": {
                "type": "boolean",
                "const": True
              }
            }
          }
        ]
      }
    },
    "gotchas": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "entry",
          "names"
        ],
        "additionalProperties": False,
        "properties": {
          "entry": {
            "type": "string",
            "minLength": 15,
            "not": {
              "pattern": "(?i)^(write clean code|add tests|follow best practices|be careful)"
            }
          },
          "names": {
            "type": "string",
            "enum": [
              "file",
              "env-var",
              "command",
              "version-pin",
              "lint-rule"
            ]
          }
        }
      }
    },
    "local_settings": {
      "type": "object",
      "required": [
        "personal_paths_grep_clean",
        "claude_local_md_gitignored"
      ],
      "additionalProperties": False,
      "properties": {
        "personal_paths_grep_clean": {
          "type": "boolean",
          "const": True
        },
        "claude_local_md_gitignored": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "resync_check": {
      "type": "object",
      "required": [
        "kind",
        "location",
        "fails_on_manifest_drift"
      ],
      "additionalProperties": False,
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "ci-job",
            "pre-commit-hook"
          ]
        },
        "location": {
          "type": "string",
          "minLength": 3
        },
        "fails_on_manifest_drift": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "monorepo": {
      "type": "object",
      "required": [
        "per_app_files",
        "root_restates_app_commands"
      ],
      "additionalProperties": False,
      "properties": {
        "per_app_files": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "app",
              "path",
              "exists",
              "referenced_by"
            ],
            "additionalProperties": False,
            "properties": {
              "app": {
                "type": "string",
                "minLength": 1
              },
              "path": {
                "type": "string",
                "pattern": "CLAUDE\\.md$"
              },
              "exists": {
                "type": "boolean",
                "const": True
              },
              "referenced_by": {
                "type": "string",
                "enum": [
                  "import",
                  "relative-path"
                ]
              }
            }
          }
        },
        "root_restates_app_commands": {
          "type": "boolean",
          "const": False
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
  "allOf": [
    {
      "if": {
        "properties": {
          "template": {
            "const": "minimal"
          }
        }
      },
      "then": {
        "properties": {
          "token_count": {
            "maximum": 250
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "template": {
            "const": "standard"
          }
        }
      },
      "then": {
        "properties": {
          "token_count": {
            "maximum": 500
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "template": {
            "const": "monorepo"
          }
        }
      },
      "then": {
        "properties": {
          "token_count": {
            "maximum": 700
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "layout": {
            "const": "monorepo"
          }
        }
      },
      "then": {
        "required": [
          "monorepo"
        ],
        "properties": {
          "template": {
            "const": "monorepo"
          }
        }
      }
    }
  ]
}

OK = {
  "repo": "acme/intake-api",
  "layout": "single",
  "template": "standard",
  "token_count": 480,
  "commands": [
    {
      "command": "make dev",
      "source": "Makefile",
      "comment": "Start development server (port 8000)",
      "ran_ok": True
    },
    {
      "command": "pytest --cov=src -x",
      "source": "pyproject.toml",
      "comment": "Run tests, stop at first failure",
      "ran_ok": True
    },
    {
      "command": "ruff check . --fix",
      "source": "pyproject.toml",
      "comment": "Lint + auto-fix (rules: E/F/I/B/T20/DJ)",
      "ran_ok": True
    },
    {
      "command": "mypy src",
      "source": "pyproject.toml",
      "comment": "Type check",
      "ran_ok": True
    },
    {
      "command": "alembic upgrade head",
      "source": "Makefile",
      "comment": "Apply migrations",
      "ran_ok": True
    }
  ],
  "secrets_scan": {
    "tool": "gitleaks",
    "clean": True,
    "env_vars_by_name_only": True,
    "env_example_referenced": True
  },
  "structure": [
    {
      "path": "src/api/",
      "purpose": "FastAPI routes, v1/ per API version"
    },
    {
      "path": "src/core/",
      "purpose": "Business logic, config, security helpers"
    },
    {
      "path": "src/models/",
      "purpose": "SQLAlchemy models"
    },
    {
      "path": "src/schemas/",
      "purpose": "Pydantic schemas"
    },
    {
      "path": "tests/",
      "purpose": "unit/ mirrors src/, integration/ hits endpoints"
    }
  ],
  "key_files": [
    {
      "path": "src/core/config.py",
      "purpose": "Settings read from env; nothing else reads env directly",
      "exists": True
    },
    {
      "path": "src/api/deps.py",
      "purpose": "FastAPI dependencies (auth, db session)",
      "exists": True
    },
    {
      "path": ".env.example",
      "purpose": "Required env vars; copy to .env before running",
      "exists": True
    }
  ],
  "gotchas": [
    {
      "entry": "DATABASE_URL has no default; the app exits at startup without it",
      "names": "env-var"
    },
    {
      "entry": "No print() in production code; ruff T20 blocks the commit",
      "names": "lint-rule"
    },
    {
      "entry": "Run alembic upgrade head before first start or the health check returns 503",
      "names": "command"
    }
  ],
  "local_settings": {
    "personal_paths_grep_clean": True,
    "claude_local_md_gitignored": True
  },
  "resync_check": {
    "kind": "ci-job",
    "location": ".github/workflows/claude-md-sync.yml",
    "fails_on_manifest_drift": True
  },
  "evidence": [
    "https://ci.example.com/acme/intake-api/runs/8812",
    "https://ci.example.com/acme/intake-api/runs/8812/gitleaks",
    "https://github.com/acme/intake-api/blob/main/.github/workflows/claude-md-sync.yml"
  ]
}

BAD = {
  "repo": "acme/intake-api",
  "layout": "single",
  "template": "standard",
  "token_count": 3100,
  "commands": [
    {
      "command": "npm run test:unit",
      "source": "package.json",
      "comment": "Tests",
      "ran_ok": False
    }
  ],
  "secrets_scan": {
    "tool": "gitleaks",
    "clean": False,
    "env_vars_by_name_only": False,
    "env_example_referenced": False
  },
  "structure": [
    {
      "path": "node_modules/",
      "purpose": "dependencies"
    },
    {
      "path": "src/",
      "purpose": "code"
    },
    {
      "path": "dist/",
      "purpose": "build output"
    }
  ],
  "key_files": [
    {
      "path": "src/settings.py",
      "purpose": "Settings",
      "exists": False
    }
  ],
  "gotchas": [
    {
      "entry": "Write clean code and add tests",
      "names": "file"
    }
  ],
  "local_settings": {
    "personal_paths_grep_clean": False,
    "claude_local_md_gitignored": False
  },
  "resync_check": {
    "kind": "ci-job",
    "location": ".github/workflows/claude-md-sync.yml",
    "fails_on_manifest_drift": False
  },
  "evidence": [
    "https://ci.example.com/acme/intake-api/runs/8812"
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
        prog="validate-claude-md-creation.py",
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
