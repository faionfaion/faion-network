Base directory for this skill: /home/nero/.claude/skills/faion-media-ops

> **Entry point:** `/faion-media-ops` — invoke directly or via `/faion-net`.

# Media Pipeline Factory

**Communication: User's language. Code/docs: English.**

Build and operate complete AI media publishing pipelines from scratch.
Covers: interview, requirements, site, TG channels, prompts, automation.
All outlets are managed centrally by **media-manager** (@nero_media_manager_bot).

Reference implementations (4 active outlets):
- `~/workspace/projects/neromedia-faion-net/` — AI/tech news, 8 languages, 8 TG channels
- `~/workspace/projects/pashtelka-faion-net/` — Ukrainian diaspora in Portugal, 1 channel
- `~/workspace/projects/longlife-faion-net/` — Health & longevity, UA, comic mascot Vita
- `~/workspace/projects/ender-faion-net/` — Roblox media for kids, UA+EN, characters EnderFaion + FaionEnder

Central control plane: `~/workspace/projects/media-manager-faion-net/`

Templates directory: `~/.claude/skills/faion-media-ops/templates/`

---

## Phase 1: DISCOVERY INTERVIEW

Conduct a structured interview. Use `AskUserQuestion` for each section.
Gather ALL answers before proposing anything.

### Q1: Media Identity

```yaml
question: "What media are you creating?"
header: "Media Identity"
multiSelect: false
options:
  - label: "News outlet"
    description: "Breaking news, reports, analysis on a topic/region"
  - label: "Expert blog"
    description: "One voice, deep expertise in a niche"
  - label: "Community media"
    description: "For a specific community (diaspora, profession, hobby)"
  - label: "Brand media"
    description: "Company blog, thought leadership, product updates"
  - label: "Digest/curation"
    description: "Curate and summarize from other sources"
```

### Q2: Topic & Audience

Ask as free text:
- What topics do you cover? (list 3-10)
- Who is your reader? (age, profession, interests, pain points)
- What language(s)? Which is primary?
- What region/city if location-specific?

### Q3: Content Strategy

```yaml
question: "What content types do you need?"
header: "Content Types"
multiSelect: true
options:
  - label: "Breaking news (300-600 words)"
  - label: "In-depth materials (600-1500 words)"
  - label: "Practical guides (800-2000 words)"
  - label: "Opinion/analysis (600-1200 words)"
  - label: "Daily digest (compilation)"
  - label: "Utility alerts (weather, transport, etc.)"
```

Follow-up: How many articles per day? What's the publishing schedule?

### Q4: Channels & Platform

```yaml
question: "Where do you publish?"
header: "Channels"
multiSelect: true
options:
  - label: "Telegram channel"
  - label: "Website (static site)"
  - label: "Both TG + Website"
  - label: "Newsletter (email)"
  - label: "Social media (Twitter/X, Instagram)"
```

### Q5: Brand Voice

Ask as free text:
- Author name/pseudonym (real-sounding or character?)
- Tone: formal, warm, ironic, academic, casual?
- Any specific voice rules? (e.g., "explain terms for immigrants")
- Visual style for images: photo, illustration, comic, minimalist?

### Q6: Content Sources

```yaml
question: "Where does content come from?"
header: "Sources"
multiSelect: true
options:
  - label: "RSS feeds (news sites)"
  - label: "Web search (Google, SearXNG)"
  - label: "APIs (weather, transport, government)"
  - label: "Manual input (editor notes)"
  - label: "Social media monitoring"
```

### Q7: Automation Level

```yaml
question: "How automated should it be?"
header: "Automation"
multiSelect: false
options:
  - label: "Full auto-pilot"
    description: "Generate + publish without human review"
  - label: "Generate + review before publish"
    description: "Generate content, human approves via admin panel"
  - label: "Semi-auto"
    description: "Human writes, AI assists with research/editing"
  - label: "Manual with AI tools"
    description: "Human drives, AI helps on demand"
```

### Q8: Technical

Ask as free text:
- Domain name (existing or new?)
- Hosting server available? (faion-net, own server, need new)
- Telegram bot (existing or create new?)
- Budget for APIs? (Claude, OpenAI images)

---

## Phase 2: PROPOSE FORMAT

Based on interview answers, propose a concrete plan:

### Output Template

