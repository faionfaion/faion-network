# Agent Integration — Figma AI Ecosystem

## When to use
- Generating web app prototypes rapidly from a text brief using Figma Make
- Removing objects or expanding image backgrounds directly on the Figma canvas without export/re-import
- Publishing a static site directly from Figma via Figma Sites for early stakeholder review
- Producing vector sketch assets using Figma Draw for illustration-heavy UI components
- Auditing a team's Figma AI feature adoption and identifying workflow gaps

## When NOT to use
- Production web development — Figma Sites output is appropriate for demos and landing pages, not complex web apps
- Complex multi-state interactive prototyping requiring custom logic — Figma Make has limited conditional logic
- Brand-critical image editing where exact pixel control matters — AI image tools (Erase/Expand) are probabilistic
- Figma Draw for precise icon creation — the generative output lacks the precision of manual vector work

## Where it fails / limitations
- Figma Make prototypes do not connect to real data sources; all content is static placeholder
- Figma Sites output is not a CMS; any content change requires re-export from Figma
- AI image expansion (Expand) generates plausible but not photorealistic fill — fails on complex textures, faces, branded photography
- Figma Draw vector outputs often require significant manual cleanup for production-ready icon sets
- AI features are gated behind Figma Professional/Organization plans — free/starter teams cannot access them
- Design token integration in Figma Make is partial; variables from the Figma file are not always respected in generated prototypes

## Agentic workflow
Agents cannot invoke Figma AI tools directly (no headless API for Make, Draw, or image tools). However, agents can: (1) generate detailed prompts optimized for Figma Make input, (2) produce structured content briefs that a human pastes into Figma Make, (3) analyze Figma REST API file exports to identify which frames are candidates for AI image enhancement, and (4) generate Figma Sites publishing checklists. The human operates Figma; the agent handles pre-processing and post-processing tasks.

### Recommended subagents
- `haiku` — generating Figma Make prompts, publishing checklists, image enhancement candidate lists
- `sonnet` — full screen brief generation, design token audit from Figma JSON, Figma Sites content review

### Prompt pattern
```
Generate a Figma Make prompt for: [screen description, e.g., "SaaS dashboard — weekly analytics overview, 3 KPI cards, line chart, recent activity list"].
Design system context: [Figma file has: color tokens blue-600, gray-100; typography: Inter; component library: Cards, Charts].
Output: one concise Figma Make-ready prompt (max 150 words) optimized for design system adherence.
```

```
Review this Figma Sites page specification for: (1) missing meta tags for SEO,
(2) content that requires CMS update capability (replace with static alternatives),
(3) interactive elements not supported in static Figma Sites export.
Input spec: [paste page outline].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `figma-rest-api` (JS) | Read file structure, export frames, inspect variables | https://www.figma.com/developers/api |
| `figma-js` | Node.js wrapper for Figma REST API | npm i figma-js |
| `figma-export` | CLI batch export of Figma frames by node name | https://github.com/lucasecdb/figma-export |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma Make | SaaS | No direct API | Browser-only; agent prepares prompts, human executes |
| Figma Draw | SaaS | No API | In-canvas generative sketching; no headless access |
| Figma Sites | SaaS | No publish API | Manual publish in-app; agent can pre-validate content |
| Figma REST API v1 | SaaS | Yes | Read files, components, variables; no write for AI features |
| Figma Webhooks | SaaS | Yes | Event triggers on file change, publish — useful for post-processing |
| Adobe Firefly API | SaaS | Yes | Alternative for image generation tasks Figma AI cannot handle |

## Templates & scripts
Figma file analysis: find frames with raster images suitable for AI Expand/Erase operations:

```python
import figma_js  # hypothetical wrapper; use requests + Figma REST API in practice
import requests

FIGMA_TOKEN = "your_token"
FILE_KEY = "your_file_key"

def find_image_nodes(file_key: str) -> list[dict]:
    """Return nodes that contain raster fills — candidates for AI image tools."""
    url = f"https://api.figma.com/v1/files/{file_key}"
    resp = requests.get(url, headers={"X-Figma-Token": FIGMA_TOKEN})
    data = resp.json()

    candidates = []
    def traverse(node: dict):
        fills = node.get("fills", [])
        for fill in fills:
            if fill.get("type") == "IMAGE":
                candidates.append({
                    "id": node["id"],
                    "name": node.get("name", "unnamed"),
                    "type": node.get("type"),
                })
        for child in node.get("children", []):
            traverse(child)

    traverse(data["document"])
    return candidates

nodes = find_image_nodes(FILE_KEY)
for n in nodes:
    print(f"{n['name']} ({n['type']}) — node ID: {n['id']}")
```

## Best practices
- Use Figma Make for 10-minute prototype generation, not as a design deliverable — always rebuild final UI in proper Figma components
- When using AI image Expand for hero banners, generate 3 variations and select the best; single-run outputs are often asymmetric
- Publish Figma Sites only on a custom subdomain with clear "prototype, not production" header for stakeholder previews
- Keep Figma Draw sketches in a separate draft page — do not mix generative vector sketches with component library frames
- Audit Figma Variables before running Figma Make to ensure color/type tokens are named clearly — Make uses variable names as context

## AI-agent gotchas
- Agents will propose Figma Make API endpoints that do not exist — Make is browser-only with no public API as of 2026
- Figma Webhooks only fire on file events, not on AI feature completion — agents cannot poll for Make/Draw results
- LLM-generated Figma Make prompts often exceed the context window the in-app AI uses effectively; keep prompts under 150 words
- Figma Sites SEO limitations (no server-side rendering) are underestimated by agents; flag for any SEO-sensitive use case

## References
- https://www.figma.com/ai/ (Figma AI overview)
- https://www.figma.com/blog/config-2025/ (Config 2025 announcement)
- https://help.figma.com/hc/en-us/articles/figma-make (Figma Make docs)
- https://www.figma.com/blog/ai-image-tools/ (AI image editing)
- https://www.figma.com/blog/introducing-figma-sites/ (Figma Sites launch)
- https://www.figma.com/developers/api (Figma REST API reference)
