# Prototyping

## Summary

**One-sentence:** Produce a prototype plan tying a chosen fidelity (paper / clickable / high-fi / code) to stated learning objectives, plus a usability test script with 3-5 scenario-based tasks.

**One-paragraph:** Interactive product representation before code. Inputs: design brief + open questions. Output: a prototype plan stating learning objectives, the chosen fidelity, what is and is NOT prototyped, the test script with 3-5 scenario-based tasks, and the decision rule for moving to development. Fidelity is chosen by learning goal, not by time available.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A risky design assumption needs validation before development starts.
- Stakeholders disagree on how a flow should work, not just how it looks.
- The team has 3+ open questions about user behaviour it cannot answer from data.

## Skip If (ANY kills it)

- No clear testing hypothesis exists — prototyping without learning goals wastes cycles.
- Post-launch optimisation where A/B testing or analytics provide faster signal at lower cost.
- The flow already ships and quantitative product analytics (heatmaps, funnel data) are available.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Design brief | doc | PM / UX |
| Open questions list | bullets | UX |
| Available recruitment pool | list | UX / ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/wireframing` | Wireframes are the upstream input for low-fi prototypes. |
| `solo/ux/ux-ui-designer/usability-testing` | The test script is consumed by usability-testing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the prototype-plan + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: objectives → fidelity → scope → build → script | ~600 |
| `content/05-examples.xml` | medium | Worked example: clickable prototype for onboarding flow | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-plan` | sonnet | Compose objectives + fidelity + scope. |
| `write-test-script` | sonnet | Compose scenario-based tasks. |
| `review-leading-questions` | opus | Detect leading phrasing before tasks go to participants. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prototype-plan.md.j2` | Prototype plan skeleton. |
| `templates/prototype-plan.md` | Prototype plan skeleton. Generated from `templates/prototype-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/testing-notes.md.j2` | Session notes template. |
| `templates/testing-notes.md` | Session notes template. Generated from `templates/testing-notes.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/scaffold-prototype.sh` | CLI scaffold for a code prototype repo. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prototyping.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[wireframing]]
- [[usability-testing]]
- [[user-interviews]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, hypothesis present, recruitment reachable) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/scaffold-prototype.sh`

```bash
#
# scaffold-prototype.sh — create a minimal HTML click-through prototype
# Usage: bash scaffold-prototype.sh <feature-name> <num-screens>
# Example: bash scaffold-prototype.sh checkout 5
FEATURE="${1:?Usage: $0 <feature-name> <num-screens>}"
NUM="${2:-3}"
mkdir -p "prototype-${FEATURE}"
for i in $(seq 1 "$NUM"); do
  cat > "prototype-${FEATURE}/screen${i}.html" <<HTML
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>${FEATURE} — Screen ${i}</title>
<style>body{font-family:sans-serif;max-width:375px;margin:auto;padding:1rem}</style>
</head>
<body>
<p><strong>Screen ${i}</strong> — replace with design</p>
$([ "$i" -lt "$NUM" ] && echo "<a href='screen$((i+1)).html'>Next &rarr;</a>")
$([ "$i" -gt 1 ] && echo "<a href='screen$((i-1)).html'>&larr; Back</a>")
</body></html>
HTML
done
echo "Prototype scaffolded: prototype-${FEATURE}/ with ${NUM} screens"
echo "Serve with: npx http-server prototype-${FEATURE}/"
```
