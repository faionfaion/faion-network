#!/usr/bin/env python3
"""Validate the L1 domains index (skills/faion/knowledge/domains.xml).

Checks performed:

    1. Root element is <domains> with attrs `version` and `generated` (canonical
       attr accepted but optional).
    2. Every <domain> child has the required attribute `id` and the required
       child elements: <count>, <scope>, <l2-index>. (The <count> can also be
       expressed as an attribute on <domain>; both forms accepted.)
    3. The path declared in <l2-index> resolves to an existing file on disk
       (relative to the repository root).

Exit codes:
    0 - PASS
    1 - FAIL (one or more findings)

Usage:
    python3 scripts/validate-domains-index.py
    python3 scripts/validate-domains-index.py --domains-file path/to/domains.xml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOMAINS = REPO_ROOT / "skills" / "faion" / "knowledge" / "domains.xml"


def validate(domains_file: Path) -> list[str]:
    findings: list[str] = []
    if not domains_file.is_file():
        return [f"domains file not found: {domains_file}"]

    try:
        tree = ET.parse(domains_file)
    except ET.ParseError as exc:
        return [f"XML parse error: {exc}"]

    root = tree.getroot()
    if root.tag != "domains":
        findings.append(f"root tag is <{root.tag}>, expected <domains>")

    for required_attr in ("version", "generated"):
        if required_attr not in root.attrib:
            findings.append(f"<domains> missing required attribute: {required_attr}")

    for domain in root.findall("domain"):
        did = domain.attrib.get("id", "<missing>")
        if "id" not in domain.attrib:
            findings.append("<domain> missing required attribute: id")

        count_attr = domain.attrib.get("count")
        count_child = domain.find("count")
        if count_attr is None and count_child is None:
            findings.append(f"domain '{did}': missing count (attribute or child)")

        scope = domain.find("scope")
        if scope is None or not (scope.text or "").strip():
            findings.append(f"domain '{did}': missing or empty <scope>")

        l2 = domain.find("l2-index")
        if l2 is None or not (l2.text or "").strip():
            findings.append(f"domain '{did}': missing or empty <l2-index>")
            continue

        l2_rel = l2.text.strip()
        l2_abs = REPO_ROOT / l2_rel
        if not l2_abs.is_file():
            findings.append(
                f"domain '{did}': l2-index path does not exist on disk: {l2_rel}"
            )

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domains-file",
                    default=str(DEFAULT_DOMAINS),
                    help="Path to domains.xml (default: skills/faion/knowledge/domains.xml)")
    args = ap.parse_args()

    findings = validate(Path(args.domains_file))
    if findings:
        sys.stdout.write("FAIL\n")
        for f in findings:
            sys.stdout.write(f"  - {f}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
