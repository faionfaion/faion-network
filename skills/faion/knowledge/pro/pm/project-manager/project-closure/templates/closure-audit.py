#!/usr/bin/env python3
"""Validate a closure_checklist.yaml for completeness and evidence links.

Each item in the YAML:
  {id: str, name: str, status: done|pending|na, owner: str,
   evidence_url: str (optional), blocker: str (optional)}

Usage: closure-audit.py <closure_checklist.yaml>
Exit 0 = all clear. Exit 1 = failures found.
"""
import sys
import yaml

REQUIRED_ITEMS = {
    "deliverable_acceptance",
    "final_costs_recorded",
    "invoices_processed",
    "purchase_orders_closed",
    "contracts_terminated",
    "team_released",
    "equipment_returned",
    "access_revoked",
    "lessons_learned_session",
    "final_report",
    "documents_archived",
    "ops_handover",
    "stakeholders_notified",
}

VALID_STATUSES = {"done", "pending", "na"}


def audit(path: str) -> list[str]:
    items: list[dict] = yaml.safe_load(open(path))
    by_id = {i["id"]: i for i in items}
    failures = []

    # Check required items exist
    missing = REQUIRED_ITEMS - set(by_id)
    for m in sorted(missing):
        failures.append(f"missing required item: {m}")

    for item in items:
        iid = item["id"]
        status = item.get("status", "")

        if status not in VALID_STATUSES:
            failures.append(f"{iid}: invalid status '{status}'")

        if status == "done" and not item.get("evidence_url"):
            failures.append(f"{iid}: marked done but no evidence_url")

        if status == "pending" and not item.get("blocker"):
            failures.append(f"{iid}: pending without blocker reason")

    return failures


def main(path: str) -> None:
    failures = audit(path)
    if failures:
        for f in failures:
            print(f"[FAIL] {f}")
        sys.exit(1)
    print("Closure checklist valid")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: closure-audit.py <closure_checklist.yaml>")
        sys.exit(2)
    main(sys.argv[1])
