<!--
purpose: Postmortem template referencing one taxonomy mode id.
consumes: incident facts + taxonomy.json
produces: postmortem doc with mode id + mitigation reference
depends-on: content/01-core-rules.xml r5
token-budget-impact: docs-only
-->
# Incident — {{title}}

- date: {{YYYY-MM-DD}}
- owner: {{name}}
- severity: {{low|medium|high|critical}}
- failure_mode_id: {{fm.x.y}}   <!-- must match taxonomy.json -->
- linked_methodology: {{slug}}   <!-- copied from taxonomy entry -->

## Timeline

- T+0   detector fired
- T+xx  triage start
- T+yy  mitigation applied
- T+zz  closed

## Root cause

(1-2 paragraphs)

## Mitigation

(1 paragraph; reference linked_methodology)

## Follow-ups

- [ ] eval case added
- [ ] runbook updated
- [ ] dashboard alert tuned
