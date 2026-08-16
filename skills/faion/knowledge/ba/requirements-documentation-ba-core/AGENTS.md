# Requirements Documentation

## Summary

**One-sentence:** Produces SRS / BRD / user-story documents conforming to a checked schema, with traceability IDs, acceptance criteria, and review state per requirement.

**One-paragraph:** Produces SRS / BRD / user-story documents conforming to a checked schema, with traceability IDs, acceptance criteria, and review state per requirement. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Regulated industry (fintech, health, gov), де треба SRS під аудит.
- Cross-team handoff: design → dev → QA → ops, де verbal context втрачається.
- Onboarding нових BA/QA — треба стабільний документ замість Slack-археології.
- Contractual SOW, де requirement-набір — частина юридичного зобов'язання.

## Applies If (ALL must hold)

- Engagement requires formal documentation (audit, regulated industry, contractual SOW).
- Multiple downstream consumers (design, dev, QA, ops) need a single source of truth.
- Cross-team handoff where verbal context will be lost.
- Onboarding new team members who need a stable requirements artefact.

## Skip If (ANY kills it)

- Single-developer prototype where the developer is also the BA.
- Pure backlog-driven Scrum where user stories live in Jira and never become an SRS.
- Throwaway experiment with no audit need.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements list | Output of elicitation / data-driven-requirements | BA |
| Traceability schema | Markdown / template | BA team |
| Acceptance criteria template | From acceptance-criteria methodology | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[acceptance-criteria]] | every requirement carries AC |
| [[requirements-traceability]] | requirement IDs feed RTM |

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
| `structure-srs` | haiku | Mechanical sectioning per IEEE 830 template. |
| `write-requirement-bodies` | sonnet | Light judgement on phrasing + completeness. |
| `validate-schema` | haiku | Run validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/brd-template.md` | Business Requirements Document skeleton. |
| `templates/srs-template.md.j2` | IEEE 830-aligned SRS skeleton. |
| `templates/srs-template.md` | IEEE 830-aligned SRS skeleton. Generated from `templates/srs-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/user-story-template.md.j2` | INVEST-compliant user story template with AC slot. |
| `templates/user-story-template.md` | INVEST-compliant user story template with AC slot. Generated from `templates/user-story-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/srs-conformance.yaml` | YAML schema enforced by validator. |
| `templates/srs_conform.py` | Conformance checker that fails CI when SRS source violates the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[acceptance-criteria]]
- [[requirements-traceability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/srs-conformance.yaml`

```yaml
schema:
  required:
    - doc_type
    - requirements
    - review_state
  requirements_item_required:
    - req_id
    - statement
    - acceptance_criteria
    - status
```

### `templates/srs_conform.py`

```python
"""srs_conform.py — fail CI if SRS source violates the conformance schema.
Usage: python srs_conform.py path/to/srs.md [schema.yaml]
Exit 0 = pass. Exit 1 = violations found.
"""
import re, sys, yaml
from pathlib import Path

schema_path = sys.argv[2] if len(sys.argv) > 2 else "srs-conformance.yaml"
schema = yaml.safe_load(Path(schema_path).read_text())
src = Path(sys.argv[1])
text = src.read_text()
errs: list[str] = []

for s in schema["mandatory_sections"]:
    if s not in text:
        errs.append(f"missing section: {s}")

fm_match = re.search(r"^---\n(.*?)\n---", text, re.S)
fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}
for k in schema["mandatory_frontmatter"]:
    if k not in fm:
        errs.append(f"missing frontmatter: {k}")

req_pat = re.compile(schema["requirement_rules"]["id_pattern"])
for line in text.splitlines():
    m = re.match(r"^\s*\*\*((BR|UR|FR|NFR)-\d{3})\*\*", line)
    if m and not req_pat.match(m.group(1)):
        errs.append(f"bad id format: {m.group(1)}")

for w in schema["requirement_rules"]["forbidden_words"]:
    for n, ln in enumerate(text.splitlines(), 1):
        if re.search(rf"\b{w}\b", ln, re.I):
            errs.append(f"line {n}: forbidden word '{w}'")

if schema["requirement_rules"]["shall_only"]:
    for n, ln in enumerate(text.splitlines(), 1):
        if re.search(r"\b(should|may|might)\b", ln, re.I):
            errs.append(f"line {n}: non-shall modal in '{ln.strip()[:60]}'")

if errs:
    sys.stderr.write("\n".join(errs) + "\n")
    sys.exit(1)
print(f"OK — {src} passes conformance schema")
```
