# Agent Integration — Information Architecture

## When to use
- Generating a sitemap or content taxonomy from a product spec, feature list, or existing content inventory
- Auditing an existing IA against card sort or tree test data to identify navigation structure mismatches
- Drafting an IA strategy document from user research findings and business requirements
- Proposing navigation label alternatives when current labels test poorly with users
- Creating a taxonomy document (content types, categories, tags, naming conventions) for a new product or major redesign

## When NOT to use
- Validating a proposed IA — agents can draft structure but cannot replace card sorting and tree testing with real users for validation
- Real-time search relevance tuning — IA shapes the browse experience; search ranking is a separate discipline
- Micro-level layout decisions — IA governs content organization, not component placement or visual hierarchy within a page

## Where it fails / limitations
- Agents generating IA from a feature list will produce an internally consistent structure that may not match user mental models — always validate with card sorting or tree testing before building
- Taxonomy decisions involve business, legal, and content governance constraints that are invisible to the agent without explicit input
- Navigation depth vs. breadth trade-offs (2 levels wide vs. 4 levels deep) require user task data the agent rarely has access to; it will default to shallow and broad, which is usually right but not always
- Large-scale IA (thousands of content items) requires faceted taxonomy and search architecture that goes well beyond what a markdown sitemap can represent
- Agents will not proactively identify "orphan" content (pages with no logical parent) without a complete content inventory as input

## Agentic workflow
A Claude agent receives a product spec or feature list and produces: (1) a proposed category structure at L1 and L2, (2) a taxonomy document defining content types, attributes, and tag groups, (3) a sitemap skeleton in markdown, and (4) a validation plan recommending which card sort type and tree test scope to run. A second agent pass takes card sort results and tree test failure data and produces a revised sitemap with specific changes justified by the data.

### Recommended subagents
- `faion-sdd-executor-agent` — converts an IA strategy document into navigation-related acceptance criteria in the SDD design doc (menu structure, URL scheme, breadcrumb logic)

### Prompt pattern
```
You are an information architect. Given the product spec below, produce:
1. A navigation structure: L1 categories (4-7 max), L2 subcategories per L1 (2-5 each)
2. For each category: label, 1-sentence description, primary content types it contains
3. Global navigation items that should appear on every page
4. A validation plan: which card sort type (open/closed/hybrid), what cards to include, what tree test tasks to write

Follow these constraints:
- Labels must be in user language, not internal terminology
- No category named "Misc", "Other", or "Resources" without specific scope
- Maximum 3 levels deep
```

```
You have tree test results: for each task, which paths users took and whether they succeeded.
Identify:
- Navigation labels users consistently misidentified (took wrong path on first click >40% of the time)
- Sections where users backtracked most
- Proposed label changes for the top 3 problem areas, with rationale

Output as a IA revision report with a before/after navigation structure table.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whimsical` (web, no CLI) | Rapid sitemap creation; shareable for stakeholder review | whimsical.com |
| `mermaid-cli` | Generate sitemap diagrams from markdown definition | `npm i -g @mermaid-js/mermaid-cli` / mermaid.js.org |
| Optimal Workshop (Treejack) | Tree testing after IA is defined; exports results as CSV | optimalworkshop.com |
| `airtable` CLI / API | Manage taxonomy documents as structured data | airtable.com/developers |
| `notion` API | Store and version IA strategy documents; query via API | developers.notion.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop (Treejack) | SaaS | Yes — CSV export | Industry standard tree testing; results processed by agent for IA revision |
| Optimal Workshop (OptimalSort) | SaaS | Yes — CSV export | Card sorting to inform IA structure |
| Miro / FigJam | SaaS | Partial | Collaborative IA diagramming; limited API for reading board content |
| Airtable | SaaS | Yes — REST API | Excellent for taxonomy management; supports relational content type definitions |
| Sanity.io | SaaS/OSS | Yes — API | Headless CMS with schema-defined content types; IA encoded as code |
| Contentful | SaaS | Yes — API | Content model (IA) defined via API; good for agent-driven taxonomy changes |

## Templates & scripts
See `templates.md` for the IA Strategy Document, Sitemap Template, and Taxonomy Document.

```python
# Generate a mermaid sitemap from a structured IA definition
# Input: list of dicts {label, children: [{label, children: []}]}

def to_mermaid(nodes: list, parent: str = "root", depth: int = 0) -> list:
    lines = []
    for node in nodes:
        safe_id = node["label"].replace(" ", "_").lower()
        lines.append(f'  {parent} --> {safe_id}["{node["label"]}"]')
        if node.get("children"):
            lines.extend(to_mermaid(node["children"], safe_id, depth + 1))
    return lines

def sitemap_diagram(ia: list) -> str:
    lines = ["graph TD", '  root["Home"]']
    lines.extend(to_mermaid(ia))
    return "\n".join(lines)
```

## Best practices
- Start with user tasks, not content types — IA should be organized around what users want to do, not how your team organizes work internally
- 4-7 L1 categories is the sweet spot for top-level navigation; below 4 feels sparse, above 7 exceeds comfortable scanning range
- Validate labels with 5 users before committing to a tree test — a wrong label makes tree test data uninterpretable
- Design for growth: define rules for where new content types will go before launching, not after content starts accumulating
- Document the IA in version-controlled markdown (not only in Figma) so engineering, SEO, and content teams can reference and diff it

## AI-agent gotchas
- Agents generating sitemaps from feature lists will create IA that mirrors the feature roadmap, not the user's mental model — explicitly instruct to use user goal framing
- Navigation label generation tends toward corporate-speak ("Solutions", "Resources", "Platform") — require plain-language alternatives in the prompt
- Agents do not spontaneously account for SEO implications of URL/category structure — if SEO matters, add a constraint to the prompt ("categories should be primary keywords")
- Human sign-off required before any IA change that affects URL structure — broken URLs cause SEO damage and user-bookmarked links failing
- Tree test validation is non-optional; treating agent-generated IA as final without testing is the most common IA failure mode

## References
- https://www.nngroup.com/articles/ia-deliverables/
- https://www.optimalworkshop.com/learn/101s/tree-testing/
- https://www.interaction-design.org/literature/topics/information-architecture
- https://alistapart.com/article/thedisciplineofcontentstrategy/
- https://www.usability.gov/how-to-and-tools/methods/information-architecture.html
