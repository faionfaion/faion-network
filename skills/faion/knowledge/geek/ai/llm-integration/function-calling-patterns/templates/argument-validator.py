"""
purpose: Pre-execution argument validator for tool calls (cross-vendor).
consumes: tool name + LLM-supplied args + registry
produces: ValidationResult (ok | errors)
depends-on: content/01-core-rules.xml r2
token-budget-impact: zero — runtime boundary
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    import jsonschema
except ImportError:
    jsonschema = None


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]


def validate_args(tool_entry: dict, args: dict) -> ValidationResult:
    if jsonschema is None:
        raise SystemExit("jsonschema required: pip install jsonschema")
    schema = tool_entry.get("input_schema") or {}
    errors: list[str] = []
    try:
        jsonschema.validate(instance=args, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{'.'.join(map(str, e.absolute_path))}: {e.message}")
    return ValidationResult(ok=not errors, errors=errors)


def to_tool_result(tool_call_id: str, result: ValidationResult) -> dict:
    if result.ok:
        return {"type": "tool_result", "tool_use_id": tool_call_id, "content": "OK"}
    return {"type": "tool_result", "tool_use_id": tool_call_id, "content": f"ValidationError: {'; '.join(result.errors)}", "is_error": True}
