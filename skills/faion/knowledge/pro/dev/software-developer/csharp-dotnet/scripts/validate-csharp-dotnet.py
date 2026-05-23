#!/usr/bin/env python3
"""validate-csharp-dotnet.py

Validate a feature-folder spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["feature", "controller", "service", "dto", "entity_config", "test"]
FEATURE_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
CTRL_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Controller$")
SVC_IFACE_RE = re.compile(r"^I[A-Z][A-Za-z0-9]+Service$")
SVC_IMPL_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Service$")
DTO_RE = re.compile(r"^[A-Z][A-Za-z0-9]+(Request|Response|Dto)$")
CONF_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Configuration$")
TEST_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Tests$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "feature" in obj and not FEATURE_RE.match(str(obj["feature"])):
        errs.append("feature must be PascalCase")
    ctrl = obj.get("controller") or {}
    if not CTRL_RE.match(str(ctrl.get("class_name", ""))):
        errs.append("controller.class_name must match *Controller PascalCase")
    if "ApiController" not in (ctrl.get("attributes") or []):
        errs.append("controller missing [ApiController] attribute")
    if ctrl.get("base_class") and ctrl["base_class"] != "ControllerBase":
        errs.append("controller.base_class must be ControllerBase")
    svc = obj.get("service") or {}
    if not SVC_IFACE_RE.match(str(svc.get("interface", ""))):
        errs.append("service.interface must match I*Service PascalCase")
    if not SVC_IMPL_RE.match(str(svc.get("implementation", ""))):
        errs.append("service.implementation must match *Service PascalCase")
    if svc.get("lifetime") not in ("scoped", "transient"):
        errs.append("service.lifetime must be scoped or transient (not singleton)")
    if "dto" in obj and not DTO_RE.match(str(obj["dto"])):
        errs.append("dto must end with Request/Response/Dto")
    if "entity_config" in obj and not CONF_RE.match(str(obj["entity_config"])):
        errs.append("entity_config must end with Configuration")
    if "test" in obj and not TEST_RE.match(str(obj["test"])):
        errs.append("test class must end with Tests")
    if obj.get("nullable_enabled") is False:
        errs.append("nullable_enabled must be true")
    return errs


OK = {
    "feature": "Orders",
    "controller": {"class_name": "OrdersController", "attributes": ["ApiController"], "base_class": "ControllerBase"},
    "service": {"interface": "IOrdersService", "implementation": "OrdersService", "lifetime": "scoped"},
    "dto": "CreateOrderRequest",
    "entity_config": "OrderConfiguration",
    "nullable_enabled": True,
    "test": "OrdersControllerTests",
    "read_path_uses_asnotracking": True,
}
BAD = {
    "feature": "orders",
    "controller": {"class_name": "OrderCtrl", "attributes": [], "base_class": "Controller"},
    "service": {"interface": "OrdersService", "implementation": "OrdersService", "lifetime": "singleton"},
    "dto": "OrderEntity",
    "entity_config": "OrderConfig",
    "nullable_enabled": False,
    "test": "Tests",
    "read_path_uses_asnotracking": False,
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
