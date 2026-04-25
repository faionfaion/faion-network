# Agent Integration — AI-Enhanced Design Systems

## When to use
- Design system has a solid token foundation (color, spacing, typography) and needs to scale component variants
- Documentation is perpetually out of date with implementation — agent can auto-generate from component source
- Design-to-code gap is causing inconsistency — agent can reconcile Figma tokens vs. CSS/Tailwind variables
- Team is growing and consistency enforcement needs automation beyond manual design review
- Usage analytics are missing — which components are actually adopted vs. documented?

## When NOT to use
- Design system foundation is weak or inconsistent — AI amplifies existing problems, not corrects them
- No structured token system exists — agent-generated variations will be arbitrary without a token lattice
- Component naming is inconsistent across Figma and codebase — agent will propagate the inconsistency at scale
- The product has fewer than ~30 components — automation overhead exceeds manual maintenance cost
- Team has not agreed on a single source of truth (Figma vs. code tokens) — AI tooling requires one authoritative source

## Where it fails / limitations
- AI-generated component variants often violate implicit design rules not captured in tokens (e.g., "buttons never have rounded corners in data-dense views")
- Documentation generated from code is accurate but mechanical — it lacks the "why" and usage guidance that human authors provide
- Token suggestion models are trained on generic design systems (Material, Ant) — suggestions may not fit brand personality
- AI cannot resolve conflicts between Figma design and code implementation — it will pick one source and silently ignore the other
- Pattern recognition for "inconsistencies" produces false positives when intentional variation exists (e.g., marketing vs. product UI deliberately differ)

## Agentic workflow
A Claude subagent can automate the documentation and consistency-check layers of a design system: parse component source (React/Vue/Angular), extract prop APIs, generate structured Storybook stories or MDX docs, and diff them against Figma component properties via the Figma REST API. Variant generation (new component states, responsive breakpoints) is a strong agentic use case when a style-guide prompt constrains the output. Human designers must review generated variants before merging into the system.

### Recommended subagents
- Custom design-system-doc-agent — reads component source files, extracts TypeScript prop interfaces, generates MDX documentation and Storybook stories
- `faion-sdd-executor-agent` — executes implementation tasks defined for design system feature additions

### Prompt pattern
```
You are a design system documentation engineer. Given this React component source:
<component_source>{{component_code}}</component_source>

And this design token file:
<tokens>{{token_json}}</tokens>

Generate:
1. A Storybook CSF3 story file with: default export metadata, 3 named stories (default, disabled, error state)
2. An MDX doc page: component description, props table, usage guidelines (do/don't), accessibility notes

Do not invent new prop names. Only use what exists in the source.
```

```
Audit this component library for token usage violations:
<components_list>{{component_files}}</components_list>
<token_file>{{tokens}}</token_file>

Flag any hardcoded color/spacing/font values that should be token references.
Return: [{file, line, hardcoded_value, suggested_token}]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `storybook` CLI | Build and serve component documentation | `npx storybook init` / storybook.js.org |
| `figma-export` | Export Figma design tokens to JSON/CSS | github.com/marcomontalbano/figma-to-code |
| `style-dictionary` CLI | Transform design tokens to platform-specific formats | `npm install -g style-dictionary` / amzn.github.io/style-dictionary |
| `chromatic` CLI | Visual regression testing for design system components | `npm install -g chromatic` / chromatic.com |
| `theo` | Design token transformation (Salesforce) | github.com/salesforce-ux/theo |
| `ts-morph` | TypeScript AST parser for prop extraction | github.com/dsherret/ts-morph |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma REST API | SaaS | Yes — REST API | Fetch component properties, variables, published library metadata |
| Storybook | OSS | Yes — Node.js API | Agent can write story files and trigger builds |
| Chromatic | SaaS | Yes — CLI + API | Visual diff on component changes; CI integration |
| Zeroheight | SaaS | Partial — REST API | Design system documentation portal; limited write API |
| Supernova | SaaS | Yes — REST API | Token sync Figma → code; design system governance |
| Tokens Studio (Figma) | SaaS plugin | Yes — JSON export | Token management with GitHub sync; agent can read exported JSON |
| Backlight | SaaS | Yes — REST API | Design system platform with component versioning API |

## Templates & scripts
See templates.md for token audit template and component doc schema.

Inline: token violation scanner:
```python
import re, json, sys
from pathlib import Path

HARDCODED_COLOR = re.compile(r'#[0-9a-fA-F]{3,6}|rgb\(|rgba\(|hsl\(')
HARDCODED_SPACING = re.compile(r'(?<!\w)(padding|margin|gap|width|height):\s*\d+px')

def scan_file(filepath: str, tokens: dict) -> list:
    issues = []
    with open(filepath) as f:
        for i, line in enumerate(f, 1):
            if HARDCODED_COLOR.search(line):
                issues.append({"file": filepath, "line": i, "type": "color", "content": line.strip()})
            if HARDCODED_SPACING.search(line):
                issues.append({"file": filepath, "line": i, "type": "spacing", "content": line.strip()})
    return issues

tokens = json.load(open(sys.argv[1]))
all_issues = []
for path in Path(sys.argv[2]).rglob("*.css"):
    all_issues.extend(scan_file(str(path), tokens))
print(json.dumps(all_issues[:50], indent=2))
```

## Best practices
- Establish one canonical token format (JSON/W3C Design Tokens spec) before connecting any AI tooling
- Use AI for documentation generation on a schedule (e.g., weekly CI job), not on every commit — reduces noise
- Gate AI-generated component variants behind a design review milestone; never auto-merge to system without review
- Track component adoption metrics via Storybook telemetry or import analysis — AI can then focus documentation effort on high-usage components
- Diff Figma component properties against code prop interfaces monthly; drift accumulates silently
- Include "do not use" examples in AI-generated docs — positive examples alone are insufficient

## AI-agent gotchas
- AI-generated Storybook stories often miss edge cases and error states — prompt explicitly for negative scenarios
- When an agent parses TypeScript prop interfaces, union types and complex generics are often misrepresented in generated docs
- Figma API returns component properties as they exist in Figma, which may lag behind code by weeks — timestamp both sources when diffing
- Token JSON structures vary between tools (Style Dictionary, Tokens Studio, W3C spec) — agent must know which format it is reading
- Component library CI pipelines are slow (visual regression can take 10+ minutes); agent-triggered Chromatic runs must be async with webhook callback

## References
- W3C Design Tokens Community Group spec — design-tokens.github.io/community-group
- Style Dictionary documentation — amzn.github.io/style-dictionary
- Storybook component story format (CSF3) — storybook.js.org/docs
- "Tokens Studio" GitHub sync guide — tokens.studio/docs
- Brad Frost "Atomic Design" methodology — atomicdesign.bradfrost.com
- "AI will not magically correct deficiencies" — Nathan Curtis, EightShapes
