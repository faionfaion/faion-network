#!/usr/bin/env python3
"""validate-backup-database-postgres.py

Validate the config artefact for the backup-database-postgres methodology
against the JSON Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = [
    "db_name",
    "backup_format",
    "verify_before_upload",
    "wal_monitoring",
    "secrets_source",
    "retention_local_days",
    "retention_remote_days",
]

ALLOWED_FORMATS = {"custom", "directory", "tar-base"}
ALLOWED_SECRETS = {"vault", "aws-secrets-manager", "gcp-secret-manager", "pgpass-0600"}
ALLOWED_STORAGE = {"s3", "gcs", "azure-blob", "restic", "pgbackrest"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("backup_format") not in ALLOWED_FORMATS:
        errs.append(f"backup_format must be one of {sorted(ALLOWED_FORMATS)}")
    if obj.get("verify_before_upload") is not True:
        errs.append("verify_before_upload must be true (rule: verify-before-upload)")
    wm = obj.get("wal_monitoring", {})
    if not isinstance(wm, dict) or "enabled" not in wm or "alert_on_failed_count_increase" not in wm:
        errs.append("wal_monitoring must be object with enabled + alert_on_failed_count_increase")
    if obj.get("secrets_source") not in ALLOWED_SECRETS:
        errs.append(f"secrets_source must be one of {sorted(ALLOWED_SECRETS)}")
    rs = obj.get("remote_storage")
    if rs is not None:
        if not isinstance(rs, dict) or rs.get("kind") not in ALLOWED_STORAGE or not rs.get("uri"):
            errs.append(f"remote_storage.kind must be one of {sorted(ALLOWED_STORAGE)} and uri set")
    rl = obj.get("retention_local_days")
    if not isinstance(rl, int) or rl < 1 or rl > 365:
        errs.append("retention_local_days must be int 1..365")
    rr = obj.get("retention_remote_days")
    if not isinstance(rr, int) or rr < 7 or rr > 3650:
        errs.append("retention_remote_days must be int 7..3650")
    return errs


OK = {
    "db_name": "billing",
    "backup_format": "custom",
    "verify_before_upload": True,
    "wal_monitoring": {"enabled": True, "alert_on_failed_count_increase": True},
    "secrets_source": "vault",
    "remote_storage": {"kind": "s3", "uri": "s3://backups-prod/postgres/billing/"},
    "retention_local_days": 7,
    "retention_remote_days": 90,
}
BAD = {
    "db_name": "billing",
    "backup_format": "plain",
    "verify_before_upload": False,
    "secrets_source": "inline",
    "retention_local_days": 0,
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
    # strip the optional doc header before validating
    if isinstance(obj, dict):
        obj.pop("__faion_header__", None)
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
