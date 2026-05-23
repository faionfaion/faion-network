#!/usr/bin/env python3
"""validate-java-junit-testing.py

Validate the test-plan manifest for the java-junit-testing methodology against
the JSON Schema declared in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = [
    "module",
    "framework",
    "test_classes",
    "coverage",
    "uses_testcontainers",
    "springboottest_count",
]
ALLOWED_LAYERS = {"controller", "service", "repository", "integration"}
ALLOWED_SLICES = {
    "@WebMvcTest",
    "@ExtendWith(MockitoExtension.class)",
    "@DataJpaTest",
    "@SpringBootTest",
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("framework") != "junit5":
        errs.append("framework must be 'junit5'")
    classes = obj.get("test_classes") or []
    if not isinstance(classes, list) or len(classes) < 1:
        errs.append("test_classes must be non-empty list")
    for i, c in enumerate(classes):
        if not str(c.get("name", "")).endswith("Test"):
            errs.append(f"test_classes[{i}].name must end with 'Test'")
        if c.get("layer") not in ALLOWED_LAYERS:
            errs.append(f"test_classes[{i}].layer must be one of {sorted(ALLOWED_LAYERS)}")
        if c.get("slice_annotation") not in ALLOWED_SLICES:
            errs.append(f"test_classes[{i}].slice_annotation must be one of {sorted(ALLOWED_SLICES)}")
        if not isinstance(c.get("test_count"), int) or c.get("test_count", 0) < 1:
            errs.append(f"test_classes[{i}].test_count must be positive integer")
    cov = obj.get("coverage") or {}
    if not isinstance(cov.get("line"), (int, float)) or cov.get("line", 0) < 70:
        errs.append("coverage.line must be >= 70")
    if not isinstance(cov.get("branch"), (int, float)) or cov.get("branch", 0) < 60:
        errs.append("coverage.branch must be >= 60")
    if cov.get("tool") != "jacoco":
        errs.append("coverage.tool must be 'jacoco'")
    if cov.get("gate_enforced_in_ci") is not True:
        errs.append("coverage.gate_enforced_in_ci must be true")
    if obj.get("uses_testcontainers") is not True:
        errs.append("uses_testcontainers must be true")
    if not isinstance(obj.get("springboottest_count"), int) or obj.get("springboottest_count", 0) > 1:
        errs.append("springboottest_count must be <= 1")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "module": "billing",
    "framework": "junit5",
    "test_classes": [
        {"name": "UserControllerTest", "layer": "controller", "slice_annotation": "@WebMvcTest", "test_count": 8},
        {"name": "UserServiceTest", "layer": "service", "slice_annotation": "@ExtendWith(MockitoExtension.class)", "test_count": 14},
        {"name": "UserRepositoryTest", "layer": "repository", "slice_annotation": "@DataJpaTest", "test_count": 6},
    ],
    "coverage": {"line": 78.4, "branch": 64.2, "tool": "jacoco", "gate_enforced_in_ci": True},
    "uses_testcontainers": True,
    "springboottest_count": 1,
    "forbidden_patterns_found": [],
}
BAD = {
    "module": "billing",
    "framework": "junit4",
    "test_classes": [{"name": "user_controller", "layer": "controller", "slice_annotation": "@SpringBootTest", "test_count": 0}],
    "coverage": {"line": 35.0, "branch": 12.0, "tool": "cobertura", "gate_enforced_in_ci": False},
    "uses_testcontainers": False,
    "springboottest_count": 5,
    "forbidden_patterns_found": ["Thread.sleep"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
