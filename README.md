# Faion Network

**Build your solopreneur business with AI-powered development framework.**

You're one person. You want to earn $20K+/month working for yourself. The challenge? You need to be a product manager, developer, marketer, and business strategist — all at once.

**Faion Network solves this.** It's a complete AI framework with 15 role-based skills and 501 battle-tested methodologies. Each skill is an expert in their field — from market research to product management to marketing.

Stop reading endless guides. Stop watching tutorials. Start building.

---

## What You Get

| Component | Count | Purpose |
|-----------|-------|---------|
| **Skills** | 15 | Role-based expertise (Product, Dev, Marketing, DevOps, UX, BA, PM, HR...) |
| **Agent** | 1 | Task executor with maximum autonomy (YOLO mode) |
| **Methodologies** | 501 | Battle-tested frameworks (Project Management Framework 7/8, Business Analysis Framework, 10 Usability Heuristics, GTM) |

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

# 2. Run Claude Code
claude

# 3. Type the main orchestrator command:
/faion-net
```

That's it. You now have access to the entire framework.

---

## Installation

### Prerequisites

- **Claude Code** CLI installed ([docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code))
- **Node.js** 18+ (for frontend development)
- **Python** 3.11+ (for Django/Flask projects)

### Step-by-Step

**Option A: Fresh Installation**

```bash
# Clone to Claude's config directory
git clone https://github.com/faionfaion/faion-network.git ~/.claude

# Verify installation
ls ~/.claude/skills      # Should show 15 faion-* folders
ls ~/.claude/agents      # Should show faion-task-executor-YOLO-agent.md
```

**Option B: Add to Existing Setup**

```bash
# Backup your current setup
cp -r ~/.claude ~/.claude.backup

# Clone and merge
git clone https://github.com/faionfaion/faion-network.git temp
cp -r temp/skills/faion-* ~/.claude/skills/
cp -r temp/agents/faion-* ~/.claude/agents/
cp -r temp/docs/* ~/.claude/docs/
rm -rf temp
```

---

## Configuration

### Recommended Settings

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
# ~/.secrets/openai (for DALL-E image generation)
export OPENAI_API_KEY="sk-..."

# ~/.secrets/cloudflare (for domain management)
export CF_EMAIL="your@email.com"
export CF_API_KEY="..."
```

---

## Usage Examples

### Start with Main Orchestrator

```bash
claude
# Type: /faion-net
```

The main orchestrator routes your request to the appropriate skill:
- Research questions → `faion-researcher`
- Product planning → `faion-product-manager`
- Development tasks → `faion-software-developer`
- Marketing needs → `faion-marketing-manager`

### SDD Workflow

```bash
claude
# Type: /faion-sdd
```

Specification-Driven Development workflow:
1. Create specifications (spec.md)
2. Design architecture (design.md)
3. Generate implementation plan
4. Execute tasks with quality gates

### Execute Feature with Quality Gates

```bash
claude
# Type: /faion-feature-executor
```

Sequential task execution with:
- Test runs after each task
- Coverage verification
- Code review cycle until all issues fixed
- Automatic task status updates

---

## Skills Overview (15)

### Orchestrators

| Skill | Purpose |
|-------|---------|
| `faion-net` | Universal orchestrator — routes to appropriate domain skill |
| `faion-sdd` | SDD workflow (specs, designs, tasks, lifecycle) |
| `faion-feature-executor` | Execute tasks with quality gates |

### Domain Skills

| Skill | Methodologies | Purpose |
|-------|---------------|---------|
| `faion-researcher` | 29 | Idea generation, market research, personas, validation |
| `faion-product-manager` | 33 | MVP/MLP, RICE, MoSCoW, roadmaps, OKRs |
| `faion-software-developer` | 82 | Python, JS/TS, Django, React, APIs, testing |
| `faion-devops-engineer` | 30 | Docker, K8s, Terraform, CI/CD, monitoring |
| `faion-ml-engineer` | 30 | LLM APIs, RAG, embeddings, AI Agents, MCP |
| `faion-marketing-manager` | 77 | GTM, landing pages, SEO/GEO/AEO, ads, email |
| `faion-project-manager` | 46 | Project Management Framework 7/8, PM tools, risk, EVM, AI in PM |
| `faion-business-analyst` | 24 | Business Analysis Framework, requirements, stakeholder analysis |
| `faion-ux-ui-designer` | 75 | 10 Usability Heuristics, accessibility, WCAG 2.2 |
| `faion-hr-recruiter` | 45 | Talent acquisition, employer branding, onboarding |
| `faion-communicator` | 9 | Mom Test, conflict resolution, SPIN selling |
| `faion-claude-code` | — | Skills, agents, hooks, MCP server configuration |

---

## Agent

One autonomous executor for maximum efficiency:

| Agent | Purpose |
|-------|---------|
| `faion-task-executor-YOLO-agent` | Maximum autonomy task execution. Full framework knowledge, all tools access, no interruptions. |

The agent has access to all 502 methodologies and executes tasks using the appropriate skill's knowledge.

---

## Methodology Categories

| Prefix | Domain | Count |
|--------|--------|-------|
| M-RES-* | Research | 29 |
| M-PRD-* | Product Management | 33 |
| M-DEV-*, M-BP-* | Development | 82 |
| M-OPS-*, M-DOC-*, M-K8S-*, M-TF-* | DevOps | 30 |
| M-ML-* | ML/AI | 30 |
| M-PM-*, M-PMT-* | Project Management | 46 |
| M-BA-* | Business Analysis | 24 |
| M-UX-* | UX/UI Design | 75 |
| M-COM-* | Communication | 9 |
| M-SDD-* | SDD Workflow | 17 |
| semantic naming | Marketing | 77 |
| semantic naming | HR/Recruiting | 45 |
| **TOTAL** | | **501** |

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

### Context Too Large

```
Error: Context limit exceeded
```

**Solution:** Use Task tool with subagents to split work into smaller chunks.

---

## Updating

Keep your framework up to date:

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

- 501 Methodologies with step-by-step guides
- Real success stories
- Premium support

### Licensing

- **Free:** Personal learning, non-commercial projects (attribution required)
- **Plus ($19/mo):** Your own commercial products
- **Pro ($35/mo):** + Client and agency work
- **Team ($35/seat/mo):** Organization management, invites, roles
- **Ultimate ($2,100/yr):** 20 seats, 70% discount

---

## Community

- **Website:** [faion.net](https://faion.net)
- **Author:** Ruslan Faion (ruslan@faion.net)

---

*Built with Faion Network — the AI framework for solopreneurs.*
