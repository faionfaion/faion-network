#!/usr/bin/env python3
"""F-067 T07: regenerate tier-manifest.json from meta.json files.

Walks `skills/faion/knowledge/<domain>/<slug>/meta.json`,
`skills/faion/playbooks/<domain>/<slug>/meta.json` (post-F-067 layout),
`skills/faion/fragments/<library>/meta.json` (F027 T06: one
meta.json per fragment library directory gates every fragment file
beneath it — the same directory-coverage rule vfs-pack applies) and
`skills/faion/tools/<pack>/meta.json` (F029: one meta.json per tool
pack gates its scripts and cards, same directory-coverage rule) and
`skills/faion/lexicon/meta.json` (F031: one meta.json gates the UA->EN
query lexicon; it is tier `free` on purpose - a paid lexicon would mean
free users cannot search in their own language) and
`skills/faion/recipes/<name>/meta.json` (F027 recipe library: one
meta.json per recipe dir gates its recipe.json and its card, same
directory-coverage rule).

The manifest `notes` field is never dropped: a version bump keeps the
previous note verbatim behind a `Prior vN:` prefix.

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
FRAGMENTS = ROOT / "skills" / "faion" / "fragments"
TOOLS = ROOT / "skills" / "faion" / "tools"
LEXICON = ROOT / "skills" / "faion" / "lexicon"
RECIPES = ROOT / "skills" / "faion" / "recipes"
BACKUP = ROOT / "skills" / "tier-manifest.json.f067-pre-bak"

TIERS = ("free", "solo", "pro", "geek")
TODAY = "2026-08-13"
NEW_VERSION = 14
NOTES_HEAD = (
    "v14: P2.3 — the dead `playbook_root` / `playbook_paths` keys are "
    "dropped from every tier block. They encoded the pre-F-067 "
    "`playbooks/<tier>/<group>/<slug>` layout, which was deleted; no "
    "code in faion-cli or faion-net-be ever read either key (the "
    "backend reads only `preview_percentage` out of a tier block, and "
    "resolves tier from `entries` / meta.json), so they were a stale "
    "map that could only mislead the next reader. `entries` is "
    "unchanged and remains the single source of path-to-tier truth."
)

# Keys under `tiers.<tier>` that no longer describe anything on disk.
# `entries` is the path-to-tier map; these were a second, stale copy.
DEAD_TIER_KEYS = ("playbook_root", "playbook_paths")


def build_notes(current_notes: str, current_version) -> str:
    """Prepend this version's note, keeping the previous one verbatim.

    Idempotent: regenerating a manifest already at NEW_VERSION returns its
    notes unchanged, so repeated runs never stack duplicate prefixes and no
    prior note is ever dropped.
    """
    if current_version == NEW_VERSION:
        return current_notes
    if not current_notes:
        return NOTES_HEAD
    return f"{NOTES_HEAD} Prior notes, verbatim: {current_notes}"


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
        "meta_fragments": 0,
        "meta_tools": 0,
        "meta_lexicon": 0,
        "meta_recipes": 0,
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

    # 3. meta.json under fragments (F027 T06: one per library dir)
    if FRAGMENTS.exists():
        for meta in FRAGMENTS.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                stats["meta_fragments"] += 1
            else:
                stats["skipped"] += 1

    # 4. meta.json under tools (F029: one per tool pack dir)
    if TOOLS.exists():
        for meta in TOOLS.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                stats["meta_tools"] += 1
            else:
                stats["skipped"] += 1

    # 5. meta.json under lexicon (F031: one entry gates the query lexicon)
    if LEXICON.exists():
        for meta in LEXICON.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                stats["meta_lexicon"] += 1
            else:
                stats["skipped"] += 1

    # 6. meta.json under recipes (F027: one per recipe dir)
    if RECIPES.exists():
        for meta in RECIPES.rglob("meta.json"):
            e = entry_from_meta(meta)
            if e:
                entries.append(e)
                stats["meta_recipes"] += 1
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
    new_manifest["tiers"] = {
        tier: {k: v for k, v in (block or {}).items() if k not in DEAD_TIER_KEYS}
        for tier, block in (manifest.get("tiers") or {}).items()
    }
    new_manifest["entries"] = entries
    new_manifest["total"] = len(entries)
    new_manifest["last_synced"] = TODAY
    new_manifest["notes"] = build_notes(manifest.get("notes", ""),
                                        manifest.get("version"))
    new_manifest["version"] = NEW_VERSION

    summary = (
        f"entries={len(entries)} "
        f"(meta_knowledge={stats['meta_knowledge']}, "
        f"meta_playbooks={stats['meta_playbooks']}, "
        f"meta_fragments={stats['meta_fragments']}, "
        f"meta_tools={stats['meta_tools']}, "
        f"meta_lexicon={stats['meta_lexicon']}, "
        f"meta_recipes={stats['meta_recipes']}, "
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
