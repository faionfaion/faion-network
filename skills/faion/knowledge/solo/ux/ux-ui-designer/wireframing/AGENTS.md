# Wireframing

## Summary

Low-fidelity representations of UI structure, layout, and functionality without visual
design details. Use to validate information hierarchy and interaction patterns before
committing to high-fidelity design. Produce layout descriptions, annotation tables, and
state checklists — then hand off to a Figma session, not as the final deliverable.

## Why

Jumping to high-fidelity design conflates structural problems with aesthetic ones.
Wireframes make layout and functionality cheap to debate and change. Stakeholders focus
on usability instead of color choices. Structural problems caught in wireframes cost a
fraction of what they cost in implemented code.

## When To Use

- Exploring multiple layout concepts before committing to one direction
- Generating a wireframe document (ASCII layout + annotation table + states) from a feature spec
- Reviewing a wireframe against acceptance criteria to flag missing states or interactions
- Creating component wireframe templates (card, form, modal) from a design system definition

## When NOT To Use

- Generating visual design — wireframes are intentionally lo-fi; skipping to polished mockups bypasses structural validation
- When stakeholders need pixel-precise layouts for developer handoff — wireframes are for alignment, not spec
- Replacing collaborative sketching sessions where team buy-in is the goal, not an artifact

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Five-step process: requirements → sketch → create → review → annotate; fidelity levels |
| `content/02-rules.xml` | What to include/exclude; annotation requirements; state coverage rules; responsive notes |
| `content/03-examples.xml` | Low and medium fidelity wireframe examples; common elements library; agentic workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/wireframe-doc.md` | Screen wireframe document: purpose, layout, annotation table, states, interactions, responsive notes |
| `templates/component-wireframe.md` | Component wireframe: variants, states, content guidelines, usage notes |
| `templates/prompt-wireframe.txt` | LLM prompt for generating a wireframe spec from a user story |