```markdown
## Proposed Media Pipeline: {name}

### Architecture
- **Site:** {domain} (Gatsby 5 static site)
- **TG Channel:** @{username} ({language})
- **Schedule:** {N} articles/day, digest at {time}
- **Languages:** {primary} {+ translations if multi-lang}

### Content Plan
| Type | Count/day | Words | Source |
|------|-----------|-------|--------|
| News | {N} | 300-600 | RSS + web search |
| Material | {N} | 600-1500 | Multi-source compilation |
| Guide | {N} | 800-2000 | Research + official sources |
| Digest | 1 | 500-1000 | Day's articles compilation |

### Pipeline Complexity
- **Simple** (5 stages): collect → generate → save → deploy → publish
- **Standard** (8 stages): + editorial plan + research + review
- **Full** (12 stages): + plan review + revision loop + TG caption + image + verify

### Estimated Setup
- Project scaffolding: create all files and configs
- Prompt engineering: {N} templates based on voice/topic
- Initial content: {N} seed articles
- Deploy & test: site + TG channel
- Cron automation: generate + publish schedule

Shall I proceed?
```

---

## Phase 3: SCAFFOLD PROJECT

### 3a. Project Structure

```
{project}/
├── CLAUDE.md                   # @AGENTS.md
├── AGENTS.md                   # Project overview
├── pipeline/
│   ├── __init__.py
│   ├── __main__.py             # python3 -m pipeline
│   ├── cli.py                  # Argument parsing, mode dispatch
│   ├── config.py               # All configuration
│   ├── context.py              # PipelineContext dataclass
│   ├── sdk.py                  # Claude Agent SDK wrapper
│   ├── json_repair.py          # JSON parsing with repair
│   ├── feeds.py                # RSS feed fetcher (if needed)
│   ├── image_gen.py            # OpenAI image generation
│   ├── telegram.py             # TG Bot API wrapper
│   ├── run_report.py           # Execution reporting
│   ├── exceptions.py           # Custom exceptions
│   ├── schemas/                # JSON schemas per stage
│   │   ├── __init__.py
│   │   ├── editorial_plan.json
│   │   ├── generation.json
│   │   ├── review.json
│   │   ├── tg_post.json
│   │   └── digest.json
│   ├── prompts/
│   │   ├── builder.py          # Jinja2 template renderer
│   │   └── templates/
│   │       ├── s0_editorial_plan.xml.j2
│   │       ├── s0b_plan_review.xml.j2
│   │       ├── s2_research.xml.j2
│   │       ├── s3_generate.xml.j2
│   │       ├── s4_review.xml.j2
│   │       ├── s5_revise.xml.j2
│   │       ├── s6_tg_post.xml.j2
│   │       ├── s11_digest.xml.j2
│   │       └── _partials/
│   │           ├── voice_guide.xml
│   │           ├── source_citation.xml
│   │           ├── anti_slop.xml
│   │           └── image_style.txt
│   ├── stages/
│   │   ├── __init__.py
│   │   ├── s0_editorial_plan.py
│   │   ├── s1_collect.py
│   │   ├── s2_research.py
│   │   ├── s3_generate.py
│   │   ├── s4_review.py
│   │   ├── s5_revise.py
│   │   ├── s6_tg_post.py
│   │   ├── s7_save.py
│   │   ├── s7_deploy.py
│   │   ├── s8_verify.py
│   │   ├── s10_pick_publish.py
│   │   └── s11_digest.py
│   └── modes/
│       ├── __init__.py
│       ├── generate.py         # Morning batch
│       ├── publish.py          # Mechanical TG publish
│       └── digest.py           # Evening digest
├── admin/
│   └── app.py                  # Flask admin panel
├── gatsby/
│   ├── gatsby-config.js
│   ├── gatsby-node.js
│   ├── package.json
│   ├── src/
│   │   ├── pages/index.js
│   │   ├── templates/article.js
│   │   ├── components/layout.js, seo.js
│   │   └── styles/global.css
│   ├── deploy.sh
│   └── static/images/
├── scripts/
│   ├── run-pipeline.sh         # Cron entry point
│   ├── send_post.py            # TG sender
│   └── manage_state.py         # State management
├── content/                    # Markdown articles
├── state/
│   ├── plans/                  # Daily editorial plans
│   ├── teasers/                # Pre-generated TG captions
│   ├── runs/                   # Pipeline run reports
│   ├── logs/                   # Pipeline logs
│   ├── summaries.json          # Article index for dedup
│   └── editor_notes.md         # Editor wishes
└── tests/                      # Pytest suite
```

### 3b. Render Templates

Use files from `~/.claude/skills/faion-media-ops/templates/` as starting points.
Render with project-specific values from the interview.

### 3c. Key Patterns

