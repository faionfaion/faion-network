# Agent Integration — Mob Programming

## When to use
- Mixed human-AI mobs: 2-4 humans + a Claude agent acting as one navigator/driver, useful for complex bug hunts and architecture spikes.
- Onboarding a new dev to a codebase — Claude provides instant context lookup while the mob discusses.
- Bug-hunt mob on a critical production incident: Claude drives shell commands and log searches while humans steer.
- Learning mob where Claude explains an unfamiliar API while humans practise.

## When NOT to use
- Quiet/individual deep-work tasks — the mob format itself is wrong, regardless of agent involvement.
- Sensitive material (security audits with secrets, PII review) — recording an agent's transcript creates compliance risk.
- Async distributed teams with high latency — mob requires real-time interaction; agent latency adds another stall.
- When the team hasn't tried mobbing yet — adding an LLM on top of a new practice doubles failure modes.

## Where it fails / limitations
- The "all in one room, one keyboard" doctrine breaks: an agent has its own context window, sees only what it's shown.
- Rotation rule ("idea must pass through someone else's hands") doesn't apply cleanly when the agent generates code from a navigator's verbal description.
- Dominance risk inverted: the agent can dictate solutions faster than humans can debate. Without facilitation discipline, mob becomes "agent codes, humans approve".
- Audio → transcript fidelity varies; navigator instructions misheard become wrong code.
- Privacy: tooling that streams the mob audio/screen to an LLM raises legal/IP issues.

## Agentic workflow
Treat the agent as a single mob participant with rotating roles. In one rotation it drives (executes commands, writes code from human dictation); in the next it navigates (proposes next step). Keep humans as facilitator and final approver; use a ~5-10 minute timer enforced by `mob.sh` or `mobti.me`. Pipe the agent into VS Code Live Share / Tuple as a co-pilot rather than the sole driver. Always end the mob with a retro that includes "what did the agent do well / poorly" as a fixed agenda item.

### Recommended subagents
- `faion-brainstorm` — diverge/converge cycles map well onto mob navigation discussions.
- `faion-improver` — post-mob retro fits the "investigate → fix → log" loop.
- General Sonnet driver subagent — fast, cheap, executes dictation reliably.
- General Opus navigator subagent — slower, used only when the mob is stuck and needs a fresh proposal.

### Prompt pattern
```
You are the agent participant in a mob session. Current role: DRIVER.
- Only edit code/run commands when a human navigator gives an explicit instruction.
- If instruction is ambiguous, ask a single clarifying question, then stop.
- After 7 minutes, hand off: print a 3-line state summary and stop.
Current goal: <one sentence>.
Recent rotation log: <last 3 instructions + outcomes>.
```
```
Role: NAVIGATOR (this rotation).
Propose the next concrete step toward <goal>. One step only, ≤3 sentences,
phrased as intent ("validate the email format") not dictation.
The human driver will type; you will not write code this rotation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mob.sh` | Git-based mob handoff (`mob start / next / done`) | https://mob.sh |
| `mobti.me` | Web mob timer | https://mobti.me |
| VS Code Live Share | Real-time multi-cursor editing | https://visualstudio.microsoft.com/services/live-share/ |
| Tuple | Low-latency pair/mob desktop sharing | https://tuple.app |
| Pop | Cross-platform pair/mob screen-share | https://pop.com |
| `tmate` | Terminal sharing for backend mobs | https://tmate.io |
| OBS + audio routing | Stream mob to a transcription pipeline (with consent) | https://obsproject.com |
| `whisper.cpp` / `faster-whisper` | Local audio→text for the agent's input | https://github.com/ggerganov/whisper.cpp |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Copilot Chat (Voice) | SaaS | Yes | Lets a navigator dictate to an LLM driver |
| Cursor / Zed CRDT | SaaS / OSS | Yes | Multi-cursor with LLM panel |
| Claude Code (this) | SaaS | Yes | Use as one mob participant via shared transcript |
| Zoom / Google Meet | SaaS | Indirect | Pipe captions to a transcription service for the agent |
| Miro / FigJam | SaaS | Yes (API) | Whiteboard for the navigator-side discussion; agent reads exported board |
| `mob-programming-rpg` | OSS | Indirect | Card prompts for human roles; agent can act as facilitator |

## Templates & scripts
Use `mob.sh` for handoffs; the methodology's `templates.md` already documents common rotation patterns. Useful companion: a tiny rotation logger so the agent stays oriented.

```bash
#!/usr/bin/env bash
# rotation-log.sh — append a rotation entry to MOB_LOG.md
# Usage: rotation-log.sh <driver> <navigator> <intent>
set -euo pipefail
DRIVER="$1"; NAV="$2"; INTENT="${3:-}"
TS=$(date -u +%FT%TZ)
echo "- $TS  driver=$DRIVER  navigator=$NAV  intent=\"$INTENT\"" >> MOB_LOG.md
mob next || true   # hand off via mob.sh if available
```

## Best practices
- Cap mob size at 4 humans + 1 agent. Above that, the agent's outputs drown human voices.
- Always assign a human facilitator who controls the agent's turn (mute/unmute, prompt review).
- Strict rotation: the agent rotates *out* of driver every 5-10 minutes, same as humans, to prevent code-monoculture.
- Log rotations to a file in the repo (not just chat history); the agent can re-read it after a context reset.
- Forbid the agent from acting on instructions it can't quote back; require an explicit "received: …" confirmation.
- Schedule one fully-human mob per week to retain the social/learning benefits.
- Mandatory breaks every 75-90 minutes — same as human-only mobs; don't let the agent's tirelessness erode them.

## AI-agent gotchas
- **Drift between rotations.** Agent loses thread when you swap navigator/driver prompts; pin the goal + last 3 actions in every prompt.
- **Over-fast driver.** Agent commits before navigators finish discussing. Add an explicit "wait for `GO` keyword" rule.
- **Silent rewrites.** Agent reformats unrelated code when "fixing one line". Restrict to changed lines only and inspect the diff before committing.
- **Lost context on rotation.** When you switch the agent from driver→navigator, its memory of the last 7 minutes is just the prompt. Maintain a `MOB_LOG.md` and feed it.
- **Audio transcription errors.** `their / there`, `then / than` flips become real bugs. Re-state instructions in chat, not just voice.
- **Confidentiality.** Don't paste internal secrets, customer data, or unreleased product info into the agent's context unless governance allows.
- **Human-in-loop checkpoint.** Final commit/push must be performed by a human, not the agent. Branch protection enforces it.

## References
- https://www.agilealliance.org/resources/experience-reports/mob-programming-agile2014/ — Woody Zuill original
- https://mobprogrammingguidebook.com/
- https://www.remotemobprogramming.org/
- https://mob.sh, https://mobti.me
- https://tuple.app/blog/why-pair-program — pair/mob context for AI augmentation
- https://github.blog/2023-06-20-how-to-research-and-plan-features-with-github-copilot/ — LLM as mob participant
