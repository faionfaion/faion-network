# Agent Integration — Recognition Rather Than Recall

## When to use
- Auditing an existing UI for recall burdens: hidden options, icon-only toolbars, multi-step flows with no context carry-over
- Reviewing component specs or wireframes to flag places where users must remember information from a previous screen
- Generating a recognition audit checklist tailored to a specific feature or user flow
- Evaluating command-line or developer-tool UIs where recall (command syntax) dominates — and proposing autocomplete or help text improvements
- Reviewing AI chat interfaces and form designs for missing autocomplete, recent history, or contextual hints

## When NOT to use
- Power-user tools where recall is intentional and expected (vim, SQL terminals, CAD shortcuts) — violating recall norms there breaks expert efficiency
- Micro-optimization pass on a product not yet past alpha — this heuristic is for refining, not architecting
- When the entire interface is already recognition-based and well-validated; an audit adds no value

## Where it fails / limitations
- Recognition aids (menus, autocomplete, thumbnails) consume screen real estate — agents auditing for recall will sometimes recommend additions that create visual clutter
- Fully enumerated recognition UIs (giant dropdowns, mega menus) can paradoxically increase cognitive load via choice overload; the heuristic has a ceiling
- Agents reviewing static screenshots cannot detect the most common recall failure: information that was visible on screen A but disappears on screen B
- "Context maintained across multi-step tasks" is a dynamic property requiring prototype or live product to evaluate; cannot be audited from specs alone

## Agentic workflow
A Claude agent receives a list of UI screens (as descriptions, wireframe annotations, or component specs) and applies the Recognition Audit template to each screen: identifying recall demands (what must users remember?), hidden options, icon-only elements, and missing recent-item affordances. The agent outputs a structured findings list with severity and a specific recognition alternative for each recall burden found. This audit feeds directly into a heuristic evaluation report or a design system backlog.

### Recommended subagents
- `faion-sdd-executor-agent` — maps audit findings to SDD spec ACs, flagging which acceptance criteria implicitly require recall from users

### Prompt pattern
```
You are a UX auditor applying Nielsen's Recognition Rather Than Recall heuristic.
Given the screen description below, identify:
1. Every place where users must remember information from a previous screen or step
2. Every icon or control with no visible text label
3. Every input field with no autocomplete, recent values, or suggestions
4. Every multi-step flow where prior selections are not shown in context

For each finding: describe the recall burden, rate impact (High/Medium/Low), and propose a specific recognition-based alternative.
```

```
Review this component spec. Flag any pattern that requires the user to recall information rather than recognize it.
Output as a table: Element | Recall Burden | Recognition Alternative | Priority
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-cli` | Accessibility audit that surfaces missing labels (icon-only, unlabeled inputs) | `npm i -g axe-cli` / github.com/dequelabs/axe-cli |
| `pa11y` | Automated accessibility scan — catches missing aria-label on icon buttons | `npm i -g pa11y` / pa11y.org |
| Lighthouse CLI | Audit for missing autocomplete attributes on form fields | `npm i -g lighthouse` / developers.google.com/web/tools/lighthouse |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma (Plugin API) | SaaS | Yes — REST + plugin API | Read layer names and component properties to detect icon-only instances |
| Storybook | OSS | Yes | Enforce label/tooltip story variants as part of component review |
| FullStory / Hotjar | SaaS | Partial | Session replay data shows where users pause, search, or use help — indirect recall signal |
| Dovetail | SaaS | Yes | Tag usability findings from sessions with "recall burden" label for pattern tracking |

## Templates & scripts
See `templates.md` for the Recognition Audit template.

```python
# Minimal recall burden scanner for Figma component export (JSON node tree)
# Flags icon-only Frame nodes (no visible text child, no tooltip annotation)
import json

def find_icon_only_nodes(nodes: list, depth=0) -> list:
    issues = []
    for node in nodes:
        if node.get("type") in ("FRAME", "COMPONENT", "INSTANCE"):
            has_text = any(c.get("type") == "TEXT" for c in node.get("children", []))
            has_tooltip = "tooltip" in node.get("name", "").lower()
            if not has_text and not has_tooltip:
                issues.append({"name": node["name"], "id": node["id"], "issue": "icon-only, no label or tooltip"})
        issues.extend(find_icon_only_nodes(node.get("children", []), depth+1))
    return issues
```

## Best practices
- Apply the heuristic per user segment: novice users need recognition aids everywhere; experts can tolerate more recall in power-user flows, but even then tooltips on shortcuts cost nothing
- Autocomplete on search and command inputs is the single highest-ROI recognition aid — prioritize this over visual thumbnails
- For multi-step forms: a persistent summary sidebar showing all previous answers eliminates the most common cross-screen recall burden
- Recent-items lists should show at least 5 entries and update immediately after use — a stale list is worse than no list
- When adding tooltips as a recall aid, keep them at ≤7 words and show them on hover with a 300ms delay to avoid noise

## AI-agent gotchas
- Agents auditing static wireframes will miss dynamic recall failures (information visible on step 1 gone by step 3) — note this limitation explicitly in output
- LLMs tend to flag icon-only elements aggressively, even for universally understood icons (magnifying glass for search, X for close); calibrate by providing a list of safe icon exceptions
- Recognition audit recommendations often conflict with aesthetic minimalism — agents should flag the tension but not resolve it unilaterally; human designer decides trade-off
- Agents cannot evaluate whether autocomplete suggestions are semantically useful without access to real user query data — they can only recommend the pattern, not validate the implementation

## References
- https://www.nngroup.com/articles/recognition-and-recall/
- https://www.nngroup.com/books/design-everyday-things-revised/
- https://www.interaction-design.org/literature/article/human-memory
- https://m3.material.io/foundations/navigation
- https://developer.apple.com/design/human-interface-guidelines/navigation
