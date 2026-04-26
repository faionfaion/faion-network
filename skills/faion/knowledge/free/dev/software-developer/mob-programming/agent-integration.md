# Agent Integration — Mob Programming

## When to use
- Whole-team work on a high-stakes change (security-critical refactor, payment flow, schema migration) where review-after-the-fact is too slow.
- Onboarding a new engineer to an unfamiliar service: they navigate, the team drives — knowledge transfers in hours, not weeks.
- "Impossible" production bug where multiple specialists' context is needed simultaneously (frontend + backend + ops).
- Killing a knowledge silo: the only person who understands `payments/` is leaving.
- Cross-team API contract design where decisions must stick — code in same room beats async PRs.
- Workshop / kata sessions for spreading a new technique (TDD, hexagonal arch) across the team.

## When NOT to use
- Routine CRUD, typo fixes, dependency bumps — overhead > benefit.
- Async / distributed teams with >3 timezones — coordination cost exceeds knowledge gain.
- Solo founder or ≤2 people — that's pair programming or solo work.
- When >50% of the time is spent waiting on a build, deploy, or external API — sit time burns the mob.
- Teams that have never paired before — start with pairing for 2-4 weeks first.
- Tasks the team genuinely needs to parallelize to hit a deadline.

## Where it fails / limitations
- **Throughput illusion.** Cycle time can drop, but raw story-point velocity often stays flat or dips. If management measures only velocity, mobbing looks "wasteful" and gets killed.
- **Driver fatigue & cognitive overload.** Without strict 5-10 min rotation people zone out; rotation discipline is the load-bearing wall.
- **Dominant voices.** One senior engineer monologues; juniors become typists. Without active facilitation the mob becomes a lecture.
- **Remote latency.** >150ms input lag on Live Share / Tuple breaks the navigator-driver feedback loop. Becomes "watch one person code on a call."
- **Tooling drift.** Different IDEs, keymaps, OS shells slow rotation. The mob's productivity equals the slowest setup.
- **No clear DoD.** Without a written goal and visible timer, sessions drift; the retro becomes "we explored a lot" — that's procrastination.
- **Burnout.** Sustained mobbing >4h/day exhausts introverts. Mix with solo blocks or attrition follows.

## Agentic workflow
Mob programming is a *human* practice — the AI value is in **facilitation and capture**, not driving. Use a Claude subagent as a silent fifth seat: it watches the screen via shared transcript, takes structured notes, surfaces decisions/ADRs, queues follow-up tasks, and runs the rotation timer. Treat the agent as the **scribe + timer + retrospective miner**, not the navigator. After the session, a second agent generates the commit message, updates `.aidocs/` decision log, and converts parking-lot items into SDD `todo/` tasks.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts mob-session decisions and parking-lot items into SDD tasks under `.aidocs/.../todo/`; verifies the mob's WIP commit matches the spec.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrubs the session transcript before publishing the retro; mobs frequently leak credentials, customer names, internal hostnames pasted into the IDE.
- A purpose-built **mob-scribe agent** (worth creating): given the live transcript, output `decisions.md`, `parking-lot.md`, `tests-added.md`, and a retro skeleton.
- `nero-sdd-executor-agent` — when mobbing on NERO repos, drives the post-session task creation directly into the NERO `.product/` lifecycle.

### Prompt pattern
Scribe pass (run live, every 10 min):
```
You are the mob scribe. Read the diff since the last checkpoint and
the last 10 minutes of voice transcript. Output:
- Decisions made (one line each, with rationale).
- Parking lot items (off-topic, who raised it).
- Tests added/changed (file + name).
- Open questions still unresolved.
Do NOT suggest code. Do not propose direction. Observe only.
```

Post-session pass:
```
Given the session transcript and final diff, produce:
1. A 50-char commit title + body explaining the why.
2. SDD task entries for each parking-lot item (path: .aidocs/.../todo/).
3. A 200-word retro draft: what worked, what slowed us, one experiment for next mob.
4. List of new patterns/mistakes to log under .aidocs/memory/.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mob` (mob.sh) | Git-based driver handoff: `mob start` / `mob next` / `mob done` | `brew install remotemobprogramming/brew/mob` ; https://mob.sh |
| `mobti.me` | Browser-based shared rotation timer with names | https://mobti.me |
| `cmdoptions/timer` or `t` (terminal countdown) | Local fallback timer | `brew install timer` |
| VS Code Live Share | Shared cursor/edit/debug session | `code --install-extension MS-vsliveshare.vsliveshare` |
| JetBrains Code With Me | IntelliJ family equivalent | bundled |
| Tuple | Low-latency pair/mob screen sharing (macOS) | https://tuple.app (commercial) |
| Pop | Free macOS/Linux pairing tool from Pivotal alumni | https://pop.com |
| `git rerere` | Auto-resolve repeated merge conflicts during `mob next` cycles | `git config rerere.enabled true` |
| `tmate` | Terminal-only mobbing for backend/devops sessions | `apt install tmate` |
| `gh pr create --draft` | Open the WIP branch as a draft PR for visibility | https://cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| mob.sh | OSS CLI | yes (scriptable) | De-facto standard for git-based handoff. Pre-commit/post-commit hooks compose well with agents. |
| Tuple | SaaS | partial | Best video latency; no public API for transcript ingestion — agent must consume Zoom/Meet transcripts instead. |
| VS Code Live Share | Free SaaS | partial | API exists for extensions; an agent can join as a participant for real-time scribing. |
| Mobti.me | Free SaaS | partial | URL-based timer; agent can scrape it to know whose turn it is. |
| Zoom / Google Meet | SaaS video | yes (via transcript export) | Required for remote mobs; transcript JSON is the agent's primary input. |
| Otter.ai / Fireflies | SaaS transcription | yes (API) | Live transcripts feed the scribe agent; cheaper than building your own. |
| Miro / FigJam | SaaS whiteboard | partial | For pre-mob design sketches; export to PNG or JSON for agent context. |
| Linear / GitHub Issues | SaaS issue tracker | yes | Parking-lot items become issues with `mob:` label, owned by the agent. |
| Coderpad / CodeSandbox Live | SaaS | yes | Sandbox mobbing for randori / interview katas; both have APIs. |

