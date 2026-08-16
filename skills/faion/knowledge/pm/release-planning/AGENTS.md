# Release Planning

## Summary

**One-sentence:** Cross-team release bundling, scheduling, and communication discipline (release-train cadence, readiness matrix, deprecation comms, change-control artefacts) for paying-customer products.

**One-paragraph:** Fixed-cadence release train (weekly/biweekly/monthly), T-7d readiness matrix per function (eng/QA/support/sales/marketing/legal), >=90-day deprecation comms with customer-facing notes, named post-release monitor with rollback triggers. Output: release-plan markdown + readiness matrix + release notes.

**Ефективно для:**

- Multi-team release крізь engineering, support, sales-enablement, marketing, legal.
- Releases з paying customers, де breaking changes/deprecations присутні.
- Release calendar slipped двічі поспіль — shrink contents, скоротити cycle.
- Regulated/contractual deploy windows із customer-facing change-control артефактами.

## Applies If (ALL must hold)

- Multi-team release crossing engineering, support, sales-enablement, marketing, and legal.
- Releases with paying customers where breaking changes or deprecations are present.
- Release calendar has slipped twice in a row.
- Regulated or contractual deploy windows require customer-facing change-control artifacts.
- Release-train cadence reviews where the PM owns whether the train left full or empty.

## Skip If (ANY kills it)

- Internal tooling without external customers.
- Pre-PMF product shipping daily without deprecation surface.
- One-shot launches — use launch-readiness-review.
- Single-team product where coordination overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release calendar | schedule | PM / release ops |
| Cross-function owner roster | table | org chart |
| Customer notification list | CRM segment | marketing / CS |
| Change-control template | doc | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[launch-readiness-review]] | Provides per-release gate framework the readiness matrix mirrors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: fixed cadence, readiness matrix, 90-day deprecation, customer-facing notes, post-release monitor | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for release-plan | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: ad-hoc dates, hidden readiness, short-deprecation, commit-log-notes | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: cadence -> matrix -> deprecation comms -> notes -> monitor | 900 |
| `content/05-examples.xml` | medium | Worked release plan with deprecation + post-release monitor | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on external customers + multi-team + breaking changes | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `readiness-matrix-author` | sonnet | Pull status from owners + assemble matrix. |
| `release-notes-customer-render` | sonnet | Convert commit log into customer-facing notes. |
| `post-release-monitor-plan` | haiku | Templated monitor + rollback assignment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-plan.md.j2` | Release plan skeleton with cadence + matrix + deprecations. |
| `templates/release-plan.md` | Release plan skeleton with cadence + matrix + deprecations. Generated from `templates/release-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/release-notes.md.j2` | Customer-facing release notes template. |
| `templates/release-notes.md` | Customer-facing release notes template. Generated from `templates/release-notes.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/release_readiness_lint.py` | Lint script for readiness matrix completeness. |
| `templates/prompt-manifest-generation.txt` | Prompt template for change-control manifest. |
| `templates/prompt-readiness-matrix.txt` | Prompt template for matrix synthesis. |
| `templates/prompt-release-notes.txt` | Prompt template for customer-facing notes. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-release-planning.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[launch-readiness-review]]
- [[stakeholder-management]]
- [[product-explainability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/release_readiness_lint.py`

