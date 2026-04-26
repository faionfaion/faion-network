#!/usr/bin/env python3
"""Validate YAML frontmatter in SDD documents.

Usage: python validate-frontmatter.py path/to/doc.md [path/to/doc2.md ...]
Exit 1 if any document has validation errors.
"""
import sys
import frontmatter

REQUIRED_BASE = {"type", "version", "status", "created"}

REQUIRED_BY_TYPE = {
    "spec": {"feature_id", "priority"},
    "design": {"feature_id", "spec_version"},
    "implementation-plan": {"feature_id", "design_version", "total_tasks"},
    "task": {"task_id", "feature_id", "complexity", "estimated_tokens"},
}

VALID_STATUS = {"draft", "review", "approved", "active", "superseded", "archived"}
VALID_PRIORITY = {"P0", "P1", "P2"}
VALID_COMPLEXITY = {"low", "medium", "high"}


def validate(path: str) -> list[str]:
    post = frontmatter.load(path)
    meta = post.metadata
    errors = []

    for field in REQUIRED_BASE:
        if field not in meta:
            errors.append(f"MISSING required field: {field}")

    doc_type = meta.get("type", "")
    for field in REQUIRED_BY_TYPE.get(doc_type, set()):
        if field not in meta:
            errors.append(f"MISSING required field for type={doc_type}: {field}")

    if "status" in meta and meta["status"] not in VALID_STATUS:
        errors.append(f"INVALID status '{meta['status']}', must be one of {VALID_STATUS}")
    if "priority" in meta and meta["priority"] not in VALID_PRIORITY:
        errors.append(f"INVALID priority '{meta['priority']}', must be one of {VALID_PRIORITY}")
    if "complexity" in meta and meta["complexity"] not in VALID_COMPLEXITY:
        errors.append(f"INVALID complexity '{meta['complexity']}', must be one of {VALID_COMPLEXITY}")
    if "version" in meta and not isinstance(meta["version"], str):
        errors.append("version must be a quoted string, e.g. \"1.0.0\" (bare 1.0.0 parses as float)")

    return errors


if __name__ == "__main__":
    failed = False
    for path in sys.argv[1:]:
        errs = validate(path)
        if errs:
            print(f"{path}:")
            for e in errs:
                print(f"  - {e}")
            failed = True
    if not failed:
        print("OK")
    sys.exit(1 if failed else 0)
