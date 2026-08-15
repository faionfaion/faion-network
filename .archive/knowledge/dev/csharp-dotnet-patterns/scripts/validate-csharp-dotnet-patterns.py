#!/usr/bin/env python3
"""validate-csharp-dotnet-patterns.py

Validate a clean-arch + CQRS feature folder spec against 02-output-contract.xml.

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

REQUIRED = ["feature", "command", "handler", "aggregate", "validator", "response_dto"]
FEATURE_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
CMD_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Command$")
HANDLER_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Handler$")
AGG_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
VAL_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Validator$")
DTO_RE = re.compile(r"^[A-Z][A-Za-z0-9]+(Response|Dto)$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "feature" in obj and not FEATURE_RE.match(str(obj["feature"])):
        errs.append("feature must be PascalCase")
    if "command" in obj and not CMD_RE.match(str(obj["command"])):
        errs.append("command must end with 'Command'")
    if "handler" in obj and not HANDLER_RE.match(str(obj["handler"])):
        errs.append("handler must end with 'Handler'")
    if "aggregate" in obj and not AGG_RE.match(str(obj["aggregate"])):
        errs.append("aggregate must be PascalCase")
    if obj.get("aggregate_has_public_setters") is True:
        errs.append("aggregate_has_public_setters must be false (rich-domain-no-setters)")
    if "validator" in obj and not VAL_RE.match(str(obj["validator"])):
        errs.append("validator must end with 'Validator'")
    if "response_dto" in obj and not DTO_RE.match(str(obj["response_dto"])):
        errs.append("response_dto must end with 'Response' or 'Dto'")
    if obj.get("response_dto", "").endswith("Entity"):
        errs.append("response_dto must not be an entity (no-entity-in-api)")
    lr = obj.get("layer_refs") or {}
    if lr.get("domain_has_ef_ref") is True:
        errs.append("domain must not reference EF Core (clean-arch-layers)")
    if lr.get("domain_has_aspnet_ref") is True:
        errs.append("domain must not reference ASP.NET Core (clean-arch-layers)")
    return errs


OK = {
    "feature": "ShipOrder",
    "command": "ShipOrderCommand",
    "handler": "ShipOrderHandler",
    "aggregate": "Order",
    "aggregate_has_public_setters": False,
    "validator": "ShipOrderValidator",
    "response_dto": "ShipOrderResponse",
    "layer_refs": {"domain_has_ef_ref": False, "domain_has_aspnet_ref": False},
}
BAD = {
    "feature": "shipOrder",
    "command": "ShipOrderRequest",
    "handler": "OrderService",
    "aggregate": "OrderDto",
    "aggregate_has_public_setters": True,
    "validator": "manualIfs",
    "response_dto": "OrderEntity",
    "layer_refs": {"domain_has_ef_ref": True, "domain_has_aspnet_ref": True},
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
