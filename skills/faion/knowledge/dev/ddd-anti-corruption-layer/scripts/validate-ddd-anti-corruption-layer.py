#!/usr/bin/env python3
"""validate-ddd-anti-corruption-layer.py

Validate an ACL spec against the schema in 02-output-contract.xml.

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

REQUIRED = [
    "domain_interface",
    "acl_implementation",
    "external_dependency",
    "error_translations",
    "fail_safe",
    "contract_tests",
]
IFACE_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
ADAPTER_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Adapter$")
DOMAIN_ERR_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Error$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    di = obj.get("domain_interface") or {}
    if not IFACE_RE.match(str(di.get("name", ""))):
        errs.append("domain_interface.name must be PascalCase")
    if di.get("imports_vendor_sdk") is True:
        errs.append("domain_interface.imports_vendor_sdk must be false")
    ai = obj.get("acl_implementation") or {}
    if not ADAPTER_RE.match(str(ai.get("name", ""))):
        errs.append("acl_implementation.name must end with 'Adapter'")
    if ai.get("layer") != "infrastructure":
        errs.append("acl_implementation.layer must be 'infrastructure'")
    if ai.get("is_only_sdk_importer") is not True:
        errs.append("acl_implementation.is_only_sdk_importer must be true")
    et = obj.get("error_translations") or []
    if not et:
        errs.append("error_translations must contain at least 1 entry")
    for t in et:
        if not DOMAIN_ERR_RE.match(str(t.get("domain_error", ""))):
            errs.append(f"domain_error '{t.get('domain_error')}' must end with 'Error'")
    fs = obj.get("fail_safe") or {}
    if fs.get("documented") is not True:
        errs.append("fail_safe.documented must be true")
    if not str(fs.get("default_behaviour", "")).strip():
        errs.append("fail_safe.default_behaviour must be non-empty")
    if not obj.get("contract_tests"):
        errs.append("contract_tests must contain at least 1 entry")
    return errs


OK = {
    "domain_interface": {"name": "InventoryChecker", "imports_vendor_sdk": False},
    "acl_implementation": {"name": "ShopifyInventoryAdapter", "layer": "infrastructure", "is_only_sdk_importer": True},
    "external_dependency": "shopify-python-sdk",
    "error_translations": [
        {"vendor_error": "ShopifyAPIError.NotFound", "domain_error": "ItemNotFoundError"},
        {"vendor_error": "ShopifyAPIError.RateLimit", "domain_error": "InventoryUnavailableError"},
    ],
    "fail_safe": {"documented": True, "default_behaviour": "assume available + retry after 60s"},
    "contract_tests": ["test_acl_translates_404_to_item_not_found"],
}
BAD = {
    "domain_interface": {"name": "shopify_client", "imports_vendor_sdk": True},
    "acl_implementation": {"name": "Helper", "layer": "domain", "is_only_sdk_importer": False},
    "external_dependency": "shopify",
    "error_translations": [],
    "fail_safe": {"documented": False, "default_behaviour": ""},
    "contract_tests": [],
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
