# Agent Integration — Pair Programming

## When to use
- Solo developer wants a "navigator" presence: Claude as live reviewer while a human drives in VS Code / JetBrains.
- Strong-style sessions where the human types, the agent dictates the line and explains why.
- Onboarding scenarios: agent plays "tour guide" through an unfamiliar repo, narrating architecture as the human navigates.
- TDD ping-pong with a human writing tests and the agent making them pass (and vice versa).
- Debugging: human shares failing repro, agent navigates hypotheses while human runs commands.

## When NOT to use
- True multi-developer pairing — adding an agent to a human-human pair fragments attention; instead, use the agent as a shared note-taker.
- Pure research / reading sessions; no need for live driving.
- Privacy-sensitive code that cannot leave the laptop (regulated, classified). Use a fully local model or skip.
- High-velocity sprints where the overhead of explaining each line slows the team below solo velocity.
- Domains where the model is weak (DSP, embedded firmware, niche DSLs) — agent suggestions add noise.

## Where it fails / limitations
- README defines roles for two humans; with an agent, the human is **always** physically the driver, but cognitively can be either role. The "who types?" rule has to be redefined per session.
- "Switch every 15-30 min" doesn't apply to an LLM — fatigue model is wrong; instead switch when context depth changes (new file, new layer).
- "Camera on" / "rapport" advice is irrelevant; needs replacement with "share screenshot of failing test" / "share git diff".
- Strong-style ("idea must go through someone else's hands") becomes degenerate with an agent — the agent has no hands. Reinterpret as "agent must articulate a single concrete instruction; human types it verbatim or rejects".
- The README treats AI as "sometimes useful" — does not address agent-led pairing as the default mode.

## Agentic workflow
Run pair-programming with an agent as a continuous **explain-then-act** loop. The human keeps the keyboard; the agent emits one bounded instruction per turn ("add a return type annotation", "extract the validation block to a helper"). After each turn the human accepts, edits, or rejects, and reports the result (test output, diff). Keep transcripts short — paste only the diff and test output back, not the whole file.

### Recommended subagents
- `faion-sdd-execution` — when the pair session is also driving an SDD task and quality gates apply.
- `simplify` — invoke at session end; it acts as a third-pair reviewer over the day's diff.
- `review` — when wrapping a session into a PR, treat the agent's reviewer pass as the second pair member.
- General-purpose subagent in **strong-style mode**: prompted to issue one instruction at a time and wait for human result.

### Prompt pattern
```
Session mode: pair-programming, strong-style. You are the navigator.
Output ONE instruction at a time, no more than 2 lines. Wait for my result before the next.
If I report a test failure, propose the next single change. Do not generate full files.
End-of-session: produce a 5-bullet retrospective and a list of follow-ups.
```

```
Tour-guide mode: I will name a directory; you produce a 5-bullet "what is here, where to start, gotchas" map.
Then I drive — you only answer follow-ups, never propose unsolicited rewrites.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| VS Code Live Share | Share IDE with another human while agent is in chat | https://visualstudio.microsoft.com/services/live-share/ |
| Tuple | Low-latency pairing tool (macOS) | https://tuple.app/ |
| Pop | Multi-cursor remote pair tool | https://pop.com/ |
| `tmux` + `tmate` | Terminal pairing fallback | https://tmate.io/ |
| `git diff --staged` / `gh pr diff` | What to paste back to the agent | docs.git-scm.com / cli.github.com |
| `entr` / `watchexec` | Re-run tests on save during ping-pong | https://github.com/eradman/entr , https://watchexec.github.io/ |
| `claude` CLI | Headless agent driver inside terminal | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tuple | SaaS | Indirect | Human-human; agent participates via chat side-channel. |
| VS Code Live Share | SaaS (free) | Indirect | Same as above. |
| GitHub Codespaces / Gitpod | SaaS | Yes | Shared dev environment; agent can be wired into terminal. |
| CodeTogether | SaaS | Indirect | Cross-IDE pairing. |
| Slack / Discord | SaaS | Yes | Side-channel for agent transcript & retros. |
| Miro / Excalidraw | SaaS | Caution | Whiteboarding — agents weak at spatial reasoning. |

## Templates & scripts
Inline session log helper — pipe terminal output to a dated transcript so the agent can read prior context:

```bash
#!/usr/bin/env bash
# scripts/pair-session.sh — start a logged pair session.
set -euo pipefail
session_dir="$HOME/.pair-sessions/$(date +%Y-%m-%d_%H%M)"
mkdir -p "$session_dir"
echo "Session: $session_dir"
# script(1) records terminal; agent can be fed `cat $session_dir/typescript`.
exec script -q "$session_dir/typescript"
```

End-of-session retrospective prompt skeleton:

```
Inputs: today's diff (`git diff main...HEAD`), tests passing (Y/N), session duration.
Output: 5 bullets — what worked, what stalled, smell to address next session, missing test, follow-up issue.
```

## Best practices
- Define the **mode** at session start: classic, ping-pong, strong-style, or tour-guide. Don't switch mid-session without resetting context.
- One instruction per turn for strong-style with an agent — multi-step instructions degrade into agent-driven solo coding.
- Keep prompts short; paste **diffs and test output**, not full files. Saves context and forces the agent to ask for what it needs.
- Take real breaks. Agent does not tire, but humans do — Pomodoro still applies on the human side.
- Run a **silent retro** at session end: agent generates a 5-bullet summary, human edits it. This becomes session memory.
- Use ping-pong specifically when the human is learning a framework — writing the failing test forces understanding of behavior.

## AI-agent gotchas
- Agent loses pairing role under length pressure — after several long turns it starts emitting full files. Re-state strong-style rules every ~10 turns.
- LLMs cannot "switch driver" because they have no fingers. The closest analog is `claude` CLI in non-interactive mode generating a patch, then the human applies it; reframe rather than emulate.
- The agent has no shared screen — context resets when the chat resets. Persist a `session.md` file the agent reads each turn for state.
- Strong-style requires the agent to **explain why** before issuing the instruction. Without a system prompt enforcing this, the agent gives instructions without rationale.
- The README's "AI as Navigator" section is correct for IDE copilots (Copilot, Cursor) — those operate at the line level. A reasoning-class agent (Claude) is better as a strategic navigator on architecture, not a tab-completer.
- Human-in-loop checkpoint: every commit during a pair session must be reviewed by the human, not auto-committed by the agent.
- Watch for "navigator pollution": agent fills silence with unsolicited suggestions during exploration. Mute it explicitly ("only answer when I ask").

## References
- https://martinfowler.com/articles/on-pair-programming.html
- https://llewellynfalco.blogspot.com/2014/06/llewellyns-strong-style-pairing.html
- https://www.amazon.com/Pair-Programming-Illuminated-Laurie-Williams/dp/0201745763
- https://tuple.app/blog
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
