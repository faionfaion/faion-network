#!/usr/bin/env python3
"""
Audit index coverage across the faion-network knowledge layer.

Verifies that every directory on disk is referenced from the matching index
file — so search and routing find everything.

Checks performed:

    1. tier-manifest.json
       - every knowledge/<tier>/<group>/<skill>/ (with SKILL.md) is in
         tiers[tier].knowledge_paths
       - every playbooks/<tier>/<slug>/ is in tiers[tier].playbook_paths
       - manifest entries that no longer exist on disk

    2. workflows/catalog.json
       - every workflows/<wf>/ (except adapters/) is in workflows{}
       - every catalog entry has a matching folder

    3. playbooks/<tier>/AGENTS.md
       - mentions every group subfolder under that tier

    4. knowledge/<tier>/<group>/<skill>/SKILL.md or CLAUDE.md
       - mentions every methodology subfolder (a subfolder containing
         methodology.xml, README.md, or AGENTS.md)

    5. structural floor
       - every KB folder has SKILL.md
       - every playbook leaf has playbook.md

Usage:
    python3 scripts/audit-index-coverage.py             # full audit
    python3 scripts/audit-index-coverage.py --strict    # exit 1 on any finding
    python3 scripts/audit-index-coverage.py --json      # machine-readable
    python3 scripts/audit-index-coverage.py --check tier-manifest

Exit codes:
    0 — clean (or non-strict)
    1 — findings under --strict
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
FAION_ROOT = SKILLS_ROOT / "faion"
KNOWLEDGE_ROOT = FAION_ROOT / "knowledge"
PLAYBOOKS_ROOT = FAION_ROOT / "playbooks"
WORKFLOWS_ROOT = FAION_ROOT / "workflows"
TIER_MANIFEST = SKILLS_ROOT / "tier-manifest.json"
WORKFLOWS_CATALOG = WORKFLOWS_ROOT / "catalog.json"

TIERS = ("free", "solo", "pro", "geek")
NON_GROUP_DIRS = {"references", "templates", "scripts", "content", "docs"}

CHECKS = ("tier-manifest", "workflows", "tier-agents", "skill-md", "structural")


@dataclass
class Finding:
    check: str
    severity: str  # error | warn
    path: str
    message: str

    def fmt(self) -> str:
        sev = "ERR " if self.severity == "error" else "WARN"
        return f"  [{sev}] {self.path} — {self.message}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, check: str, severity: str, path: str, message: str) -> None:
        self.findings.append(Finding(check, severity, path, message))

    def by_check(self) -> dict[str, list[Finding]]:
        out: dict[str, list[Finding]] = {c: [] for c in CHECKS}
        for f in self.findings:
            out.setdefault(f.check, []).append(f)
        return out

    def errors(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")

    def warnings(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warn")


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def is_methodology_folder(p: Path) -> bool:
    """A methodology folder contains methodology.xml, README.md, or AGENTS.md
    and is not a meta-folder."""
    if not p.is_dir():
        return False
    if p.name in NON_GROUP_DIRS:
        return False
    return any((p / f).is_file() for f in ("methodology.xml", "README.md", "AGENTS.md"))


def is_playbook_leaf(p: Path) -> bool:
    return p.is_dir() and (p / "playbook.md").is_file()


def is_flat_kb(group_dir: Path) -> bool:
    """A flat-shape KB has its own AGENTS.md and children are methodologies
    (containing methodology.xml). Example: knowledge/geek/sdlc-ai/."""
    if not (group_dir / "AGENTS.md").is_file():
        return False
    for child in group_dir.iterdir():
        if child.is_dir() and (child / "methodology.xml").is_file():
            return True
    return False


@dataclass
class KB:
    path: Path
    shape: str  # "router" (SKILL.md) | "flat" (AGENTS.md only)
    tier: str
    group: str  # for router KBs the group dir name; for flat KBs equals the KB name
    name: str

    @property
    def manifest_key(self) -> str:
        if self.shape == "flat" and self.group == self.name:
            return f"faion/knowledge/{self.tier}/{self.group}"
        return f"faion/knowledge/{self.tier}/{self.group}/{self.name}"


def discover_kbs() -> dict[str, list[KB]]:
    """tier -> [KB] covering both shapes (router and flat)."""
    out: dict[str, list[KB]] = {t: [] for t in TIERS}
    for tier in TIERS:
        tier_dir = KNOWLEDGE_ROOT / tier
        if not tier_dir.is_dir():
            continue
        for group_dir in sorted(tier_dir.iterdir()):
            if not group_dir.is_dir() or group_dir.name in NON_GROUP_DIRS:
                continue
            if is_flat_kb(group_dir):
                # the group folder IS the KB; methodologies sit directly under it
                out[tier].append(KB(group_dir, "flat", tier, group_dir.name, group_dir.name))
                continue
            for skill_dir in sorted(group_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue
                if (skill_dir / "SKILL.md").is_file():
                    shape = "router"
                elif (skill_dir / "AGENTS.md").is_file() and any(
                    (c / "methodology.xml").is_file() for c in skill_dir.iterdir() if c.is_dir()
                ):
                    shape = "flat"
                else:
                    shape = "router"  # default; will trigger structural error
                out[tier].append(KB(skill_dir, shape, tier, group_dir.name, skill_dir.name))
    return out


def discover_playbook_groups() -> dict[str, list[Path]]:
    """tier -> [group folder paths]."""
    out: dict[str, list[Path]] = {t: [] for t in TIERS}
    for tier in TIERS:
        tier_dir = PLAYBOOKS_ROOT / tier
        if not tier_dir.is_dir():
            continue
        for group_dir in sorted(tier_dir.iterdir()):
            if group_dir.is_dir():
                out[tier].append(group_dir)
    return out


def discover_workflow_folders() -> list[Path]:
    if not WORKFLOWS_ROOT.is_dir():
        return []
    out = []
    for d in sorted(WORKFLOWS_ROOT.iterdir()):
        if not d.is_dir() or d.name == "adapters":
            continue
        out.append(d)
    return out


# ---- check 1: tier-manifest -------------------------------------------------

def check_tier_manifest(report: Report) -> None:
    if not TIER_MANIFEST.is_file():
        report.add("tier-manifest", "error", rel(TIER_MANIFEST), "missing tier-manifest.json")
        return

    manifest = json.loads(TIER_MANIFEST.read_text())
    tiers_cfg = manifest.get("tiers", {})

    kbs_by_tier = discover_kbs()
    pg_by_tier = discover_playbook_groups()

    for tier in TIERS:
        tcfg = tiers_cfg.get(tier, {})
        declared_k = set(tcfg.get("knowledge_paths", []))
        declared_p = set(tcfg.get("playbook_paths", []))

        actual_k = {kb.manifest_key for kb in kbs_by_tier[tier]}
        actual_p = {f"faion/playbooks/{tier}/{g.name}" for g in pg_by_tier[tier]}

        for missing in sorted(actual_k - declared_k):
            report.add("tier-manifest", "error", missing,
                       f"knowledge dir not in tiers.{tier}.knowledge_paths")
        for stale in sorted(declared_k - actual_k):
            report.add("tier-manifest", "warn", stale,
                       f"manifest lists tiers.{tier}.knowledge_paths that does not exist")

        for missing in sorted(actual_p - declared_p):
            report.add("tier-manifest", "error", missing,
                       f"playbook dir not in tiers.{tier}.playbook_paths")
        for stale in sorted(declared_p - actual_p):
            report.add("tier-manifest", "warn", stale,
                       f"manifest lists tiers.{tier}.playbook_paths that does not exist")


# ---- check 2: workflows catalog --------------------------------------------

def check_workflows_catalog(report: Report) -> None:
    if not WORKFLOWS_CATALOG.is_file():
        report.add("workflows", "error", rel(WORKFLOWS_CATALOG), "missing catalog.json")
        return

    catalog = json.loads(WORKFLOWS_CATALOG.read_text())
    declared = set(catalog.get("workflows", {}).keys())
    actual = {p.name for p in discover_workflow_folders()}

    for missing in sorted(actual - declared):
        report.add("workflows", "error", f"workflows/{missing}",
                   "workflow folder not in catalog.json")
    for stale in sorted(declared - actual):
        report.add("workflows", "warn", f"catalog.json:{stale}",
                   "catalog entry has no matching folder")


# ---- check 3: tier-level playbook AGENTS.md --------------------------------

def check_tier_playbook_indexes(report: Report) -> None:
    pg_by_tier = discover_playbook_groups()
    for tier in TIERS:
        idx = PLAYBOOKS_ROOT / tier / "AGENTS.md"
        if not idx.is_file():
            report.add("tier-agents", "error", rel(idx), "missing tier AGENTS.md")
            continue
        text = idx.read_text()
        for group in pg_by_tier[tier]:
            # tolerate `name/` or `` `name` `` or backtick-wrapped, etc.
            patterns = [f"`{group.name}/`", f"`{group.name}`", f"{group.name}/"]
            if not any(p in text for p in patterns):
                report.add("tier-agents", "error",
                           f"faion/playbooks/{tier}/{group.name}",
                           f"group not mentioned in {rel(idx)}")


# ---- check 4: per-KB SKILL.md mentions methodologies -----------------------

def check_skill_md_indexes(report: Report) -> None:
    """Each KB index (SKILL.md for router, AGENTS.md for flat) must mention
    every methodology folder it contains."""
    kbs_by_tier = discover_kbs()
    for tier in TIERS:
        for kb in kbs_by_tier[tier]:
            if kb.shape == "flat":
                index_files = [kb.path / "AGENTS.md"]
            else:
                index_files = [kb.path / "SKILL.md", kb.path / "CLAUDE.md"]
            haystack_parts = []
            for cand in index_files:
                if cand.is_file():
                    haystack_parts.append(cand.read_text())
            haystack = "\n".join(haystack_parts)
            primary = next((f for f in index_files if f.is_file()), index_files[0])

            for child in sorted(kb.path.iterdir()):
                if not is_methodology_folder(child):
                    continue
                name = child.name
                patterns = [
                    f"`{name}`", f"{name}.md", f"{name}/", f"]({name}",
                    f"({name})", f" {name} ", f"\n{name}\n",
                ]
                if not any(p in haystack for p in patterns):
                    report.add("skill-md", "warn",
                               rel(child),
                               f"methodology not referenced in {rel(primary)}")


# ---- check 5: structural floor --------------------------------------------

def check_structural(report: Report) -> None:
    kbs_by_tier = discover_kbs()
    for tier in TIERS:
        for kb in kbs_by_tier[tier]:
            if kb.shape == "router":
                if not (kb.path / "SKILL.md").is_file():
                    report.add("structural", "error",
                               rel(kb.path), "KB folder missing SKILL.md (router shape)")
                if not (kb.path / "CLAUDE.md").is_file():
                    report.add("structural", "warn",
                               rel(kb.path), "KB folder missing CLAUDE.md")
            elif kb.shape == "flat":
                if not (kb.path / "AGENTS.md").is_file():
                    report.add("structural", "error",
                               rel(kb.path), "flat KB missing AGENTS.md index")

    for tier in TIERS:
        tier_dir = PLAYBOOKS_ROOT / tier
        if not tier_dir.is_dir():
            continue
        for group_dir in sorted(tier_dir.iterdir()):
            if not group_dir.is_dir():
                continue
            # every leaf under playbooks/<tier>/<group>/* should have playbook.md
            for slug_dir in sorted(group_dir.iterdir()):
                if not slug_dir.is_dir():
                    continue
                if not (slug_dir / "playbook.md").is_file():
                    report.add("structural", "error",
                               rel(slug_dir),
                               "playbook leaf missing playbook.md")

    for wf in discover_workflow_folders():
        if not (wf / "AGENTS.md").is_file():
            report.add("structural", "error",
                       rel(wf), "workflow missing AGENTS.md")


# ---- main ------------------------------------------------------------------

CHECK_FUNCS = {
    "tier-manifest": check_tier_manifest,
    "workflows": check_workflows_catalog,
    "tier-agents": check_tier_playbook_indexes,
    "skill-md": check_skill_md_indexes,
    "structural": check_structural,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", choices=CHECKS, action="append",
                    help="run only the named check(s); default = all")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any finding (error or warn)")
    ap.add_argument("--errors-only", action="store_true",
                    help="suppress warnings in human output")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = ap.parse_args()

    selected = args.check or list(CHECKS)
    report = Report()
    for c in selected:
        CHECK_FUNCS[c](report)

    if args.json:
        out = {
            "errors": report.errors(),
            "warnings": report.warnings(),
            "findings": [
                {"check": f.check, "severity": f.severity,
                 "path": f.path, "message": f.message}
                for f in report.findings
            ],
        }
        print(json.dumps(out, indent=2))
    else:
        grouped = report.by_check()
        for c in selected:
            findings = grouped.get(c, [])
            errs = [f for f in findings if f.severity == "error"]
            warns = [f for f in findings if f.severity == "warn"]
            shown = errs if args.errors_only else findings
            status = "OK" if not errs and (args.errors_only or not warns) else (
                f"{len(errs)} err, {len(warns)} warn")
            print(f"[{c}] {status}")
            for f in shown:
                print(f.fmt())
        print()
        print(f"Total: {report.errors()} errors, {report.warnings()} warnings")

    if args.strict and report.findings:
        return 1
    if report.errors():
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
