# Agent Integration — Information Architecture Templates

## When to use
- When producing IA deliverables for a new product, site redesign, or content migration project
- When a sitemap, taxonomy, or navigation spec needs to go from research insights → structured document quickly
- When onboarding a new team member who needs to understand the product's content structure
- When multiple stakeholders need a shared IA reference that is version-controlled

## When NOT to use
- As a substitute for user research informing the IA — templates structure the output, they do not replace card sorting or tree testing
- When the information space is too small to warrant formal IA documentation (fewer than 20 pages/features — a simple outline suffices)
- When the taxonomy is actively contested between stakeholders — resolve the conflict before producing artifacts

## Where it fails / limitations
- Templates create a false sense of completion; a filled-in sitemap is not validated IA until tested with users
- Taxonomy documents drift out of sync with live products without a governance owner assigned
- Generic templates do not capture product-specific edge cases (e.g., multi-tenant SaaS, geo-restricted content)
- Page inventory tables become large and difficult to maintain manually as sites grow past ~200 pages

## Agentic workflow
An agent can generate a first-draft IA strategy document or sitemap from a content inventory list, existing navigation structure, or a product description. The agent fills in the template skeleton with plausible groupings, labels, and taxonomy terms. A human then validates the groupings against user mental models (card sort results) and adjusts labels for clarity. The agent can regenerate a revised version after incorporating feedback.

For ongoing maintenance, an agent can diff a current sitemap against a previous version, flag newly added pages not yet categorized, and suggest taxonomy placement.

### Recommended subagents
- `faion-sdd-executor-agent` — generate IA deliverables (sitemap, taxonomy doc, navigation spec) from a structured research brief
- General Claude subagent — draft IA strategy document from a content inventory list or product description

### Prompt pattern
```
You are an information architect. Given this content inventory: [list of pages/items]
Generate a sitemap following this template: [paste sitemap template]

Group items by: user task (not org structure).
Label each group using plain language, avoiding internal jargon.
Flag any items that don't fit neatly — do not force them into a category.
```

```
Given this sitemap (v1): [sitemap]
And these card sort results showing how users group the following items: [results]
Suggest: (a) which category labels to rename, (b) which items are in the wrong group, (c) any missing categories.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `markdown-toc` | Auto-generate table of contents for large IA docs | `npm i -g markdown-toc` / github.com/jonschlinkert/markdown-toc |
| `tree` | Generate directory-tree representations of file-based IA | `brew install tree` / built-in on Linux |
| `csvkit` | Process page inventory CSVs for analysis and filtering | `pip install csvkit` / csvkit.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop | SaaS | Partial (API) | Card sorting + tree testing; results export via API |
| Whimsical | SaaS | No | Fast sitemap diagramming; no programmatic API |
| Miro | SaaS | Partial (REST API) | Collaborative IA work; API allows creating boards and cards |
| Airtable | SaaS | Yes (REST API) | Taxonomy and page inventory management; agent-friendly CRUD |
| Notion | SaaS | Yes (REST API) | IA documentation hub; API supports reading/writing pages |
| OmniGraffle | Desktop | No | Professional sitemap tool; no agent integration |

## Templates & scripts
See `templates.md` for: IA strategy document, sitemap template (with legend), taxonomy document template, and example IA patterns (mega menu, hub-and-spoke, flat structure).

Inline: generate a page inventory CSV skeleton:
```python
import csv, sys

def gen_page_inventory(pages: list[dict], outfile: str = "page-inventory.csv"):
    """
    pages: list of {url, title, section, priority, template, owner}
    Writes a CSV page inventory file.
    """
    fields = ["url", "title", "section", "priority", "template", "owner", "notes"]
    with open(outfile, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for p in pages:
            w.writerow({**{k: "" for k in fields}, **p})
    print(f"Written: {outfile} ({len(pages)} rows)")
```

## Best practices
- Start with the IA strategy document before creating the sitemap — strategy defines the organization scheme; sitemap visualizes it
- Keep taxonomy document and sitemap in sync; they describe the same structure from different angles
- Assign a taxonomy owner responsible for approvals when new content types or categories are added
- Use sentence case for all navigation labels; avoid title case (it reads as shouting) and ALL CAPS
- Limit primary navigation to 7 items maximum (Miller's Law); secondary items go in section nav or footer
- Version-control IA documents alongside product specs so design decisions have historical context

## AI-agent gotchas
- Agents will produce plausible-looking groupings that reflect common web patterns, not your users' actual mental models — always validate against card sort data
- LLMs default to topic-based organization schemes; if your product needs task-based IA, specify this explicitly in the prompt
- Generated taxonomy labels often include jargon; instruct the agent to flag any term users might not recognize
- Agents cannot know which content is high-priority for business goals — supply this explicitly or the agent will treat all content equally
- For large content inventories (200+ items), break the task into sections; single-pass generation loses coherence

## References
- Rosenfeld, L., Morville, P., Arango, J. "Information Architecture for the Web and Beyond." O'Reilly, 2015.
- Covert, A. "How to Make Sense of Any Mess." Self-published, 2014. Free at howtomakesenseofanymess.com
- NNg IA deliverables: https://www.nngroup.com/articles/ia-deliverables/
- Usability.gov IA methods: https://www.usability.gov/how-to-and-tools/methods/information-architecture.html
- IDF IA deliverables guide: https://www.interaction-design.org/literature/article/information-architecture-deliverables
