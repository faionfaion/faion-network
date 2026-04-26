# Requirements Traceability

## Summary

Link requirements to their origins and to downstream artifacts using a closed set of five typed link roles (satisfies, derives, implements, verifies, conflicts). The RTM is a generated artifact from frontmatter-typed links in source files — never hand-edited. Three separate coverage gates: forward (BR → TC, target ≥ 95%), backward (TC → BR, target 100%), horizontal (conflicts/derives, target 0 cycles).

## Why

Without typed traceability, a changed business requirement causes unknown downstream impact, tests lack justification, and auditors cannot verify completeness. A generated matrix from source-typed links is immune to manual decay and gives impact-analysis in O(n) graph walks rather than manual search.

## When To Use

- Pre-audit, pre-release, or before a major refactor: needs a single defensible coverage answer
- Designing a new RTM schema from scratch: deciding which artifact types are nodes and which link roles are allowed
- Migrating from spreadsheet RTMs to requirements-as-code (frontmatter links)
- Teaching subagents what "satisfies", "derives", "verifies" mean before letting them propose links
- Lightweight projects where generated matrix from typed markdown links covers the audit surface

## When NOT To Use

- You only need tool/vendor guidance — use the sibling `business-analyst/requirements-traceability/`
- Discovery or pre-PMF: lock-in of an RTM encodes premature decisions
- One-shot prototypes, internal scripts, throwaway spikes — overhead exceeds value
- Team will not enforce link discipline — an out-of-date matrix is worse than none
- Pure SLO/SRE work where the trace artifact is a dashboard alert rule, not a requirement

## Content

| File | What's inside |
|------|---------------|
| `content/01-link-model.xml` | Five link roles, three trace directions, coverage gates, granularity rules, matrix vs graph decision |
| `content/02-agentic.xml` | Agentic workflow, subagent roles, two-shot prompt pattern, AI gotchas, mandatory human checkpoints |

## Templates

| File | Purpose |
|------|---------|
| `templates/rtm-template.md` | RTM table with coverage summary and orphan/gap sections |
| `templates/rtm_min.py` | Minimum-viable RTM generator from frontmatter links with pre-commit hook config |
