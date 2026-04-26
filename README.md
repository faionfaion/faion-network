# Faion Network

**Build your solopreneur business with AI-powered development framework.**

You're one person. You want to earn $20K+/month working for yourself. The challenge? You need to be a product manager, developer, marketer, and business strategist — all at once.

**Faion Network solves this.** A complete AI framework with 52 domain knowledge bases and 1,300+ battle-tested methodologies, plus applied-workflow skills for SDD execution, multi-agent brainstorming, and session-based improvement.

Stop reading endless guides. Stop watching tutorials. Start building.

---

## What You Get

| Component | Count | Purpose |
|-----------|-------|---------|
| **Umbrella skill** | 1 | `faion` — 52 domain knowledge bases routed by topic |
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
/faion
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
ls ~/.claude/skills       # faion, faion-brainstorm, faion-feature-executor, ...
ls ~/.claude/skills/faion/knowledge/   # free/ solo/ pro/ geek/
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
# Invoke: /faion
```

All domain knowledge lives under `faion/knowledge/<tier>/<group>/<name>/`, partitioned by pricing tier. Read on demand:

- **Free (8):** `knowledge/free/dev/python-developer/`, `knowledge/free/dev/javascript-developer/`, `knowledge/free/marketing/marketing-manager/`, ...
- **Solo (13):** `knowledge/solo/dev/frontend-developer/`, `knowledge/solo/sdd/sdd/`, `knowledge/solo/infra/server-craft/`, ...
- **Pro (24):** `knowledge/pro/infra/devops-engineer/`, `knowledge/pro/ba/business-analyst/`, `knowledge/pro/marketing/growth-marketer/`, ...
- **Geek (7):** `knowledge/geek/ai/ai-agents/`, `knowledge/geek/ai/rag-engineer/`, `knowledge/geek/ai/claude-code/`, ...

Full tier map: [faion/SKILL.md](skills/faion/SKILL.md). Authoritative path list: [tier-manifest.json](skills/tier-manifest.json).

### SDD Workflow

Read `knowledge/solo/sdd/sdd/` and `knowledge/solo/sdd/sdd-planning/` for specs, designs, implementation plans. Then:

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
├── faion/                   # Umbrella — all domain knowledge
│   ├── SKILL.md
│   ├── CLAUDE.md
│   └── knowledge/
│       ├── free/          (8)  dev core (Python, JS, testing, quality, backend/devtools, full-stack) + marketing-manager router
│       ├── solo/         (13)  frontend, API, architect, automation, server-craft, SDD, product planning/ops, UI, content, SEO, comms
│       ├── pro/          (24)  backend systems/enterprise, DevOps/CI-CD/infra, PM, product-manager, BA, UX research, growth/GTM/PPC/SMM/CRO, research, HR
│       └── geek/          (7)  ML engineer, AI agents, RAG, ML ops, multimodal AI, LLM integration, Claude Code
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

Only top-level skills are invocable: `faion`, `faion-brainstorm`, `faion-feature-executor`, `faion-improver`, `faion-sdd-execution`, `faion-media-ops`.

Domain knowledge is NOT invocable as sub-skills — load via Read. Knowledge paths are tier-prefixed:

```
Read: ~/.claude/skills/faion/knowledge/free/dev/python-developer/SKILL.md
Read: ~/.claude/skills/faion/knowledge/solo/sdd/sdd/SKILL.md
Read: ~/.claude/skills/faion/knowledge/pro/infra/devops-engineer/SKILL.md
Read: ~/.claude/skills/faion/knowledge/geek/ai/ai-agents/SKILL.md
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
