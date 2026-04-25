# Agent Integration — Pair Programming

## When to use
- Solo developer wants a constant navigator on complex/unfamiliar code, especially TDD ping-pong style.
- Onboarding a new repo: agent plays "tour guide", explains architecture, gotchas, hot files, history, while user drives.
- Strong-style learning: human is novice, agent must verbalize intent before any keystroke; user types every character.
- Rubber-ducking with a thinking partner that asks clarifying questions, suggests edge cases, names risks.
- Resident "navigator" during late-night solo coding when no human pair is available.

## When NOT to use
- Real interpersonal pair programming dynamics (mentoring, social pressure, knowledge distribution, bus-factor reduction). Agents simulate poorly.
- Tasks already well-specified and mechanical — agent is overhead vs straight delegation.
- Sensitive/critical code with regulatory review requirements where two human approvers are mandatory.
- Tasks where the user's growth depends on struggle (interview prep, deliberate practice). Agent removes useful friction.
- Long architectural debates — agent will sycophantically agree; better to use multi-agent brainstorm (`faion-brainstorm`).

## Where it fails / limitations
- Agent has no shared mental model of the codebase between sessions; "pair memory" resets without scaffolding.
- Strong-style purity broken: in CLI tooling agents type the code themselves, not the human. "Navigator" boundary is fuzzy.
- Agent rarely pushes back hard; lacks the social authority a senior pair brings. Disagreement-driven design loss.
- No social/team benefits (knowledge distribution, mentoring, morale). Don't claim agent pairing replaces team pairing.
- Token/cost: 4-6h continuous pairing burns large context windows. Forces compaction → loses early decisions.
- Async fatigue cuts both ways: human zones out; agent can't notice or call a break.

## Agentic workflow
Pick a style explicitly: ping-pong (TDD), tour guide (read-only narration), or strong-style (human types only). For ping-pong: an agent writes one failing test, human makes it pass, human writes next failing test, agent makes it pass — alternating commits. For tour guide: agent uses `Read` and `Glob` to walk the codebase from an entry point, narrating; human does not type code. For strong-style: agent emits typing instructions ("now type `def parse(s: str) -> dict:`") and refuses to use Edit tool itself; human pastes/types. Maintain a session journal so memory survives compaction.

### Recommended subagents
- `pair-navigator` — strategic-level partner: asks "what about empty input?", names patterns, spots risks. Sonnet.
- `tdd-pingpong` — alternates roles; tracks whose turn it is in a session-state file.
- `tour-guide` — read-only repo narrator; drives Glob/Read/Grep, explains architecture and history (`git log -p`).
- `mob-facilitator` — for group sessions, time-boxes, rotates drivers, tracks decisions.
- `simplify` (built-in skill) — periodic "step back, simplify what we just wrote" pass.
- `claude-code` IDE pairing via VS Code Claude Code extension or `tmux`-attached `claude` session.

### Prompt pattern
Strong-style entry:
```
We're pairing in strong-style: I drive, you navigate.
Constraints:
- You may NOT use Edit/Write tools. Output only English instructions or ≤6-line code snippets I will type.
- Before any code, state intent in one sentence.
- Ask me to confirm understanding when introducing a new concept.
- After every 25-min block, suggest a 5-min break and a role discussion.
Goal: <task>. Current file: <path>.
```

