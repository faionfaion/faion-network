# Work Breakdown Structure

## Summary

**One-sentence:** Frames WBS as a deliverable-oriented scope baseline (PMI standard): noun-based hierarchical decomposition, 100% rule, 8-80 hour leaves, and a Dictionary entry per leaf — the spine from which schedule, cost, RACI, and SDD tasks derive.

**One-paragraph:** WBS is *the* scope baseline. Schedule and cost are derived from it; they are NOT contained in it. Without a deliverable-oriented WBS, scope statement → estimates → schedule decouple silently and forgotten work surfaces during execution. The 100% rule + 8-80 hour leaf rule + WBS Dictionary (included/excluded scope, acceptance criteria, owner, hours, dependencies) make the artefact actionable instead of decorative. This methodology codifies the PMI standard for project-manager workflow (sibling [[wbs-creation]] is the build-focused playbook; this one is the framing methodology consumed by RACI, schedule, EVM, and SDD task generation). Append-only IDs preserve traceability across change requests, risk entries, and tasks.

**Ефективно для:**

- Translating an approved SOW into an estimable, assignable work-package tree before scheduling.
- Bidding on fixed-scope work requiring bottom-up estimation.
- Diffing a drafted WBS against the scope statement to find gaps / overlaps (100% rule audit).
- Re-baselining after a change request — mutating only the affected branch with append-only IDs.

## Applies If (ALL must hold)

- Approved scope statement / SOW exists.
- ≥ 70% of deliverables are known well enough to enumerate.
- Change-control process exists so WBS edits route through CR.
- Version control hosts the WBS YAML + Dictionary cards.

## Skip If (ANY kills it)

- Pure Scrum / Kanban driven by a product backlog — duplicate sources of truth.
- Discovery / research projects with < 30% of scope known.
- Solo work on a feature under 2 weeks — a checklist is simpler.
- Innovation / platform exploration with emergent deliverables — use rolling-wave planning.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved SOW / scope statement | Markdown / signed PDF | sponsor |
| Glossary of deliverable terms | YAML | BA / PM |
| Anchor estimates (≥ 3 known-good) | YAML | history |
| Architecture sketch (optional) | Markdown | architect |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wbs-creation]] | Sibling — the build-focused playbook; this methodology is the framing standard. |
| [[raci-ai-assisted]] | Each WBS leaf needs exactly one accountable role; RACI consumes WBS leaves. |
| [[value-stream-management]] | Flow / DORA metrics are reported by-branch using WBS IDs as labels. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: deliverable-orientation, 100% rule, 8-80 sizing, overhead branches, append-only IDs, Dictionary required | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `WBS` + Dictionary + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: verb-default, schedule-bleed (dates in WBS), uneven depth, hallucinated owners, ID reuse after delete | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: ideate L1 → decompose → 100% check → size → Dictionary → baseline | ~800 |
| `content/05-examples.xml` | medium | One worked WBS: MVP launch, 5 L1 branches, balanced depth, Dictionary entry shown | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: node shape, overhead present, weight sum, leaf size, id collision → action + rule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wbs-decomposer` | sonnet | Light judgment on deliverable taxonomy. |
| `wbs-dictionary-writer` | sonnet | Per-leaf card with included/excluded scope + AC. |
| `100-rule-validator` | haiku | Mechanical sum check. |
| `8-80-validator` | haiku | Mechanical bound check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-template.md.j2` | Hierarchical WBS outline with PM + all mandatory branches |
| `templates/wbs-template.md` | Hierarchical WBS outline with PM + all mandatory branches Generated from `templates/wbs-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/wbs-dict-entry.md` | Single work-package Dictionary card |
| `templates/wbs-validate.py` | Helper validator (weight + 8-80) consumed by Step 6 |
| `templates/_smoke-test.json` | Minimum-viable filled `WBS` for validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-work-breakdown-structure.py` | Validate a `WBS` against the JSON Schema + invariants | Pre-commit on WBS edits |

## Related

- [[wbs-creation]]
- [[raci-ai-assisted]]
- [[value-stream-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides per node whether to: split a too-large leaf, merge a too-small leaf, reject a verb-named node, refuse renumbering on id collision, or add a missing overhead branch. Each leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/wbs-validate.py`

