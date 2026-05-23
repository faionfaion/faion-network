#!/usr/bin/env python3
"""validate-vui-privacy-security.py

Validate the artefact for the vui-privacy-security methodology against the schema in
content/02-output-contract.xml.

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
import re
import sys
from pathlib import Path

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
JURIS = {'US', 'UK', 'EU', 'JP', 'CA', 'BR', 'AU'}
AUTH_METHODS = {'pin', 'biometric', 'tap-confirm', '2fa'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'vui-privacy-security':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'jurisdictions' not in obj:
        errs.append(f"missing required field: " + 'jurisdictions')
    if 'trust_indicators' not in obj:
        errs.append(f"missing required field: " + 'trust_indicators')
    if 'step_up_auth' not in obj:
        errs.append(f"missing required field: " + 'step_up_auth')
    if 'redaction' not in obj:
        errs.append(f"missing required field: " + 'redaction')
    if 'retention' not in obj:
        errs.append(f"missing required field: " + 'retention')
    if 'deletion_control' not in obj:
        errs.append(f"missing required field: " + 'deletion_control')


    jur = obj.get("jurisdictions") or []
    if not isinstance(jur, list) or not jur:
        errs.append("jurisdictions must be non-empty list")
    ti = obj.get("trust_indicators") or {}
    if ti.get("visual") is not True:
        errs.append("trust_indicators.visual must be true")
    if ti.get("audio") is not True:
        errs.append("trust_indicators.audio must be true")
    sua = obj.get("step_up_auth") or {}
    sas = sua.get("sensitive_actions")
    if not isinstance(sas, list):
        errs.append("step_up_auth.sensitive_actions must be list")
    red = obj.get("redaction") or {}
    if red.get("on_device") is not True:
        errs.append("redaction.on_device must be true")
    cats = red.get("categories") or []
    if not isinstance(cats, list) or not cats:
        errs.append("redaction.categories must be non-empty list")
    ret = obj.get("retention") or {}
    td = ret.get("transcript_days")
    if not isinstance(td, int) or td < 0 or td > 30:
        errs.append("retention.transcript_days must be 0-30")
    if obj.get("deletion_control") is not True:
        errs.append("deletion_control must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'vui-privacy-security', 'version': '1.1.0', 'produces': 'spec'}, 'jurisdictions': ['EU', 'US', 'CA'], 'trust_indicators': {'visual': True, 'audio': True}, 'step_up_auth': {'sensitive_actions': [{'intent': 'send-payment', 'method': 'biometric'}, {'intent': 'change-account', 'method': 'pin'}]}, 'redaction': {'on_device': True, 'categories': ['name', 'account_number', 'ssn', 'address']}, 'retention': {'transcript_days': 14}, 'deletion_control': True}
BAD = {'jurisdictions': [], 'trust_indicators': {'visual': False, 'audio': False}, 'step_up_auth': {'sensitive_actions': []}, 'redaction': {'on_device': False, 'categories': []}, 'retention': {'transcript_days': 365}, 'deletion_control': False}


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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
