# MCP Server Catalog

**Communication: User's language. Code: English.**

## Purpose

Reference catalog of popular MCP servers organized by category.

---

## Marketing & Ads

| Service | Package | Tools |
|---------|---------|-------|
| **Google Ads** | `google-ads-mcp` | Campaign management, reporting |
| **Meta Ads** | `@pipeboard-co/meta-ads-mcp` | FB/IG ads, audiences, A/B testing |
| **Mailgun** | `@mailgun/mailgun-mcp-server` | Transactional email, analytics |
| **SendGrid** | `sendgrid-mcp` | Email marketing, templates |

```bash
# Meta Ads (Facebook, Instagram)
claude mcp add meta-ads -s user -e META_ACCESS_TOKEN=... -- npx -y @pipeboard-co/meta-ads-mcp

# Google Ads
claude mcp add google-ads -s user -e GOOGLE_ADS_DEVELOPER_TOKEN=... -- npx -y google-ads-mcp

# Mailgun
claude mcp add mailgun -s user -e MAILGUN_API_KEY=... -e MAILGUN_DOMAIN=... -- npx -y @mailgun/mailgun-mcp-server

# SendGrid
claude mcp add sendgrid -s user -e SENDGRID_API_KEY=... -- npx -y sendgrid-mcp
```

---

## Product Analytics

| Service | Package | Tools |
|---------|---------|-------|
| **Mixpanel** | Hosted MCP | Analytics, funnels, cohorts |
| **Amplitude** | `amplitude-mcp` | Event analytics |
| **PostHog** | `posthog-mcp` | Product analytics, feature flags |
| **Stripe** | `@stripe/mcp` | Payments, subscriptions |

```bash
# Mixpanel (hosted - OAuth)
# Connect via https://mixpanel.com/mcp

# PostHog
claude mcp add posthog -s user -e POSTHOG_API_KEY=... -e POSTHOG_HOST=... -- npx -y posthog-mcp

# Stripe
claude mcp add stripe -s user -e STRIPE_SECRET_KEY=... -- npx -y @stripe/mcp --tools=all
```

---

## Project Management

| Service | Package | Tools |
|---------|---------|-------|
| **Jira** | `@anthropic/jira-mcp` | Issues, sprints, boards |
| **Linear** | `@anthropic/linear-mcp` | Issue tracking |
| **ClickUp** | `@taazkareem/clickup-mcp-server` | Tasks (36 tools) |
| **Trello** | `trello-mcp` | Boards, cards, lists |
| **Monday** | `@waystation/mcp` | Workspaces |
| **Asana** | `asana-mcp` | Projects, tasks |

```bash
# Jira
claude mcp add jira -s user \
  -e JIRA_URL=https://your.atlassian.net \
  -e JIRA_EMAIL=email \
  -e JIRA_API_TOKEN=token \
  -- npx -y @anthropic/jira-mcp

# Linear
claude mcp add linear -s user -e LINEAR_API_KEY=... -- npx -y @anthropic/linear-mcp

# ClickUp
claude mcp add clickup -s user -e CLICKUP_API_KEY=... -- npx -y @taazkareem/clickup-mcp-server

# Trello
claude mcp add trello -s user -e TRELLO_API_KEY=... -e TRELLO_TOKEN=... -- npx -y trello-mcp
```

---

## Development

| Service | Package | Tools |
|---------|---------|-------|
| **GitHub** | `@anthropic/github-mcp` | Repos, PRs, issues |
| **GitLab** | `gitlab-mcp` | GitLab API |
| **PostgreSQL** | `@anthropic/postgres-mcp` | Database queries |
| **Redis** | `redis-mcp` | Cache operations |
| **Docker** | `docker-mcp` | Container management |

```bash
# GitHub
claude mcp add github -s user -e GITHUB_TOKEN=... -- npx -y @anthropic/github-mcp

# PostgreSQL
claude mcp add postgres -s user -e DATABASE_URL=postgres://... -- npx -y @anthropic/postgres-mcp
```

---

## Design

| Service | Package | Tools |
|---------|---------|-------|
| **Figma** | `@anthropic/figma-mcp` | Design-to-code |
| **Figma (local)** | Desktop app | Layer inspection |

```bash
# Figma (remote)
claude mcp add figma -s user -- npx -y @anthropic/figma-mcp
```

---

## Knowledge & Docs

| Service | Package | Tools |
|---------|---------|-------|
| **Airtable** | `airtable-mcp` | Database access |
| **Notion** | `@notionhq/notion-mcp-server` | Pages, databases |
| **Google Sheets** | `google-sheets-mcp` | Spreadsheet access |
| **Confluence** | `@anthropic/confluence-mcp` | Wiki pages |

