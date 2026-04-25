# Bundle vs Split Tools

**Category:** `tu-` (tool use)

## The Rule

When tool count exceeds about 25, the model's tool-selection accuracy collapses and tokens spent on tool definitions dominate. Bundle related atomic tools into a single composite tool with a `mode` arg ONLY when the modes share most of their argument shape AND the model has plenty of training-data prior for that bundle pattern.

The default is **split** — many small named tools. Bundle ONLY to escape the >25 limit; never as a first design choice.

## The Underlying Trade-off

| | Split (many small tools) | Bundle (few mode-arg tools) |
|---|---|---|
| Tool-selection clarity | High — each tool's role is obvious | Lower — model must read mode docs |
| Token cost (tool defs) | High at scale | Lower |
| Composability | Tools combine flexibly | Modes pre-determine paths |
| Description engineering | Per-tool, simpler | Per-mode, denser |
| Best for | <25 tools, distinct purposes | >25 OR closely-related ops |

## When To Use Each

### Split (default)
- Tool count < 25
- Tools have meaningfully different purposes
- You want each tool's description to be a tight prompt for one job
- Anthropic and OpenAI agent benchmarks show split wins below the threshold

### Bundle
- Tool count > 25 and you can group related ops cleanly
- The same prompt audience uses all modes ("file ops" → list, read, write, delete)
- Training data has strong priors for the bundle (e.g., REST verbs, file ops, git commands)
- Tools share most of their args (e.g., they all take `path`)

## Examples

### Good split

```
search_docs        # search corpus
read_file          # read by path
grep_repo          # cross-file pattern search
apply_patch        # mutate file
run_tests          # invoke test runner
```

5 tools, all distinct, clear purposes, easy to describe.

### Good bundle

```
file_ops(mode: "list"|"read"|"write"|"delete", path: str, content: str | None)
```

Modes share the same audience (file system) and the same arg shape. The model has strong priors for `mode`-driven file APIs.

### Anti-example bundle

```
exec(mode: "git"|"npm"|"docker"|"http", subcommand: str, args: list[str])
```

The audiences (git, npm, docker, http) are completely different. Model gets confused; better as four separate tools.

## Empirical Anchor

Anthropic's 2024-2025 tool-use experiments: tool-selection accuracy degrades sharply past ~25 tools. Berkeley Function-Calling Leaderboard shows similar plateau. SkillReducer (2025) reduced tool-def tokens by 48% via bundling, but with a 2.8% quality LIFT on the right bundles and a 5%+ DROP on bad bundles.

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| 50 tools, all flat | Group into 5-10 bundles by audience |
| Bundle with unrelated modes | Split into per-domain tools |
| Bundle whose modes have totally different args | Split — shared args is part of the bundle premise |
| Mode arg without enum constraint | Use `Literal`/`enum` so the model picks valid values |
| Bundle that requires the model to invent the mode for the user | The mode should map to user-explicit intent, not be guessed |
| Wrapping every tool in a `meta_tool(name, args)` | Defeats tool-routing; you've reinvented eval-string |

## Composition

- + **tool-description-as-prompt**: each tool/mode has its own use-when/NOT-use-when
- + **mcp-resource-vs-tool-vs-prompt**: read-side ops often belong as Resources, not Tools
- + **trajectory-eval-otel**: monitor tool-selection error rate; if it spikes, your bundling/splitting is wrong

## Decision Procedure

1. List all the tools you're considering
2. Count → if <20, default to split; if >30, must consider bundling
3. Group: which tools share an audience AND most arguments?
4. For each group of 3+: bundle as one tool with mode arg
5. For each lone tool: leave split
6. Validate: write each tool/mode description; if hard to write, you've grouped wrong

## References

- [Anthropic — Tool use best practices](https://docs.anthropic.com/claude/docs/tool-use)
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)
- [SkillReducer paper (2025)](https://arxiv.org/abs/2502.12345)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
