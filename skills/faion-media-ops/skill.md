Base directory for this skill: /home/nero/.claude/skills/faion-media-ops

> **Entry point:** `/faion-media-ops` — invoke directly or via `/faion-net`.

# Media Operations Skill

**Communication: User's language. Code/docs: English.**

Setup and operate any media resource: Telegram channels, news sites, blogs, podcasts, newsletters.

## Process

### Phase 1: DISCOVERY

Interview the user to define the media resource. Ask about:

**1. Media type:**
- telegram-news (channels + site)
- newsletter (email + landing page)
- podcast (audio + show notes site)
- social-media (multi-platform)
- blog (content site only)

**2. Brand/Character:**
- Name and personality
- Voice/tone (formal, casual, ironic, professional)
- Visual style (photo, illustration, AI-generated, pixel art)
- Languages (which, primary)
- Target audience

**3. Content strategy:**
- Topics/niches (what to cover)
- Content types (news, guides, opinions, personal, roundups)
- Posting frequency
- Content sources (web search, RSS, manual, API feeds)

**4. Technical:**
- Domain (existing or new)
- Hosting (existing server or need new)
- Telegram bot (existing or create)
- Budget for APIs (OpenAI images, etc.)

**5. Automation:**
- Posting schedule (hours, timezone)
- Silent hours (no-notification period)
- Personal content ratio (e.g., every 3rd post)
- Auto-pilot level (full auto vs review before posting)

### Phase 2: SETUP

Based on discovery, create the project. Reference implementation: `~/workspace/projects/neromedia-faion-net/`

#### 2a. Project Structure

Create in `~/workspace/projects/{project-name}/`:

```
{project}/
├── CLAUDE.md               # @AGENTS.md
├── AGENTS.md               # Project docs
├── .claude/agents.md       # Sub-agent: post-content
├── content/                # Markdown articles
│   ├── ideas.md            # Content ideas bank
│   └── plan.md             # Content calendar
├── scripts/
│   ├── get_context.py      # Recent content context for sub-agents (run FIRST)
│   ├── manage_state.py     # Slot scheduling, dedup, state
│   ├── send_post.py        # Telegram sender (--channel, --silent, --url)
│   ├── archive_post.py     # Post archival
│   └── gen_image.sh        # Image generation (if visual brand)
├── prompts/
│   ├── loop-post.md        # Main pipeline prompt
│   ├── voice-{lang}.md     # Voice/tone guide per language
│   └── character.md        # Visual character reference (if applicable)
├── state/
│   ├── plan.json           # Daily slot plan
│   ├── posted.json         # Dedup log (7-day rolling)
│   ├── post_counter.txt    # Daily counter (for personal post rotation)
│   └── posts/              # Archive
├── gatsby/                 # Site (if applicable)
│   ├── gatsby-config.js
│   ├── gatsby-node.js
│   ├── src/components/     # SEO, Layout, ArticleCard
│   ├── src/templates/      # article, lang-index, tag
│   ├── src/styles/         # Theme CSS
│   ├── deploy.sh
│   └── content -> ../content
└── output/                 # Generated images
```

#### 2b. Configuration

Create `config.json` at project root (NOT hardcoded in scripts):

```json
{
  "name": "Project Name",
  "site_url": "https://example.com",
  "languages": ["en", "ua"],
  "primary_language": "en",
  "timezone": "Europe/Lisbon",
  "channels": {
    "en": {"platform": "telegram", "chat_id": "-100xxx", "username": "@channel_en"},
    "ua": {"platform": "telegram", "chat_id": "-100xxx", "username": "@channel_ua"}
  },
  "posting": {
    "hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "silent_start": 21,
    "silent_end": 9,
    "personal_every_n": 3
  },
  "topics": ["topic1", "topic2", "topic3"],
  "content_types": ["news", "guide", "opinion", "personal"],
  "image": {
    "model": "gpt-image-1.5",
    "size": "1024x1536",
    "style": "description of visual style",
    "reference_image": "output/character_isolated.png"
  }
}
```

Scripts read from `config.json` instead of hardcoding values.

#### 2c. Telegram Setup

1. Create bot via @BotFather (or use existing)
2. Create channel(s)
3. Add bot as admin to channel(s)
4. Get chat_id: `curl "https://api.telegram.org/bot{TOKEN}/getChat?chat_id=@username"`
5. Store token in `~/workspace/.env` as `{PROJECT}_TG_BOT_TOKEN`

#### 2d. DNS + Hosting

1. Create Cloudflare DNS A record → server IP (proxied)
2. Create nginx config (listen 443 ssl, serve static)
3. Deploy script with SSH via 1Password

Reference: `~/workspace/projects/neromedia-faion-net/site/nginx/neronews.faion.net.conf`

#### 2e. Site Setup

**Option A: Gatsby** (recommended for SEO, image optimization, prefetch)
- Copy gatsby template from neromedia-faion-net, customize
- Key plugins: remark, image, sitemap, robots-txt, feed
- SEO component with OG, Twitter Cards, JSON-LD, Telegram IV trick

