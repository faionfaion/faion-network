# Agent Integration — Figma AI Ecosystem

## When to use
- Generating web application prototypes from a product brief using Figma Make before any engineering work begins
- Using Figma Draw to sketch vector graphics or icon concepts that a designer then refines
- Publishing a landing page or microsite directly from Figma Sites when the team has no frontend capacity
- Applying non-destructive image editing (erase, isolate, expand) to assets inside Figma without exporting to Photoshop
- Evaluating Figma's AI suite as the primary generative tool before committing to Adobe Firefly or standalone tools

## When NOT to use
- When production-quality code output is required — Figma Make outputs are prototype-grade, not deployable code
- When the design system is token-driven and complex — Figma AI tools do not reliably respect custom token systems
- When the team needs deterministic, reproducible outputs — all Figma AI features are non-deterministic
- When the design artifact must be version-controlled at the code level — Figma files are binary; Figma Sites output is not Git-tracked
- When strict WCAG compliance is required from day one — Figma AI outputs consistently miss accessibility requirements

## Where it fails / limitations
- Figma Make prototypes cannot be exported as clean, maintainable code — they are demo-quality and not suitable for handoff to engineering
- Figma Sites generates static output only; no server-side rendering, no dynamic data, no backend integration
- Figma Draw vector generation is limited to simple shapes and icons; complex illustration requires manual refinement
- AI Image Tools (erase, expand) work on raster images only; they do not understand vector layers or component structure
- None of Figma's AI features are driveable via the REST API — all require a human in the Figma UI session
- Figma Make has no versioning; iterating discards previous state unless the designer manually duplicates frames
- Output quality degrades for non-standard UI patterns (data-dense tables, custom charts, complex navigation)

## Agentic workflow
Figma's AI tools (Make, Draw, Sites, Image Tools) are all UI-only and cannot be triggered by agents via API. The practical agent integration surface is the Figma REST API for reading file structure and the Figma Webhooks API for event-driven reactions (e.g., "when a frame is updated, run an audit"). An agent can prepare a structured prompt for a human to paste into Figma Make, monitor file changes via webhooks, and post-process exported assets. For Figma Sites, an agent can audit the published URL with accessibility and performance tools post-publish. The agent role in the Figma AI ecosystem is prompt preparation, output validation, and downstream processing — not direct invocation.

### Recommended subagents
- `faion-sdd-executor-agent` — prepares a Figma Make prompt from a feature spec, logs it for human execution, then audits the result
- Custom Figma webhook listener — receives file-changed events and triggers an agent audit pass

### Prompt pattern
```
# Figma Make prompt template (paste into Figma Make UI)
Create a web application prototype for: {feature_name}

Layout requirements:
- Header with logo, nav links, and CTA button
- Hero section: headline, subheadline, primary CTA, secondary CTA
- Features grid: 3 columns, icon + title + description per card
- Footer: links, copyright

Style: {style_direction} (e.g., "clean SaaS, blue primary, Inter font")
Content: use realistic placeholder content, not Lorem Ipsum

Do NOT generate: sign-up forms, payment flows, or multi-step wizards.
```

