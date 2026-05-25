#!/usr/bin/env python3
"""F-067 T07: regenerate tier-manifest.json from meta.json files.

Walks `skills/faion/knowledge/<domain>/<slug>/meta.json` and
`skills/faion/playbooks/<domain>/<slug>/meta.json` (post-F-067 layout).

Usage:
    python3 scripts/regen-tier-manifest.py            # write to skills/tier-manifest.json
    python3 scripts/regen-tier-manifest.py --dry-run  # print summary, write nothing
    python3 scripts/regen-tier-manifest.py --diff     # dry-run + diff vs current manifest
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # faion-network repo root
MANIFEST = ROOT / "skills" / "tier-manifest.json"
KNOWLEDGE = ROOT / "skills" / "faion" / "knowledge"
PLAYBOOKS = ROOT / "skills" / "faion" / "playbooks"
BACKUP = ROOT / "skills" / "tier-manifest.json.f067-pre-bak"

TIERS = ("free", "solo", "pro", "geek")
TODAY = "2026-05-23"
NEW_VERSION = 8
NEW_NOTES = (
    "v8: F-067 closed — corpus restructured to domain-first layout; "
    "tier-manifest now derived from <domain>/<slug>/meta.json files."
)


def entry_from_meta(meta_path: Path) -> dict | None:
    """Build a manifest entry from a meta.json file."""
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    d = meta_path.parent
    return {
        "slug": meta.get("slug") or d.name,
        "tier": meta.get("tier"),
        "path": str(d.relative_to(ROOT)),
        "content_id": meta.get("content_id") or "",
        "domain": meta.get("domain") or "",
        "group": meta.get("group") or "",
        "status": meta.get("status") or "draft",
        "version": meta.get("version") or "1.0.0",
    }


def collect_entries() -> tuple[list[dict], dict]:
    """Walk knowledge + playbooks meta.json files.

    Returns (entries, stats).
    """
    entries: list[dict] = []
    stats = {
        "meta_knowledge": 0,
        "meta_playbooks": 0,
        "skipped": 0,
    }

    # 1. meta.json under knowledge (post-F-067 layout)
    if KNOWLEDGE.exists():
        for meta in KNOWLEDGE.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                stats["meta_knowledge"] += 1
            else:
                stats["skipped"] += 1

    # 2. meta.json under playbooks (post-F-067 layout)
    if PLAYBOOKS.exists():
        for meta in PLAYBOOKS.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                stats["meta_playbooks"] += 1
            else:
                stats["skipped"] += 1

    entries.sort(key=lambda e: (e["tier"] or "", e["path"]))
    return entries, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Do not write; print summary only.")
    ap.add_argument("--diff", action="store_true",
                    help="Dry-run + show diff vs current tier-manifest.json.")
    args = ap.parse_args()

    if not MANIFEST.exists():
        print(f"ERROR: {MANIFEST} not found", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text())
    entries, stats = collect_entries()

    new_manifest = dict(manifest)
    new_manifest["entries"] = entries
    new_manifest["total"] = len(entries)
    new_manifest["last_synced"] = TODAY
    new_manifest["version"] = NEW_VERSION
    new_manifest["notes"] = NEW_NOTES

    summary = (
        f"entries={len(entries)} "
        f"(meta_knowledge={stats['meta_knowledge']}, "
        f"meta_playbooks={stats['meta_playbooks']}, "
        f"skipped={stats['skipped']})"
    )
    print(summary)

    if args.diff or args.dry_run:
        current = manifest.get("entries", [])
        cur_by_path = {e["path"]: e for e in current}
        new_by_path = {e["path"]: e for e in entries}
        added = sorted(set(new_by_path) - set(cur_by_path))
        removed = sorted(set(cur_by_path) - set(new_by_path))
        changed = []
        for p in sorted(set(cur_by_path) & set(new_by_path)):
            if cur_by_path[p] != new_by_path[p]:
                changed.append(p)
        print(f"diff vs current: +{len(added)} added, -{len(removed)} removed, ~{len(changed)} changed")
        if args.diff:
            for p in added[:20]:
                print(f"  + {p}")
            if len(added) > 20:
                print(f"  ... and {len(added) - 20} more added")
            for p in removed[:20]:
                print(f"  - {p}")
            if len(removed) > 20:
                print(f"  ... and {len(removed) - 20} more removed")
            for p in changed[:20]:
                print(f"  ~ {p}")
                for k in sorted(set(cur_by_path[p]) | set(new_by_path[p])):
                    a = cur_by_path[p].get(k)
                    b = new_by_path[p].get(k)
                    if a != b:
                        print(f"       {k}: {a!r} -> {b!r}")
            if len(changed) > 20:
                print(f"  ... and {len(changed) - 20} more changed")
        # Header diff
        print("header diff:")
        for k in ("version", "total", "last_synced", "notes"):
            print(f"  {k}: {manifest.get(k)!r} -> {new_manifest.get(k)!r}")

    if args.dry_run or args.diff:
        print("DRY-RUN: not writing.")
        return 0

    # Live mode: back up + write
    BACKUP.write_text(MANIFEST.read_text(), encoding="utf-8")
    MANIFEST.write_text(json.dumps(new_manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"wrote {MANIFEST} (backup at {BACKUP})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
