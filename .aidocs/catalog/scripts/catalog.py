#!/usr/bin/env python3
"""Catalog generator: CSV-first index of faion-network knowledge base.

Subcommands:
    init     Walk skills/faion/knowledge → write empty CSVs
    status   Print phase + done/total counts (or DONE)
    pick     Emit next batch of 50 unfilled rows as JSON to stdout
    update   Apply JSON {key: description} → patch CSV in place
    render   CSV → docs/catalog.md + docs/catalog.json
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE = ROOT / "skills" / "faion" / "knowledge"
CATALOG = ROOT / ".aidocs" / "catalog"
DATA = CATALOG / "data"
DOMAINS_CSV = DATA / "domains.csv"
METHODS_CSV = DATA / "methodologies.csv"
DOCS = ROOT / "docs"
OUT_MD = DOCS / "catalog.md"
OUT_JSON = DOCS / "catalog.json"

BATCH_SIZE = 25
TIER_ORDER = ["free", "solo", "pro", "geek"]


def cmd_init() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    domains = []
    methods = []
    for tier_dir in sorted(KNOWLEDGE.iterdir()):
        if not tier_dir.is_dir():
            continue
        tier = tier_dir.name
        for group_dir in sorted(tier_dir.iterdir()):
            if not group_dir.is_dir():
                continue
            group = group_dir.name
            for domain_dir in sorted(group_dir.iterdir()):
                if not domain_dir.is_dir():
                    continue
                domain = domain_dir.name
                skill_path = domain_dir / "SKILL.md"
                domains.append({
                    "tier": tier,
                    "group": group,
                    "domain": domain,
                    "skill_path": str(skill_path.relative_to(ROOT)) if skill_path.exists() else "",
                    "description": "",
                })
                for method_dir in sorted(domain_dir.iterdir()):
                    if not method_dir.is_dir():
                        continue
                    methodology = method_dir.name
                    readme = method_dir / "README.md"
                    methods.append({
                        "tier": tier,
                        "group": group,
                        "domain": domain,
                        "methodology": methodology,
                        "readme_path": str(readme.relative_to(ROOT)) if readme.exists() else "",
                        "description": "",
                    })

    with DOMAINS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["tier", "group", "domain", "skill_path", "description"])
        w.writeheader()
        w.writerows(domains)

    with METHODS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["tier", "group", "domain", "methodology", "readme_path", "description"],
        )
        w.writeheader()
        w.writerows(methods)

    sys.stdout.write(f"init: domains={len(domains)} methodologies={len(methods)}\n")


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def _phase_and_pending() -> tuple[str, list[dict], Path]:
    domains = _load_csv(DOMAINS_CSV)
    pending_d = [r for r in domains if not r.get("description", "").strip()]
    if pending_d:
        return "domains", pending_d, DOMAINS_CSV
    methods = _load_csv(METHODS_CSV)
    pending_m = [r for r in methods if not r.get("description", "").strip()]
    if pending_m:
        return "methodologies", pending_m, METHODS_CSV
    return "done", [], METHODS_CSV


def cmd_status() -> None:
    domains = _load_csv(DOMAINS_CSV)
    methods = _load_csv(METHODS_CSV)
    d_done = sum(1 for r in domains if r.get("description", "").strip())
    m_done = sum(1 for r in methods if r.get("description", "").strip())
    if d_done == len(domains) and m_done == len(methods):
        sys.stdout.write("DONE\n")
        return
    if d_done < len(domains):
        sys.stdout.write(f"phase=domains done={d_done}/{len(domains)}\n")
    else:
        sys.stdout.write(f"phase=methodologies done={m_done}/{len(methods)}\n")


def _row_key(row: dict, kind: str) -> str:
    if kind == "domains":
        return f"{row['tier']}|{row['group']}|{row['domain']}"
    return f"{row['tier']}|{row['group']}|{row['domain']}|{row['methodology']}"


def cmd_pick(skip: int = 0, size: int = BATCH_SIZE, out_path: str | None = None) -> None:
    phase, pending, _ = _phase_and_pending()
    if phase == "done":
        out = json.dumps({"phase": "done", "rows": []})
        if out_path:
            Path(out_path).write_text(out, encoding="utf-8")
        else:
            sys.stdout.write(out)
        return
    batch = pending[skip:skip + size]
    payload = {
        "phase": phase,
        "batch_size": len(batch),
        "instructions": (
            "For each row read the file at the path field, then write ONE paragraph "
            "(3-5 sentences, English, plain practical language) covering: what problem "
            "it solves, when to apply, the value delivered. No marketing, no code blocks. "
            "For domains the path is SKILL.md (write 1-2 paragraphs scoping the domain)."
        ),
        "rows": [
            {
                "key": _row_key(r, phase),
                "tier": r["tier"],
                "group": r["group"],
                "domain": r["domain"],
                **({"methodology": r["methodology"], "path": r["readme_path"]}
                   if phase == "methodologies"
                   else {"path": r["skill_path"]}),
            }
            for r in batch
        ],
    }
    out = json.dumps(payload, ensure_ascii=False, indent=2)
    if out_path:
        Path(out_path).write_text(out, encoding="utf-8")
        sys.stdout.write(f"pick: phase={phase} skip={skip} size={len(batch)} out={out_path}\n")
    else:
        sys.stdout.write(out)


def cmd_update(json_path: str) -> None:
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    phase, _, csv_path = _phase_and_pending()
    if phase == "done":
        sys.stdout.write("update: nothing pending\n")
        return
    rows = _load_csv(csv_path)
    fields = list(rows[0].keys()) if rows else []
    updated = 0
    for r in rows:
        key = _row_key(r, phase)
        if key in data and not r.get("description", "").strip():
            desc = data[key].strip().replace("\r\n", " ").replace("\n", " ")
            r["description"] = desc
            updated += 1
    _write_csv(csv_path, rows, fields)
    sys.stdout.write(f"update: phase={phase} updated={updated}/{len(data)}\n")


def cmd_render() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    domains = _load_csv(DOMAINS_CSV)
    methods = _load_csv(METHODS_CSV)

    by_dk = defaultdict(list)
    for m in methods:
        by_dk[(m["tier"], m["group"], m["domain"])].append(m)

    by_tier = defaultdict(list)
    for d in domains:
        by_tier[d["tier"]].append(d)

    lines: list[str] = []
    lines.append("# Faion Network Catalog")
    lines.append("")
    lines.append(
        f"{len(methods)} methodologies across {len(domains)} domain skills, "
        "organized by pricing tier (free → solo → pro → geek)."
    )
    lines.append("")

    for tier in TIER_ORDER:
        tier_domains = by_tier.get(tier, [])
        if not tier_domains:
            continue
        tier_method_count = sum(
            len(by_dk[(d["tier"], d["group"], d["domain"])]) for d in tier_domains
        )
        lines.append(
            f"## {tier.title()} ({len(tier_domains)} domains, {tier_method_count} methodologies)"
        )
        lines.append("")
        for d in tier_domains:
            lines.append(f"### {d['domain']} ({d['group']})")
            lines.append("")
            lines.append(d.get("description", "").strip() or "_(description pending)_")
            lines.append("")
            ms = by_dk.get((d["tier"], d["group"], d["domain"]), [])
            for m in ms:
                desc = m.get("description", "").strip() or "_(pending)_"
                lines.append(f"- **{m['methodology']}** — {desc}")
            lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    payload = {
        "domain_count": len(domains),
        "methodology_count": len(methods),
        "tiers": [],
    }
    for tier in TIER_ORDER:
        tier_domains = by_tier.get(tier, [])
        if not tier_domains:
            continue
        tier_block = {"name": tier, "domains": []}
        for d in tier_domains:
            ms = by_dk.get((d["tier"], d["group"], d["domain"]), [])
            tier_block["domains"].append({
                "group": d["group"],
                "domain": d["domain"],
                "description": d.get("description", ""),
                "methodologies": [
                    {"name": m["methodology"], "description": m.get("description", "")}
                    for m in ms
                ],
            })
        payload["tiers"].append(tier_block)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stdout.write(f"render: {OUT_MD} + {OUT_JSON}\n")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write(__doc__ or "")
        return 2
    cmd = argv[1]
    if cmd == "init":
        cmd_init()
    elif cmd == "status":
        cmd_status()
    elif cmd == "pick":
        skip = 0
        size = BATCH_SIZE
        out_path = None
        i = 2
        while i < len(argv):
            tok = argv[i]
            if tok == "--skip" and i + 1 < len(argv):
                skip = int(argv[i + 1]); i += 2
            elif tok == "--size" and i + 1 < len(argv):
                size = int(argv[i + 1]); i += 2
            elif tok == "--out" and i + 1 < len(argv):
                out_path = argv[i + 1]; i += 2
            else:
                sys.stderr.write(f"unknown pick arg: {tok}\n"); return 2
        cmd_pick(skip=skip, size=size, out_path=out_path)
    elif cmd == "update":
        if len(argv) < 3:
            sys.stderr.write("usage: catalog.py update <json-path>\n")
            return 2
        cmd_update(argv[2])
    elif cmd == "render":
        cmd_render()
    else:
        sys.stderr.write(f"unknown subcommand: {cmd}\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
