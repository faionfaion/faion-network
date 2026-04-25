# Agent Integration — Flexibility and Efficiency of Use

## When to use
- Auditing a feature spec or UI inventory for missing keyboard shortcuts, batch operations, and power-user accelerators
- Generating a Flexibility Audit report (shortcut coverage, customization options, multi-path availability) from an action list
- Reviewing keyboard shortcut schemes for consistency with platform conventions (Mac, Windows, web)
- Identifying progressive disclosure opportunities: places where advanced options can be hidden without affecting novice users
- Code review: checking that CLI tools, APIs, and automation scripts expose the same operations as the UI (agent-accessibility parity)

## When NOT to use
- When the product serves a single narrow use case with one user type — novice/expert spectrum design is unnecessary
- Very early wireframing stages — flexibility patterns are implementation-level concerns, not concept-level
- When the bottleneck is performance or data latency, not interaction efficiency — keyboard shortcuts do not help if the action itself is slow
- For consumer mobile apps with infrequent use — most mobile app users are perpetual novices; keyboard shortcut schemes do not apply

## Where it fails / limitations
- Agent cannot test whether shortcuts are actually discoverable in a rendered interface (tooltip rendering, menu labeling) without visual access
- Shortcut conflicts with browser/OS defaults are hard to detect without live testing; agent provides pattern guidance but not conflict detection
- Customization recommendations may conflict with technical constraints in the specific framework being used
- Batch operation design requires data model knowledge that agent typically lacks without codebase context

## Agentic workflow
A Claude subagent receives an action inventory (list of user-facing operations in a product) and outputs a Flexibility Audit table: each action assessed for Shortcut coverage, Multiple path availability, Batch support, and Customizability. It cross-references against platform shortcut conventions (Mac, Windows, browser standards) and flags missing accelerators for high-frequency actions. For each gap, it generates a specific recommendation (add shortcut, add bulk select, add quick-action command palette).

### Recommended subagents
- `faion-sdd-executor-agent` — execute the audit as a structured SDD task, output to a spec document
- General Claude subagent with UX heuristics role — assess feature specs for novice/expert balance

### Prompt pattern
```
You are a UX auditor applying Nielsen's Heuristic #7 (Flexibility and Efficiency of Use).
Given the action list below, produce a Flexibility Audit table with columns:
Action | Shortcut Exists | Platform-Consistent | Discoverable | Batch Support | Alternative Paths | Recommendation

Platform conventions to check against:
- Mac: Cmd+S (save), Cmd+Z (undo), Cmd+K (command palette)
- Windows/Linux: Ctrl equivalents
- Web: no Ctrl+W (closes tab), Ctrl+F (browser find takes precedence)

For each action without a shortcut and used more than once per session, recommend a shortcut.
For each action that affects multiple items, recommend a batch variant.

Actions to audit:
[list of user-visible operations]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Playwright | Test keyboard shortcut behavior and command palette functionality | `npm install -D playwright` / https://playwright.dev |
| Hotkey detection libs (hotkeys-js) | Audit existing shortcut registrations in a React/JS codebase | `npm install hotkeys-js` / https://github.com/jaywcjlove/hotkeys |
| xdotool (Linux) | Simulate keyboard input for manual shortcut testing in GUI apps | `apt install xdotool` / https://www.semicomplete.com/projects/xdotool/ |
| eslint-plugin-jsx-a11y | Lint for missing keyboard handlers on interactive elements | `npm install -D eslint-plugin-jsx-a11y` / https://github.com/jsx-eslint/eslint-plugin-jsx-a11y |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial (REST read) | Export component tree; agent checks for shortcut label annotations and command palette components |
| VS Code extension API | OSS | Yes | Reference for keyboard shortcut registration patterns; agent can generate `keybindings.json` contribution code |
| Cmdk (cmdk.dev) | OSS | Yes | React command palette component; agent can generate implementation code from action inventory |
| kbar | OSS | Yes | Another command palette library; agent can generate kbar action definitions from a feature list |
| PostHog | OSS/SaaS | Yes (API) | Track shortcut usage vs. mouse-click ratios per action; data-driven efficiency audit |
| Heap | SaaS | No direct API | Similar usage analytics; export required |

## Templates & scripts
See `templates.md` for the Flexibility Audit template. Below is a script to extract all keyboard event listeners from a React codebase to identify existing shortcut coverage:

```bash
#!/usr/bin/env bash
# find-shortcuts.sh — find all keyboard shortcut registrations in a JS/TS codebase
# Usage: bash find-shortcuts.sh ./src
SRC="${1:-.}"

echo "=== onKeyDown handlers ==="
grep -r "onKeyDown\|onKeyUp\|onKeyPress\|addEventListener.*keydown" \
  --include="*.{js,jsx,ts,tsx}" "$SRC" \
  | grep -v node_modules \
  | grep -v ".test." \
  | sed 's/^/  /'

echo ""
echo "=== useHotkeys / hotkeys-js registrations ==="
grep -r "useHotkeys\|hotkeys(" \
  --include="*.{js,jsx,ts,tsx}" "$SRC" \
  | grep -v node_modules \
  | sed 's/^/  /'

echo ""
echo "=== Keyboard shortcut display (aria-keyshortcuts) ==="
grep -r "aria-keyshortcuts\|kbd\|shortcut" \
  --include="*.{js,jsx,ts,tsx,html}" "$SRC" \
  | grep -v node_modules \
  | sed 's/^/  /'
```

## Best practices
- Implement a command palette (Ctrl+K / Cmd+K) as the single discoverability surface for all shortcuts — it serves both novice (can discover via search) and expert (can type known shortcut) users
- Show keyboard shortcuts in menu items and tooltips; shortcuts that are not discoverable do not exist for most users
- Maintain shortcut conventions from the native platform; overriding Ctrl+W, Ctrl+N, or Ctrl+T in a web app creates severe friction
- For batch operations: always make single-item actions work first, then add multi-select + bulk action as an accelerator layer
- Progressive disclosure for settings: expose the 3-5 most-used settings immediately; put the remaining 80% behind "Advanced" — do not hide primary settings
- Measure shortcut adoption via analytics (track keyboard vs. mouse event source per action) before investing in additional shortcut work

## AI-agent gotchas
- Agent shortcut recommendations must be validated against the specific framework and browser environment; some shortcuts conflict with browser defaults that vary by OS
- Customization features recommended by agent (custom shortcuts, saved layouts) have significant implementation cost; agent does not account for build complexity when recommending them
- Human-in-loop checkpoint: power-user feature decisions affect product complexity and support burden — a PM or lead must approve before implementation
- Agent-generated command palette action lists may include internal/admin actions that should not be exposed to end users; filter the output before implementation
- Novice/expert balance recommendations are population-level judgments; agent cannot assess the actual user distribution of your specific product without usage data

## References
- https://www.nngroup.com/articles/flexibility-efficiency-heuristic/
- https://developer.apple.com/design/human-interface-guidelines/keyboards
- https://m3.material.io/foundations/navigation
- https://www.smashingmagazine.com/2021/09/keyboard-shortcuts-web-applications/
- Alan Cooper, Robert Reimann & David Cronin, *About Face: The Essentials of Interaction Design* (4th ed.)
