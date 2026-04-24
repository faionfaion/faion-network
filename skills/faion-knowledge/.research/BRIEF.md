# Methodology Research Brief (subagent prompt template)

You are researching ONE methodology inside `skills/faion-knowledge/knowledge/`. Produce a single deliverable: a new file `agent-integration.md` placed alongside the methodology's existing `README.md`.

## Inputs provided to you

- **Absolute path** to the methodology directory (contains `README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`).

## What to research (deep, multi-angle)

1. **Read the existing methodology** (README first, then skim the other 4 files) to ground yourself in what it actually is.
2. **Agentic usage** — how does this methodology fit with Claude/AI subagents? Which subagents in this repo (look in `agents/` or `skills/*/agents/`) are relevant? What prompt patterns work best?
3. **CLI tools & APIs** — which command-line tools, SDKs, or APIs are the industry standard for this methodology? (web-search allowed)
4. **Services & apps** — which SaaS, open-source tools, or platforms are widely used? Prefer ones that expose APIs/CLIs agents can drive.
5. **Templates & scripts** — is there a reusable script, config template, or boilerplate that accelerates this methodology? If a small script (≤50 lines bash/python) would materially help, write it inline in the output file.
6. **When to use / when NOT to use / where it fails** — be concrete. Name the situations. Don't hand-wave.
7. **Best practices for implementation** — the non-obvious ones, from real-world usage.
8. **AI-agent-specific gotchas** — where does this methodology break down when executed by an LLM agent? What human-in-the-loop checkpoints are required?

## Output format — `agent-integration.md`

Use this exact skeleton (markdown, terse, no filler):

```markdown
# Agent Integration — <Methodology Name>

## When to use
- <bullet: concrete situation>
- ...

## When NOT to use
- <bullet>
- ...

## Where it fails / limitations
- <bullet>
- ...

## Agentic workflow
<2–4 sentences on how to drive this methodology with Claude subagents. Name specific subagents from this repo if relevant.>

### Recommended subagents
- `<agent-name>` — <what it does in this flow>
- ...

### Prompt pattern
<1–2 short prompt snippets showing how to invoke an agent for this methodology>

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ... | ... | ... |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ... | ... | ... | ... |

## Templates & scripts
<Either: "See `templates.md` for X" OR inline a new script/template if it materially helps. Keep inline scripts ≤50 lines.>

## Best practices
- <bullet>
- ...

## AI-agent gotchas
- <bullet: where LLM execution goes wrong>
- ...

## References
- <URL or book/paper>
- ...
```

## Rules

- **Do not edit** existing methodology files (README.md, checklist.md, etc.). Only create `agent-integration.md`.
- **No filler**. Every bullet must be specific. "Use best practices" is banned.
- **Prefer real tools you can name** over generic advice. If you're not sure a tool exists, web-search.
- **Length target**: 150–300 lines. Shorter if the topic is narrow.
- **No emojis**. No marketing voice.
- **Ukrainian is NOT used** — write in English.
- If you cannot produce a genuinely useful `agent-integration.md` (methodology is too thin or too redundant with README), write a 30-line note explaining why and stop. That's an acceptable output.

## Return to caller

After writing the file, return ONLY a one-line summary: `WROTE <absolute-path> (<line-count> lines) — <3-word-essence>`. No other text.
