# Faion Network

**Build your solopreneur business with AI-powered development framework.**

You're one person. You want to earn $20K+/month working for yourself. The challenge? You need to be a product manager, developer, marketer, and business strategist — all at once.

**Faion Network solves this.** It's a complete AI framework that gives you 28 specialized skills and 32 autonomous agents. Each one is an expert in their field — from market research to landing page design to SEO optimization.

Stop reading endless guides. Stop watching tutorials. Start building.

---

## What You Get

| Component | Count | Purpose |
|-----------|-------|---------|
| **Skills** | 28 | Domain expertise (SDD, SEO, Django, Product Research...) |
| **Agents** | 32 | Autonomous workers (execute tasks, research, write specs) |
| **Methodologies** | 282 | Battle-tested frameworks (PMBOK, BABOK, UX, Growth) |

### Who This Is For

- **Aspiring Solopreneurs** — Turn your skills into a $20K/month business
- **Developers** — Ship products, not just code
- **Founders** — Move fast with AI-powered workflows

---

## Quick Start

Get your first result in under 5 minutes.

```bash
# 1. Clone the repository
git clone https://github.com/faionfaion/faion-network.git ~/.claude

# 2. Run a command
claude

# Then type:
/faion-net
```

That's it. You now have access to the entire framework.

---

## Installation

### Prerequisites

- **Claude Code** CLI installed ([docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code))
- **Node.js** 18+ (for some skills)
- **Python** 3.9+ (for Django, Flask skills)

### Step-by-Step

**Option A: Fresh Installation**

```bash
# Clone to Claude's config directory
git clone https://github.com/faionfaion/faion-network.git ~/.claude

# Verify installation
ls ~/.claude/skills  # Should show 28 faion-* folders
ls ~/.claude/agents  # Should show 32 faion-*.md files
```

**Option B: Add to Existing Setup**

```bash
# Backup your current setup
cp -r ~/.claude ~/.claude.backup

# Clone skills and agents only
cd ~/.claude
git clone https://github.com/faionfaion/faion-network.git temp
cp -r temp/skills/faion-* skills/
cp -r temp/agents/faion-* agents/
cp -r temp/commands/* commands/
rm -rf temp
```

**Option C: Selective Installation**

Only want specific skills?

```bash
# Example: Install only SEO and Django skills
git clone --depth 1 https://github.com/faionfaion/faion-network.git temp
cp -r temp/skills/faion-seo ~/.claude/skills/
cp -r temp/skills/faion-dev-django ~/.claude/skills/
rm -rf temp
```

---

## Configuration

### Required Settings

Add to your `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
  }
}
```

### Optional: API Keys

Some skills benefit from external APIs:

```bash
# ~/.secrets/openai (for image generation)
export OPENAI_API_KEY="sk-..."

# ~/.secrets/cloudflare (for domain management)
export CF_EMAIL="your@email.com"
export CF_API_KEY="..."
```

---

## Usage Examples

### Start a New Project

```bash
claude
# Type: /faion-project-bootstrap
```

This will:
1. Guide you through idea validation
2. Create project constitution
3. Set up SDD documentation structure
4. Generate initial tasks

### Write a Specification

```bash
claude
# Type: /faion-writing-specifications
```

Interactive dialogue to create a complete spec.md with:
- Problem statement
- Target audience
- Acceptance criteria
- Edge cases

### Research Competitors

```bash
claude
# Type: /faion-product-research
```

Triggers research agents to analyze:
- Market size (TAM/SAM/SOM)
- Competitor features and pricing
- User pain points from Reddit/forums

### Build a Landing Page

```bash
claude
# Type: /faion-landing-page
```

Creates high-converting landing with:
- Value proposition
- Social proof
- Pricing sections
- SEO optimization

### Execute Tasks

```bash
claude
# Type: /faion-do-all-tasks
```

Autonomously executes all tasks from your backlog:
- Reads specs and designs
- Implements code
- Runs tests
- Moves completed tasks to done/

---

## Skills Overview

### Core Workflow

| Skill | Purpose |
|-------|---------|
| `faion-writing-specifications` | Create spec.md through dialogue |
| `faion-writing-design-docs` | Technical implementation design |
| `faion-writing-implementation-plan` | Task breakdown for execution |
| `faion-make-tasks` | Generate task files from plans |
| `faion-execute-task` | Run single task via agent |
| `faion-do-all-tasks` | Execute entire backlog |

### Research & Discovery

| Skill | Purpose |
|-------|---------|
| `faion-idea-discovery` | Generate and validate business ideas |
| `faion-product-research` | Market size, competitors, personas |
| `faion-project-naming` | Name generation and domain checking |

### Development

| Skill | Purpose |
|-------|---------|
| `faion-dev-django` | Django 5.x patterns and architecture |
| `faion-dev-ui-design` | Component libraries, Storybook |
| `faion-landing-page` | High-converting landing pages |

### Optimization

| Skill | Purpose |
|-------|---------|
| `faion-seo` | Technical SEO, hreflang, schemas |
| `faion-review` | Code and document reviews |
| `faion-reflexion` | Learn from mistakes |

---

## Agents Overview

Agents are autonomous workers. They execute complex tasks independently.

### Research Agents

- `faion-market-researcher` — TAM/SAM/SOM analysis
- `faion-competitor-analyzer` — Feature and pricing comparison
- `faion-persona-builder` — User personas from real feedback
- `faion-pain-point-researcher` — Reddit, forums, reviews

### Implementation Agents

- `faion-task-executor` — Execute SDD tasks
- `faion-task-creator` — Create task files with context
- `faion-api-designer` — API contracts and OpenAPI specs

### Review Agents

- `faion-spec-reviewer` — Specification quality check
- `faion-design-reviewer` — Technical design validation
- `faion-hallucination-checker` — Verify task completion

### Specialized

- `faion-seo-agent` — SEO audits and optimization
- `faion-hooks-expert` — Claude Code hooks creation
- `faion-landing-designer` — Landing page design

---

## Troubleshooting

### Skills Not Found

```
Error: Skill 'faion-*' not found
```

**Solution:** Verify skills are in correct location:
```bash
ls ~/.claude/skills/faion-*/SKILL.md
```

### Permission Denied

```
Error: Permission denied for Bash tool
```

**Solution:** Update settings.json to allow required tools:
```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Write", "Edit"]
  }
}
```

### Agent Not Loading

```
Error: Agent 'faion-*-agent' not available
```

**Solution:** Check agent file exists:
```bash
ls ~/.claude/agents/faion-*.md
```

### Context Too Large

```
Error: Context limit exceeded
```

**Solution:** Use `/faion-task-parallelizer` to split large tasks into smaller chunks.

---

## Learn More

**Full Documentation:** [faion.net](https://faion.net)

- 282 Methodologies with step-by-step guides
- Video tutorials
- Real success stories
- Premium support

### Licensing

- **Free:** Personal learning, non-commercial projects (attribution required)
- **Plus ($19/mo):** Your own commercial products
- **Pro ($35/mo):** + Client and agency work
- **Ultimate ($2,100/yr):** 20 Pro licenses

---

## Community

- **Website:** [faion.net](https://faion.net)
- **Author:** Ruslan Faion (ruslan@faion.net)

---

*Built with Faion Network — the AI framework for solopreneurs.*
