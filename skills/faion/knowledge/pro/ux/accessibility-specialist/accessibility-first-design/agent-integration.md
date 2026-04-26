# Agent Integration — Accessibility-First Design

## When to use
- New product / new feature design — apply at wireframe + visual-design stage to avoid 70-80% of post-launch a11y debt.
- Design-system foundation work (colors, typography, focus states, spacing tokens).
- Component library being built — bake a11y into each primitive's API and stories.
- Brand refresh / theme rework — ensure new palette passes contrast at design time, not at QA.
- Onboarding new designers / dev to a project — use the checklist as standards baseline.

## When NOT to use
- Late-stage retrofit of an existing product — use `a11y-testing` to find issues, then fix systematically. This methodology is preventative.
- Pure backend / API-only product without UI.
- Highly internal expert tooling where you knowingly trade off some criteria with documented reason.
- Product targeting a single platform with platform-native components that handle a11y for you (still verify, but lighter touch).

## Where it fails / limitations
- Design-time checks (contrast, target size) catch only ~50-60% of issues; runtime issues (ARIA misuse, keyboard traps) need code-level audits.
- Designers using Figma/Sketch can't test screen-reader behavior — only previews. Real AT testing happens post-handoff.
- Touch-target rules conflict with information-density goals (data tables, pro tools); needs case-by-case judgment.
- "Inclusive design principles" are guidelines, not pass/fail; agents struggle to apply them without context.
- Progressive enhancement only works if the team commits to it; partial buy-in produces JS-only UIs that fail without scripts.

## Agentic workflow
Agents help most at handoff: convert design specs to a11y annotations (heading levels, ARIA labels, focus order, alt text drafts), check tokens (contrast, sizing) against WCAG, generate semantic HTML scaffolds from a wireframe description, audit error/empty/loading states. Agents are weak at: judging visual hierarchy, evaluating motion comfort, weighing brand-vs-a11y tradeoffs. Pipeline: design tokens → contrast/size linter → component scaffold (semantic HTML) → axe regression in Storybook.

### Recommended subagents
- `faion-sdd-executor-agent` — gate component "done" on a11y checklist conformance + Storybook axe pass.
- Token-audit subagent — given color tokens, output the full pairwise WCAG contrast matrix and flag failing pairs by usage.
- Component-scaffold subagent — given a Figma component description, produce semantic HTML + minimal ARIA skeleton.
- Annotation-writer subagent — convert Figma layer names + comments into A11y Annotation Kit format for dev handoff.
- See also: `a11y-testing`, `wcag-22-compliance`, `cognitive-inclusion-design`.

### Prompt pattern
```
Audit this design-system color token JSON. For each FG/BG pairing actually
used in components, compute the WCAG ratio and flag:
  - <4.5 for body text → FAIL.
  - <3.0 for non-text UI / focus → FAIL.
  - <7.0 if AAA target → WARN.
Return a markdown table sorted by ratio asc.
```

```
Convert this wireframe description to semantic HTML scaffold:
- Choose correct landmark elements (header/nav/main/aside/footer).
- Heading hierarchy.
- Buttons vs. links per behavior.
- Form labels with for/id.
- Required ARIA only (no overuse).
Return HTML + a list of ARIA labels for the dev to localize.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pa11y` / `pa11y-ci` | Static page scanning during dev | `npm i -g pa11y` |
| `@axe-core/cli` | Headless axe | `npm i -g @axe-core/cli` |
| `storybook-addon-a11y` | a11y panel in Storybook | https://storybook.js.org/addons/@storybook/addon-a11y |
| `eslint-plugin-jsx-a11y` | Lint JSX for a11y issues | `npm i -D eslint-plugin-jsx-a11y` |
| `axe-playwright` / `cypress-axe` / `jest-axe` | Component-level a11y assertions | `npm i -D` |
| Figma plugin: A11y Annotation Kit | Annotation handoff | https://www.figma.com/community/plugin/731310036968334777 |
| Stark (Figma/Sketch/XD) | Contrast, color blindness, focus | https://www.getstark.co |
| `tonik` / `polaris-tokens` style-dictionary | Token build with contrast checks | https://amzn.github.io/style-dictionary/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stark | SaaS / plugin | plugin only | Best design-stage tooling; team plans for handoff. |
| Figma + a11y plugins (A11y Annotation Kit, Contrast, Able) | plugin | manual | Use during design crit. |
| Chromatic + a11y addon | SaaS | API/CI | Visual regression + a11y per Storybook story. |
| Token Studio (Figma) | SaaS / plugin | plugin | Manage tokens with contrast metadata. |
| Specify / zeroheight | SaaS | API | Design-system docs with a11y notes per component. |
| Material Design / Apple HIG / Fluent | docs | n/a | Use as platform-native baselines. |
| Microsoft Inclusive Design Toolkit | docs | n/a | Persona spectrum exercises. |