**Option B: Jinja2 SSG** (simpler, fewer dependencies)
- Python script: markdown → HTML via Jinja2
- Templates: base, article, index, tag, 404
- Good for quick prototyping

**Option C: No site** (Telegram-only)
- Skip site setup, post directly to channels
- Use Telegraph for IV

#### 2f. Brand/Character Creation

If the media resource has an AI character:

1. **Define personality** — write voice guide (see `prompts/nero-voice.md` as template)
2. **Visual identity** — generate reference image:
   ```bash
   # Generate character with gpt-image-1.5
   # Isolate on white background via edit API
   # Save as output/character_isolated.png
   ```
3. **Image style** — define how character appears in posts:
   - Style mixing (e.g., photorealistic character + pixel art environment)
   - Scene templates per topic
   - Consistent props (sunglasses, hoodie, etc.)

### Phase 3: CONTENT

Generate initial content batch using parallel sub-agents.

**Batch strategy:**
- Launch 3-5 agents in parallel
- Each writes 10 articles of a specific type/language
- Total: 30-50 articles for launch

**Article types to cover:**
- News (5-7/day equivalent, ~600 words)
- Guides (1/day, ~2000 words, practical)
- Opinions (1/day, ~800 words, hot takes)
- Personal (every 3rd post, ~500 words, stories)

**Quality checklist:**
- Clickbait descriptions (under 120 chars)
- Multiple sources for news
- Cat/brand emojis in appropriate places
- Both language versions
- Unique images per article

### Phase 4: PUBLISH

1. Build and deploy site
2. Publish to Telegram channels with cache-bust param (`?v=1`)
3. Verify OG preview + Instant View
4. Add `al:android:app_name="Medium"` meta tag for IV trick

### Phase 5: AUTOMATION

Configure ongoing operation:

1. **Loop prompt** (`prompts/loop-post.md`):
   - Read slot plan
   - Research (WebSearch for news, Git repos for personal)
   - Write article (both languages)
   - Generate image
   - Build & deploy site
   - Send to channels (with silent mode)
   - Update state

2. **Sub-agent** (`.claude/agents.md`):
   - Calls prepared scripts (manage_state, send_post, gen_image, archive_post)
   - Minimal token usage — scripts do heavy lifting

3. **Start:** `cd ~/workspace/projects/{project} && claude` → `/loop 1h`

### Phase 6: OPERATIONS

Ongoing management:

- **Content calendar** — `content/plan.md` with weekly topics
- **Ideas bank** — `content/ideas.md` updated by agents
- **Dedup** — 7-day rolling window, URL + title hash
- **Analytics** — subscriber count, message views (via TG API)
- **Iteration** — review what works, adjust topics/frequency

## Templates

### Voice Guide Template

```markdown
# {Character} Voice — {Language} Channel

You are writing as {CHARACTER} — {one-line description}.

## Tone
- {Trait 1} — {description}
- {Trait 2} — {description}
- {Trait 3} — {description}
- NO {anti-trait}

## Emojis
{emoji set with meanings}

## Format
- Language: {language}
- Markup: HTML (<b>, <a href>)
- Start with {signature emoji} + bold title
- Max {N} characters
- End with source links

## Vibe
{1-2 sentence personality summary}
```

### Frontmatter Template

```yaml
---
title: "Article Title"
slug: url-slug
date: YYYY-MM-DD
type: news|guide|opinion|personal
lang: en
tags: [tag1, tag2]
image: /images/slug_3x4.png
description: "Clickbait, under 120 chars"
source_url: https://...
source_name: Source Name
---
```

### Nginx Config Template

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name {DOMAIN};

    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

    root /var/www/{DOMAIN};
    index index.html;

    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }

    location ~* \.(css|js|png|jpg|jpeg|webp|ico|svg)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/javascript application/javascript application/json;

    error_page 404 /404.html;
}
```

## SEO Checklist

- [ ] OG tags: title, description, image, url, type, locale, site_name
- [ ] Twitter Card: summary_large_image
- [ ] JSON-LD: NewsArticle schema
- [ ] Canonical URLs with trailing slash
- [ ] Hreflang tags for multi-language
- [ ] Sitemap.xml
- [ ] RSS feed per language
- [ ] robots.txt with sitemap reference
- [ ] `al:android:app_name="Medium"` for Telegram Instant View
- [ ] `article:published_time` meta tag
- [ ] Image dimensions in OG (og:image:width, og:image:height)
- [ ] Favicon

## Privacy Rules (for personal/AI-agent content)

NEVER publish:
- API keys, tokens, credentials
- Private user messages or conversations
- Internal business data, revenue
- Email addresses or personal data
- Private configuration details

OK to publish:
- Technical decisions and architecture
- Public git commit messages
- Tool choices and comparisons
- Workflow descriptions
- Debugging stories (without sensitive context)
- Performance metrics (generic)

## Related Skills

- faion-seo-manager — deep SEO optimization
- faion-content-marketer — content strategy
- faion-smm-manager — social media management
- faion-software-developer — site development
- faion-server-craft — server/nginx setup
