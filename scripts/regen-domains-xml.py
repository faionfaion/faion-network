#!/usr/bin/env python3
"""F-067 T09 — regenerate domains.xml (L1) + per-domain INDEX.xml (L2).

Walks `skills/faion/knowledge/` for `meta.json` files (the F-067 canonical
metadata source). Generates:

  1. `skills/faion/knowledge/domains.xml` — L1 index of all domains, each
     with description + slug count.
  2. `skills/faion/knowledge/<domain>/INDEX.xml` — L2 index per domain,
     listing all slugs in that domain (slug + tier + summary).

The L1 index preserves rich existing per-domain metadata (scope,
typical-asks, decision-tree, disambiguation) by reading the current
domains.xml when present, then refreshing `count` attrs and slug
inventory. If domains.xml is absent, a minimal stub is generated.

Usage:
  regen-domains-xml.py              # dry-run, print summary
  regen-domains-xml.py --preview    # dry-run + save samples to .aidocs/_progress/
  regen-domains-xml.py --write      # write to disk (backs up existing domains.xml)

HARD RULES (per F-067 T09):
  - NEVER overwrite an existing domains.xml without backing it up first.
  - Output must parse cleanly with xml.etree.ElementTree.
  - UTF-8 + lowercase tags.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"
DOMAINS_XML = KNOWLEDGE / "domains.xml"

PROGRESS_DIR = (
    REPO_ROOT.parent / ".aidocs" / "_progress" / "F-067" / "samples"
)

META_KEYS = ("slug", "tier", "group", "domain", "summary")

# Sub-paths to ignore inside knowledge/.
SKIP_DIR_PARTS = {"templates", "scripts", "content", "__pycache__"}


# ---------------------------------------------------------------------------
# meta.json parsing
# ---------------------------------------------------------------------------


def load_meta_json(p: Path) -> dict[str, str] | None:
    """Load meta.json (F-067 canonical metadata source)."""
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return {k: ("" if data.get(k) is None else str(data.get(k))) for k in META_KEYS}


def methodology_entry(leaf_dir: Path) -> dict[str, str] | None:
    """Resolve a methodology entry from `<leaf>/meta.json`."""
    meta = leaf_dir / "meta.json"
    if meta.is_file():
        return load_meta_json(meta)
    return None


# ---------------------------------------------------------------------------
# Walk knowledge/
# ---------------------------------------------------------------------------


def collect() -> dict[str, list[dict[str, str]]]:
    """Walk knowledge/, group methodologies by domain.

    A "methodology leaf" is any directory containing a `meta.json` file.
    """
    by_domain: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[Path] = set()

    # Collect candidate leaves via meta.json walk (F-067 canonical layout).
    candidates: list[Path] = list(KNOWLEDGE.rglob("meta.json"))

    for marker in candidates:
        leaf = marker.parent
        if leaf in seen:
            continue
        # Skip if any path part is on the skip list (e.g. templates/, scripts/)
        rel_parts = leaf.relative_to(KNOWLEDGE).parts
        if any(part in SKIP_DIR_PARTS for part in rel_parts):
            continue
        # Skip the knowledge root itself
        if leaf == KNOWLEDGE:
            continue
        seen.add(leaf)
        info = methodology_entry(leaf)
        if not info:
            continue
        domain = (info.get("domain") or "").strip()
        slug = (info.get("slug") or "").strip()
        if not domain or not slug:
            continue
        rel = leaf.relative_to(REPO_ROOT)
        info["path"] = str(rel)
        info["summary"] = (info.get("summary") or "").strip()
        by_domain[domain].append(info)

    # Sort each domain's slugs alphabetically
    for entries in by_domain.values():
        entries.sort(key=lambda e: e.get("slug", ""))

    return by_domain


# ---------------------------------------------------------------------------
# Render L2 INDEX.xml per domain
# ---------------------------------------------------------------------------


def render_l2_index(domain: str, entries: list[dict[str, str]]) -> str:
    """Render a domain's L2 INDEX.xml — flat slug list with tier + summary."""
    today = date.today().isoformat()
    out: list[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append(
        f'<index domain="{escape(domain)}" count="{len(entries)}" '
        f'version="3.0" generated="{today}">'
    )
    out.append(
        f"  <description>L2 index of methodologies in the {escape(domain)} "
        f"domain. The retriever reads this after picking {escape(domain)} "
        f"from L1 domains.xml. Entries list slug + tier + summary; open the "
        f"leaf meta.json / content/*.xml for full payload.</description>"
    )
    for e in entries:
        slug = escape(e.get("slug", ""))
        tier = escape(e.get("tier", ""))
        path = escape(e.get("path", ""))
        summary = escape(
            (e.get("summary") or "").replace("\n", " ").strip()
        )
        out.append(
            f'  <methodology slug="{slug}" tier="{tier}" path="{path}">'
        )
        out.append(f"    <summary>{summary}</summary>")
        out.append("  </methodology>")
    out.append("</index>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Render L1 domains.xml
# ---------------------------------------------------------------------------


def read_existing_domain_metadata() -> dict[str, dict] | None:
    """Read existing domains.xml to preserve rich per-domain metadata.

    Returns a dict of:
      {
        "header_children": [<ET.Element>, ...],   # decision-tree, disambiguation, description, ...
        "domains": {
          "<domain-id>": {
            "scope": "...",
            "l2_index": "...",
            "typical_asks": ["...", ...],
          }
        }
      }

    Returns None if no existing file.
    """
    if not DOMAINS_XML.is_file():
        return None
    try:
        tree = ET.parse(DOMAINS_XML)
    except ET.ParseError:
        return None
    root = tree.getroot()
    result: dict = {
        "root_attrib": dict(root.attrib),
        "header_children": [],
        "domains": {},
    }
    for child in root:
        if child.tag == "domain":
            did = child.attrib.get("id", "").strip()
            if not did:
                continue
            entry: dict = {"scope": "", "l2_index": "", "typical_asks": []}
            for sub in child:
                if sub.tag == "scope":
                    entry["scope"] = (sub.text or "").strip()
                elif sub.tag == "l2-index":
                    entry["l2_index"] = (sub.text or "").strip()
                elif sub.tag == "typical-asks":
                    for ask in sub.findall("ask"):
                        entry["typical_asks"].append((ask.text or "").strip())
            result["domains"][did] = entry
        else:
            result["header_children"].append(child)
    return result


def render_l1_domains(
    by_domain: dict[str, list[dict[str, str]]],
    existing: dict | None,
) -> str:
    """Render domains.xml — refreshed counts, preserved metadata if any."""
    today = date.today().isoformat()
    total = sum(len(v) for v in by_domain.values())
    domain_ids = sorted(by_domain.keys())

    out: list[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append(
        f'<domains version="2.0" generated="{today}" canonical="{len(domain_ids)}" total_methodologies="{total}">'
    )

    # Header content — preserve existing description / decision-tree /
    # disambiguation if present, else emit a minimal description.
    if existing and existing["header_children"]:
        for el in existing["header_children"]:
            # Serialize each header child verbatim (re-indented to 2 spaces).
            xml = ET.tostring(el, encoding="unicode")
            # Add a leading two-space indent on each line for readability
            xml_lines = xml.strip().splitlines()
            out.append("  " + xml_lines[0])
            for line in xml_lines[1:]:
                out.append("  " + line)
            out.append("")
    else:
        out.append(
            "  <description>L1 index of methodology domains. The retriever "
            "reads this first, then drills into at most 3 candidate domains' "
            "INDEX.xml.</description>"
        )

    # Per-domain blocks
    for did in domain_ids:
        count = len(by_domain[did])
        meta = (existing or {}).get("domains", {}).get(did)
        out.append(f'  <domain id="{escape(did)}" count="{count}">')
        if meta and meta.get("scope"):
            out.append(f"    <scope>{escape(meta['scope'])}</scope>")
        else:
            out.append(
                f"    <scope>Methodologies in the {escape(did)} domain.</scope>"
            )
        if meta and meta.get("l2_index"):
            out.append(f"    <l2-index>{escape(meta['l2_index'])}</l2-index>")
        else:
            out.append(
                f"    <l2-index>skills/faion/knowledge/{escape(did)}/INDEX.xml</l2-index>"
            )
        if meta and meta.get("typical_asks"):
            out.append("    <typical-asks>")
            for ask in meta["typical_asks"]:
                out.append(f"      <ask>{escape(ask)}</ask>")
            out.append("    </typical-asks>")
        out.append("  </domain>")
        out.append("")

    out.append("</domains>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Verify generated XML parses
# ---------------------------------------------------------------------------


def verify_parses(xml: str, label: str) -> bool:
    try:
        ET.fromstring(xml)
        return True
    except ET.ParseError as exc:
        sys.stderr.write(f"[error] {label} failed to parse: {exc}\n")
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--write",
        action="store_true",
        help="write to disk (default: dry-run, prints summary)",
    )
    ap.add_argument(
        "--preview",
        action="store_true",
        help="save sample domains.xml + one INDEX.xml under .aidocs/_progress/F-067/samples/",
    )
    args = ap.parse_args()

    by_domain = collect()
    existing = read_existing_domain_metadata()

    # ---- Render L1 ----
    l1_xml = render_l1_domains(by_domain, existing)
    if not verify_parses(l1_xml, "domains.xml"):
        return 2

    # ---- Render L2 per domain ----
    l2_outputs: dict[str, str] = {}
    for did in sorted(by_domain.keys()):
        l2_xml = render_l2_index(did, by_domain[did])
        if not verify_parses(l2_xml, f"{did}/INDEX.xml"):
            return 2
        l2_outputs[did] = l2_xml

    # ---- Summary ----
    sys.stdout.write(
        f"[domains] {len(by_domain)} domains, "
        f"{sum(len(v) for v in by_domain.values())} methodologies total\n"
    )
    for did in sorted(by_domain.keys()):
        sys.stdout.write(f"  - {did}: {len(by_domain[did])}\n")

    # ---- Preview write ----
    if args.preview:
        PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
        preview_l1 = PROGRESS_DIR / "domains-xml-preview.xml"
        preview_l1.write_text(l1_xml, encoding="utf-8")
        sys.stdout.write(f"[preview] wrote {preview_l1}\n")
        # pick first domain (alphabetical) for L2 sample
        if l2_outputs:
            first = sorted(l2_outputs.keys())[0]
            sample_l2 = PROGRESS_DIR / f"INDEX-{first}-preview.xml"
            sample_l2.write_text(l2_outputs[first], encoding="utf-8")
            sys.stdout.write(f"[preview] wrote {sample_l2}\n")

    # ---- Real write ----
    if args.write:
        # Back up existing domains.xml
        if DOMAINS_XML.is_file():
            backup = DOMAINS_XML.with_suffix(
                f".xml.bak-{date.today().isoformat()}"
            )
            # Avoid clobbering an existing backup
            n = 0
            while backup.exists():
                n += 1
                backup = DOMAINS_XML.with_suffix(
                    f".xml.bak-{date.today().isoformat()}.{n}"
                )
            shutil.copy2(DOMAINS_XML, backup)
            sys.stdout.write(f"[backup] {DOMAINS_XML} -> {backup}\n")
        DOMAINS_XML.write_text(l1_xml, encoding="utf-8")
        sys.stdout.write(f"[write] {DOMAINS_XML}\n")

        for did, xml in l2_outputs.items():
            target = KNOWLEDGE / did / "INDEX.xml"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(xml, encoding="utf-8")
            sys.stdout.write(f"[write] {target}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
