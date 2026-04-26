# Agent Integration — Claude Advanced Features

## When to use
- **Extended Thinking**: multi-step math, architecture decisions, debugging complex bugs, strategic planning — when visible reasoning improves trust or accuracy
- **Computer Use**: automating GUI-only workflows (legacy apps, browser automation, desktop testing) in sandboxed environments
- **Prompt Caching**: any pipeline that calls Claude repeatedly with the same system prompt or document context (> 1024 tokens stable prefix)
- **Batch API**: offline enrichment, content generation, nightly analysis — any workload where 24-hour latency is acceptable in exchange for 50% cost reduction

## When NOT to use
- Extended Thinking: simple extraction, classification, or templating tasks — thinking adds latency and tokens without benefit
- Computer Use: production systems with live credentials or databases — human-in-the-loop required; never unattended
- Prompt Caching: prompts that change on every call — cache will never hit; you pay write cost with no read benefit
- Batch API: real-time user-facing responses — 24-hour SLA makes it unsuitable for synchronous pipelines

## Where it fails / limitations
- Extended Thinking is incompatible with `temperature` parameter — setting both raises an API error
- Extended Thinking thinking tokens count toward `max_tokens` budget — always set `max_tokens` well above the thinking `budget_tokens`
- Computer Use (beta) requires external screen/input infrastructure (VNC, xdotool, pyautogui) — the API only generates action commands
- Prompt Cache TTL is 5 minutes (extended on use) — cache misses are silent; monitor `cache_read_input_tokens` to confirm hits
- Batch API results may take up to 24 hours; no guarantee on sub-hour completion; no partial result access
- Cache prefix must be byte-identical — trailing whitespace, version string changes, or dynamic timestamps all bust the cache
- Computer Use tool schemas are versioned (`computer_20241022`) — beta version may change without notice

## Agentic workflow
Extended Thinking fits as the reasoning step in a multi-stage pipeline: a Claude Opus subagent reasons through a problem and returns both `thinking` and `answer` blocks; the answer block is validated and passed downstream. Prompt Caching is transparent to the agentic caller — just add `cache_control` to stable content and monitor the `usage` object for cache hit rates. Batch API is ideal for `faion-poll-agents` style background processing: dispatch batches, poll for completion, consume results. Computer Use requires a dedicated operator agent with VM control and a human escalation path for unexpected UI states.

### Recommended subagents
- `faion-sdd-executor-agent` — uses Extended Thinking for architecture decision tasks; Batch API for offline spec enrichment
- `nero-sdd-executor-agent` — uses Prompt Caching on long system prompts; Extended Thinking for complex reasoning tasks

### Prompt pattern
```python
# Extended Thinking — returns (thinking, answer)
import anthropic
client = anthropic.Anthropic()

def think_deeply(problem: str, budget: int = 8000) -> tuple[str, str]:
    resp = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=budget + 4096,  # must exceed budget_tokens
        thinking={"type": "enabled", "budget_tokens": budget},
        messages=[{"role": "user", "content": problem}]
    )
    thinking = next((b.thinking for b in resp.content if b.type == "thinking"), "")
    answer = next((b.text for b in resp.content if b.type == "text"), "")
    return thinking, answer
```

```python
# Prompt Caching — cache stable system prompt
def call_with_cache(system_text: str, user_msg: str) -> str:
    resp = client.beta.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        betas=["prompt-caching-2024-07-31"],
        system=[{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_msg}]
    )
    # Log cache metrics
    u = resp.usage
    hit_rate = u.cache_read_input_tokens / max(u.input_tokens, 1)
    return resp.content[0].text, hit_rate
```

```python
# Batch API — submit and poll
def submit_batch(prompts: list[dict]) -> str:
    """Submit list of {id, prompt} dicts. Returns batch_id."""
    reqs = [{"custom_id": p["id"], "params": {
        "model": "claude-sonnet-4-20250514", "max_tokens": 1024,
        "messages": [{"role": "user", "content": p["prompt"]}]
    }} for p in prompts]
    return client.beta.messages.batches.create(requests=reqs).id
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` SDK | All advanced features via Python | `pip install anthropic` |
| `xdotool` | X11 mouse/keyboard for Computer Use on Linux | `apt install xdotool` |
| `pyautogui` | Cross-platform GUI automation for Computer Use | `pip install pyautogui` |
| `playwright` | Browser automation as Computer Use alternative | `pip install playwright` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | All four features available on prod endpoint |
| AWS Bedrock | SaaS | Yes | Claude via Bedrock; Extended Thinking available; check Batch support |
| Scrapybara | SaaS | Yes | Managed Computer Use infrastructure (VM + browser) for Claude |
| Steel.dev | SaaS | Yes | Browser-as-a-service for Computer Use browser automation |
| Helicone | SaaS | Yes | Cache hit rate monitoring in dashboard |

## Templates & scripts
See `templates.md` for Computer Use action handler pattern. Batch polling loop (≤50 lines):

```python
import time

def poll_and_collect(batch_id: str, poll_interval: int = 60) -> list[dict]:
    """Poll Batch API until done. Returns list of {id, text}."""
    while True:
        batch = client.beta.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            results = []
            for r in client.beta.messages.batches.results(batch_id):
                if r.result.type == "succeeded":
                    results.append({
                        "id": r.custom_id,
                        "text": r.result.message.content[0].text
                    })
                else:
                    results.append({"id": r.custom_id, "error": str(r.result.error)})
            return results
        time.sleep(poll_interval)
```

## Best practices
- Extended Thinking: start with `budget_tokens=5000`; increase only if answer quality is insufficient — more thinking does not always mean better answers
- Extended Thinking: always set `max_tokens` to at least `budget_tokens + 2048` to avoid truncation of the answer block
- Prompt Caching: put the most stable content first (system instructions), dynamic content last (user message) — cache is prefix-matched
- Prompt Caching: measure `cache_read_input_tokens / input_tokens` ratio; target > 70% for cost benefit
- Batch API: group requests by model and max_tokens to simplify result processing; use custom_id that maps to your DB primary key
- Computer Use: always implement a timeout per action cycle; set maximum iteration count; route unknown UI states to human review
- Do not mix Extended Thinking with streaming unless you can parse `thinking` SSE deltas — the event format differs from text deltas

## AI-agent gotchas
- Extended Thinking with `budget_tokens=0` disables thinking silently — always set at least 1024
- `thinking` blocks must be preserved in multi-turn history when continuing a thinking conversation — stripping them breaks context
- Prompt Cache write cost is 25% higher than regular input tokens — on first call you pay more; savings start from second call
- Batch API has no webhook; only poll-based status check — build your own polling loop or use a cron job
- Computer Use generates OS-level commands (click, type, key) — executing them without sandboxing is a critical security risk
- Batch API `errored` results do not retry automatically — you must detect and resubmit failed items
- Extended Thinking outputs can include model reasoning about its own limitations — do not expose thinking blocks to end users

## References
- https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://docs.anthropic.com/en/api/messages-batches
- https://www.anthropic.com/research/claude-computer-use