```python
"""Validate wbs.yaml: 100% rule (weight_pct children sum) + 8-80h leaf effort rule.

Input YAML structure:
  items:
    - id: "1"
      name: "Project Management"
      weight_pct: 15
      children:
        - id: "1.1"
          name: "Planning Documentation"
          effort_hours: 20

Usage: wbs-validate.py <wbs.yaml>
Exit 0 = valid. Exit 1 = failures found.
"""
import sys
import yaml

REQUIRED_PACKAGES = {
    "project management", "qa", "quality", "testing",
    "deployment", "documentation", "training", "transition",
}
ERR: list[str] = []


def walk(node: dict) -> None:
    children = node.get("children", [])
    if children:
        weights = [c.get("weight_pct", 0) for c in children]
        total = sum(weights)
        if abs(total - 100) > 0.5:
            ERR.append(
                f"{node['id']} '{node['name']}': children sum to {total:.1f}%, expected 100"
            )
        for child in children:
            walk(child)
    else:
        hours = node.get("effort_hours")
        if hours is None:
            ERR.append(f"{node['id']} '{node['name']}': leaf missing effort_hours")
        elif not (8 <= float(hours) <= 80):
            ERR.append(
                f"{node['id']} '{node['name']}': effort {hours}h violates 8-80 rule"
            )
        deliverable = node.get("deliverable") or node.get("acceptance_criteria")
        if not deliverable:
            ERR.append(f"{node['id']} '{node['name']}': leaf missing deliverable or acceptance_criteria")


def collect_names(node: dict, names: set) -> None:
    names.add(node["name"].lower())
    for child in node.get("children", []):
        collect_names(child, names)


def check_overhead(items: list) -> None:
    all_names: set[str] = set()
    for item in items:
        collect_names(item, all_names)
    for pkg in REQUIRED_PACKAGES:
        if not any(pkg in name for name in all_names):
            ERR.append(f"WBS: missing required overhead package '{pkg}'")


def main(path: str) -> None:
    doc = yaml.safe_load(open(path))
    items = doc.get("items", doc) if isinstance(doc, dict) else doc
    for top in items:
        walk(top)
    check_overhead(items)
    if ERR:
        for e in ERR:
            print(f"[FAIL] {e}")
        sys.exit(1)
    print("WBS valid")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wbs-validate.py <wbs.yaml>")
        sys.exit(2)
    main(sys.argv[1])
```

### `templates/_smoke-test.json`

```json
{
  "project": "smoke",
  "version": "1.0",
  "items": [
    {
      "id": "1",
      "name": "Project Management",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 12
    },
    {
      "id": "2",
      "name": "Authentication Module",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 22
    },
    {
      "id": "2.1",
      "name": "Login Endpoint",
      "level": 2,
      "kind": "work_package",
      "parent": "2",
      "weight_pct": 60
    },
    {
      "id": "2.2",
      "name": "Logout Endpoint",
      "level": 2,
      "kind": "work_package",
      "parent": "2",
      "weight_pct": 40
    },
    {
      "id": "3",
      "name": "Quality Assurance",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 18
    },
    {
      "id": "4",
      "name": "Deployment",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 14
    },
    {
      "id": "5",
      "name": "Documentation",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 12
    },
    {
      "id": "6",
      "name": "Training",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 11
    },
    {
      "id": "7",
      "name": "Transition",
      "level": 1,
      "kind": "deliverable",
      "parent": null,
      "weight_pct": 11
    }
  ],
  "dictionary": [
    {
      "id": "2.1",
      "name": "Login Endpoint",
      "description": {
        "included": "POST /login with session token",
        "excluded": "OAuth providers"
      },
      "deliverable": "Working /login endpoint + integration test",
      "acceptance_criteria": [
        "Returns 200 + token on valid creds",
        "Returns 401 on invalid"
      ],
      "owner": "Backend Team Lead",
      "effort_hours": 20,
      "dependencies": []
    },
    {
      "id": "2.2",
      "name": "Logout Endpoint",
      "description": {
        "included": "POST /logout invalidates session",
        "excluded": "Global logout across devices"
      },
      "deliverable": "Working /logout endpoint + integration test",
      "acceptance_criteria": [
        "Returns 204 on valid session",
        "Session invalidated server-side"
      ],
      "owner": "Backend Team Lead",
      "effort_hours": 12,
      "dependencies": [
        "2.1"
      ]
    }
  ]
}
```
