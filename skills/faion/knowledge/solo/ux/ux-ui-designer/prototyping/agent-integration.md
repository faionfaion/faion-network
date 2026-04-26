# Agent Integration — Prototyping

## When to use
- Agent needs to specify which screens/flows to prototype before handing off to a designer
- Generating a structured prototype plan document (objectives, scope, fidelity, test tasks) from a design brief
- Producing prototype testing scripts and observation frameworks for user sessions
- Synthesizing prototype test findings into prioritized issue lists
- Deciding fidelity level given project constraints (time, complexity, what needs to be learned)

## When NOT to use
- The interaction is too complex or motion-dependent for text-based specification (agent can plan but cannot build the prototype itself)
- A live coded prototype is needed — agent can write React/HTML prototypes but this crosses from planning into implementation
- No clear testing hypothesis exists — prototyping without defined learning goals wastes cycles
- Post-launch optimization work — use A/B testing or analytics instead of new prototypes

## Where it fails / limitations
- Agents cannot create or interact with Figma/Framer/ProtoPie files directly (no native API write access via Claude)
- Agent-written HTML/CSS prototypes miss micro-interaction nuance that affects perceived quality in user tests
- Prototype scope decisions made by agent without domain knowledge may omit edge cases that matter to real users
- Agent synthesis of test notes is only as good as the notes provided — thin observation data → thin insights

## Agentic workflow
A Claude subagent receives a feature brief (user goal, technical constraints, open design questions) and outputs a complete `Prototype Plan` document: objectives, fidelity rationale, scope (included/excluded flows), interactive element table, and a usability test script with tasks. After human-run testing, a second agent pass synthesizes raw session notes into a ranked issue list with severity ratings and recommended design changes.

### Recommended subagents
- `faion-sdd-executor-agent` — structure the prototype plan as an SDD task and produce the deliverable document
- General Claude subagent with research role — synthesize test session notes into affinity-mapped themes

### Prompt pattern
```
You are a UX designer creating a prototype plan.
Input: [feature brief, user goals, constraints, open questions]
Output a markdown Prototype Plan with:
1. Learning objectives (max 3, each a testable question)
2. Fidelity decision with rationale
3. In-scope flows (numbered steps per flow)
4. Interactive elements table (Element | Interaction | Expected behavior)
5. Usability test script (intro, 3-5 tasks, wrap-up)
Flag any flows you recommend excluding with reason.
```

```
You are a UX researcher synthesizing prototype test notes.
Input: [raw session notes, N=X participants]
Output:
- Top 5 issues ranked by severity (Critical/Major/Minor)
- Per-issue: observation, affected flow, suggested fix
- Positive findings worth preserving in final design
- Recommended next step: iterate and re-test, or proceed to development?
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Playwright | Automate interaction with HTML/code prototypes for smoke-test validation | `npm install -D playwright` / https://playwright.dev |
| Puppeteer | Screenshot HTML prototypes at multiple viewport sizes | `npm install puppeteer` / https://pptr.dev |
| http-server | Serve static HTML prototype locally without build step | `npm install -g http-server` / https://github.com/http-party/http-server |
| Storybook | Component-level interactive prototyping in code (React, Angular, Vue) | `npx storybook@latest init` / https://storybook.js.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial (REST read) | Read-only API can export frames/components; prototype creation requires manual UI |
| Maze | SaaS | Partial | Unmoderated test platform; create tests via UI, export results as CSV for agent synthesis |
| UserTesting | SaaS | No agent API | Session recordings exported manually; transcripts can be fed to agent for synthesis |
| ProtoPie Connect | SaaS/desktop | No | Advanced animations; no scriptable API |
| Framer | SaaS | No direct API | Code components (React) embeddable; agent can write component code |
| Loom | SaaS | No | Useful for async stakeholder reviews of prototype walkthroughs |

## Templates & scripts
See `templates.md` for the full `Prototype Plan` and `Prototype Testing Notes` templates. Below is a minimal bash script to scaffold a code prototype directory:

```bash
#!/usr/bin/env bash
# scaffold-prototype.sh — create a minimal HTML click-through prototype
# Usage: bash scaffold-prototype.sh my-feature 3
FEATURE="${1:?Usage: $0 <feature-name> <num-screens>}"
NUM="${2:-3}"
mkdir -p "prototype-${FEATURE}"
for i in $(seq 1 "$NUM"); do
  cat > "prototype-${FEATURE}/screen${i}.html" <<HTML
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>${FEATURE} — Screen ${i}</title>
<style>body{font-family:sans-serif;max-width:375px;margin:auto;padding:1rem}</style>
</head>
<body>
<p><strong>Screen ${i}</strong> — replace with design</p>
$([ "$i" -lt "$NUM" ] && echo "<a href='screen$((i+1)).html'>Next →</a>")
$([ "$i" -gt 1 ] && echo "<a href='screen$((i-1)).html'>← Back</a>")
</body></html>
HTML
done
echo "Prototype scaffolded: prototype-${FEATURE}/ with ${NUM} screens"
echo "Serve with: npx http-server prototype-${FEATURE}/"
```

## Best practices
- Always write learning objectives before choosing fidelity — fidelity follows what you need to learn, not timeline pressure
- Prototype the riskiest assumption in the design, not the easiest-to-build flow
- Use realistic content (real product names, plausible data) — placeholder text invalidates navigation and reading behavior tests
- Limit moderated test tasks to 3-5 per session; more tasks produce fatigue, not more insight
- Document "what we did NOT prototype and why" — this prevents stakeholder scope creep during handoff
- After testing, produce a diff of the pre-test prototype plan vs. post-test findings before starting iteration

## AI-agent gotchas
- Agent-generated test scripts may include leading questions ("did you find it easy to...") — review all questions for neutrality before use
- Synthesis of test notes must not average away minority findings; a single user who could not complete a critical task is a severity-1 issue regardless of sample size
- Human-in-loop checkpoint: agent must not decide unilaterally to "proceed to development" — that decision belongs to the designer/PM after reviewing the synthesis report
- Fidelity recommendations from agent are based on described constraints; agent cannot assess stakeholder risk appetite or political pressures that influence real fidelity choices
- Code prototypes written by agent are not production code — they should not be committed to the main codebase or used as a basis for implementation without full engineering review

## References
- https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma
- https://www.gv.com/sprint/ (Design Sprint by Jake Knapp)
- https://www.nngroup.com/articles/prototyping-tools/
- https://www.framer.com/features/prototyping/
- Todd Zaki Warfel, *Prototyping: A Practitioner's Guide* (Rosenfeld Media)
