# Requirements Traceability

## Summary

**One-sentence:** Produces a Requirements Traceability Matrix (RTM) linking each requirement forward to design / code / test / release artefacts and backward to source elicitation.

**One-paragraph:** Produces a Requirements Traceability Matrix (RTM) linking each requirement forward to design / code / test / release artefacts and backward to source elicitation. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Audit-driven engagement (ISO/SOC2/FDA), де bidirectional traceability — обов'язково.
- Cross-team initiative, де requirement розходиться у design/code/test/release.
- Defect investigation: треба знайти який requirement був mis-implemented.
- Change-impact analysis перед великим CR — щоб порахувати ripple.

## Applies If (ALL must hold)

- Engagement under audit (ISO, SOC2, FDA, gov) requires bidirectional traceability.
- Large multi-team initiative where requirements ripple into many artefacts.
- Defect investigation needs to identify which requirement was misimplemented.
- Change-impact analysis where downstream artefacts must be located fast.

## Skip If (ANY kills it)

- Small initiative (<10 requirements) where traceability overhead > value.
- Throwaway prototype with no audit need.
- Tooling already provides traceability natively (Polarion, Jama) and an extra matrix is redundant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements register | Output of requirements-documentation | BA |
| Design artefact list | Wiki / Confluence | architects |
| Code repository | Git | engineering |
| Test plan | Output of acceptance-criteria + test management tool | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-documentation]] | source of requirement IDs |
| [[acceptance-criteria]] | AC IDs feed the test column |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-artefact-refs` | haiku | Mechanical scan of design / code / test for requirement-ID references. |
| `build-matrix` | sonnet | Assemble RTM with per-direction completeness. |
| `flag-gaps` | sonnet | Identify orphan requirements + orphan code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rtm-template.md.j2` | RTM matrix template with columns: req_id, design_ref, code_ref, test_ref, release_ref. |
| `templates/rtm-template.md` | RTM matrix template with columns: req_id, design_ref, code_ref, test_ref, release_ref. Generated from `templates/rtm-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rtm_min.py` | Stdlib RTM generator that scans repo for req-ID mentions. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[requirements-documentation]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rtm_min.py`

```python
#!/usr/bin/env python3
"""rtm_min.py — scan repo for requirement-ID mentions, emit RTM JSON."""
from __future__ import annotations
import json, pathlib, re, sys

REQ_RE = re.compile(r'\bREQ-[A-Z0-9-]+\b')

def main(root: str) -> int:
    rtm: dict[str, list[str]] = {}
    for p in pathlib.Path(root).rglob('*'):
        if not p.is_file() or p.suffix not in {'.md', '.ts', '.py', '.js'}: continue
        try: txt = p.read_text(errors='ignore')
        except Exception: continue
        for m in REQ_RE.finditer(txt):
            rtm.setdefault(m.group(0), []).append(str(p))
    print(json.dumps(rtm, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
```
