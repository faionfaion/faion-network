# AGENT-02: Anthropic Claude Agent SDK + Claude Code — Production Methodologies

**Focus:** Claude-specific tricks (April 2026 state). Sources: anthropic.com, claude.com, platform.claude.com, code.claude.com, github.com/anthropics.

---

## M-01: cache-prefix-order-tools-system-messages
**Category:** cost-
**Sources:**
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching
**Rule:** Place `cache_control: {"type": "ephemeral"}` on the LAST tool definition (and end of system prompt) — Anthropic builds cache prefixes strictly in `tools → system → messages` order, so a single breakpoint at the end of static tool/system content captures the entire stable prefix.
**When to use:** Any agent making more than one call inside a 5-min window with identical tool defs and stable system prompt — typical agent loops, multi-turn chat, ReAct.
**When NOT to use:** Single-shot extraction calls; A/B tests where tool list keeps mutating; conversations where user content is at the start (no static prefix).
**Example/snippet:**
```python
tools=[
  {"name": "search", "input_schema": {...}},
  {"name": "fetch",  "input_schema": {...},
   "cache_control": {"type": "ephemeral"}},   # caches ALL tools
]
system=[{"type": "text", "text": LONG_SYSTEM,
         "cache_control": {"type": "ephemeral"}}]
```
**Why it works:** Cache hits cost 10% of base input (0.1x). Adding/removing one tool — even an unused one — invalidates everything downstream. Putting the breakpoint at the END of static content lets the longest matching prefix get reused; up to 4 breakpoints allowed but most agents need only 2 (tools-end, system-end).

---

## M-02: subagent-as-context-firewall
**Category:** mem-
**Sources:**
- https://claude.com/blog/subagents-in-claude-code
- https://platform.claude.com/docs/en/agent-sdk/subagents
- https://www.richsnapp.com/article/2025/10-05-context-management-with-subagents-in-claude-code
**Rule:** Delegate ANY task that produces large noisy intermediate output (test runs, log greps, doc fetches, multi-file searches) to a Claude Code subagent — the verbose output stays in the subagent's window, only the summary returns to the parent. Treat subagents as protection of parent context, not just parallelism.
**When to use:** Test execution, codebase exploration, fetching long docs, log analysis, anything where you need the conclusion but not the trail. Ideal when output > 5k tokens but answer is < 500 tokens.
**When NOT to use:** Tasks where the parent needs to SEE the intermediate state (debugging, pair-programming flow). Trivial work where subagent overhead exceeds savings.
**Example/snippet:**
```markdown
# .claude/agents/test-runner.md
---
name: test-runner
tools: Bash, Read
---
Run pytest, return ONLY: pass/fail count + first 3 failing test names + 1-line root cause each.
```
**Why it works:** Subagent has its own fresh context window — only the parent's prompt string crosses the boundary, only the final assistant message returns. Per Anthropic's blog, the key insight is "isolation > parallelism" for context hygiene.

---

## M-03: forced-tool-as-structured-output
**Category:** so-
**Sources:**
- https://platform.claude.com/cookbook/tool-use-extracting-structured-json
- https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs
**Rule:** For guaranteed JSON shape, define a single tool whose `input_schema` is your target schema, then set `tool_choice = {"type": "tool", "name": "<that_tool>"}` — the model literally cannot return prose, only a tool-call payload matching the schema.
**When to use:** Data extraction, classification, any pipeline stage that feeds a typed downstream consumer. Faster + more reliable than parsing free-text JSON.
**When NOT to use:** When you also need extended thinking — `tool_choice: tool` and `tool_choice: any` are INCOMPATIBLE with thinking (returns 400). When you have native `output_config.format` available on Claude 4.6+ (use that instead).
**Example/snippet:**
```python
tools=[{"name":"record_extraction","input_schema":{
  "type":"object","required":["name","email","sentiment"],
  "properties":{"name":{"type":"string"},
                "email":{"type":"string"},
                "sentiment":{"enum":["pos","neg","neu"]}}}}]
tool_choice={"type":"tool","name":"record_extraction"}
```
**Why it works:** Tool calls are constrained-decoded against the schema at the token level — no post-hoc JSON parsing, no retries on malformed brackets. Pre-dates the formal `structured_outputs` feature and still works on every Claude model since 3.5.

