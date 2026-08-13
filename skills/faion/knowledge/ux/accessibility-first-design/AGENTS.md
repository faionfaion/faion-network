# Accessibility-First Design

## Summary

**One-sentence:** Design-phase methodology preventing 70-80% of WCAG 2.2 AA violations via token-grounded color/contrast, semantic-first components, and a11y handoff annotations baked into the design system.

**One-paragraph:** Audit-and-fix is reactive. Accessibility-first design encodes constraints into design tokens (4.5:1 body / 3:1 large / 3:1 non-text), uses semantic component archetypes (button vs link vs combobox) at the design stage, annotates role/name/state/keyboard/focus per layer, and pairs with a11y-annotation-pattern-library + design-tokens-fundamentals. Outcome: most WCAG defects never enter the codebase. Output is a design-system spec listing every token, archetype, and constraint with the SCs it prevents.

**Ефективно для:**

- Greenfield design system: запекти contrast/spacing/motion constraints у tokens.
- Solo designer без a11y-аудитора — prevention > expensive remediation.
- Bake WCAG SCs у component archetypes на етапі design, не в код.
- Reduced motion / dark mode / locale — variants з контрактом WCAG-сумісності.

## Applies If (ALL must hold)

- New design system or major component-library rework is in progress.
- Tokens, archetypes, and patterns are authored before component code.
- Product targets WCAG 2.1 AA or 2.2 AA.

## Skip If (ANY kills it)

- Legacy product mid-lifecycle — use accessibility-evaluation for remediation.
- Marketing-page one-off — heavy token system is overkill.
- Native iOS/Android with platform-provided components — use platform a11y guidance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Brand palette | hex list | brand guidelines |
| Typography scale | type ramp | design tokens |
| Component archetype inventory | list | design system |
| WCAG version target | 2.1 or 2.2 | product brief |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[design-tokens-fundamentals]] | Token architecture this methodology constrains |
| [[a11y-annotation-pattern-library]] | Annotation patterns baked into the system |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: token-encoded-contrast, semantic-first-components, focus-visible-always, reduced-motion-baked, locale-aware-direction | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for design-system a11y spec | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: brand-overrides-contrast, outline-none-globally, motion-without-reduced-motion-variant | 700 |
| `content/04-procedure.xml` | essential | 5 steps: tokens → archetypes → patterns → annotations → spec | 800 |
| `content/05-examples.xml` | essential | Worked example: button + form-field tokens + archetype spec | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: design phase → prevention vs remediation | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `token-contrast-calc` | haiku | Deterministic WCAG contrast math. |
| `archetype-mapping` | sonnet | Behaviour → archetype judgement. |
| `system-spec-draft` | sonnet | Markdown spec assembly. |

## Templates

| File | Purpose |
|------|---------|
| `templates/a11y_quick.ts` | TypeScript contrast calculator + token-pair checker |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-accessibility-first-design.py` | Validate a11y-first design-system spec JSON | Pre-commit on tokens/components changes |

## Related

- [[design-tokens-fundamentals]]
- [[a11y-annotation-pattern-library]]
- [[accessibility-evaluation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/a11y_quick.ts`

```typescript
export function relativeLuminance(hex: string): number {
  const c = hex.replace('#', '');
  const rgb = [parseInt(c.slice(0,2),16), parseInt(c.slice(2,4),16), parseInt(c.slice(4,6),16)].map(v => v/255);
  const lin = rgb.map(v => v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4));
  return 0.2126*lin[0] + 0.7152*lin[1] + 0.0722*lin[2];
}
export function contrast(fg: string, bg: string): number {
  const [l1, l2] = [relativeLuminance(fg), relativeLuminance(bg)].sort((a,b)=>b-a);
  return (l1+0.05)/(l2+0.05);
}
export function pass(fg: string, bg: string, kind: 'body'|'large'|'non-text'): boolean {
  const r = contrast(fg, bg);
  return kind === 'body' ? r >= 4.5 : r >= 3;
}
```
