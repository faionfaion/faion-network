# Wireframing

## Summary

**One-sentence:** Produce a wireframe document (layout description + annotation table + state checklist + open questions) covering ≥3 layout variants per key screen and ALL states (default, empty, loading, error, success, permission-gated) without visual styling.

**One-paragraph:** Low-fidelity representations of UI structure, layout, and functionality without visual design details. Inputs: feature spec + content inventory + technical constraints. Output: a wireframe doc per screen (layout description + annotated element table + state checklist + open questions). Use to validate hierarchy and interaction patterns before committing to high-fi design. Hand off to a Figma session — never as the final deliverable.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Exploring layout concepts before committing to one direction.
- A feature spec + acceptance criteria exist.
- Wireframe output will be reviewed by humans before high-fi design.

## Skip If (ANY kills it)

- Need polished mockups for developer handoff — wireframes are not specs.
- Replacing collaborative sketching when team buy-in is the goal (not the artefact).
- Visual design phase — wireframes are intentionally lo-fi.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec + acceptance criteria | doc | PM |
| Content inventory (real product names, plausible data) | list | content / PM |
| Technical constraints (component library, viewport) | doc | engineering |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/prototyping` | Wireframes become clickable prototypes downstream. |
| `solo/ux/ux-ui-designer/mobile-ux` | Mobile breakpoint notes required per screen. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the wireframe doc + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: inputs → variants → annotate → states → open-questions | ~600 |
| `content/05-examples.xml` | medium | Worked example for a single screen with 3 layout variants + states | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `layout-variants` | sonnet | Generate 3+ layout options per screen. |
| `annotate-elements` | sonnet | Per-element behaviour + states table. |
| `surface-questions` | opus | Flag ambiguity / missing acceptance criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wireframe-doc.md.j2` | Wireframe document skeleton. |
| `templates/wireframe-doc.md` | Wireframe document skeleton. Generated from `templates/wireframe-doc.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/component-wireframe.md.j2` | Single-component wireframe template. |
| `templates/component-wireframe.md` | Single-component wireframe template. Generated from `templates/component-wireframe.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/prompt-wireframe.txt` | Agent prompt skeleton for wireframe generation. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wireframing.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prototyping]]
- [[mobile-ux]]
- [[recognition-over-recall]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, spec available, ≥3 variants required) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-wireframe.txt`

```text
You are a UX designer producing a low-fidelity wireframe specification.
Given the user story below, produce a wireframe document for each screen in the flow.

For each screen:

1. ASCII layout diagram
   - Use boxes and text labels only (no colors, no styling)
   - Show: header/nav, content areas, calls to action, form elements, footer
   - Keep boxes clearly labeled: [Button name], [Form field: Label], [Image placeholder], [List of items]

2. Annotation table
   - Columns: Element | Description | Behavior / Notes
   - Include: every interactive element, every content area, every conditional element
   - Be specific about behavior: "clicking X opens modal Y", not "triggers action"

3. States checklist
   - Mark which states this screen must handle: Default / Empty / Loading / Error / Success / Permission Denied
   - For each state: describe what the user sees (one sentence per state)

4. Responsive notes
   - What changes at mobile breakpoint (375px)
   - What collapses, reorders, or becomes a different component

5. Open Questions
   - Any ambiguous requirement that needs a design decision before engineering begins
   - Do not guess — flag ambiguity explicitly

Rules:
- Do not produce high-fidelity visuals or specify colors/fonts
- Do not produce clickable prototypes
- Include all error, empty, loading, and permission-denied states — not just the happy path
- Generate at least 2 layout variants for the primary screen before recommending one

USER STORY:
[paste user story here]

ACCEPTANCE CRITERIA:
[paste ACs here]
```