---

## M-04: interleaved-thinking-between-tool-calls
**Category:** tu-
**Sources:**
- https://platform.claude.com/docs/en/build-with-claude/extended-thinking
- https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking
**Rule:** For agent loops on Opus 4.6/4.7 or Sonnet 4.6, enable `adaptive thinking` (default on these models) — Claude will think between every tool call, reflecting on results before deciding next action. This is automatic; you only need to NOT disable it.
**When to use:** Multi-step agent workflows where each tool result changes the plan (debugging, research, code investigation, planning loops).
**When NOT to use:** Stateless extraction; high-throughput classification (Haiku); when forcing tool_choice (incompatible — see M-03). When latency-critical and budget should be 'low' or off.
**Example/snippet:**
```python
client.messages.create(
  model="claude-opus-4-7",
  thinking={"type":"enabled","budget_tokens":16000},  # adaptive uses what it needs
  tools=[...],
  ... )
# Claude thinks → calls tool A → thinks about result → calls B → answers.
```
**Why it works:** Without interleaved thinking, the model commits to a tool sequence before seeing results. With it, each tool result enters the next "think" block, so the agent can change strategy mid-loop. Token limit becomes the entire context window when interleaved thinking is on with tools.

---

## M-05: dontask-mode-for-locked-down-agents
**Category:** tu-
**Sources:**
- https://code.claude.com/docs/en/permissions
- https://platform.claude.com/docs/en/agent-sdk/permissions
**Rule:** For headless/CI agents, set `permission_mode: "dontAsk"` and explicitly populate `allowed_tools` — anything not on the list is silently denied (not prompted). Combine with `PreToolUse` hooks for fine-grained per-call gates.
**When to use:** CI/CD, scheduled agents, batch jobs, untrusted environments. Anywhere a human can't respond to permission prompts.
**When NOT to use:** Interactive dev sessions (use `default` or `acceptEdits`). When you actually want to discover what tools the agent tries (use `default` first, audit, then lock down).
**Example/snippet:**
```json
// .claude/settings.json
{ "permissionMode": "dontAsk",
  "allowedTools": ["Read","Grep","Bash(pytest:*)","mcp__github__*"],
  "deniedTools":  ["Bash(rm:*)","Bash(curl:*)"] }
```
**Why it works:** Rule eval order is `deny → ask → allow`; `dontAsk` converts unmatched calls into denials instead of prompts — eliminating hangs in non-interactive contexts. `bypassPermissions` is the unsafe alternative; prefer `dontAsk` + explicit allow-list.

---

## M-06: posttool-hook-as-quality-gate
**Category:** lp-
**Sources:**
- https://code.claude.com/docs/en/hooks-guide
- https://platform.claude.com/docs/en/agent-sdk/hooks
**Rule:** Wire `PostToolUse` hooks with matcher `"Write|Edit"` to run linters/formatters/typecheckers AFTER every file mutation — failures inject feedback back into the agent's next turn, turning the agent into a self-correcting loop without you writing the loop.
**When to use:** Code-editing agents, doc generation, anything with verifiable output. Replaces manual "check after every change" prompts.
**When NOT to use:** Read-only research agents. When the validator is slow (>5s) — agent loop will stall.
**Example/snippet:**
```json
{ "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type":"command","command":"ruff check $CLAUDE_FILE_PATH"}]
    }]}}
```
**Why it works:** Hook stderr is fed back as a tool-result error message — the model SEES the lint failure on its next turn and self-corrects. Deterministic control layer that doesn't rely on the model remembering to run checks.

---