**SDK pattern** (from both projects):
```python
# structured_query — no tools, JSON output
# Disables ALL built-in CLI tools to prevent Opus from using them
options = ClaudeAgentOptions(
    model=model,
    system_prompt=system_prompt,
    permission_mode="bypassPermissions",
    allowed_tools=[],
    disallowed_tools=["Read", "Glob", "Grep", "Bash", "Write", "Edit",
                      "WebSearch", "WebFetch", "Agent", "TodoWrite", "TodoRead"],
    max_turns=1,
    cwd="/tmp",  # Don't load project CLAUDE.md
)

# agent_query — with tools, free text output
options = ClaudeAgentOptions(
    model=model,
    system_prompt=system_prompt,
    permission_mode="bypassPermissions",
    allowed_tools=["WebSearch", "WebFetch", "Read", "Glob"],
    cwd=project_root,
)
```

**Prompt split pattern** (all templates):
```xml
<system>
System prompt here (role, rules, context)
</system>
===SPLIT===
<task>
User prompt here (specific instructions, data, schema)
</task>
```

**Review loop pattern** (proven in both projects):
```python
for cycle in range(MAX_REVIEW_CYCLES):
    review = structured_query(review_prompt, review_schema)
    if review["approved"] and cycle >= 1:  # min 1 revision
        break
    revised = structured_query(revise_prompt, revision_schema)
    ctx.article = revised["article"]
```

**Batch generation pattern** (from pashtelka):
```python
plan = editorial_plan.run()  # Get 10-12 topics
collect()                     # RSS, existing slugs
for topic in plan["articles"]:
    if already_written(topic): continue
    research() → generate() → review_loop() → tg_caption() → image() → save()
    mark_written(topic)
deploy_site()  # Single deploy after all articles
```

**TG text link pattern** (NOT buttons):
```python
# Append link as text, not inline keyboard button
caption = f'{teaser_text}\n\n<a href="{url}">{label} →</a>'
# Prepend invisible link for OG preview
caption = f'<a href="{url}">\u00a0</a>{caption}'
payload = {
    "text": caption,
    "parse_mode": "HTML",
    "link_preview_options": {"prefer_large_media": True, "show_above_text": True, "url": url},
}
```

**Monthly summaries optimization** (from neromedia fix):
```python
# Recent (7 days): full summary for detailed dedup
# Older (8-30 days): title + type only (saves 70% prompt tokens)
# Cap at 80 articles max
```

---

## Phase 4: SETUP INFRASTRUCTURE

### 4a. Telegram Channel

1. Create channel (if new): TG → New Channel → name, username, photo
2. Bot: use existing @nero_open_bot or create via @BotFather
3. Add bot as admin to channel
4. Get chat_id:
   ```bash
   curl "https://api.telegram.org/bot{TOKEN}/getChat?chat_id=@{username}"
   ```
5. Store in `~/workspace/.env`:
   ```
   {PROJECT}_TG_BOT_TOKEN=...
   {PROJECT}_TG_CHANNEL_ID=...
   ```

### 4b. Domain & DNS

1. Cloudflare: Add A record → server IP (proxied)
2. SSL: auto via Cloudflare proxy or Let's Encrypt on server

### 4c. Server (nginx)

```bash
# SSH to server
ssh faion@46.225.58.119 -p 22022

# Create nginx config
sudo nano /etc/nginx/sites-available/{domain}
# Use template from templates/nginx.conf.j2

sudo ln -s /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 4d. Gatsby Site

```bash
cd {project}/gatsby
npm install
npx gatsby develop  # Test locally
npx gatsby build    # Production build
```

### 4e. Admin Panel

```bash
cd {project}/admin
pip install flask
ADMIN_USER=admin ADMIN_PASS=... python3 app.py
# Access at http://localhost:5001
```

---

## Phase 5: CREATE CONTENT

### 5a. Seed Content

Generate 10-20 initial articles:
```bash
cd {project}
python3 -m pipeline generate --dry-run  # Test without deploy
python3 -m pipeline generate             # Full run
```

### 5b. Quality Check

- Read generated articles on site
- Check TG previews (OG images, captions)
- Verify editorial plan diversity
- Test review loop (are revisions improving quality?)

---

## Phase 6: REGISTER IN MEDIA-MANAGER

All outlets are managed by the central media-manager at `~/workspace/projects/media-manager-faion-net/`.
**Do NOT add cron entries directly.** Media-manager handles scheduling, monitoring, and TG control.

### 6a. Add outlet to settings.py

Edit `~/workspace/projects/media-manager-faion-net/config/settings.py`:

```python
MEDIA_OUTLETS["new_outlet"] = MediaConfig(
    name="Display Name",
    slug="new_outlet",
    project_dir=PROJECTS_DIR / "new-outlet-faion-net",
    tg_bot_token="...",  # shared @nero_open_bot or @nero_media_manager_bot
    tg_channel_id="-100...",  # from getChat API
    tg_channel_username="channel_username",
    site_url="https://outlet.faion.net",
    lang=["ua", "en"],  # or just "ua"
    cron_generate="0 7 * * *",
    cron_publish="5 9,12,15,18 * * *",
    cron_digest="5 19 * * *",
)
```

### 6b. Update landing page

Add outlet metadata to `~/workspace/projects/media-manager-faion-net/app/api/landing.py`:

```python
OUTLET_META["new_outlet"] = {
    "emoji": "...",
    "tagline": "...",
    "description": "...",
    "color": "#...",
    "gradient": "linear-gradient(135deg, ...)",
    "features": ["..."],
}
```

### 6c. Update AGENTS.md for media-manager

Add the new outlet to the "Managed Media" table in media-manager's AGENTS.md.

### 6d. Update projects/AGENTS.md

Add new project to the workspace project index.

### 6e. Monitoring

Media-manager provides centralized monitoring:
- **Bot commands:** `/status`, `/logs`, `/plan` — via @nero_media_manager_bot
- **Health monitor:** automatic checks for missing articles, stale pipelines
- **Morning briefing:** daily summary sent to management chat
- **Agent commands:** `/ask`, `/analyze`, `/fix` for investigation

Additional monitoring guide: `~/workspace/scripts/media-monitoring-checklist.md`

### 6f. Manual pipeline operations

```bash
# Test without deploy/publish
cd {project} && python3 -m pipeline generate --dry-run -v