```
# Agent: prepare and log the prompt
import pathlib, datetime

def prepare_figma_make_prompt(spec: dict) -> str:
    prompt = f"""Create a prototype for: {spec['feature_name']}
Layout: {spec['layout']}
Style: {spec['style']}
Content: realistic placeholders"""
    log_path = pathlib.Path("figma-prompts") / f"{datetime.date.today()}-{spec['slug']}.md"
    log_path.parent.mkdir(exist_ok=True)
    log_path.write_text(f"# Figma Make Prompt\n\n{prompt}\n")
    return prompt
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| figma-export (community) | Export frames/components to SVG/PNG/PDF from Figma files | github.com/lucaorio/figma-export |
| Lighthouse CLI | Audit Figma Sites published pages for performance + a11y | npm i -g lighthouse |
| axe-cli | Accessibility audit on Figma Sites published output | npm i -g axe-cli |
| playwright | E2E interaction test on Figma Sites pages | npm i -D playwright |
| webhooks.site (dev) | Receive and inspect Figma webhook payloads during development | webhooks.site |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma REST API | SaaS | Yes | Read file structure, components, styles; limited write. No AI feature access. |
| Figma Webhooks API | SaaS | Yes | Event-driven: file_update, library_publish, comment events. Trigger agent audits. |
| Figma Make | SaaS (UI-only) | No | Prompt-based prototype generation; no API or CLI. Human must operate. |
| Figma Sites | SaaS (UI-only) | No (publish) / Yes (audit) | Publish is UI-only; published URLs can be audited by agents. |
| Figma Draw | SaaS (UI-only) | No | Vector generation inside Figma canvas; no external API. |
| Builder.io | SaaS | Yes — Figma plugin + REST | Converts Figma designs to production-quality code; agent can call Builder REST API post-conversion. |
| Zeplin | SaaS | Partial — REST API | Design-to-spec platform; agents can read component specs from Zeplin API. |

## Templates & scripts
See templates.md for Figma prompt templates.

Figma Sites post-publish audit script (bash, ~25 lines):

```bash
#!/bin/bash
# Audit a Figma Sites published URL for accessibility and performance
# Usage: ./audit-figma-sites.sh https://your-figma-site.figma.site

URL="$1"
REPORT_DIR="figma-sites-audit"
mkdir -p "$REPORT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "Running Lighthouse audit on $URL..."
npx lighthouse "$URL" \
  --output json,html \
  --output-path "$REPORT_DIR/lighthouse-$TIMESTAMP" \
  --chrome-flags="--headless" \
  --only-categories=accessibility,performance,best-practices

echo "Running axe accessibility scan..."
axe "$URL" --reporter json > "$REPORT_DIR/axe-$TIMESTAMP.json"

echo "Audit complete. Reports in $REPORT_DIR/"
echo "Lighthouse: $REPORT_DIR/lighthouse-$TIMESTAMP.report.html"
echo "Axe: $REPORT_DIR/axe-$TIMESTAMP.json"
```

## Best practices
- Use Figma Make for early ideation only — define a clear checkpoint (e.g., stakeholder demo) after which the prototype is discarded and rebuilt in production code
- Prepare Figma Make prompts as structured documents (not freeform) so they can be reused, versioned, and improved across design iterations
- After using Figma Sites to publish, always run a Lighthouse + axe audit — the published output is not accessibility-validated by Figma
- Use Figma Webhooks to trigger downstream agent workflows (spec generation, audit, asset export) rather than polling the REST API
- For image operations (erase, isolate, expand), work on copies of assets — Figma AI image edits are not reversible after file save
- Separate Figma AI output frames from production design frames using a clear naming convention (e.g., `[AI Draft] Feature Name`) so they are never confused with handoff-ready work

## AI-agent gotchas
- There is no API or programmatic interface to Figma Make, Figma Draw, or Figma Sites publishing — any agent workflow that claims to "use Figma Make" requires a human at the keyboard
- Figma Webhooks send file-level events, not node-level — an agent cannot know which specific frame changed without diffing the full file before and after
- Figma REST API rate limit is 150 requests/minute per token; large file traversals for audit purposes can hit this quickly — implement backoff
- Figma file JSON can be 50–500 MB for complex files; agents must request specific node subtrees (`?ids=node_id`) rather than the full file
- Figma Make output is not stable across sessions — re-generating with the same prompt produces different results; do not treat any Figma Make output as a canonical reference
- Figma Sites published URLs do not reflect file changes until manually re-published; agents monitoring the URL may audit stale content

## References
- https://www.figma.com/ai/
- https://www.figma.com/developers/api
- https://www.figma.com/developers/webhooks
- https://www.figma.com/blog/config-2025/
- https://help.figma.com/hc/en-us/articles/figma-make
- https://www.figma.com/blog/introducing-figma-sites/
