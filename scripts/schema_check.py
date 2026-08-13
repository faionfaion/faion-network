#!/usr/bin/env python3
"""A dependency-free JSON Schema checker for the subset docs/schemas/ uses.

The corpus validators are stdlib-only by house style and run on machines
that have no `pip install` step, so importing `jsonschema` would make a
validator that silently does not run — the worst kind. This module
implements exactly the keywords the schemas under `docs/schemas/` are
written with, and refuses any schema that uses one it does not know, so
a schema can never quietly stop being enforced:

    $ref (local #/$defs/... only) · $defs · type · const · enum
    required · properties · additionalProperties · propertyNames
    pattern · minLength · minimum · maximum
    items · prefixItems · minItems · maxItems

Cross-checked against the `jsonschema` package during development on
every meta.json and recipe.json in the tree; both agree, including on
the deliberate failures used to demonstrate red before green.

Usage:
    from schema_check import load, check
    schema = load(Path("docs/schemas/recipe.schema.json"))
    for problem in check(instance, schema):
        print(problem)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

# Annotation keywords carry no constraint; anything else unknown is a
# schema this checker must not pretend to enforce.
IGNORED = {"$schema", "$id", "title", "description", "default", "examples"}
KNOWN = {
    "$ref", "$defs", "type", "const", "enum", "required", "properties",
    "additionalProperties", "propertyNames", "pattern", "minLength",
    "minimum", "maximum", "items", "prefixItems", "minItems", "maxItems",
}

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


class SchemaError(Exception):
    """The schema itself is wrong — a keyword this checker cannot enforce."""


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _at(where: str, key) -> str:
    return f"{where}/{key}" if where else str(key)


def _resolve(ref: str, root: dict) -> dict:
    if not ref.startswith("#/"):
        raise SchemaError(f"only local $ref is supported, got {ref!r}")
    node = root
    for part in ref[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            raise SchemaError(f"$ref {ref!r} does not resolve")
        node = node[part]
    return node


def _is_type(value, name: str) -> bool:
    expected = TYPES.get(name)
    if expected is None:
        raise SchemaError(f"unknown type {name!r}")
    if name in ("integer", "number") and isinstance(value, bool):
        return False
    if name == "integer":
        return isinstance(value, int)
    return isinstance(value, expected)


def check(instance, schema: dict, root: dict | None = None,
          where: str = "") -> list[str]:
    """Every way `instance` violates `schema`, as human-readable strings."""
    root = schema if root is None else root
    problems: list[str] = []

    unknown = set(schema) - KNOWN - IGNORED
    if unknown:
        raise SchemaError(f"unsupported keyword(s) at {where or '<root>'}: "
                          f"{', '.join(sorted(unknown))}")

    if "$ref" in schema:
        return check(instance, _resolve(schema["$ref"], root), root, where)

    def bad(msg: str) -> None:
        problems.append(f"{where or '<root>'}: {msg}")

    if "type" in schema and not _is_type(instance, schema["type"]):
        bad(f"expected {schema['type']}, got {type(instance).__name__}")
        return problems

    if "const" in schema and instance != schema["const"]:
        bad(f"must be {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        bad(f"{instance!r} is not one of {schema['enum']}")

    if isinstance(instance, str):
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            bad(f"{instance!r} does not match {schema['pattern']}")
        if "minLength" in schema and len(instance) < schema["minLength"]:
            bad(f"is {len(instance)} chars, minimum is {schema['minLength']}")

    if isinstance(instance, int) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            bad(f"{instance} is below minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            bad(f"{instance} is above maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                bad(f"missing required key {key!r}")
        properties = schema.get("properties", {})
        names = schema.get("propertyNames")
        extra = schema.get("additionalProperties")
        for key, value in instance.items():
            if names is not None:
                problems += check(key, names, root, _at(where, f"{key} (name)"))
            if key in properties:
                problems += check(value, properties[key], root, _at(where, key))
            elif extra is False:
                bad(f"unexpected key {key!r}")
            elif isinstance(extra, dict):
                problems += check(value, extra, root, _at(where, key))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            bad(f"has {len(instance)} item(s), minimum is {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            bad(f"has {len(instance)} item(s), maximum is {schema['maxItems']}")
        prefix = schema.get("prefixItems", [])
        for i, value in enumerate(instance):
            if i < len(prefix):
                problems += check(value, prefix[i], root, _at(where, i))
                continue
            rest = schema.get("items")
            if rest is False:
                bad(f"item {i} ({value!r}) is beyond the allowed sequence")
            elif isinstance(rest, dict):
                problems += check(value, rest, root, _at(where, i))

    return problems