## M-07: progressive-disclosure-skill-md
**Category:** mem-
**Sources:**
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
**Rule:** Author Skills as a 3-level pyramid: (1) YAML frontmatter (always loaded, ≤30 lines, just `name`+`description`+triggers); (2) `SKILL.md` body (loaded on activation, ≤500 lines); (3) `scripts/`, `references/`, `assets/` (loaded only when SKILL.md tells Claude to read them).
**When to use:** Any reusable capability >100 lines of instructions. Domain-specific workflows reused across projects (e.g. "how to deploy", "how we write commits").
**When NOT to use:** One-off instructions (put in `CLAUDE.md` instead). Logic better expressed as a tool (use MCP). Extremely tiny rules (inline them).
**Example/snippet:**
```yaml
---
name: faion-deploy
description: Use when user asks to deploy a faion-net project. Handles op_unlock, deploy-gh.sh selection, post-deploy verification.
---
# Body kept <500 lines; refs to scripts/select-target.sh and references/runbook.md
```
**Why it works:** Claude scans only frontmatter into system prompt — keeps base context small. SKILL.md loads only when triggered. Bundled files load only when explicitly read. Solves the "import everything" anti-pattern that bloats context.

---

## M-08: model-tier-routing-haiku-sonnet-opus
**Category:** mm-
**Sources:**
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://www.augmentcode.com/guides/ai-model-routing-guide
**Rule:** Use Haiku 4.5 ($1/$5) as the front-door classifier/router that decides whether a request is trivial (Haiku answers), medium (Sonnet 4.6), or hard (Opus 4.6/4.7). Target a 70/20/10 split for ~50-80% cost reduction vs all-Sonnet baseline.
**When to use:** Production agent products with mixed workload (chat, support, classification, generation). Any workload >100k requests/month.
**When NOT to use:** Workflows where Haiku regression on a "simple" call cascades catastrophically (e.g. financial decisions). Per user's NERO rule: never downgrade for cost in personal NERO LLM calls — this rule is for THIRD-PARTY products at scale.
**Example/snippet:**
```python
verdict = haiku.classify(req, schema=RouteSchema)  # cheap
model = {"trivial":"haiku","medium":"sonnet","hard":"opus"}[verdict.tier]
return anthropic.messages.create(model=model, ...)
```
**Why it works:** Sonnet 4.6 hits 79.6% on SWE-bench vs Opus 80.8% (1.2pt gap, 5x cheaper). For classification/extraction Haiku matches Sonnet because reasoning capacity isn't the bottleneck. Routing exploits the per-task quality plateau.

---

## M-09: claude-code-as-headless-subagent-runtime
**Category:** cli-
**Sources:**
- https://code.claude.com/docs/en/headless
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://platform.claude.com/docs/en/agent-sdk/streaming-output
**Rule:** Use `claude -p "<prompt>" --output-format stream-json --allowedTools "..."` from any script/cron/CI as a fully-loaded agent runtime — you get tool use, hooks, skills, MCP, permission system, all from a single binary. Far simpler than wiring an Agent SDK loop yourself.
**When to use:** Cron-driven background agents, CI bots, one-shot ops tasks (deploy, audit, fix). Anywhere you'd otherwise reach for the Python/TS Agent SDK but the surface area of CC is enough.
**When NOT to use:** Custom agent loops with bespoke control flow (use Agent SDK directly). Web-app backends needing per-user concurrency (use SDK + your own session store). When you must avoid Node.js dependency.
**Example/snippet:**
```bash
claude -p "Run pytest, fix any failing test, commit if green" \
  --permission-mode dontAsk \
  --allowedTools "Read,Edit,Bash(pytest:*),Bash(git:*)" \
  --output-format stream-json | jq -r 'select(.type=="result").result'
```
**Why it works:** Claude Code is itself an Agent SDK app — invoking `-p` skips the REPL but keeps the entire stack (hooks, skills, MCP, permissions, compaction). You inherit years of agent-loop engineering for free.

---

