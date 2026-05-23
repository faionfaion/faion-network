#!/usr/bin/env python3
"""F-067 T07: regenerate tier-manifest.json from meta.json files.

Walks `skills/faion/knowledge/<domain>/<slug>/meta.json` and
`skills/faion/playbooks/<domain>/<slug>/meta.json` (post-F-067 layout).

Until T11 lands the migration, falls back to AGENTS.md frontmatter so the
pre-migration corpus keeps producing the same 2625 entries as F-066 v7.

Usage:
    python3 scripts/regen-tier-manifest.py            # write to skills/tier-manifest.json
    python3 scripts/regen-tier-manifest.py --dry-run  # print summary, write nothing
    python3 scripts/regen-tier-manifest.py --diff     # dry-run + diff vs current manifest
"""
import argparse
import json
import re
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


def parse_frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return m.group(1) if m else None


def fm_get(fm: str | None, key: str) -> str | None:
    if not fm:
        return None
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", fm, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def tier_from_path(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).parts
    if not rel:
        return None
    return rel[0] if rel[0] in TIERS else None


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


def entry_from_agents_md(agents_path: Path, root: Path) -> dict | None:
    """F-067 transitional fallback; remove after T11."""
    d = agents_path.parent
    if d.name == "templates":
        return None
    fm = parse_frontmatter(agents_path.read_text(encoding="utf-8", errors="replace"))
    if not fm:
        return None
    slug = fm_get(fm, "slug")
    if not slug:
        return None
    tier = tier_from_path(d, root) or fm_get(fm, "tier")
    return {
        "slug": slug,
        "tier": tier,
        "path": str(d.relative_to(ROOT)),
        "content_id": fm_get(fm, "content_id") or "",
        "domain": fm_get(fm, "domain") or "",
        "group": fm_get(fm, "group") or "",
        "status": fm_get(fm, "status") or "draft",
        "version": fm_get(fm, "version") or "1.0.0",
    }


def collect_entries() -> tuple[list[dict], dict]:
    """Walk knowledge + playbooks. Prefer meta.json; fall back to AGENTS.md.

    Returns (entries, stats).
    """
    entries: list[dict] = []
    seen_paths: set[str] = set()
    stats = {
        "meta_knowledge": 0,
        "meta_playbooks": 0,
        "fallback_knowledge": 0,
        "fallback_playbooks": 0,
        "skipped": 0,
    }

    # 1. meta.json under knowledge (post-F-067 layout)
    if KNOWLEDGE.exists():
        for meta in KNOWLEDGE.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                seen_paths.add(e["path"])
                stats["meta_knowledge"] += 1

    # 2. meta.json under playbooks (post-F-067 layout)
    if PLAYBOOKS.exists():
        for meta in PLAYBOOKS.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                seen_paths.add(e["path"])
                stats["meta_playbooks"] += 1

    # 3. F-067 transitional fallback; remove after T11.
    #    Walk AGENTS.md frontmatter when meta.json is absent.
    #    Mirrors F-066 v7 behaviour: knowledge-only (playbooks were not in v7).
    if KNOWLEDGE.exists():
        for agents in KNOWLEDGE.rglob("AGENTS.md"):
            d = agents.parent
            # skip if a meta.json already covered this dir
            if str(d.relative_to(ROOT)) in seen_paths:
                continue
            e = entry_from_agents_md(agents, KNOWLEDGE)
            if e:
                entries.append(e)
                seen_paths.add(e["path"])
                stats["fallback_knowledge"] += 1
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
        f"fallback_knowledge={stats['fallback_knowledge']}, "
        f"fallback_playbooks={stats['fallback_playbooks']}, "
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
