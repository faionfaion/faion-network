#!/usr/bin/env python3
"""
F-067 migration: tier-first layout → domain-first layout + meta.json split.

Walks every methodology under `skills/faion/knowledge/{free,solo,pro,geek}/`
(and optionally every playbook under `skills/faion/playbooks/{free,solo,pro,geek}/`),
parses YAML frontmatter from each `AGENTS.md`, computes the new
`<domain>/<slug>/` path, and either prints the plan (dry-run) or executes
the move + meta.json write + frontmatter strip.

The frontmatter parser is a minimal hand-rolled subset of YAML — no PyYAML.
Supports the shapes the corpus actually uses:

    key: scalar value
    key: "quoted value"
    key: [a, b, c]            # flow-style list of scalars
    key:                      # block-style list
      - a
      - b

Anything more exotic is rejected with a parse error.

USAGE
    python3 scripts/migrate-f067.py --dry-run --scope both
    python3 scripts/migrate-f067.py --root path/to/faion-network --dry-run
    python3 scripts/migrate-f067.py --scope methodologies            # live
    python3 scripts/migrate-f067.py --scope methodologies --yes      # live, no prompt
    python3 scripts/migrate-f067.py --dry-run --rename-map scripts/slug-rename-map.json

A `--dry-run / --no-dry-run` flag IS REQUIRED — there is no default. This
keeps the destructive-vs-safe choice explicit at every invocation.

DRY-RUN OUTPUT
    Writes a JSON plan to stdout — a list of
        {slug, old_path, new_path, meta_json}
    objects, followed by a summary line on stderr:
        planned=N would_skip=M conflicts=K

LIVE MODE
    Performs, for each planned methodology:
      1. `git mv <old> <new>`            (preserves history)
      2. write `<new>/meta.json`         (14 keys, canonical order)
      3. strip frontmatter from `<new>/AGENTS.md` (body verbatim)
    Aborts before any disk write if duplicate slugs or path collisions
    are detected. Live mode prompts for confirmation unless `--yes`.

EDGE CASES
    * Missing frontmatter           → SKIP + warn
    * Duplicate slug across tiers   → ABORT
    * `meta.json` already at target → ABORT
    * Paths with spaces             → handled (subprocess argv, no shell)
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

# --- constants ---------------------------------------------------------------

TIERS = ("free", "solo", "pro", "geek")

# Canonical key order for meta.json emission (matches meta-json-spec.md §3).
META_KEYS: tuple[str, ...] = (
    "slug",
    "tier",
    "domain",
    "group",
    "version",
    "status",
    "last_reviewed",
    "maintainers",
    "summary",
    "content_id",
    "complexity",
    "produces",
    "est_tokens",
    "tags",
)

# Defaults for keys missing in source frontmatter (most relevant for playbooks
# which only carry 12 of the 14 fields). The migration is conservative: we
# warn for each filled default so downstream validators surface what needs
# human curation.
PLAYBOOK_DEFAULTS: dict[str, Any] = {
    "produces": "plan",
    "est_tokens": 2000,
    "tags": [],
}

DEFAULT_VERSION = "0.1.0"
DEFAULT_STATUS = "draft"
DEFAULT_COMPLEXITY = "medium"


# --- minimal YAML frontmatter parser -----------------------------------------


class FrontmatterError(ValueError):
    """Raised when frontmatter cannot be parsed."""


def extract_frontmatter_block(text: str) -> tuple[str, str] | None:
    """Return (frontmatter_block, body) or None if no frontmatter present."""
    if not text.startswith("---"):
        return None
    # First line must be exactly '---' (allow trailing newline).
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None
    # Find the closing '---' line.
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            # Drop a single leading blank line in body for cleanliness.
            if body.startswith("\n"):
                body = body[1:]
            return fm, body
    return None


def _strip_inline_comment(value: str) -> str:
    # Drop YAML-style inline `# comment` (only when preceded by whitespace,
    # and not inside quotes). Our corpus rarely uses them, but be safe.
    in_squote = in_dquote = False
    for i, ch in enumerate(value):
        if ch == "'" and not in_dquote:
            in_squote = not in_squote
        elif ch == '"' and not in_squote:
            in_dquote = not in_dquote
        elif ch == "#" and not in_squote and not in_dquote:
            if i == 0 or value[i - 1] in (" ", "\t"):
                return value[:i].rstrip()
    return value


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _parse_scalar(value: str) -> Any:
    """Cast a scalar YAML value to int / bool / None / str."""
    raw = value.strip()
    if raw == "":
        return ""
    # Quoted → always string (preserves leading zeros etc.).
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]
    # Booleans / null (YAML 1.1 minimal set, lower-case only — corpus norm).
    if raw in ("true", "True"):
        return True
    if raw in ("false", "False"):
        return False
    if raw in ("null", "~"):
        return None
    # Int?
    try:
        return int(raw)
    except ValueError:
        pass
    return raw


def _parse_flow_list(value: str) -> list[Any]:
    """Parse `[a, b, "c d"]` → list. Bracket-balanced split."""
    inner = value.strip()
    if not (inner.startswith("[") and inner.endswith("]")):
        raise FrontmatterError(f"expected flow list, got {value!r}")
    inner = inner[1:-1].strip()
    if not inner:
        return []
    items: list[str] = []
    buf: list[str] = []
    in_squote = in_dquote = False
    for ch in inner:
        if ch == "'" and not in_dquote:
            in_squote = not in_squote
            buf.append(ch)
        elif ch == '"' and not in_squote:
            in_dquote = not in_dquote
            buf.append(ch)
        elif ch == "," and not in_squote and not in_dquote:
            items.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        items.append("".join(buf).strip())
    return [_parse_scalar(it) for it in items if it]


def parse_frontmatter(fm: str) -> dict[str, Any]:
    """Parse the minimal YAML subset used in the corpus."""
    data: dict[str, Any] = {}
    lines = fm.split("\n")
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        # Discard blank lines and pure-comment lines.
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        # We only support top-level keys (no nested mappings).
        if raw_line.startswith((" ", "\t")):
            # A continuation that wasn't consumed by the block-list branch
            # below is an error — corpus does not have nested mappings.
            raise FrontmatterError(f"unexpected indented line: {raw_line!r}")
        if ":" not in raw_line:
            raise FrontmatterError(f"missing ':' in line: {raw_line!r}")
        key, _, rest = raw_line.partition(":")
        key = key.strip()
        rest_clean = _strip_inline_comment(rest).rstrip()
        # Three shapes: scalar / flow list / block list.
        if rest_clean.strip() == "":
            # Block list: subsequent indented "- " lines.
            items: list[Any] = []
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip() == "" or nxt.lstrip().startswith("#"):
                    j += 1
                    continue
                if not nxt.startswith((" ", "\t")):
                    break
                stripped_nxt = nxt.strip()
                if not stripped_nxt.startswith("- "):
                    # Block-mapping continuation we don't support.
                    raise FrontmatterError(
                        f"unsupported block-mapping under {key!r}: {nxt!r}"
                    )
                items.append(_parse_scalar(stripped_nxt[2:]))
                j += 1
            data[key] = items
            i = j
            continue
        value = rest_clean.strip()
        if value.startswith("["):
            data[key] = _parse_flow_list(value)
        else:
            data[key] = _parse_scalar(value)
        i += 1
    return data


# --- plan model --------------------------------------------------------------


class MigrationItem:
    __slots__ = (
        "slug",
        "old_path",
        "new_path",
        "meta",
        "kind",
        "warnings",
    )

    def __init__(
        self,
        slug: str,
        old_path: Path,
        new_path: Path,
        meta: dict[str, Any],
        kind: str,
        warnings: list[str],
    ) -> None:
        self.slug = slug
        self.old_path = old_path
        self.new_path = new_path
        self.meta = meta
        self.kind = kind  # "methodology" | "playbook"
        self.warnings = warnings

    def to_plan_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "slug": self.slug,
            "old_path": str(self.old_path),
            "new_path": str(self.new_path),
            "meta_json_preview": self.meta,
            "warnings": self.warnings,
        }


# --- collection logic --------------------------------------------------------


def is_methodology_agents(path: Path, root_dir: Path) -> bool:
    """Heuristic: methodology AGENTS.md sit at folder depth >= 4 under tier."""
    # path relative to root_dir (which is .../knowledge or .../playbooks).
    try:
        rel = path.relative_to(root_dir)
    except ValueError:
        return False
    parts = rel.parts
    # parts: <tier>/.../<slug>/AGENTS.md  → at least 4 parts to be a leaf
    # (i.e. tier + group + ... + slug + AGENTS.md). Reject tier-/group-level
    # index files which sit at depth 2 or 3.
    if len(parts) < 4:
        return False
    if parts[0] not in TIERS:
        return False
    if parts[-1] != "AGENTS.md":
        return False
    return True


def collect_agents_files(scope_root: Path) -> list[Path]:
    """All AGENTS.md files under any tier that look like leaf methodologies."""
    matches: list[Path] = []
    for tier in TIERS:
        tier_dir = scope_root / tier
        if not tier_dir.is_dir():
            continue
        for agents_path in tier_dir.rglob("AGENTS.md"):
            if is_methodology_agents(agents_path, scope_root):
                matches.append(agents_path)
    return matches


def build_methodology_meta(
    fm: dict[str, Any],
    folder: Path,
    expected_slug: str,
    tier_from_path: str,
) -> tuple[dict[str, Any], list[str]]:
    """Construct a 14-key meta dict for a methodology, returning (meta, warnings)."""
    warnings: list[str] = []
    meta: dict[str, Any] = {}

    slug = fm.get("slug") or expected_slug
    if slug != expected_slug:
        warnings.append(
            f"frontmatter slug={slug!r} disagrees with folder name {expected_slug!r}; using folder name"
        )
        slug = expected_slug
    meta["slug"] = slug

    tier = fm.get("tier") or tier_from_path
    if tier != tier_from_path:
        warnings.append(
            f"frontmatter tier={tier!r} disagrees with path tier {tier_from_path!r}; using frontmatter"
        )
    meta["tier"] = tier

    domain = fm.get("domain")
    if not domain:
        # Fall back to the group as domain (corpus convention for items where
        # group == domain). Warn so the operator inspects them post-migration.
        domain = fm.get("group")
        warnings.append(f"missing domain key; falling back to group={domain!r}")
    meta["domain"] = domain

    meta["group"] = fm.get("group") or domain
    meta["version"] = fm.get("version") or DEFAULT_VERSION
    meta["status"] = fm.get("status") or DEFAULT_STATUS
    meta["last_reviewed"] = fm.get("last_reviewed") or date.today().isoformat()

    maintainers = fm.get("maintainers")
    if isinstance(maintainers, list) and maintainers:
        meta["maintainers"] = [str(m) for m in maintainers]
    elif isinstance(maintainers, str) and maintainers:
        meta["maintainers"] = [maintainers]
    else:
        meta["maintainers"] = ["faion-network"]
        warnings.append("maintainers empty/missing; defaulting to ['faion-network']")

    meta["summary"] = fm.get("summary") or ""
    if not meta["summary"]:
        warnings.append("summary missing")

    meta["content_id"] = fm.get("content_id") or ""
    if not meta["content_id"]:
        warnings.append("content_id missing (must be recomputed before commit)")

    meta["complexity"] = fm.get("complexity") or DEFAULT_COMPLEXITY
    meta["produces"] = fm.get("produces") or "spec"

    est = fm.get("est_tokens")
    if isinstance(est, int):
        meta["est_tokens"] = est
    else:
        try:
            meta["est_tokens"] = int(est) if est else 2000
        except (TypeError, ValueError):
            meta["est_tokens"] = 2000
            warnings.append(f"est_tokens not an int ({est!r}); defaulted to 2000")

    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    meta["tags"] = [str(t) for t in tags]

    # Re-order to canonical sequence (json.dumps preserves insertion order).
    ordered = {k: meta[k] for k in META_KEYS if k in meta}
    return ordered, warnings


def build_playbook_meta(
    fm: dict[str, Any],
    folder: Path,
    expected_slug: str,
    tier_from_path: str,
) -> tuple[dict[str, Any], list[str]]:
    """Construct a 14-key meta dict for a playbook (uses goal→domain mapping)."""
    warnings: list[str] = []
    meta: dict[str, Any] = {}

    slug = fm.get("slug") or expected_slug
    if slug != expected_slug:
        warnings.append(
            f"frontmatter slug={slug!r} disagrees with folder name {expected_slug!r}; using folder name"
        )
        slug = expected_slug
    meta["slug"] = slug

    tier = fm.get("tier") or tier_from_path
    meta["tier"] = tier

    # For playbooks the "domain" axis is the goal-character category (matches
    # the existing `playbooks/by-goal/<goal>/` taxonomy).
    domain = fm.get("goal")
    if not domain:
        domain = fm.get("group")
        warnings.append(f"missing goal key; falling back to group={domain!r} as domain")
    meta["domain"] = domain

    meta["group"] = fm.get("group") or domain
    meta["version"] = fm.get("version") or DEFAULT_VERSION
    meta["status"] = fm.get("status") or DEFAULT_STATUS
    meta["last_reviewed"] = fm.get("last_reviewed") or date.today().isoformat()

    maintainers = fm.get("maintainers")
    if isinstance(maintainers, list) and maintainers:
        meta["maintainers"] = [str(m) for m in maintainers]
    elif isinstance(maintainers, str) and maintainers:
        meta["maintainers"] = [maintainers]
    else:
        meta["maintainers"] = ["faion-network"]
        warnings.append("maintainers empty/missing; defaulting to ['faion-network']")

    meta["summary"] = fm.get("summary") or ""
    if not meta["summary"]:
        warnings.append("summary missing")

    meta["content_id"] = fm.get("content_id") or ""
    if not meta["content_id"]:
        warnings.append("content_id missing (must be recomputed before commit)")

    meta["complexity"] = fm.get("complexity") or DEFAULT_COMPLEXITY
    meta["produces"] = fm.get("produces") or PLAYBOOK_DEFAULTS["produces"]

    est = fm.get("est_tokens")
    if isinstance(est, int):
        meta["est_tokens"] = est
    else:
        try:
            meta["est_tokens"] = int(est) if est else PLAYBOOK_DEFAULTS["est_tokens"]
        except (TypeError, ValueError):
            meta["est_tokens"] = PLAYBOOK_DEFAULTS["est_tokens"]
            warnings.append(f"est_tokens not an int ({est!r}); defaulted")

    tags = fm.get("tags") or PLAYBOOK_DEFAULTS["tags"]
    if isinstance(tags, str):
        tags = [tags]
    meta["tags"] = [str(t) for t in tags]

    ordered = {k: meta[k] for k in META_KEYS if k in meta}
    return ordered, warnings


def collect_plan(
    scope_root: Path,
    kind: str,
    targets_root: Path,
) -> tuple[list[MigrationItem], list[str], list[str]]:
    """
    Walk a scope root and produce (items, skipped_paths, errors).

    `scope_root` is e.g. `skills/faion/knowledge/`.
    `targets_root` is the same dir — new paths are computed relative to it.
    """
    items: list[MigrationItem] = []
    skipped: list[str] = []
    errors: list[str] = []

    agents_files = collect_agents_files(scope_root)
    for agents_path in agents_files:
        folder = agents_path.parent
        slug = folder.name
        try:
            text = agents_path.read_text(encoding="utf-8")
        except OSError as e:
            errors.append(f"{agents_path}: read failed — {e}")
            continue

        fm_block = extract_frontmatter_block(text)
        if fm_block is None:
            skipped.append(f"{agents_path}: no YAML frontmatter")
            continue

        fm_text, _body = fm_block
        try:
            fm = parse_frontmatter(fm_text)
        except FrontmatterError as e:
            errors.append(f"{agents_path}: frontmatter parse error — {e}")
            continue

        try:
            rel = agents_path.relative_to(scope_root)
        except ValueError:
            errors.append(f"{agents_path}: not under scope root {scope_root}")
            continue
        tier_from_path = rel.parts[0]

        if kind == "methodology":
            meta, warnings = build_methodology_meta(fm, folder, slug, tier_from_path)
        elif kind == "playbook":
            meta, warnings = build_playbook_meta(fm, folder, slug, tier_from_path)
        else:
            raise AssertionError(f"unknown kind {kind!r}")

        domain = meta.get("domain")
        if not domain:
            errors.append(f"{agents_path}: cannot determine domain — skipping")
            continue

        new_path = targets_root / str(domain) / slug
        items.append(
            MigrationItem(
                slug=slug,
                old_path=folder,
                new_path=new_path,
                meta=meta,
                kind=kind,
                warnings=warnings,
            )
        )
    return items, skipped, errors


# --- rename-map loader -------------------------------------------------------


class RenameMap:
    """Maps an old_path (relative to repo root) to the planned rename action.

    Keys are stored as the trailing repo-relative path
    (e.g. `skills/faion/knowledge/solo/dev/software-developer/ab-testing`).
    """

    def __init__(self, entries: list[dict[str, Any]]) -> None:
        self._by_old_path: dict[str, dict[str, Any]] = {}
        for e in entries:
            old_path = e["old_path"].lstrip("/")
            self._by_old_path[old_path] = e

    def lookup(self, repo_relative_folder: str) -> dict[str, Any] | None:
        return self._by_old_path.get(repo_relative_folder.lstrip("/"))

    @classmethod
    def load(cls, path: Path) -> RenameMap:
        with path.open() as f:
            data = json.load(f)
        return cls(data.get("renames", []))

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for e in self._by_old_path.values():
            counts[e.get("action", "?")] += 1
        return dict(counts)


def apply_rename_map(
    items: list[MigrationItem],
    rename_map: RenameMap,
    targets_root: Path,
) -> tuple[list[MigrationItem], list[MigrationItem], list[str]]:
    """Apply rename-map actions to a planned items list.

    Returns (kept_items, deleted_items, applied_log).
      * action=keep:   item unchanged (rebuilt path with map's new_domain/new_slug if present).
      * action=rename: item.slug and item.new_path rewritten to the renamed value.
      * action=delete: item removed from plan and surfaced in deleted_items.
      * action=manual-review: item removed and flagged in applied_log.

    Items not present in the map pass through unchanged.
    """
    kept: list[MigrationItem] = []
    deleted: list[MigrationItem] = []
    log: list[str] = []
    repo_root = targets_root.parent.parent.parent  # knowledge -> faion -> skills -> repo
    # Robustness: derive repo_root by stripping the four expected levels.
    # `targets_root` is `<repo>/skills/faion/knowledge` (or .../playbooks).
    # We need the bit AFTER repo_root for keys.
    parts = list(targets_root.parts)
    # Find the index of `skills` from the right; everything before it is repo_root.
    try:
        idx = len(parts) - 1 - list(reversed(parts)).index("skills")
        repo_root = Path(*parts[:idx])
    except ValueError:
        repo_root = targets_root.parent.parent.parent

    for it in items:
        try:
            rel = it.old_path.relative_to(repo_root)
        except ValueError:
            rel = it.old_path
        entry = rename_map.lookup(str(rel))
        if entry is None:
            # Pass through unchanged.
            kept.append(it)
            continue
        action = entry.get("action")
        if action == "keep":
            # Possibly remap domain/slug from the map (must agree with item).
            new_domain = entry.get("new_domain") or it.meta.get("domain")
            new_slug = entry.get("new_slug") or it.slug
            it.slug = new_slug
            it.meta["slug"] = new_slug
            it.meta["domain"] = new_domain
            it.new_path = targets_root / str(new_domain) / new_slug
            kept.append(it)
            log.append(f"keep: {rel} -> {new_domain}/{new_slug}")
            continue
        if action == "rename":
            new_domain = entry.get("new_domain") or it.meta.get("domain")
            new_slug = entry["new_slug"]
            it.slug = new_slug
            it.meta["slug"] = new_slug
            it.meta["domain"] = new_domain
            it.new_path = targets_root / str(new_domain) / new_slug
            kept.append(it)
            log.append(f"rename: {rel} -> {new_domain}/{new_slug}")
            continue
        if action == "delete":
            deleted.append(it)
            log.append(f"delete: {rel} (kept_path={entry.get('kept_path')})")
            continue
        if action == "manual-review":
            log.append(f"manual-review: {rel} — skipped from plan")
            continue
        log.append(f"unknown-action {action!r}: {rel} — passing through unchanged")
        kept.append(it)
    return kept, deleted, log


# --- validation --------------------------------------------------------------


def detect_conflicts(items: list[MigrationItem]) -> list[str]:
    """Return human-readable conflict lines (empty list = no conflicts).

    Slug-uniqueness is scoped to (kind, domain, slug): the same slug may exist
    in two different domains as long as the destination paths differ. The
    F-067 layout uses `<domain>/<slug>/` as canonical, so two different
    domains owning the same slug is non-conflicting (e.g. `dev/accessibility`
    and `frontend/accessibility`).
    """
    conflicts: list[str] = []

    # Duplicate slugs scoped to (kind, domain, slug).
    by_slug: dict[tuple[str, str, str], list[MigrationItem]] = defaultdict(list)
    for it in items:
        domain = it.meta.get("domain", "?")
        by_slug[(it.kind, domain, it.slug)].append(it)
    for (kind, domain, slug), group in by_slug.items():
        if len(group) > 1:
            paths = ", ".join(str(g.old_path) for g in group)
            conflicts.append(
                f"duplicate slug ({kind}) {slug!r} in domain {domain!r} across: {paths}"
            )

    # Duplicate new_path (different slugs collide on the same target).
    by_target: dict[Path, list[MigrationItem]] = defaultdict(list)
    for it in items:
        by_target[it.new_path].append(it)
    for target, group in by_target.items():
        if len(group) > 1:
            slugs = ", ".join(g.slug for g in group)
            conflicts.append(f"path collision at {target}: slugs={slugs}")

    # Existing meta.json at target.
    for it in items:
        meta_target = it.new_path / "meta.json"
        if meta_target.exists():
            conflicts.append(f"meta.json already exists at {meta_target}")

    return conflicts


# --- execution ---------------------------------------------------------------


def render_meta_json(meta: dict[str, Any]) -> str:
    """Canonical meta.json text — 2-space indent, trailing newline."""
    return json.dumps(meta, indent=2, ensure_ascii=False) + "\n"


def strip_frontmatter(text: str) -> str:
    block = extract_frontmatter_block(text)
    if block is None:
        return text
    _fm, body = block
    if not body.endswith("\n"):
        body += "\n"
    return body


def run_git_mv(old_path: Path, new_path: Path, repo_root: Path) -> None:
    new_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "mv", str(old_path), str(new_path)],
        check=True,
        cwd=repo_root,
    )


def execute_plan(items: list[MigrationItem], repo_root: Path) -> None:
    for it in items:
        run_git_mv(it.old_path, it.new_path, repo_root)
        (it.new_path / "meta.json").write_text(
            render_meta_json(it.meta), encoding="utf-8"
        )
        agents_path = it.new_path / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")
        agents_path.write_text(strip_frontmatter(text), encoding="utf-8")


# --- CLI ---------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="F-067 migration: tier-first → domain-first layout + meta.json split.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    dry = parser.add_mutually_exclusive_group(required=True)
    dry.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Print the move plan; touch no files.",
    )
    dry.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        help="Execute the migration (git mv + meta.json + AGENTS.md trim).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="faion-network repo root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--scope",
        choices=("methodologies", "playbooks", "both"),
        default="both",
        help="Which corpus to migrate (default: both).",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the live-mode confirmation prompt.",
    )
    parser.add_argument(
        "--rename-map",
        type=Path,
        default=None,
        help=(
            "Path to a slug-rename-map.json (F-067 T13). When passed, the plan "
            "is post-processed: keep/rename rewrite the slug+domain; delete "
            "removes the source from the plan; manual-review entries are "
            "skipped and surfaced on stderr."
        ),
    )
    return parser.parse_args(argv)


def collect_for_scope(
    root: Path,
    scope: str,
    rename_map: RenameMap | None = None,
) -> tuple[list[MigrationItem], list[str], list[str], list[MigrationItem], list[str]]:
    """Collect plan items, optionally applying a rename-map.

    Returns (items, skipped, errors, deleted_items, rename_map_log).
    """
    items: list[MigrationItem] = []
    skipped: list[str] = []
    errors: list[str] = []
    deleted: list[MigrationItem] = []
    rm_log: list[str] = []

    if scope in ("methodologies", "both"):
        kroot = root / "skills" / "faion" / "knowledge"
        if not kroot.is_dir():
            errors.append(f"knowledge root not found: {kroot}")
        else:
            i, s, e = collect_plan(kroot, "methodology", kroot)
            if rename_map is not None:
                i, d, log = apply_rename_map(i, rename_map, kroot)
                deleted.extend(d)
                rm_log.extend(log)
            items.extend(i)
            skipped.extend(s)
            errors.extend(e)

    if scope in ("playbooks", "both"):
        proot = root / "skills" / "faion" / "playbooks"
        if not proot.is_dir():
            errors.append(f"playbook root not found: {proot}")
        else:
            i, s, e = collect_plan(proot, "playbook", proot)
            if rename_map is not None:
                i, d, log = apply_rename_map(i, rename_map, proot)
                deleted.extend(d)
                rm_log.extend(log)
            items.extend(i)
            skipped.extend(s)
            errors.extend(e)

    return items, skipped, errors, deleted, rm_log


def confirm(prompt: str) -> bool:
    try:
        ans = input(prompt).strip().lower()
    except EOFError:
        return False
    return ans in ("y", "yes")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    root = args.root.resolve()
    if not (root / "skills" / "faion").is_dir():
        sys.stderr.write(
            f"error: --root {root} does not look like a faion-network repo\n"
        )
        return 2

    rename_map: RenameMap | None = None
    if args.rename_map:
        if not args.rename_map.is_file():
            sys.stderr.write(f"error: rename-map not found: {args.rename_map}\n")
            return 2
        rename_map = RenameMap.load(args.rename_map)
        sys.stderr.write(
            f"loaded rename-map from {args.rename_map}: stats={rename_map.stats()}\n"
        )

    items, skipped, errors, deleted, rm_log = collect_for_scope(
        root, args.scope, rename_map=rename_map
    )
    conflicts = detect_conflicts(items)

    # Plan output (always JSON-on-stdout for both modes; summary on stderr).
    plan = {
        "scope": args.scope,
        "root": str(root),
        "items": [it.to_plan_dict() for it in items],
        "skipped": skipped,
        "errors": errors,
        "conflicts": conflicts,
        "deleted_by_rename_map": [it.to_plan_dict() for it in deleted],
        "rename_map_log": rm_log,
    }
    sys.stdout.write(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")

    sys.stderr.write(
        f"planned={len(items)} would_skip={len(skipped)} "
        f"conflicts={len(conflicts)} errors={len(errors)} "
        f"deleted_by_map={len(deleted)}\n"
    )

    if args.dry_run:
        return 0 if not conflicts and not errors else 1

    # --- live mode ---
    if conflicts or errors:
        sys.stderr.write(
            "aborting: resolve conflicts/errors above before running live.\n"
        )
        return 1
    if not items:
        sys.stderr.write("nothing to migrate.\n")
        return 0

    if not _git_available():
        sys.stderr.write("error: git not on PATH; required for live mode.\n")
        return 2
    if not _is_clean_worktree(root):
        sys.stderr.write(
            "error: working tree is not clean. Commit or stash before running live.\n"
        )
        return 2

    if not args.yes:
        sys.stderr.write(
            f"\nAbout to migrate {len(items)} folders under {root}.\n"
            f"This will perform git mv + meta.json write + AGENTS.md trim for each.\n"
        )
        if not confirm("Proceed? [y/N] "):
            sys.stderr.write("aborted by user.\n")
            return 1

    try:
        execute_plan(items, repo_root=root)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"git mv failed: {e}\n")
        return 1
    sys.stderr.write(f"migration complete: {len(items)} folders moved.\n")
    return 0


def _git_available() -> bool:
    return shutil.which("git") is not None


def _is_clean_worktree(root: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            check=True,
            cwd=root,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return result.stdout.strip() == ""


if __name__ == "__main__":
    sys.exit(main())
