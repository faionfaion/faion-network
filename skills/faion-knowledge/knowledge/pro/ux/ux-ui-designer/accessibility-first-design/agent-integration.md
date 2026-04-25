# Agent Integration — Accessibility-First Design

## When to use
- Starting a new product, design system, or major redesign — preventing a11y issues at design time is 5-10x cheaper than post-launch remediation.
- Establishing design-token contrast rules and focus-state baselines for a component library.
- Onboarding new designers — the checklist is the working agreement.
- Pre-handoff QA: validating Figma frames before engineering begins, catching contrast and target-size issues at the lowest cost.

## When NOT to use
- Pure code-fix sprints where designs are frozen — code-level a11y patterns (semantic HTML, ARIA, focus management) are the right tool then.
- Marketing landing pages with one-off visual gimmicks — apply the principles but don't gate launch on full WCAG 2.2 AAA.
- When the design hasn't started — load design before checklists, otherwise you constrain ideation prematurely.

## Where it fails / limitations
- Catches roughly 70-80% of issues; the remaining 20-30% (focus order, screen-reader semantics, dynamic ARIA, keyboard traps) require code-level review.
- Contrast checks miss subtle issues: gradient backgrounds, focus rings on hover, text-over-image overlays.
- Touch-target metric (44x44) is a heuristic — actual usability depends on spacing, not size alone.
- "Color not the only indicator" rule is easy to write, hard to verify automatically — needs human or model interpretation.

## Agentic workflow
Run a Figma-plugin-driven audit before handoff: subagent A pulls frames via Figma REST API, subagent B runs contrast/target/focus checks, subagent C generates a remediation list with specific frame IDs and proposed fixes. Loop with the designer; don't merge fixes blindly. Engineering handoff includes the audit report so dev knows what's been checked and what wasn't.

### Recommended subagents
- `figma-a11y-auditor` — pulls frames + tokens, checks contrast, target sizes, focus states.
- `semantic-html-checker` — reviews dev handoff specs for `<div>`-soup vs semantic landmarks.
- `motion-and-time-checker` — flags auto-play animations, no pause control, time limits.
- `accessibility-specialist` (existing skill) — invoke for WCAG 2.2 / 3.0 deep audits.

### Prompt pattern
```
For each Figma frame, output JSON:
{ frame_id, issues: [{ rule, severity, element_id, current, required, fix_hint }] }
Rules to check: contrast (4.5:1 body, 3:1 large), target_size (>=44x44), focus_visible,
color_only, motion_pause, time_limit, semantic_handoff_present.
Severity: blocker (WCAG 2.2 AA fail) | warn | info.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` | Run a11y rules against rendered HTML | `npm i -D @axe-core/cli` |
| `pa11y` | URL-based a11y testing in CI | `npm i -g pa11y` |
| `lighthouse` | Includes a11y category, easy CI integration | `npm i -g lighthouse` |
| `figma-rest-api` clients | Pull frames/tokens for audit | https://www.figma.com/developers/api |
| `playwright` + `axe-playwright` | E2E + a11y in same run | `npm i -D @axe-core/playwright` |
| `wcag-color` (Node lib) | Contrast math beyond simple ratios (APCA, WCAG 3) | `npm i wcag-color` |
| `tota11y` (browser bookmarklet) | Visual a11y QA in browser | https://khan.github.io/tota11y/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stark (Figma plugin) | SaaS | Partial (REST limited) | Strong contrast/color-blindness sim, focus-order check. |
| Able (Figma plugin) | SaaS | Limited | Lightweight contrast checks. |
| Deque axe DevTools | SaaS + browser ext | Yes (CLI) | Most-used a11y CI tool. |
| Equal Access (IBM) | OSS | Yes | Headless a11y scanner. |
| Storybook a11y addon | OSS | Yes | Per-component runtime checks. |
| EvinceQA | SaaS | Yes (REST) | Continuous a11y monitoring. |

## Templates & scripts
Inline contrast + target-size calculator (≤45 lines).

```ts
// a11y-quick.ts
type RGB = [number, number, number];
const lum = ([r, g, b]: RGB) => {
  const f = (v: number) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
export const contrast = (a: RGB, b: RGB) => {
  const [L1, L2] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (L1 + 0.05) / (L2 + 0.05);
};
export const meets = (
  ratio: number,
  level: "AA" | "AAA",
  size: "body" | "large",
) => {
  const min = level === "AAA"
    ? size === "body" ? 7 : 4.5
    : size === "body" ? 4.5 : 3;
  return ratio >= min;
};
export const targetOk = (w: number, h: number, density = 1) =>
  w * density >= 44 && h * density >= 44;
```

## Best practices
- Embed contrast and target-size constraints in design tokens; primitives that fail standards never get exported.
- Bake focus-visible styles into base components, not opt-in — designers forget, devs inherit the lapse.
- Pair the checklist with a Figma library: every interactive component has a focus state variant. No focus variant = component not approved.
- Track a11y issues found at design vs handoff vs production. The shift-left is your KPI.
- Annotate non-visible semantics in handoff (heading levels, ARIA roles, aria-label intent) — devs recreate it inconsistently otherwise.

## AI-agent gotchas
- Models hallucinate WCAG criterion numbers (e.g. quoting "WCAG 1.4.13" when the issue is 1.4.11). Constrain to a known list and verify.
- LLM contrast estimation from screenshots is unreliable; always extract actual hex from tokens or DOM.
- "Color not the only indicator" rule needs model reasoning over UI states — it gets false positives on icons that already have labels. Provide context.
- Auto-fix proposals from agents often break visual hierarchy (darkening brand color to pass AA). Flag for designer review, don't apply.
- Human checkpoint: real screen-reader and keyboard-only tester pass on critical flows before release. Tools cannot replace this.

## References
- WCAG 2.2 standard: https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- APCA (WCAG 3 contrast model) draft: https://git.apcacontrast.com/
- Apple HIG accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Material Design accessibility: https://m3.material.io/foundations/accessible-design/overview
- Inclusive Components by Heydon Pickering: https://inclusive-components.design/