# Full generation + deploy + publish
cd {project} && python3 -m pipeline generate -v

# Via media-manager bot
/generate new_outlet    # in TG chat with @nero_media_manager_bot
/status new_outlet
```

---

## Phase 7: ITERATE

- Review content quality weekly
- Update voice guide based on feedback
- Add/remove RSS sources
- Adjust editorial balance rules
- Add new content types
- Expand to more languages/channels

---

## Pipeline Complexity Levels

### Level 1: MINIMAL (5 stages, ~500 LOC)
For: simple blog, single topic, low volume

```
collect → generate → save → deploy → publish_tg
```

No editorial plan, no review, no research agent.

### Level 2: STANDARD (8 stages, ~1200 LOC)
For: news outlet, moderate volume, quality matters

```
editorial_plan → collect → research → generate → review_loop → save → deploy → publish_tg
```

With plan review, research with web search, 1-2 review cycles.

### Level 3: FULL (12+ stages, ~2500 LOC)
For: professional media, multi-language, high volume

```
editorial_plan → plan_review → collect → research → generate → review_loop(3) →
tg_caption → tg_review → translate(N) → image_gen → save → deploy → verify → publish_tg → digest
```

With: multi-language, image generation, TG caption optimization, site verification, batch processing.

---

## Templates Index

### Pipeline Code (`templates/pipeline/`)
| File | Purpose |
|------|---------|
| `sdk.py.j2` | Claude Agent SDK wrapper |
| `context.py.j2` | PipelineContext dataclass |
| `config.py.j2` | Configuration constants |
| `cli.py.j2` | CLI entry point |
| `stages/*.py.j2` | Stage implementations |
| `modes/generate.py.j2` | Batch generation mode |

### Prompts (`templates/prompts/`)
| File | Purpose |
|------|---------|
| `editorial_plan.xml.j2` | Daily topic planning |
| `research.xml.j2` | Web research |
| `generate.xml.j2` | Article writing |
| `review.xml.j2` | Quality review |
| `tg_post.xml.j2` | TG caption |
| `digest.xml.j2` | Daily digest |
| `_partials/*.xml` | Reusable prompt fragments |

### Schemas (`templates/schemas/`)
| File | Purpose |
|------|---------|
| `editorial_plan.json` | Plan output |
| `generation.json` | Article output |
| `review.json` | Review result |
| `tg_post.json` | TG caption output |
| `digest.json` | Digest output |

### Site (`templates/gatsby/`)
| File | Purpose |
|------|---------|
| `gatsby-config.js.j2` | Gatsby config with plugins |
| `gatsby-node.js.j2` | Page creation from markdown |
| `src/templates/article.js.j2` | Article page |
| `src/pages/index.js.j2` | Home page |
| `src/components/layout.js.j2` | Layout wrapper |
| `src/styles/global.css.j2` | Global styles |
| `deploy.sh.j2` | SSH deploy script |

### Admin (`templates/admin/`)
| File | Purpose |
|------|---------|
| `app.py.j2` | Flask admin panel |

### Scripts (`templates/scripts/`)
| File | Purpose |
|------|---------|
| `run-pipeline.sh.j2` | Cron runner |
| `send_post.py.j2` | TG sender |
| `manage_state.py.j2` | State management |

---

## Related Skills

- `faion-seo-manager` — deep SEO optimization
- `faion-content-marketer` — content strategy
- `faion-smm-manager` — social media management
- `faion-server-craft` — server/nginx setup
- `faion-software-architect` — system design decisions
