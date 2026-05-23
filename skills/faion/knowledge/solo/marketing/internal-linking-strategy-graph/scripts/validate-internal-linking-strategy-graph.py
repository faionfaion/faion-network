#!/usr/bin/env python3
"""validate-internal-linking-strategy-graph.py

Validate the internal-link graph spec + audit bundle against
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
import sys
from pathlib import Path


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("site", "clusters", "audit"):
        if k not in obj:
            errs.append("missing required: " + k)
    site = obj.get("site", {})
    if isinstance(site, dict):
        for k in ("domain", "indexed_page_count", "crawl_date"):
            if k not in site:
                errs.append("site missing " + k)
        ic = site.get("indexed_page_count")
        if isinstance(ic, int) and ic < 30:
            errs.append("site.indexed_page_count must be >= 30")
    clusters = obj.get("clusters", [])
    if not isinstance(clusters, list) or not clusters:
        errs.append("clusters must be non-empty list")
    else:
        for i, c in enumerate(clusters):
            for k in ("cluster_id", "hub_url", "spoke_urls"):
                if k not in c:
                    errs.append("clusters[" + str(i) + "] missing " + k)
            spokes = c.get("spoke_urls", [])
            if not isinstance(spokes, list) or len(spokes) < 4:
                errs.append("clusters[" + str(i) + "] spoke_urls must be >=4")
    audit = obj.get("audit", {})
    if isinstance(audit, dict):
        for k in ("orphans", "low_inbound_spokes", "exact_match_anchor_targets",
                  "missing_hub_link_spokes"):
            if k not in audit:
                errs.append("audit missing " + k)
        if audit.get("orphans"):
            errs.append("audit.orphans must be empty (any orphan kills the spec)")
        for row in audit.get("low_inbound_spokes", []):
            if isinstance(row, dict) and row.get("inbound_count", 0) < 2:
                errs.append("audit.low_inbound_spokes: " + str(row.get("url"))
                            + " has inbound_count<2")
        for row in audit.get("exact_match_anchor_targets", []):
            if isinstance(row, dict) and row.get("anchor_form_count", 0) < 3:
                errs.append("audit.exact_match_anchor_targets: " + str(row.get("url"))
                            + " has anchor_form_count<3")
        if audit.get("missing_hub_link_spokes"):
            errs.append("audit.missing_hub_link_spokes must be empty (every spoke must link to its hub)")
    return errs


OK = {
    "site": {"domain": "blog.example.com", "indexed_page_count": 120, "crawl_date": "2026-05-22"},
    "clusters": [{
        "cluster_id": "saas-pricing",
        "hub_url": "https://blog.example.com/saas-pricing-guide",
        "spoke_urls": [
            "https://blog.example.com/spoke-1",
            "https://blog.example.com/spoke-2",
            "https://blog.example.com/spoke-3",
            "https://blog.example.com/spoke-4",
        ],
    }],
    "audit": {
        "orphans": [],
        "low_inbound_spokes": [],
        "exact_match_anchor_targets": [],
        "missing_hub_link_spokes": [],
    },
}
BAD = {
    "site": {"domain": "x", "indexed_page_count": 10, "crawl_date": "later"},
    "clusters": [{"cluster_id": "tiny", "hub_url": "x", "spoke_urls": []}],
    "audit": {"orphans": ["https://x/orphan"], "low_inbound_spokes": [{"url": "u", "inbound_count": 0}],
              "exact_match_anchor_targets": [{"url": "u", "anchor_form_count": 1}],
              "missing_hub_link_spokes": ["https://x/spoke"]},
}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
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
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