## Templates & scripts

The methodology covers protocols and roles; what's missing is a session bootstrapper. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# mob-session.sh — start a mob session with timer, scribe log, draft PR.
# Usage: mob-session.sh "Add idempotency keys to /payments"
set -euo pipefail
goal="${1:?usage: mob-session.sh GOAL}"
slug=$(echo "$goal" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-' | cut -c1-40)
ts=$(date +%Y%m%d-%H%M)
log=".aidocs/mob/${ts}-${slug}.md"
mkdir -p "$(dirname "$log")"
cat > "$log" <<EOF
# Mob session: $goal
- Started: $(date -Is)
- Driver rotation: 10 min
- Roles: $(git config --get-all mob.participant 2>/dev/null | paste -sd, -)

## Decisions
## Parking lot
## Tests added
## Retro
EOF
git switch -c "mob/${slug}" 2>/dev/null || git switch "mob/${slug}"
mob start --branch "mob/${slug}" 10
gh pr create --draft --title "WIP mob: $goal" --body-file "$log" || true
( while true; do sleep 600; tput bel; say "rotate" 2>/dev/null || echo -e "\a ROTATE"; done ) &
echo $! > /tmp/mob-timer.pid
echo "Log: $log  Timer PID: $(cat /tmp/mob-timer.pid)"
```

Pair with `mob done && kill $(cat /tmp/mob-timer.pid)` at session end. Wire the scribe agent to tail `$log` every 10 minutes.

## Best practices
- **Goal on the wall.** Single-sentence DoD visible at all times. If you can't write it, don't start the mob.
- **Strong-style navigation.** "For an idea to go from your head to the computer, it must go through someone else's hands." Eliminates expert hijacking.
- **5-10 minute rotation, no exceptions.** Even mid-thought. Builds the muscle; once the team trusts handoffs, switch to natural transitions.
- **Identical dev env.** Standardize keymap, font size, OS shortcuts before the first mob — or pair mismatched people deliberately to surface friction.
- **Parking lot is sacred.** Off-topic ideas go to the lot, never derail the mob. Review at retro.
- **Hard breaks every 75-90 min.** Real breaks, away from the screen. Skipping them is the #1 cause of post-mob exhaustion.
- **Mob the hard half-hour, solo the easy two hours.** Don't mob the whole day; pick the high-leverage segment.
- **Retro every session, in writing.** A mob without a retro is theater; the retro is where the team actually learns.
- **Senior pairs with junior on rotation.** Always alternate experience levels at the keyboard; otherwise juniors only ever drive.

## AI-agent gotchas
- **The agent is not a navigator.** LLMs will happily propose code; in mob mode that overrides human navigators and collapses the practice. Lock the agent to "observe + capture" via system prompt.
- **Transcript hallucination.** Speech-to-text mishears jargon ("Kafka" → "kept ya"); the agent will then invent decisions that were never made. Always cite timestamp + speaker in the scribe output, and require human sign-off on the decisions section before commit.
- **Rotation timing drift.** If the agent runs the timer, beware of model-call latency causing 30-60s skew. Use a local `setInterval` / shell timer; the agent only *announces*.
- **Parking-lot inflation.** Agents over-extract every aside as a parking-lot item; the list becomes 40 entries no one revisits. Cap at 10 per session, ranked by how often the topic was raised.
- **Privacy leak.** Mob screens contain prod credentials, PII pasted into IDEs, customer names, internal URLs. Run `password-scrubber-agent` before any external sharing of the transcript, retro, or PR description.
- **Bias toward "everything went great."** Agents inherit the meeting's positive close; retros come out anodyne. Force a structured "what slowed us, what was awkward, what should we stop" prompt.
- **No HITL on commits.** Never let the agent merge `mob done` to main automatically. The human mob owns the green-light; the agent only drafts the commit message.
- **Remote-only blind spot.** Agents miss body language; a confused face is invisible in the transcript. Schedule a brief "any silent confusion?" round-robin every rotation.
- **Onboarding paradox.** Agents will cheerfully scribe for a 2-person "mob" — but that's pairing. Refuse to start scribing with <3 humans; tell the user to use the pair-programming methodology.

## References
- Zuill, W. (2014). "Mob Programming: A Whole Team Approach." Agile Alliance Experience Report. https://www.agilealliance.org/resources/experience-reports/mob-programming-agile2014/
- Buchner, M. (2020). "Remote Mob Programming." https://www.remotemobprogramming.org/
- Falco, M. (2018). "Mob Programming Guidebook." https://mobprogrammingguidebook.com/
- mob.sh CLI. https://mob.sh
- Mobti.me timer. https://mobti.me
- Llewellyn Falco — Strong-Style Pairing. https://llewellynfalco.blogspot.com/2014/06/llewellyns-strong-style-pairing.html
- Sibling methodology in this repo: `free/dev/software-developer/pair-programming/` (start here before mobbing).