## M-10: xml-structured-prompts-not-json
**Category:** so-
**Sources:**
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
- https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
**Rule:** Wrap input sections in XML tags (`<context>`, `<task>`, `<examples>`, `<input>`, `<output_format>`) — Claude is specifically RLHF-tuned to parse these reliably. JSON-as-prompt-input is worse: it competes with JSON output, escapes newlines, and is harder to edit.
**When to use:** Any prompt mixing instructions + variable input + examples + format spec. All multi-section system prompts. Subagent prompts.
**When NOT to use:** One-sentence prompts. When the output IS JSON (then the prompt being XML keeps signal separated). Don't over-tag — single-sentence sections don't need their own tag.
**Example/snippet:**
```xml
<task>Classify the email below.</task>
<examples><example><input>Get rich quick!</input><output>spam</output></example></examples>
<email>{user_email}</email>
<output_format>Return only one word: spam|ham</output_format>
```
**Why it works:** Anthropic's training data heavily features XML-tagged structure; Claude treats these tags as semantic boundaries rather than text. Per Anthropic docs: tags reduce misinterpretation, enable post-hoc extraction with regex, and combine cleanly with `<thinking>` for chain-of-thought.

---

## M-11: batch-api-stacks-with-cache-95-percent-savings
**Category:** cost-
**Sources:**
- https://platform.claude.com/docs/en/about-claude/pricing
- https://www.anthropic.com/news/prompt-caching
**Rule:** For non-real-time agent workloads (overnight pipelines, eval runs, content generation queues), submit via the Message Batches API for 50% off — and prompt-caching discounts STACK on top, yielding up to 95% effective savings vs uncached real-time.
**When to use:** Async workloads tolerating up to 24h latency: nightly summarization, eval suites, bulk extraction, content pre-generation, neromedia/pashtelka content pipelines.
**When NOT to use:** Interactive chat, real-time tool-use loops, anything user-facing. Workloads with strict SLAs <1h.
**Example/snippet:**
```python
batch = client.messages.batches.create(requests=[
  {"custom_id": f"doc-{i}",
   "params": {"model": "claude-sonnet-4-6",
              "system": [{"type":"text","text":STABLE_PROMPT,
                          "cache_control":{"type":"ephemeral"}}],
              "messages":[...]}}
  for i, doc in enumerate(docs)])
```
**Why it works:** Cache write inside batch is still 1.25x but only paid once per prefix; subsequent batch items hit cache at 0.1x AND the batch 0.5x. (0.5 × 0.1) = 5% of baseline read cost. For pipelines with shared system prompts this is the single biggest cost lever.

---

## M-12: subagent-prompt-is-the-only-channel
**Category:** pl-
**Sources:**
- https://www.richsnapp.com/article/2025/10-05-context-management-with-subagents-in-claude-code
- https://platform.claude.com/docs/en/agent-sdk/subagents
**Rule:** Treat the subagent invocation prompt as the ONLY data channel from parent → child. Inline every file path, error message, prior decision, and constraint the subagent needs — its context starts fresh and cannot read the parent's conversation. Conversely, instruct the subagent to return a structured, minimal report (parent reads only the final assistant message).
**When to use:** Every subagent dispatch. Especially in multi-step workflows where the subagent needs context that's already in the parent.
**When NOT to use:** Never; this is the rule, not a tactic.
**Example/snippet:**
```text
# Parent prompts subagent:
Investigate flaky test in tests/api/test_auth.py::test_login.
Recent change: commit abc123 added rate-limit middleware.
Suspected cause: race in token cache.
Return ONLY: 2-line root cause + the exact file:line + suggested fix as diff.
```
**Why it works:** Subagents have isolated context — they don't see parent state. Frontloading context AND constraining output schema turns the subagent into a pure function with bounded I/O, which is the entire reason to use one (token budget protection).

---

# Summary
12 methodologies covering: prompt caching mechanics, subagent context isolation, forced-tool structured output, interleaved thinking, locked-down permissions, PostToolUse self-correction, Skills progressive disclosure, model-tier routing, Claude Code as headless runtime, XML prompt structure, Batch+Cache stacking, subagent prompt-as-channel.