Ping-pong entry:
```
TDD ping-pong. I write failing test → you make it pass → you write next failing test → I make it pass.
Hard rules:
- You only Edit production code on your "make it pass" turn; never tests on that turn.
- Write the simplest code to pass — refactor in a separate commit.
- After each green, commit with "test:" or "feat:" prefix.
Start by reading <test file>; on my "your turn" signal, take the make-pass step.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code CLI) | Headless pairing partner in terminal | https://docs.anthropic.com/en/docs/claude-code |
| VS Code Claude Code extension | In-IDE pairing with shared context | Marketplace |
| `tmux` + shared session | Two-pane pair: agent in one, code in other | system pkg |
| `mob` (mob.sh) | Mob/pair turn timer + handoff via git | https://mob.sh |
| `pomo` / `pomodoro` CLI | 25/5 timer to enforce breaks | many implementations |
| `git autosave` aliases | Frequent commits to support short turns | git config |
| `tig` / `lazygit` | Terminal git UI for pair-friendly review | system pkg |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| VS Code Live Share | SaaS (free) | Partial — humans pairing; agent joins via terminal | Co-edit + co-debug. Best general-purpose remote pair. |
| Tuple | SaaS (paid, macOS) | No (human-only) | Lowest latency human pair; pair an agent in a separate terminal alongside. |
| Pop | SaaS (free tier) | Partial | Multi-cursor screen sharing for human pair; agent on side. |
| CodeTogether | SaaS | Partial | Cross-IDE; agent runs in headless terminal. |
| GitHub Codespaces / Gitpod | SaaS | Yes | Disposable pairing env with agent + human + tests. |
| Anthropic Claude Code | SaaS | Yes — primary integration | Use as the navigator runtime. |
| Cursor / Windsurf | SaaS | Yes — IDE-native AI pair | Alternative if not on Claude Code. |
| GitHub Copilot Chat / Workspace | SaaS | Partial — limited tool use | Inline navigator-lite. |

## Templates & scripts
See `templates.md` for ground rules, session structures, and ping-pong scripts. Lightweight session journal:

```bash
#!/usr/bin/env bash
# pair-journal.sh — log start/switch/end with timestamp; survives agent compaction
set -euo pipefail
JOURNAL="${PAIR_JOURNAL:-.pair-journal.md}"
EVENT="${1:?event required: start|switch|note|end}"; shift || true
echo "- $(date -Iseconds) $EVENT $*" >> "$JOURNAL"
case "$EVENT" in
  start) echo "Goal: $*" >> "$JOURNAL" ;;
  end)   git add "$JOURNAL" && git commit -m "chore: pair session $(date +%F)" ;;
esac
```

## Best practices
- Declare the style up-front in prompt: ping-pong / tour guide / strong-style. Mixed-style pairing degrades to "agent does it all".
- Keep session goal in a single sentence at the top of the journal; agent re-reads on every compaction.
- Commit at every green test or natural break; supports clean handoff and easy revert.
- Time-box sessions to 90-120 min with explicit breaks. Long sessions degrade both human focus and agent context quality.
- Force the agent to ask "should I" before any non-trivial change; sycophantic auto-edit kills the pair dynamic.
- Use a separate `simplify` pass (built-in skill) at the end of each session to undo over-engineering.
- Track outcomes (bugs found, tests written) per session; compare vs solo. Don't assume agent pairing helps without measurement.

## AI-agent gotchas
- Strong-style violation: agent has tools to Edit and will quietly use them. Constrain via prompt + remove Edit/Write from allowed tools if possible.
- Ping-pong cheating: agent writes test AND prod code in the same turn. Enforce turn-state in journal; abort when violated.
- Memory loss across compaction: decisions made hour 1 forgotten by hour 3. Mitigate with `.pair-journal.md` re-read on each turn.
- Sycophancy: agent agrees with bad designs; structurally lacks the senior-engineer "no". Periodically run a hostile-review subagent ("explain why this design is wrong") as counterweight.
- Scope creep: agent finds adjacent issues, expands the task. Pin scope in journal; reject out-of-scope edits in turn-end check.
- Fatigue invisibility: agent can't notice human fatigue. Hard-coded Pomodoro timer with mandatory 5-min breaks compensates.
- Privacy: agent reads .env, secrets, customer data while exploring. Pre-scope allowed paths or use `password-scrubber-agent`.
- Cost: tour-guide sessions over a 50-file repo blow context windows. Pre-summarize the repo (`tree -L 2`, `Glob` of key files) and inject the summary instead of letting the agent crawl freely.

## References
- Laurie Williams — "Pair Programming Illuminated"
- Martin Fowler — "On Pair Programming" (https://martinfowler.com/articles/on-pair-programming.html)
- Llewellyn Falco — "Strong-Style Pairing"
- Kent Beck — "Test-Driven Development: By Example" (ping-pong)
- Tuple — "The Pairing Tool" handbook
- Anthropic — Claude Code Best Practices
