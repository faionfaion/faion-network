#!/usr/bin/env python3
"""Validate an MCP server manifest against the F-066 output contract.

Usage:
  validate-model-context-protocol.py <manifest.json>           Validate one manifest file.
  validate-model-context-protocol.py --self-test               Run against built-in fixtures.
  validate-model-context-protocol.py --help                    Show this help.

Exit codes:
  0 — manifest valid against contract.
  1 — manifest violates one or more contract rules (each printed to stderr).
  2 — usage error or unreadable input.

Inputs:  one JSON file matching `02-output-contract.xml` schema.
Outputs: violation list on stderr (one per line), exit code per above.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9_.]{1,63}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def violations(manifest: dict) -> list[str]:
    errs: list[str] = []
    for key in ("server_name", "server_version", "transport", "tools", "registration"):
        if key not in manifest:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    if not NAME_RE.match(manifest["server_name"]):
        errs.append(f"server_name invalid: {manifest['server_name']!r}")
    if not SEMVER_RE.match(manifest["server_version"]):
        errs.append(f"server_version not semver: {manifest['server_version']!r}")
    if manifest["transport"] not in ("stdio", "streamable-http"):
        errs.append(f"transport must be 'stdio' or 'streamable-http', got {manifest['transport']!r}")

    tools = manifest["tools"]
    if not isinstance(tools, list) or not tools:
        errs.append("tools must be a non-empty list")
        return errs

    names = [t.get("name", "") for t in tools]
    has_health = any(n in ("ping", "health") for n in names)
    if not has_health:
        errs.append("at least one tool must be named 'ping' or 'health' (r1-health-probe)")

    if len(set(names)) != len(names):
        errs.append("tool names must be unique within a server (r2-unique-names)")

    for tool in tools:
        n = tool.get("name", "")
        if not TOOL_NAME_RE.match(n):
            errs.append(f"tool name invalid: {n!r}")
        desc = tool.get("description", "")
        if len(desc) < 16:
            errs.append(f"tool {n!r} description must be >=16 chars (got {len(desc)})")
        schema = tool.get("inputSchema") or {}
        flat = json.dumps(schema)
        for forbidden in ("oneOf", "anyOf", "$ref"):
            if forbidden in flat:
                errs.append(f"tool {n!r} inputSchema uses {forbidden} — schemas must be flat (r3-flat-schema)")

    auth_mode = (manifest.get("auth") or {}).get("mode", "none")
    if manifest["transport"] == "streamable-http" and auth_mode == "none":
        errs.append("streamable-http transport requires auth.mode != 'none' (r5-remote-oauth)")

    reg = manifest.get("registration") or {}
    if "claude_code_settings" not in reg:
        errs.append("registration.claude_code_settings is required (paste-ready block)")

    return errs


_FIXTURE_GOOD = {
    "server_name": "faion-weather",
    "server_version": "1.2.0",
    "transport": "stdio",
    "auth": {"mode": "none"},
    "tools": [
        {"name": "ping", "description": "Health probe; returns server status and version", "inputSchema": {"type": "object", "properties": {}}},
        {"name": "weather.get_current", "description": "Get current weather for a city by name",
         "inputSchema": {"type": "object", "required": ["city"], "properties": {"city": {"type": "string"}}}},
    ],
    "registration": {"claude_code_settings": {"mcpServers": {"faion-weather": {"command": "python", "args": ["/srv/server.py"]}}}},
}

_FIXTURE_BAD = {
    "server_name": "WeatherV2",
    "server_version": "v1",
    "transport": "sse",
    "auth": {"mode": "none"},
    "tools": [{"name": "do", "description": "do stuff", "inputSchema": {"oneOf": [{"type": "string"}]}}],
}


def self_test() -> int:
    good_errs = violations(_FIXTURE_GOOD)
    bad_errs = violations(_FIXTURE_BAD)
    failed = False
    if good_errs:
        sys.stderr.write(f"self-test: good fixture should be clean, got: {good_errs}\n")
        failed = True
    if not bad_errs:
        sys.stderr.write("self-test: bad fixture should fail, got no errors\n")
        failed = True
    if failed:
        return 1
    sys.stdout.write(f"self-test ok (bad fixture surfaced {len(bad_errs)} violations)\n")
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv or not argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return self_test()
    target = Path(argv[0])
    try:
        manifest = json.loads(target.read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"cannot read manifest {target}: {e}\n")
        return 2
    errs = violations(manifest)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write(f"{target}: ok\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
