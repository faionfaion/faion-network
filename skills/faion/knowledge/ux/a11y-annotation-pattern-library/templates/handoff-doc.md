<!-- purpose: Dev-handoff doc structure resolving each annotation to verbatim contract -->
<!-- consumes: annotated design file + library snippets -->
<!-- produces: dev-readable handoff-doc.md -->
<!-- depends-on: templates/annotation-snippet-library.md -->
<!-- token-budget-impact: ~800 per screen -->


# Handoff — <screen name>

For each interactive component, paste the resolved annotation block.

## <component name>
- archetype: <one of 8>
- role: <ARIA role>
- name: <user-facing label>
- states: <comma-separated>
- keyboard: <key → action map>
- focus_behaviour: <description>
- WCAG SC: <2.4.3 | 4.1.2 | ...>

Focus order across the screen (numbered): 1, 2, 3 ...
