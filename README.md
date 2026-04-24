# Faion Network

**Build your solopreneur business with AI-powered development framework.**

You're one person. You want to earn $20K+/month working for yourself. The challenge? You need to be a product manager, developer, marketer, and business strategist — all at once.

**Faion Network solves this.** A complete AI framework with 52 domain knowledge bases and 1,300+ battle-tested methodologies, plus applied-workflow skills for SDD execution, multi-agent brainstorming, and session-based improvement.

Stop reading endless guides. Stop watching tutorials. Start building.

---

## What You Get

| Component | Count | Purpose |
|-----------|-------|---------|
| **Umbrella skill** | 1 | `faion-knowledge` — 52 domain knowledge bases routed by topic |
| **Applied skills** | 5 | Brainstorm, SDD execution, feature executor, improver, media ops |
| **Methodologies** | 1,300+ | Battle-tested frameworks across dev, AI, infra, product, PM, BA, UX, marketing, research |

### Who This Is For

- **Aspiring Solopreneurs** — Turn your skills into a $20K/month business
- **Developers** — Ship products, not just code
- **Founders** — Move fast with AI-powered workflows

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/faionfaion/faion-network.git ~/.claude

# 2. Run Claude Code
claude

# 3. Invoke the knowledge umbrella:
/faion-knowledge
```

---

## Installation

### Prerequisites

- **Claude Code** CLI ([docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code))
- **Node.js** 18+ (for frontend development)
- **Python** 3.11+ (for Django/FastAPI projects)

### Fresh Installation

```bash
git clone https://github.com/faionfaion/faion-network.git ~/.claude

# Verify
ls ~/.claude/skills       # faion-knowledge, faion-brainstorm, faion-feature-executor, ...
ls ~/.claude/skills/faion-knowledge/knowledge/   # dev/ ai/ infra/ product/ pm/ ba/ ux/ marketing/ research/ comms/ sdd/
```

### Merge into Existing Setup

```bash
cp -r ~/.claude ~/.claude.backup
git clone https://github.com/faionfaion/faion-network.git temp
cp -r temp/skills/* ~/.claude/skills/
cp -r temp/agents/faion-* ~/.claude/agents/ 2>/dev/null || true
rm -rf temp
```

---

## Configuration

### Recommended Settings

Add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
  }
}
```

### Optional: API Keys

```bash
# ~/.secrets/openai (for image generation)
export OPENAI_API_KEY="sk-..."

# ~/.secrets/cloudflare (for domain management)
export CF_EMAIL="your@email.com"
export CF_API_KEY="..."
```

---

## Usage

### Knowledge Umbrella

```bash
claude
# Invoke: /faion-knowledge
```

All domain knowledge lives under `faion-knowledge/knowledge/<group>/<name>/`. Read domain content on demand:

- Dev: `knowledge/dev/python-developer/`, `knowledge/dev/frontend-developer/`, ...
- AI: `knowledge/ai/ai-agents/`, `knowledge/ai/rag-engineer/`, ...
- Infra: `knowledge/infra/devops-engineer/`, `knowledge/infra/server-craft/`, ...
- Product/PM/BA/UX/Marketing/Research/Comms/SDD — see [faion-knowledge/SKILL.md](skills/faion-knowledge/SKILL.md)

### SDD Workflow

Read `knowledge/sdd/sdd/` and `knowledge/sdd/sdd-planning/` for specs, designs, implementation plans. Then:

```bash
/faion-feature-executor {project} {feature}
```

Sequential task execution with test runs, coverage checks, and code review cycles.

### Multi-Agent Brainstorm

```bash
/faion-brainstorm How to improve our deployment pipeline?
```

Diverge (10 research agents) → Converge (synthesis) → Review (8 adversarial reviewers) → Finalize.

### Session Improvement

```bash
/faion-improver
```

Capture patterns, mistakes, and decisions from the current session into `.aidocs/memory/`.

---

## Knowledge Structure

```
skills/
├── faion-knowledge/                   # Umbrella — all domain knowledge
│   ├── SKILL.md
│   ├── CLAUDE.md
│   └── knowledge/
│       ├── dev/          (13)  Python, JS, Go, Rust, Java, C#, backend, frontend, API, testing, architecture, automation, code quality
│       ├── ai/            (7)  ML, agents, RAG, ML ops, multimodal, LLM integration, Claude Code
│       ├── infra/         (4)  DevOps, CI/CD, infrastructure, server craft
│       ├── product/       (3)  PM, planning, operations
│       ├── pm/            (3)  Project, Agile, Traditional
│       ├── ba/            (3)  BA, core, modeling
│       ├── ux/            (5)  UX/UI, UI, UX research, user research, accessibility
│       ├── marketing/     (8)  Marketing, GTM, content, growth, CRO, SEO, PPC, SMM
│       ├── research/      (2)  Researcher, market research
│       ├── comms/         (2)  Communicator, HR recruiter
│       └── sdd/           (2)  SDD, SDD planning
├── faion-brainstorm/                  # Multi-agent diverge/converge/review
├── faion-sdd-execution/               # Quality gates, reflexion learning
├── faion-feature-executor/            # Sequential SDD task execution
├── faion-improver/                    # Session-based audit/improve loop
└── faion-media-ops/                   # Media pipeline templates
```

Each methodology = 5-file pattern: `README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`.

---

## Troubleshooting

### Skill Not Found

```
Error: Skill 'faion-*' not found
```

Only top-level skills are invocable: `faion-knowledge`, `faion-brainstorm`, `faion-feature-executor`, `faion-improver`, `faion-sdd-execution`, `faion-media-ops`.

Domain knowledge is NOT invocable as sub-skills — load via Read:

```
Read: ~/.claude/skills/faion-knowledge/knowledge/dev/python-developer/SKILL.md
```

### Permission Denied

Update `settings.json`:

```json
{"permissions": {"allow": ["Bash", "Read", "Write", "Edit"]}}
```

---

## Updating

```bash
cd ~/.claude
./scripts/update.sh
```

Or manually:
```bash
cd ~/.claude
git pull origin master
```

---

## Learn More

**Full Documentation:** [faion.net](https://faion.net)

### Licensing

- **Free:** Personal learning, non-commercial (attribution required)
- **Solo ($19/mo):** Ship your own commercial products
- **Pro ($35/mo):** Client and agency work, full professional toolkit
- **Geek ($99/mo):** AI agents, ML, RAG — advanced methodologies
- **Team ($35/seat/mo):** Organization management, Pro access per seat
- **Ultimate ($2,100/yr):** 20 seats, Geek access, dedicated support

---

## Community

- **Website:** [faion.net](https://faion.net)
- **Author:** Ruslan Faion (ruslan@faion.net)

---

*Built with Faion Network — the AI framework for solopreneurs.*
