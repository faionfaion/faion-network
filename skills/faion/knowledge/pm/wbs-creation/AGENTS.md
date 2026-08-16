# WBS Creation

## Summary

**One-sentence:** Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule (nouns not verbs), 8-80 hour leaf sizing, and a per-leaf WBS Dictionary with explicit acceptance criteria.

**One-paragraph:** Without a WBS, scope is ambiguous: estimates are guesses, dependencies are invisible, and forgotten work surfaces too late to recover. The 100% rule forces completeness — if all children are done, the parent is done. Deliverable orientation (nouns not verbs) keeps the tree stable when implementation decisions change. This methodology codifies the discipline: noun-only nodes, mandatory overhead branches (PM/QA/Deployment/Documentation/Training/Transition — typically 15-25% of effort), 8-80 hour leaves, append-only IDs (CR/risk/task references survive renumbering), and a Dictionary entry per leaf carrying scope-included/excluded, deliverable, acceptance criteria, owner, hours, and dependencies. Two-pass agentic workflow: ideate Level-1 → decompose each branch → Dictionary entries; human review mandatory between passes.

**Ефективно для:**

- Predictive / waterfall projects with fixed scope (agency contracts, ERP rollouts, hardware launches).
- Hybrid: WBS at program level, sprints underneath each work package.
- Cost-loaded schedules and EVM tracking — WBS is the spine for cost accounts.
- Compliance projects (SOC2, HIPAA, ISO 27001) where the 100% rule maps to control coverage.

## Applies If (ALL must hold)

- Project has a signed scope statement or SOW.
- Deliverables are known well enough that ≥ 70% of scope can be enumerated.
- A change-control process exists so WBS edits route through CR, not chat.
- Team uses version control where the WBS YAML and Dictionary cards live.

## Skip If (ANY kills it)

- Pure-agile teams driven by a product backlog — WBS calcifies what should flex.
- Discovery / R&D where deliverables are emergent — use hypothesis backlog instead.
- Fast-moving startup product work where scope changes weekly — overhead exceeds value.
- Solo work on a feature under 2 weeks — a checklist beats a WBS.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved scope statement | Markdown / signed PDF | sponsor |
| Glossary of deliverable terms | YAML | BA or PM |
| Anchor estimates (≥ 3 known-good) | YAML | history / SME |
| Architecture sketch (optional) | Markdown | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[work-breakdown-structure]] | Sibling methodology; this one is the "build" focus, the sibling is the broader frame. |
| [[raci-ai-assisted]] | Each leaf needs exactly one accountable (A) role — RACI maps onto WBS leaves. |
| [[team-development]] | Skills-matrix feeds the owner-role field per leaf. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: deliverable-orientation (nouns), 100% rule, 8-80 sizing, overhead branches, append-only IDs, WBS Dictionary mandatory | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `WBS` + Dictionary entry + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: verb-default, uneven depth, hallucinated owners/dates, consolidation to fit count, ID reuse after delete | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: ideate L1 → decompose → 100%-check → size → Dictionary → validate | ~800 |
| `content/05-examples.xml` | medium | One worked WBS: e-commerce MVP, 5 branches, 12 leaves, balanced depth, full Dictionary entry for one leaf | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: scope known? size? overhead present? depth balanced? → action + rule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wbs-decomposer` | sonnet | Light judgment on deliverable taxonomy. |
| `wbs-dictionary-writer` | sonnet | Per-leaf card with judgment on AC + exclusions. |
| `validate-100-rule` | haiku | Mechanical sum-of-children check. |
| `validate-8-80-sizing` | haiku | Mechanical bound check on leaves. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-outline.md.j2` | Hierarchical WBS outline skeleton with numbered levels |
| `templates/wbs-outline.md` | Hierarchical WBS outline skeleton with numbered levels Generated from `templates/wbs-outline.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/wbs-dictionary-entry.md.j2` | Single work-package Dictionary card with all required fields |
| `templates/wbs-dictionary-entry.md` | Single work-package Dictionary card with all required fields Generated from `templates/wbs-dictionary-entry.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/wbs-validate.py` | Helper used by Step 6 to validate weight + 8-80 against wbs.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable filled `WBS` for validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wbs-creation.py` | Validate a `WBS` against the JSON Schema + 100% rule + 8-80 leaves | Pre-commit on WBS edits |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[work-breakdown-structure]]
- [[raci-ai-assisted]]
- [[team-development]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides when to: (a) split a leaf for 8-80, (b) merge a too-small leaf, (c) reject a verb-named node, (d) add a missing overhead branch, or (e) refuse to renumber. Every leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/wbs-validate.py`

```python
"""Validate wbs.yaml: 100% rule (weight_pct children sum) + 8-80h leaf rule.

Input YAML structure:
  items:
    - id: "1"
      name: "Project Management"
      weight_pct: 15
      children:
        - id: "1.1"
          name: "Planning Documentation"
          effort_hours: 20
"""
import sys
import yaml

REQUIRED_PACKAGES = {
    "project management", "qa", "quality", "deployment",
    "documentation", "training", "transition",
}
ERR = []


def walk(node):
    children = node.get("children", [])
    if children:
        weights = [c.get("weight_pct", 0) for c in children]
        total = sum(weights)
        if abs(total - 100) > 0.5:
            ERR.append(
                f"{node['id']} '{node['name']}': children sum to {total}%, expected 100"
            )
        for child in children:
            walk(child)
    else:
        hours = node.get("effort_hours")
        if hours is None:
            ERR.append(f"{node['id']} '{node['name']}': leaf missing effort_hours")
        elif not (8 <= hours <= 80):
            ERR.append(
                f"{node['id']} '{node['name']}': effort {hours}h violates 8-80 rule"
            )


def check_overhead(nodes):
    all_names = set()

    def collect(n):
        all_names.add(n["name"].lower())
        for c in n.get("children", []):
            collect(c)

    for n in nodes:
        collect(n)

    for pkg in REQUIRED_PACKAGES:
        if not any(pkg in name for name in all_names):
            ERR.append(f"WBS: missing required overhead package '{pkg}'")


def main(path):
    doc = yaml.safe_load(open(path))
    items = doc.get("items", doc) if isinstance(doc, dict) else doc
    for top in items:
        walk(top)
    check_overhead(items)
    if ERR:
        print("\n".join(f"[FAIL] {e}" for e in ERR))
        sys.exit(1)
    print("WBS valid")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wbs-validate.py <wbs.yaml>")
        sys.exit(2)
    main(sys.argv[1])
```

### `templates/_smoke-test.yaml`

```yaml
items:
  - id: "1"
    name: "Project Management"
    level: 1
    kind: "deliverable"
    weight_pct: 12
  - id: "2"
    name: "Authentication Module"
    level: 1
    kind: "deliverable"
    weight_pct: 22
  - id: "3"
    name: "Quality Assurance"
    level: 1
    kind: "deliverable"
    weight_pct: 18
  - id: "4"
    name: "Deployment"
    level: 1
    kind: "deliverable"
    weight_pct: 14
  - id: "5"
    name: "Documentation"
    level: 1
    kind: "deliverable"
    weight_pct: 12
  - id: "6"
    name: "Training"
    level: 1
    kind: "deliverable"
    weight_pct: 11
  - id: "7"
    name: "Transition"
    level: 1
    kind: "deliverable"
    weight_pct: 11
```
