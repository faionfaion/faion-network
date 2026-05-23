#!/usr/bin/env python3
"""validate-java-junit-testing.py

Validate a Spring Boot test-class spec against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 valid · 1 invalid · 2 usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["test_class", "scope", "annotations", "uses_assertj"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Test$")
SCOPES = {"controller", "service", "repository", "integration"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "test_class" in obj and not NAME_RE.match(str(obj["test_class"])):
        errs.append("test_class must end with 'Test'")
    if obj.get("scope") not in SCOPES:
        errs.append(f"scope must be one of {sorted(SCOPES)}")
    ann = [str(a) for a in obj.get("annotations") or []]
    scope = obj.get("scope")
    if scope == "controller" and not any("@WebMvcTest" in a for a in ann):
        errs.append("controller scope requires @WebMvcTest")
    if scope == "service" and not any("MockitoExtension" in a for a in ann):
        errs.append("service scope requires @ExtendWith(MockitoExtension.class)")
    if scope == "repository" and not any("@DataJpaTest" in a for a in ann):
        errs.append("repository scope requires @DataJpaTest")
    if scope == "integration" and obj.get("uses_testcontainers") is not True:
        errs.append("integration scope requires uses_testcontainers=true")
    if obj.get("uses_assertj") is not True:
        errs.append("uses_assertj must be true")
    if obj.get("parametric_inputs_use_parameterized_test") is False:
        errs.append("parametric inputs must use @ParameterizedTest")
    if obj.get("uses_h2_for_relational") is True:
        errs.append("uses_h2_for_relational must be false (testcontainers-for-integration)")
    return errs


OK = {
    "test_class": "OrdersControllerTest",
    "scope": "controller",
    "annotations": ["@WebMvcTest(OrdersController.class)", "@AutoConfigureMockMvc"],
    "uses_assertj": True,
    "uses_mock_bean": True,
    "uses_testcontainers": False,
    "parametric_inputs_use_parameterized_test": True,
    "uses_h2_for_relational": False,
}
BAD = {
    "test_class": "OrdersTest",
    "scope": "controller",
    "annotations": ["@SpringBootTest"],
    "uses_assertj": False,
    "uses_mock_bean": False,
    "parametric_inputs_use_parameterized_test": False,
    "uses_h2_for_relational": True,
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