```python
"""

#!/usr/bin/env python3
"""
release_readiness_lint.py — fail CI if any "green" row lacks an evidence link.

Input:  release-readiness.md (table with columns: function, artifact, owner, status, evidence_link)
Usage:  python release_readiness_lint.py release-readiness.md
Exit:   0 = clean, 1 = at least one violation (suitable for pre-merge hook).
"""
import re, sys, pathlib

p = pathlib.Path(sys.argv[1])
lines = p.read_text(encoding="utf-8").splitlines()
rows = [ln for ln in lines if ln.startswith("|") and "---" not in ln]
if len(rows) < 2:
    sys.exit("readiness matrix has no rows")

hdr = [c.strip().lower() for c in rows[0].strip("|").split("|")]
need = {"function", "artifact", "owner", "status", "evidence_link"}
missing = need - set(hdr)
if missing:
    sys.exit(f"missing required columns: {missing}")

idx = {c: hdr.index(c) for c in need}
url_re = re.compile(r"https?://\S+")
violations = []

for ln in rows[1:]:
    cells = [c.strip() for c in ln.strip("|").split("|")]
    if len(cells) < len(hdr):
        continue
    status = cells[idx["status"]].lower()
    evidence = cells[idx["evidence_link"]]
    fn = cells[idx["function"]]
    art = cells[idx["artifact"]]
    if status == "green" and not url_re.search(evidence):
        violations.append(f"GREEN without evidence URL: {fn} / {art}")
    if status in ("yellow", "red") and not cells[idx["owner"]]:
        violations.append(f"{status.upper()} without named owner: {fn} / {art}")

if violations:
    print("\n".join(violations))
    sys.exit(1)
print(f"OK: {len(rows) - 1} rows, all green cells have evidence")
```

### `templates/prompt-manifest-generation.txt`

```text
You are a release-planning agent. Read the project tracker via API/CLI for
items where status="ready-for-release" AND fixVersion="vX.Y.Z". Cross-check:
  - CI green for the target branch (last 24h)
  - All linked PRs merged
  - definition-of-done checklist complete (cite the DoD doc path)
  - Migrations have a rollback script committed

For each item, output:
  ticket_id, title, owner, risk (L/M/H + 1-line rationale),
  customer_visible (Y/N), breaking_change (Y/N), feature_flag (name or "none").

Emit a manifest.md table. Flag any item that fails any check as BLOCKED
with the missing condition. Do NOT auto-remove blocked items; the PM decides.

Hard rules:
  - Do NOT invent tickets not in the tracker query result.
  - breaking_change must be human-asserted, not inferred from PR title alone.
  - Regenerate at T-1 day from the same source; never reuse a T-3 manifest.
```

### `templates/prompt-readiness-matrix.txt`

```text
Read manifest.md and the team-roster doc. For each customer_visible=Y item,
build a readiness row with columns:
  function (eng | docs | support | marketing | legal | sales-enablement | infra)
  artifact (specific deliverable, not "ready")
  owner (named person)
  status (green | yellow | red | n/a)
  evidence_link (URL to the doc/PR/ticket proving green; required for green)

Yellow/red rows must include a blocker and expected-resolution-date.
Output to release-readiness.md. Refuse to mark green without an evidence_link.

Hard rules:
  - Never write "done" or "complete" in the artifact column; name the specific deliverable.
  - If the team roster has no owner for a function, mark status=red with blocker="owner undefined".
  - Do not skip any of the 7 functions even if n/a — make the n/a explicit.
```

### `templates/prompt-release-notes.txt`

```text
Read manifest.md and the merged-PR descriptions. Draft customer-facing
release notes in this exact structure:
  # vX.Y.Z (YYYY-MM-DD)
  ## Highlights         (1-2 sentences, plain English, no marketing adjectives)
  ## New                (bullet per feature, what + why-it-matters, no codenames)
  ## Improved           (bullet per change, observable user impact)
  ## Fixed              (bullet per fix, link to public issue if any)
  ## Breaking changes   (with migration steps, not just a warning)
  ## Known issues       (be honest; workarounds where possible)
  ## Deprecations       (timeline + replacement)

Hard rules:
  - No "excited" / "delighted" / "thrilled" / "powerful" / "seamless" / "next-gen" / "revolutionary".
  - No internal codenames without a one-line gloss.
  - If a section has no content, omit the header entirely (do not write "None").
  - Cite the merge SHA per bullet in an HTML comment for traceability: <!-- sha:abc1234 -->
  - Output a draft for human review. Do not publish.
  - Known issues section is required if any issues are known. Its absence when issues exist is a policy violation.
```