## Templates & scripts
See README design checklist. Inline contrast-matrix generator from style-dictionary tokens:

```python
#!/usr/bin/env python3
# contrast_matrix.py tokens.json
import json, sys
def lum(hex_):
    h = hex_.lstrip("#"); r,g,b = (int(h[i:i+2],16)/255 for i in (0,2,4))
    def f(c): return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    la,lb = sorted([lum(a),lum(b)])
    return (lb+0.05)/(la+0.05)
tokens = {k:v for k,v in json.load(open(sys.argv[1])).items() if v.startswith("#")}
print("| FG | BG | Ratio | AA-text | AA-UI |")
print("|----|----|-------|---------|-------|")
for f, fc in tokens.items():
    for b, bc in tokens.items():
        if f == b: continue
        r = ratio(fc, bc)
        if r >= 3:
            print(f"| {f} | {b} | {r:.2f} | {'OK' if r>=4.5 else 'FAIL'} | {'OK' if r>=3 else 'FAIL'} |")
```

## Best practices
- Bake contrast checks into the design-system token build pipeline; fail CI when a token pair drops below threshold for its declared use.
- Write a11y acceptance criteria into every component spec (focus states, keyboard, ARIA, touch target).
- Use semantic HTML first; reach for ARIA only when no native equivalent exists. Rule: "no ARIA is better than bad ARIA".
- Define focus order in design (numbered overlay) before dev handoff.
- Annotate every image at design time — alt text either inline or "decorative" tag.
- Touch targets: 24×24 px is WCAG 2.2 minimum; 44×44 px is platform recommendation. Use 44 for all primary actions.
- Run `eslint-plugin-jsx-a11y` + Storybook a11y addon as merge-blocking CI.
- Pair with `cognitive-inclusion-design` when designing forms, errors, and learning content.

## AI-agent gotchas
- Agents over-add ARIA roles ("role=button" on actual `<button>`); enforce "no ARIA when native exists" rule in prompts.
- LLM-generated alt text invents content for unfamiliar imagery — supply caption/context or require human approval for non-decorative images.
- Heading-hierarchy guesses miss visual context (an H1-styled subtitle is not an H1) — require designer-confirmed heading structure as input.
- Agent skip-link suggestions can collide with framework routers (anchor + SPA route); ensure preventDefault + focus management.
- Color suggestions to "fix contrast" can break brand palette; agents should propose tonal scale extensions, not arbitrary hex changes.
- Auto-applied `prefers-reduced-motion` can hide essential CSS-driven loaders; provide static fallback, not just "remove animation".
- Agents tend to satisfy axe but miss focus visibility on dark themes; require visual regression with Chromatic or Percy + a11y addon.
- "Use ARIA labels everywhere" ≠ accessible; redundant labels confuse screen readers (announces twice). Agent must check pairing.

## References
- WebAIM intro to web accessibility — https://webaim.org/intro/
- W3C accessibility principles — https://www.w3.org/WAI/fundamentals/accessibility-principles/
- A11y Project checklist — https://www.a11yproject.com/checklist/
- Material Design accessibility — https://m3.material.io/foundations/accessible-design/overview
- Apple HIG accessibility — https://developer.apple.com/design/human-interface-guidelines/accessibility
- WCAG 2.2 quick reference — https://www.w3.org/WAI/WCAG22/quickref/
- Inclusive Design Principles (Heydon Pickering et al.) — https://inclusivedesignprinciples.org
- "No ARIA is better than bad ARIA" — https://www.w3.org/TR/using-aria/#rule1
