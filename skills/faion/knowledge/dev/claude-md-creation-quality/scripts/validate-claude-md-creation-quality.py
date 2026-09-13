#!/usr/bin/env python3
"""validate-claude-md-creation-quality.py

Validate the artefact produced by the claude-md-creation-quality methodology against the JSON
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
  "$id": "faion://claude-md-creation-quality/output.schema.json",
  "title": "CLAUDE.md quality record",
  "type": "object",
  "required": [
    "repo",
    "layout",
    "root_file",
    "secrets",
    "commands",
    "imports",
    "local_scope",
    "prohibitions",
    "emphasis_ratio",
    "refs_check",
    "reviewer",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "handle": {
      "type": "string",
      "pattern": "^[a-z-]+:[a-z0-9._-]+$"
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
        "single-package",
        "multi-package"
      ]
    },
    "root_file": {
      "type": "object",
      "required": [
        "line_budget",
        "budget_declared_in_first_comment",
        "line_count",
        "within_budget",
        "ci_line_check"
      ],
      "additionalProperties": False,
      "properties": {
        "line_budget": {
          "type": "integer",
          "minimum": 10,
          "maximum": 300
        },
        "budget_declared_in_first_comment": {
          "type": "boolean",
          "const": True
        },
        "line_count": {
          "type": "integer",
          "minimum": 1
        },
        "within_budget": {
          "type": "boolean",
          "const": True
        },
        "ci_line_check": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "secrets": {
      "type": "object",
      "required": [
        "scanner",
        "runs_in_ci",
        "runs_in_pre_commit",
        "clean",
        "referenced_by_name_only"
      ],
      "additionalProperties": False,
      "properties": {
        "scanner": {
          "type": "string",
          "enum": [
            "gitleaks",
            "trufflehog"
          ]
        },
        "runs_in_ci": {
          "type": "boolean",
          "const": True
        },
        "runs_in_pre_commit": {
          "type": "boolean",
          "const": True
        },
        "clean": {
          "type": "boolean",
          "const": True
        },
        "referenced_by_name_only": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "commands": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "invocation",
          "verbatim",
          "exit_code"
        ],
        "additionalProperties": False,
        "properties": {
          "invocation": {
            "type": "string",
            "minLength": 2,
            "not": {
              "pattern": "(?i)^(run|execute|start) the "
            }
          },
          "verbatim": {
            "type": "boolean",
            "const": True
          },
          "exit_code": {
            "type": "integer",
            "const": 0
          }
        }
      }
    },
    "imports": {
      "type": "object",
      "required": [
        "pasted_repo_content",
        "entries"
      ],
      "additionalProperties": False,
      "properties": {
        "pasted_repo_content": {
          "type": "boolean",
          "const": False
        },
        "entries": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "path",
              "exists",
              "hop_depth"
            ],
            "additionalProperties": False,
            "properties": {
              "path": {
                "type": "string",
                "minLength": 1
              },
              "exists": {
                "type": "boolean",
                "const": True
              },
              "hop_depth": {
                "type": "integer",
                "minimum": 1,
                "maximum": 5
              }
            }
          }
        }
      }
    },
    "local_scope": {
      "type": "object",
      "required": [
        "personal_content_in_committed_file",
        "claude_local_md_gitignored"
      ],
      "additionalProperties": False,
      "properties": {
        "personal_content_in_committed_file": {
          "type": "boolean",
          "const": False
        },
        "claude_local_md_gitignored": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "subdir_files": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "package",
          "path",
          "exists"
        ],
        "additionalProperties": False,
        "properties": {
          "package": {
            "type": "string",
            "minLength": 1
          },
          "path": {
            "type": "string",
            "pattern": "/CLAUDE\\.md$"
          },
          "exists": {
            "type": "boolean",
            "const": True
          }
        }
      }
    },
    "root_has_per_package_commands": {
      "type": "boolean",
      "const": False
    },
    "prohibitions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "line",
          "consequence_stated",
          "emphasised"
        ],
        "additionalProperties": False,
        "properties": {
          "line": {
            "type": "string",
            "minLength": 10,
            "pattern": "(?i)(never|do not|don't|must not)"
          },
          "consequence_stated": {
            "type": "boolean",
            "const": True
          },
          "emphasised": {
            "type": "boolean"
          }
        }
      }
    },
    "emphasis_ratio": {
      "type": "number",
      "minimum": 0,
      "maximum": 0.25
    },
    "refs_check": {
      "type": "object",
      "required": [
        "kind",
        "location",
        "all_refs_exist"
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
        "all_refs_exist": {
          "type": "boolean",
          "const": True
        }
      }
    },
    "reviewer": {
      "$ref": "#/definitions/handle"
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
      "layout": {
        "const": "multi-package"
      }
    }
  },
  "then": {
    "required": [
      "subdir_files",
      "root_has_per_package_commands"
    ]
  }
}

OK = {
  "repo": "acme/platform",
  "layout": "multi-package",
  "root_file": {
    "line_budget": 100,
    "budget_declared_in_first_comment": True,
    "line_count": 84,
    "within_budget": True,
    "ci_line_check": True
  },
  "secrets": {
    "scanner": "gitleaks",
    "runs_in_ci": True,
    "runs_in_pre_commit": True,
    "clean": True,
    "referenced_by_name_only": True
  },
  "commands": [
    {
      "invocation": "pnpm install --frozen-lockfile",
      "verbatim": True,
      "exit_code": 0
    },
    {
      "invocation": "pnpm turbo run test --filter=...[origin/main]",
      "verbatim": True,
      "exit_code": 0
    },
    {
      "invocation": "pnpm turbo run lint",
      "verbatim": True,
      "exit_code": 0
    }
  ],
  "imports": {
    "pasted_repo_content": False,
    "entries": [
      {
        "path": "CONTRIBUTING.md",
        "exists": True,
        "hop_depth": 1
      },
      {
        "path": "docs/adr/README.md",
        "exists": True,
        "hop_depth": 2
      }
    ]
  },
  "local_scope": {
    "personal_content_in_committed_file": False,
    "claude_local_md_gitignored": True
  },
  "subdir_files": [
    {
      "package": "api",
      "path": "apps/api/CLAUDE.md",
      "exists": True
    },
    {
      "package": "web",
      "path": "apps/web/CLAUDE.md",
      "exists": True
    },
    {
      "package": "infra",
      "path": "infra/CLAUDE.md",
      "exists": True
    }
  ],
  "root_has_per_package_commands": False,
  "prohibitions": [
    {
      "line": "never edit /srv/app directly: it is the deploy target, the repo is the source",
      "consequence_stated": True,
      "emphasised": True
    },
    {
      "line": "do not run pnpm install without --frozen-lockfile: the lockfile drifts and CI fails on the next push",
      "consequence_stated": True,
      "emphasised": False
    },
    {
      "line": "never commit CLAUDE.local.md: it carries machine paths that break every other clone",
      "consequence_stated": True,
      "emphasised": False
    }
  ],
  "emphasis_ratio": 0.04,
  "refs_check": {
    "kind": "ci-job",
    "location": ".github/workflows/claude-md-refs.yml",
    "all_refs_exist": True
  },
  "reviewer": "tl:mreyes",
  "evidence": [
    "https://ci.example.com/acme/platform/runs/5120",
    "https://github.com/acme/platform/pull/1187"
  ]
}

BAD = {
  "repo": "acme/platform",
  "layout": "multi-package",
  "root_file": {
    "line_budget": 100,
    "budget_declared_in_first_comment": False,
    "line_count": 480,
    "within_budget": False,
    "ci_line_check": False
  },
  "secrets": {
    "scanner": "gitleaks",
    "runs_in_ci": True,
    "runs_in_pre_commit": False,
    "clean": False,
    "referenced_by_name_only": False
  },
  "commands": [
    {
      "invocation": "run the tests",
      "verbatim": False,
      "exit_code": 1
    }
  ],
  "imports": {
    "pasted_repo_content": True,
    "entries": [
      {
        "path": "docs/deep/chain/six/hops/README.md",
        "exists": True,
        "hop_depth": 6
      }
    ]
  },
  "local_scope": {
    "personal_content_in_committed_file": True,
    "claude_local_md_gitignored": False
  },
  "root_has_per_package_commands": True,
  "prohibitions": [
    {
      "line": "IMPORTANT: never touch the config",
      "consequence_stated": False,
      "emphasised": True
    }
  ],
  "emphasis_ratio": 0.6,
  "refs_check": {
    "kind": "ci-job",
    "location": ".github/workflows/claude-md-refs.yml",
    "all_refs_exist": False
  },
  "reviewer": "team:platform",
  "evidence": [
    "https://ci.example.com/acme/platform/runs/5119"
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
        prog="validate-claude-md-creation-quality.py",
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
