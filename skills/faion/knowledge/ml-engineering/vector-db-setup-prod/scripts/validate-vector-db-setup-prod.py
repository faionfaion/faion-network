#!/usr/bin/env python3
"""validate-vector-db-setup-prod.py — validate prod-deploy.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["deploy_mode", "storage", "resources", "ha", "backup", "checklist"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    storage = obj.get("storage", {})
    if isinstance(storage, dict) and not storage.get("durable"):
        errs.append("storage.durable must be true (r1-durable-persistence)")
    res = obj.get("resources", {})
    if isinstance(res, dict):
        for k in ("cpu_limit", "memory_limit_gb"):
            if k not in res:
                errs.append(f"resources.{k} missing (r2-resource-limits)")
    backup = obj.get("backup", {})
    if isinstance(backup, dict):
        drill = backup.get("last_restore_drill")
        if drill:
            try:
                drill_date = datetime.fromisoformat(drill).replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) - drill_date > timedelta(days=120):
                    errs.append("backup.last_restore_drill older than 120 days (r4-backup-and-restore-drilled)")
            except ValueError:
                errs.append("backup.last_restore_drill not ISO date")
        if backup.get("retention_days", 0) < 7:
            errs.append("backup.retention_days must be >= 7")
    cl = obj.get("checklist", {})
    if isinstance(cl, dict) and not cl.get("pre_deploy_passed"):
        errs.append("checklist.pre_deploy_passed must be true (r5-pre-post-deploy-checklist)")
    return errs


FIXTURE_VALID = """
deploy_mode: k8s-statefulset
storage: {class: ebs-gp3, size_gb: 200, durable: true}
resources: {cpu_request: "2", cpu_limit: "4", memory_request_gb: 16, memory_limit_gb: 24}
ha: {strategy: single-with-snapshot, replicas: 1}
backup: {schedule_cron: "0 3 * * *", retention_days: 30, destination: s3://x, last_restore_drill: "2026-04-15"}
checklist: {pre_deploy_passed: true, post_deploy_passed: true}
"""

FIXTURE_INVALID = """
deploy_mode: k8s-statefulset
storage: {class: emptyDir, size_gb: 200, durable: false}
resources: {cpu_request: "2", memory_request_gb: 16}
ha: {strategy: none, replicas: 1}
backup: {schedule_cron: "0 3 * * *", retention_days: 3, destination: s3://x, last_restore_drill: "2025-01-01"}
checklist: {pre_deploy_passed: false, post_deploy_passed: false}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n"); return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n"); return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-vector-db-setup-prod", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
