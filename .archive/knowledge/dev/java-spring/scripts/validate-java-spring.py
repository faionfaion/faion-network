#!/usr/bin/env python3
"""validate-java-spring.py

Validate a layered Spring Boot feature spec against 02-output-contract.xml.

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

REQUIRED = ["feature", "controller", "service", "request_dto", "response_dto"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
CTRL_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Controller$")
SVC_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Service$")
REQ_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Request$")
RES_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Response$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "feature" in obj and not NAME_RE.match(str(obj["feature"])):
        errs.append("feature must be PascalCase")
    ctrl = obj.get("controller") or {}
    if not CTRL_RE.match(str(ctrl.get("class_name", ""))):
        errs.append("controller.class_name must end with Controller")
    if ctrl.get("has_transactional") is True:
        errs.append("controller.has_transactional must be false (thin-controller)")
    if ctrl.get("calls_repository_directly") is True:
        errs.append("controller.calls_repository_directly must be false (thin-controller)")
    svc = obj.get("service") or {}
    if not SVC_RE.match(str(svc.get("class_name", ""))):
        errs.append("service.class_name must end with Service")
    if svc.get("transactional_present") is not True:
        errs.append("service.transactional_present must be true (transactional-on-service-only)")
    if svc.get("returns_entity") is True:
        errs.append("service.returns_entity must be false (record-dtos-with-validation)")
    req = obj.get("request_dto") or {}
    if not REQ_RE.match(str(req.get("class_name", ""))):
        errs.append("request_dto.class_name must end with Request")
    if req.get("is_record") is not True:
        errs.append("request_dto.is_record must be true")
    if req.get("has_bean_validation") is not True:
        errs.append("request_dto.has_bean_validation must be true")
    res = obj.get("response_dto") or {}
    if not RES_RE.match(str(res.get("class_name", ""))):
        errs.append("response_dto.class_name must end with Response")
    if res.get("is_record") is not True:
        errs.append("response_dto.is_record must be true")
    async_obj = obj.get("async") or {}
    if async_obj and async_obj.get("self_invocation") is True:
        errs.append("async.self_invocation must be false (async-via-named-executor)")
    return errs


OK = {
    "feature": "Orders",
    "controller": {"class_name": "OrdersController", "has_transactional": False, "calls_repository_directly": False, "list_endpoint_uses_pageable": True},
    "service": {"class_name": "OrdersService", "transactional_present": True, "returns_entity": False},
    "request_dto": {"class_name": "CreateOrderRequest", "is_record": True, "has_bean_validation": True},
    "response_dto": {"class_name": "OrderResponse", "is_record": True},
    "async": {"self_invocation": False, "executor_name": "emailExecutor", "executor_bean_defined": True},
}
BAD = {
    "feature": "Orders",
    "controller": {"class_name": "OrderCtrl", "has_transactional": True, "calls_repository_directly": True},
    "service": {"class_name": "OrdersService", "transactional_present": False, "returns_entity": True},
    "request_dto": {"class_name": "CreateOrderReq", "is_record": False, "has_bean_validation": False},
    "response_dto": {"class_name": "OrderResp", "is_record": False},
    "async": {"self_invocation": True},
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
