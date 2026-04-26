# Agent Integration — Recognition Rather Than Recall

## When to use
- UI audit: reviewing an existing interface for cognitive load issues
- Design review: checking new component designs before implementation
- Accessibility review: recognition aids are disproportionately important for users with cognitive disabilities
- Command-palette or search interface design: autocomplete and suggestions are the primary recognition mechanism
- Onboarding flow design: new users have zero recall of your UI; every step must surface what to do next

## When NOT to use
- When the interface is exclusively for expert power-users who have internalized shortcuts (e.g., vim, git CLI) — recall is the design intent
- When screen real estate is genuinely constrained (e.g., mobile watch apps) — some hiding is unavoidable; add tooltips
- When adding recognition aids would create visual noise that harms scannability — balance with aesthetic simplicity

## Where it fails / limitations
- Adding too many recognition aids (labels, tooltips, recent items, suggestions) simultaneously creates visual clutter — recognition support has diminishing returns
- Autocomplete systems surfacing wrong suggestions erode trust faster than blank fields
- Recent items panels can expose sensitive data to shared-device users
- Recognition aids add implementation complexity (state management for recents, fuzzy matching for search) that teams deprioritize under time pressure
- Static checklist audits miss dynamic state transitions where recognition fails (multi-step wizard with no summary panel)

## Agentic workflow
Claude subagents can perform recognition audits against provided screenshots or component code, generating a filled Recognition Audit template with ranked issues and recommended fixes. Agents can also generate autocomplete suggestion logic or "recent items" component specs. Code-level audits (checking for `aria-label` presence, tooltip implementation, icon-only buttons) are reliable; visual judgment about whether recognition support is sufficient requires human validation.

### Recommended subagents
- `faion-usability-agent` — runs recognition audit against UI descriptions or component specs; generates issue table with severity and fix
- `faion-sdd-executor-agent` — implements recognition pattern fixes in code (adds labels, tooltips, recent items state)

### Prompt pattern
```
Audit this UI for violations of the Recognition Rather Than Recall heuristic (Nielsen #6).
For each violation:
1. Describe what the user must remember
2. Rate severity: High (blocks task) / Medium (slows task) / Low (friction only)
3. Propose a specific recognition-based alternative

UI description / component list:
{ui_description_or_code}
```

```
Generate a recent-items component specification for the following context.
Requirements:
- Show last N items (configurable)
- Each item: icon, label, timestamp
- Click restores the item's context
- Clear history option
- No PII stored in localStorage; session-scoped only

Context: {app_context}
Items represent: {item_type}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` CLI | Automated accessibility audit (detects missing labels) | `npm i -g axe-cli`; deque.com/axe |
| `pa11y` | Automated a11y scanner including label checks | `npm i -g pa11y`; pa11y.org |
| `eslint-plugin-jsx-a11y` | Linter rule: flag icon-only buttons missing aria-label | `npm i -D eslint-plugin-jsx-a11y` |
| `storybook-addon-a11y` | Per-component a11y audit in Storybook | storybook.js.org/addons/@storybook/addon-a11y |
| `playwright` | Automated UI regression + a11y assertions | playwright.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Axe DevTools | SaaS + OSS | Yes | API for automated scans in CI; flags missing labels |
| Deque WorldSpace | SaaS | Yes | Enterprise a11y management platform; API available |
| Fuse.js | OSS | Yes | Client-side fuzzy search for recognition-based filtering |
| Algolia | SaaS | Yes | Search-as-a-service with autocomplete API |
| Typesense | OSS | Yes | Self-hosted; typo-tolerant search for autocomplete |
| FullStory | SaaS | Partial | Session recordings to observe recall failures in the wild |

## Templates & scripts
See `templates.md` for Recognition Audit template.

Inline script — detect icon-only buttons in HTML (no label, no tooltip):
```python
from bs4 import BeautifulSoup

def find_recall_violations(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    violations = []

    for btn in soup.find_all(["button", "a"]):
        text = btn.get_text(strip=True)
        aria_label = btn.get("aria-label", "")
        title = btn.get("title", "")
        has_img = bool(btn.find("img") or btn.find("svg"))

        if has_img and not text and not aria_label and not title:
            violations.append({
                "element": str(btn)[:80],
                "issue": "Icon-only control: user must recall meaning",
                "severity": "High",
                "fix": "Add aria-label or visible text label",
            })

    return violations

violations = find_recall_violations(open("component.html").read())
for v in violations:
    print(v)
```

## Best practices
- Audit with icon-only buttons as your first filter — they are the most common recognition failure and easiest to fix (add `aria-label` + visible tooltip)
- Implement recent items with a maximum of 5-7 entries; more than that shifts the cognitive pattern back to recall (scanning a long list)
- Search autocomplete should show results after 2 characters, not 0 (no query) or 3+ (too slow to provide recognition)
- In multi-step forms, show a persistent summary sidebar of all prior inputs — users filling out step 4 should not need to remember what they entered on step 1
- Smart defaults (pre-filled from user history or profile) reduce recall load more effectively than helper text
- Test recognition support specifically with users who are new to the interface — expert users compensate with recall; new users expose recognition gaps

## AI-agent gotchas
- Agents auditing UI from text descriptions will miss visual recognition failures (e.g., two similar icons adjacent to each other); provide annotated screenshots or component names with their icon descriptions
- Agents implementing "recent items" tend to use `localStorage` without considering session isolation or PII implications; specify storage scope explicitly
- Autocomplete suggestions generated by agents may not account for the latency cost — specify debounce timing (typically 150-300ms) in the implementation prompt
- Recognition audit severity ratings by agents default to "Medium" for everything; require explicit criteria (High = task cannot be completed without recall)
- Human checkpoint required for visual design decisions — agents can identify technical violations but not judge whether added labels harm the aesthetic balance of the layout

## References
- Nielsen Norman Group: Recognition vs. Recall in UX — https://www.nngroup.com/articles/recognition-and-recall/
- Don Norman: *The Design of Everyday Things* (Basic Books)
- Interaction Design Foundation: Human Memory in UX — https://www.interaction-design.org/literature/article/human-memory
- axe-core GitHub: https://github.com/dequelabs/axe-core
- Fuse.js fuzzy search: https://www.fusejs.io
- Typesense OSS search: https://typesense.org
