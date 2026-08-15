#!/usr/bin/env python3
"""Validate an edge-freshness report against the cdn-fronted-static-deploy contract.

Input  : a JSON file shaped by content/02-output-contract.xml.
Output : one line per violation on stdout, or a single OK line.

Dev-time only, stdlib only, no network. The report is produced by whatever probe
the project already has; this script only decides whether the report is honest —
it never contacts the edge itself.

Usage:
  validate-cdn-fronted-static-deploy.py <report.json>
  validate-cdn-fronted-static-deploy.py --self-test
  validate-cdn-fronted-static-deploy.py --help

Options:
  --json    machine-readable output

Exit codes: 0 valid, 1 violations found, 2 usage or IO failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EDGE_STATUS = {"HIT", "MISS", "DYNAMIC", "EXPIRED", "BYPASS", "UNKNOWN"}
PROBE_VERDICT = {"FRESH", "STALE", "UNVERIFIED"}
REPORT_VERDICT = {"PASS", "FAIL"}
REQUIRED_TOP = ("artefact_id", "generated", "site", "probes", "gates", "verdict")
REQUIRED_GATES = ("asset_stamp_check", "deploy_allow_list", "sw_registration_versioned")
REQUIRED_PROBE = ("url", "edge_status", "edge_bytes", "origin_bytes", "verdict")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
IPV4_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
CONN_RE = re.compile(r"[^\s/@]+@[^\s/@]+")
STAMP_RE = re.compile(r"[?&]v=[0-9a-zA-Z]+")

DEFAULT_AGE_BUDGET = 300


def _fail(out: list[str], code: str, msg: str) -> None:
    out.append("%s %s" % (code, msg))


def validate(report: object) -> list[str]:
    """Return a list of violation strings; empty means the report is valid."""
    out: list[str] = []
    if not isinstance(report, dict):
        return ["E000 report root must be a JSON object"]

    for key in REQUIRED_TOP:
        if key not in report:
            _fail(out, "E001", "missing required key: %s" % key)
    if out:
        return out

    generated = report.get("generated")
    if not isinstance(generated, str) or not DATE_RE.match(generated):
        _fail(out, "E002", "generated must be an ISO date (YYYY-MM-DD)")

    site = report.get("site")
    if not isinstance(site, str) or len(site) < 3:
        _fail(out, "E003", "site must be a non-empty hostname")
    else:
        # f5 — no infra identifiers in a committed artefact.
        if IPV4_RE.search(site):
            _fail(out, "E005", "site contains an address literal; probe the public name")
        if CONN_RE.search(site):
            _fail(out, "E005", "site looks like a connection string (user@host)")

    budget = report.get("max_age_budget_seconds", DEFAULT_AGE_BUDGET)
    if not isinstance(budget, int) or budget < 0:
        _fail(out, "E006", "max_age_budget_seconds must be a non-negative integer")
        budget = DEFAULT_AGE_BUDGET

    gates = report.get("gates")
    if not isinstance(gates, dict):
        _fail(out, "E007", "gates must be an object")
        gates = {}
    for gate in REQUIRED_GATES:
        if gate not in gates:
            _fail(out, "E007", "gates is missing required flag: %s" % gate)
        elif not isinstance(gates[gate], bool):
            _fail(out, "E007", "gate %s must be a boolean" % gate)

    probes = report.get("probes")
    if not isinstance(probes, list) or not probes:
        _fail(out, "E008", "probes must be a non-empty array")
        probes = []

    stale_seen = False
    for idx, probe in enumerate(probes):
        where = "probes[%d]" % idx
        if not isinstance(probe, dict):
            _fail(out, "E009", "%s must be an object" % where)
            continue
        missing = [k for k in REQUIRED_PROBE if k not in probe]
        if missing:
            _fail(out, "E009", "%s missing: %s" % (where, ", ".join(missing)))
            continue

        url = probe["url"]
        status = probe["edge_status"]
        verdict = probe["verdict"]
        edge_bytes = probe["edge_bytes"]
        origin_bytes = probe["origin_bytes"]
        age = probe.get("edge_age_seconds", 0)
        stamped = probe.get("stamped")

        if not isinstance(url, str) or not url.startswith("/"):
            _fail(out, "E009", "%s url must be a root-relative path" % where)
        if status not in EDGE_STATUS:
            _fail(out, "E009", "%s edge_status %r not in %s"
                  % (where, status, sorted(EDGE_STATUS)))
        if verdict not in PROBE_VERDICT:
            _fail(out, "E009", "%s verdict %r not in %s"
                  % (where, verdict, sorted(PROBE_VERDICT)))
        if not isinstance(edge_bytes, int) or not isinstance(origin_bytes, int):
            _fail(out, "E009", "%s edge_bytes and origin_bytes must be integers" % where)
            continue
        if verdict == "STALE":
            stale_seen = True

        # f1 — byte disagreement outranks any self-reported FRESH.
        if verdict == "FRESH" and edge_bytes != origin_bytes:
            _fail(out, "E101", "%s claims FRESH but edge served %d bytes and origin "
                               "holds %d" % (where, edge_bytes, origin_bytes))
        # f2 — an aged HIT is stale until proven otherwise.
        if verdict == "FRESH" and status == "HIT" and isinstance(age, int) and age > budget:
            _fail(out, "E102", "%s claims FRESH on a HIT aged %ds against a %ds budget"
                  % (where, age, budget))
        # f3 — an unstamped asset path means the hashing rule was never applied.
        if isinstance(url, str) and url.startswith("/assets/"):
            if stamped is False or (stamped is None and not STAMP_RE.search(url)):
                _fail(out, "E103", "%s is an asset URL with no content-hash stamp" % where)
        # f6 — UNKNOWN is never a pass.
        if verdict == "FRESH" and status == "UNKNOWN":
            _fail(out, "E106", "%s cannot be FRESH with edge_status UNKNOWN" % where)

    # f4 — the report may record a failure; it may not round it up.
    top_verdict = report.get("verdict")
    if top_verdict not in REPORT_VERDICT:
        _fail(out, "E010", "verdict %r not in %s" % (top_verdict, sorted(REPORT_VERDICT)))
    elif top_verdict == "PASS":
        false_gates = [g for g in REQUIRED_GATES if gates.get(g) is False]
        if false_gates:
            _fail(out, "E104", "verdict PASS with failing gates: %s" % ", ".join(false_gates))
        if stale_seen:
            _fail(out, "E104", "verdict PASS with at least one STALE probe")

    return out


GOOD = {
    "artefact_id": "release-probe", "generated": "2026-08-15", "site": "example.test",
    "max_age_budget_seconds": 300,
    "probes": [
        {"url": "/assets/js/main.js?v=9f21c0ab41", "edge_status": "MISS",
         "edge_age_seconds": 0, "edge_bytes": 10487, "origin_bytes": 10487,
         "stamped": True, "verdict": "FRESH"},
    ],
    "gates": {"asset_stamp_check": True, "deploy_allow_list": True,
              "sw_registration_versioned": True},
    "verdict": "PASS",
}

# The measured 2026-07-28 incident, written out as the artefact nobody produced.
INCIDENT = {
    "artefact_id": "release-probe", "generated": "2026-07-28", "site": "203.0.113.10",
    "max_age_budget_seconds": 300,
    "probes": [
        {"url": "/assets/js/main.js", "edge_status": "HIT", "edge_age_seconds": 280134,
         "edge_bytes": 735, "origin_bytes": 10487, "stamped": False, "verdict": "FRESH"},
    ],
    "gates": {"asset_stamp_check": False, "deploy_allow_list": True,
              "sw_registration_versioned": False},
    "verdict": "PASS",
}


def self_test() -> int:
    failures = 0

    def expect(name: str, payload: object, codes: set[str]) -> None:
        nonlocal failures
        got = {v.split(" ", 1)[0] for v in validate(payload)}
        if got != codes:
            failures += 1
            print("FAIL %s: expected %s, got %s" % (name, sorted(codes), sorted(got)))
        else:
            print("ok   %s" % name)

    expect("valid report", GOOD, set())
    expect("2026-07-28 incident", INCIDENT, {"E005", "E101", "E102", "E103", "E104"})

    no_gate = json.loads(json.dumps(GOOD))
    del no_gate["gates"]["deploy_allow_list"]
    expect("missing gate flag", no_gate, {"E007"})

    unknown = json.loads(json.dumps(GOOD))
    unknown["probes"][0]["edge_status"] = "UNKNOWN"
    expect("UNKNOWN cannot be FRESH", unknown, {"E106"})

    stale = json.loads(json.dumps(GOOD))
    stale["probes"][0]["verdict"] = "STALE"
    expect("PASS over a STALE probe", stale, {"E104"})

    aged = json.loads(json.dumps(GOOD))
    aged["probes"][0]["edge_status"] = "HIT"
    aged["probes"][0]["edge_age_seconds"] = 280134
    expect("aged HIT called FRESH", aged, {"E102"})

    expect("root must be an object", ["not", "a", "dict"], {"E000"})

    print("self-test: %s" % ("PASS" if failures == 0 else "%d FAILED" % failures))
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-cdn-fronted-static-deploy.py",
        description="Validate an edge-freshness report (see content/02-output-contract.xml).",
    )
    parser.add_argument("report", nargs="?", help="path to the report JSON file")
    parser.add_argument("--self-test", action="store_true", help="replay the built-in fixtures")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args(argv)

    if ns.self_test:
        return self_test()
    if not ns.report:
        parser.error("provide a report file or --self-test")

    path = Path(ns.report)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print("cannot read %s: %s" % (path, exc), file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print("invalid JSON in %s: %s" % (path, exc), file=sys.stderr)
        return 2

    violations = validate(payload)
    if ns.json:
        print(json.dumps({"path": str(path), "ok": not violations,
                          "violations": violations}, indent=2))
    elif violations:
        print("FAIL %s" % path)
        for v in violations:
            print("  " + v)
    else:
        print("OK %s" % path)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