```bash
# Notion
claude mcp add notion -s user -e NOTION_API_KEY=... -- npx -y @notionhq/notion-mcp-server

# Airtable
claude mcp add airtable -s user -e AIRTABLE_API_KEY=... -- npx -y airtable-mcp
```

---

## Social Media

| Service | Package | Tools |
|---------|---------|-------|
| **Twitter/X** | `mcp-twitter-server` | Posts, search (53 tools) |
| **Instagram** | `instagram-mcp` | Analytics, posts |
| **LinkedIn** | via `social-media-mcp-server` | Posts |
| **Telegram** | `telegram-mcp` | Messages, groups |

```bash
# Twitter/X (comprehensive)
claude mcp add twitter -s user \
  -e TWITTER_API_KEY=... \
  -e TWITTER_API_SECRET=... \
  -e TWITTER_ACCESS_TOKEN=... \
  -e TWITTER_ACCESS_SECRET=... \
  -- npx -y mcp-twitter-server

# Telegram
claude mcp add telegram -s user \
  -e TELEGRAM_API_ID=... \
  -e TELEGRAM_API_HASH=... \
  -- npx -y telegram-mcp

# Multi-platform (Twitter, LinkedIn, FB, IG via Ayrshare)
claude mcp add social -s user \
  -e AYRSHARE_API_KEY=... \
  -e GROQ_API_KEY=... \
  -- npx -y social-media-mcp-server
```

---

## E-commerce

| Service | Package | Tools |
|---------|---------|-------|
| **Stripe** | `@stripe/mcp` | Payments, subscriptions |
| **Shopify** | `shopify-mcp` | Products, orders |

```bash
# Stripe (official)
claude mcp add stripe -s user -e STRIPE_SECRET_KEY=... -- npx -y @stripe/mcp --tools=all

# Shopify
claude mcp add shopify -s user \
  -e SHOPIFY_STORE_URL=... \
  -e SHOPIFY_ACCESS_TOKEN=... \
  -- npx -y shopify-mcp
```

---

## AI & Generative

| Service | Package | Tools |
|---------|---------|-------|
| **OpenAI/DALL-E** | `openai-mcp` | Image generation |
| **Replicate** | `replicate-mcp` | ML models |
| **ElevenLabs** | `elevenlabs-mcp` | Voice synthesis |

```bash
# DALL-E / OpenAI Images
claude mcp add dalle -s user -e OPENAI_API_KEY=... -- npx -y openai-mcp

# ElevenLabs
claude mcp add elevenlabs -s user -e ELEVENLABS_API_KEY=... -- npx -y elevenlabs-mcp
```

---

## Infrastructure

| Service | Package | Tools |
|---------|---------|-------|
| **Cloudflare** | `@cloudflare/mcp-server-cloudflare` | DNS, Workers, KV, R2 |
| **Hetzner** | `mcp-hetzner` | Server management |
| **AWS** | `aws-mcp` | AWS services |
| **Vercel** | `vercel-mcp` | Deployments |

```bash
# Cloudflare (13 servers!)
claude mcp add cloudflare -s user \
  -e CLOUDFLARE_API_TOKEN=... \
  -e CLOUDFLARE_ACCOUNT_ID=... \
  -- npx -y @cloudflare/mcp-server-cloudflare

# Hetzner
claude mcp add hetzner -s user -e HETZNER_API_TOKEN=... -- npx -y mcp-hetzner
```

---

## Browser & Automation

| Service | Package | Tools |
|---------|---------|-------|
| **Puppeteer** | `@anthropic/puppeteer-mcp` | Browser automation |
| **Playwright** | `@anthropic/playwright-mcp` | Cross-browser testing |

```bash
claude mcp add puppeteer -s user -- npx -y @anthropic/puppeteer-mcp
claude mcp add playwright -s user -- npx -y @anthropic/playwright-mcp
```

---

## Communication

| Service | Package | Tools |
|---------|---------|-------|
| **Slack** | `@anthropic/slack-mcp` | Messages, channels |
| **Discord** | `mcp-discord` | Bot integration |

```bash
claude mcp add slack -s user -e SLACK_BOT_TOKEN=xoxb-... -- npx -y @anthropic/slack-mcp
```

---

## Memory

| Service | Package | Tools |
|---------|---------|-------|
| **Memory** | `@anthropic/memory-mcp` | Persistent memory |

```bash
claude mcp add memory -s user -- npx -y @anthropic/memory-mcp
```

---

## Resources

- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Create new skill from template | haiku | Mechanical task with clear structure |
| Design agent architecture for complex task | opus | Requires reasoning about delegation and isolation |
| Configure MCP server for Claude | sonnet | Implementation with moderate complexity |
| Write agent system prompt | sonnet | Requires clear communication and nuance |
| Set up hook for pre-commit security | haiku | Mechanical script configuration |
| Implement custom slash command | sonnet | Coding with context and interaction |

