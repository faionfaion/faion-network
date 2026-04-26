# Recognition Rather Than Recall

## Summary

Nielsen Heuristic #6: minimize memory load by making options, actions, and context visible
rather than requiring users to remember them. Users should recognize what to do from
visible cues rather than recall it from memory. Apply when auditing UIs, reviewing
component specs, or designing multi-step flows.

## Why

Recognition requires seeing and choosing; recall requires remembering without a cue.
Recognition is faster, more accurate, and available to all user populations including
occasional users, older users, and users with cognitive disabilities. Every recall burden
adds cognitive load that increases errors, slows task completion, and reduces adoption.

## When To Use

- Auditing an existing UI for hidden options, icon-only toolbars, or multi-step flows with no context carry-over
- Reviewing wireframes or component specs for places where users must remember prior screen content
- Designing search, navigation, or command interfaces — autocomplete and recents are high-ROI here
- Reviewing AI chat or developer-tool UIs for missing help text, suggestions, or history

## When NOT To Use

- Power-user tools where recall is intentional (vim, SQL terminals, CAD shortcuts) — violating recall norms breaks expert efficiency
- Micro-optimization on a product not past alpha — this heuristic is for refining, not architecting
- When the interface is already fully recognition-based and validated — audit adds no value

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Recognition vs. recall distinction; four design principles; cognitive load mechanism |
| `content/02-patterns.xml` | Implementation patterns: visible options, contextual info, recognition aids, autocomplete, recent items |
| `content/03-examples.xml` | Good examples (Google Search, Spotify, VS Code); bad examples (codes, hidden features, no context) |

## Templates

| File | Purpose |
|------|---------|
| `templates/recognition-audit.md` | Audit table: task, recall required, recognition alternative, priority |
| `templates/prompt-audit.txt` | LLM prompt for auditing a screen description against this heuristic |
