#!/usr/bin/env python3
"""validate-ai-elicitation-prompt-patterns.py

Validate a prompt-pattern artefact (YAML or JSON) against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to pattern file (YAML or JSON)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PHASES = {"interview-prep", "follow-up", "paraphrase-back", "persona-probe"}
SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
PATTERN_ID = re.compile(r"^[a-z][a-z0-9-]+$")


def _parse_yaml_or_json(text: str) -> object:
    text = text.strip()
    if text.startswith("{"):
        return json.loads(text)
    # tiny YAML loader (key: value, lists, scalars) — stdlib only
    return _yaml_minimal(text)


def _yaml_minimal(text: str) -> dict:
    """Tiny YAML parser sufficient for our skeleton shape."""
    root: dict = {}
    stack: list = [(0, root)]
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        while stack and indent < stack[-1][0]:
            stack.pop()
        body = line.lstrip(" ")
        parent = stack[-1][1]
        if body.startswith("- "):
            value = body[2:].strip()
            if isinstance(parent, list):
                container = parent
            else:
                # caller should have allocated a list — synthesize
                container = parent.setdefault("_implicit_list", [])
            if value.startswith("{") and value.endswith("}"):
                # inline mapping
                item: dict = {}
                inner = value[1:-1].strip()
                for kv in inner.split(","):
                    if ":" in kv:
                        k, v = kv.split(":", 1)
                        item[k.strip()] = _scalar(v.strip())
                container.append(item)
            else:
                container.append(_scalar(value))
            continue
        if ":" in body:
            key, _, val = body.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                # nested mapping or list
                new_obj: dict | list = {}
                # peek next line to decide
                # We default to dict; if subsequent lines start with "- " we will retrofit
                parent[key] = new_obj
                stack.append((indent + 2, new_obj))
            elif val == "|":
                # block scalar — read remaining lines at deeper indent
                parent[key] = ""  # filled below via continuation
                stack.append((indent + 2, {"__block_target__": (parent, key)}))
            else:
                if isinstance(parent, dict) and "__block_target__" in parent:
                    tgt_parent, tgt_key = parent["__block_target__"]
                    tgt_parent[tgt_key] += body + "\n"
                else:
                    parent[key] = _scalar(val)
    # post-pass: convert _implicit_list to actual lists where parent had no values
    def fixup(node):
        if isinstance(node, dict):
            for k, v in list(node.items()):
                if isinstance(v, dict) and set(v.keys()) == {"_implicit_list"}:
                    node[k] = v["_implicit_list"]
                else:
                    fixup(v)
        elif isinstance(node, list):
            for v in node:
                fixup(v)

    fixup(root)
    return root


def _scalar(v: str):
    if v in ("true", "True"):
        return True
    if v in ("false", "False"):
        return False
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v.strip('"').strip("'")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be mapping"]
    for k in ("pattern_id", "phase", "slots", "skeleton", "output_schema_ref",
             "eval_reference", "budget", "version_tag"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    pid = obj.get("pattern_id", "")
    if isinstance(pid, str) and not PATTERN_ID.match(pid):
        errs.append("pattern_id must be kebab-case [a-z0-9-]+")
    if obj.get("phase") not in PHASES:
        errs.append(f"phase must be one of {sorted(PHASES)}")
    slots = obj.get("slots", [])
    if not isinstance(slots, list) or len(slots) < 1:
        errs.append("slots must be non-empty list")
    sk = obj.get("skeleton", "")
    if not isinstance(sk, str) or len(sk) < 32:
        errs.append("skeleton must be string with length >= 32 (rule r2)")
    if not obj.get("output_schema_ref"):
        errs.append("output_schema_ref required (rule r4)")
    if not obj.get("eval_reference"):
        errs.append("eval_reference required (rule r2)")
    budget = obj.get("budget", {})
    if not isinstance(budget, dict) or "tokens_in" not in budget or "tokens_out" not in budget:
        errs.append("budget.tokens_in and budget.tokens_out required (rule r3)")
    vt = obj.get("version_tag", "")
    if not isinstance(vt, str) or not SEMVER.match(vt):
        errs.append("version_tag must match ^v\\d+\\.\\d+\\.\\d+$ (rule r1)")
    return errs


OK_FIXTURE = {
    "pattern_id": "interview-prep-v1",
    "phase": "interview-prep",
    "slots": [{"name": "stakeholder_role", "type": "string", "required": True}],
    "skeleton": "Prepare 5 open questions for {{stakeholder_role}} grounded in the brief paragraphs.",
    "output_schema_ref": "templates/output-schema.json#/interview_questions",
    "eval_reference": "evals/interview-prep.jsonl",
    "budget": {"tokens_in": 800, "tokens_out": 400},
    "version_tag": "v1.0.0",
}
BAD_FIXTURE = {"pattern_id": "InterviewPrep", "skeleton": "Draft some Qs", "version_tag": "latest"}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = _parse_yaml_or_json(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
