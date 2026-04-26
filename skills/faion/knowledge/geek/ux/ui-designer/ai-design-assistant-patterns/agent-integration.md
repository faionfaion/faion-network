# Agent Integration — AI Design Assistant Patterns

## When to use
- Implementing a contextual AI assistant inside a design tool (Figma plugin, custom web app) where the assistant reacts to what the user has selected or is editing
- Building a review-mode assistant that audits a design artifact (spec, mockup, component) and returns structured feedback
- Automating design documentation: converting a Figma file or component JSON into human-readable specs, changelogs, or handoff notes
- Evaluating which interaction pattern (sidebar, modal, inline) fits a given tool's UX before building an AI feature

## When NOT to use
- When the design problem is novel or strategic — AI assistant patterns are for execution support, not vision-setting
- When the assistant would need to make irreversible changes autonomously — all AI design actions must be reversible or human-confirmed
- When context window is insufficient to hold the full design artifact (large Figma file JSON > 200k tokens) — the assistant will hallucinate missing details
- When the user base has low AI literacy — assistant patterns require users to interpret and validate output, which is a skill

## Where it fails / limitations
- Sidebar assistants degrade when the user's working context changes faster than the assistant's context window updates — the assistant gives stale suggestions
- Modal assistants disrupt flow for complex iterative tasks; users abandon them after 2–3 interactions if the UI requires too many clicks
- Inline assistants in design tools are technically constrained by plugin sandboxing — they cannot access the full file graph, only selected nodes
- Review-mode assistants produce false positives at scale; without a confidence threshold filter, the noise overwhelms useful signal
- Documentation assistants hallucinate component descriptions when the design uses non-standard naming conventions or lacks descriptive layer names
- No assistant pattern handles emotional or brand-feel feedback reliably — "make it feel more premium" is not a machine-executable instruction

## Agentic workflow
Agents implement AI design assistant patterns by selecting the right interaction mode based on task type: contextual for real-time suggestions, modal for batch or complex generation, inline for micro-corrections, review for audit passes. In a Claude subagent pipeline, the most practical pattern is review-mode: the agent receives a design artifact (Figma JSON export, Storybook component list, or spec document), applies a structured rubric, and returns a structured feedback report (JSON or Markdown) that a human designer acts on. For documentation generation, the agent reads the artifact and produces specs in a defined template. Human-in-loop checkpoints are required before any feedback is presented to stakeholders or any change is applied to a live design system.

### Recommended subagents
- `faion-sdd-executor-agent` — executes a design review task: reads spec, applies rubric, writes feedback file
- Custom design-doc agent — reads Figma export JSON, generates component documentation in a defined Markdown template

### Prompt pattern
```
You are a design review assistant. Review the following component spec against these criteria:
1. Accessibility: WCAG AA contrast, keyboard navigation documented, aria roles specified
2. Consistency: tokens used match design system (no hardcoded hex values)
3. Edge cases: empty state, loading state, error state defined
4. Responsiveness: behavior at 320px, 768px, 1440px described

Component spec:
<spec>
{component_spec}
</spec>

Return JSON: {"passed": [], "failed": [{"criterion": "", "detail": "", "suggestion": ""}]}
```

```
# Inline suggestion pattern
Selected layer: {layer_name}
Layer type: {layer_type}
Current properties: {properties_json}

Suggest 3 specific improvements for this layer. Each suggestion must be:
- Actionable (specify the exact change)
- Justified (reference a design principle or token)
- Non-breaking (no structural changes, only property edits)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| figma-api (Node) | Fetch design context (selected nodes, styles) for assistant input | npm i @figma/rest-api-spec |
| anthropic SDK | Drive Claude as the assistant engine | pip install anthropic / npm i @anthropic-ai/sdk |
| jsonschema (Python) | Validate structured assistant output before acting on it | pip install jsonschema |
| diff-so-fancy | Human-readable diff of design spec versions (before/after assistant suggestions) | npm i -g diff-so-fancy |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude API (Anthropic) | SaaS | Yes | Primary engine for contextual, review, and doc-gen assistant patterns |
| Figma REST API | SaaS | Yes | Source of design context (nodes, styles, components) for the assistant |
| Figma UXP Plugin SDK | OSS | Yes (in-browser) | Build sidebar/inline assistants that run inside Figma; sandboxed JS environment |
| Storybook | OSS | Yes — Node | Component documentation that can be parsed and fed to a review assistant |
| Zeroheight / Supernova | SaaS | Partial | Design system doc platforms; can receive generated docs via API |
| Linear | SaaS | Yes — REST | Log assistant-generated feedback as issues for designer follow-up |

## Templates & scripts
See templates.md for review rubric templates.

Design review pipeline (Python, ~45 lines):

```python
import os, json
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

RUBRIC = """
Review this component spec for:
1. Accessibility (WCAG AA contrast, keyboard nav, aria roles)
2. Token consistency (no hardcoded values)
3. State completeness (empty, loading, error)
4. Responsive behavior (320px / 768px / 1440px)

Return JSON: {"passed": [], "failed": [{"criterion": "", "detail": "", "suggestion": ""}]}
"""

def review_component(spec: str) -> dict:
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"{RUBRIC}\n\nComponent spec:\n{spec}"}
        ],
    )
    text = resp.content[0].text
    # Extract JSON block
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

if __name__ == "__main__":
    import sys
    spec = open(sys.argv[1]).read()
    result = review_component(spec)
    failed = result.get("failed", [])
    print(f"Issues found: {len(failed)}")
    for f in failed:
        print(f"  [{f['criterion']}] {f['detail']} → {f['suggestion']}")
```

## Best practices
- Choose the interaction pattern before building: sidebar for always-on suggestions, modal for focused generation, inline for micro-edits, review for batch audit — mixing patterns in one tool creates confusion
- Always return structured output (JSON) from the assistant, not prose, so the application layer can act on it programmatically
- Apply a confidence or relevance filter to assistant suggestions before displaying them — showing every suggestion from a large batch buries the useful ones
- For documentation generation, define the output template first and instruct the assistant to fill it — never ask for freeform docs and then parse them
- Cache assistant responses keyed on the design artifact hash to avoid redundant API calls when the design hasn't changed
- Log all assistant interactions (input context, output, user action taken) for future fine-tuning and pattern analysis
- For in-plugin (UXP) assistants, keep context payloads under 50k tokens — strip hidden layers, locked frames, and non-visible nodes before sending

## AI-agent gotchas
- Design context from Figma can be arbitrarily large; always truncate or scope the input before sending to the model — uncontrolled context → high cost + degraded quality
- Inline assistant suggestions that modify node properties must go through a reversible operation (Figma undo stack); agents that batch-apply changes without undo hooks can corrupt files
- The Claude API has a context window but no memory of prior design sessions — assistant continuity must be maintained by the application, not the model
- Review assistants trained on generic design principles will miss project-specific standards (spacing scale, brand palette, component naming) — inject project-specific rules as system prompt context
- Structured JSON output from Claude occasionally wraps in markdown code fences; always strip ``` blocks before JSON parsing
- UXP plugin sandbox does not allow external HTTP requests by default; assistant calls to Claude must proxy through a backend service

## References
- https://www.figma.com/plugin-docs/
- https://www.anthropic.com/api
- https://www.nngroup.com/articles/ai-design-tools/
- https://www.smashingmagazine.com/2025/01/ai-design-assistants/
- https://www.interaction-design.org/literature/article/ai-design-assistants
