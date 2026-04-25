# Agent Integration — AI Content Strategy

## When to use
- Building a multi-channel content pipeline where AI handles drafts and humans edit/approve before publishing.
- Planning a content calendar that requires 10+ pieces per week — AI handles volume, human handles quality gate.
- Implementing a systematic content repurposing workflow: one long-form piece → social posts + email + newsletter.
- When content output has declined due to bandwidth constraints and AI can restore throughput with human oversight.
- Setting up SEO-optimized content production where AI generates keyword-targeted outlines and first drafts.

## When NOT to use
- Breaking news or time-sensitive reactive commentary — AI drafting delay and review cycles are too slow.
- Highly regulated content (medical, legal, financial advice) where AI hallucinations in claims carry compliance risk.
- Personal brand content that requires authentic lived experience — AI cannot fake genuine first-person insight without hallucination risk.
- When brand voice is still undefined — AI will amplify generic "marketing voice" rather than a distinct brand personality.

## Where it fails / limitations
- AI-generated content without E-E-A-T signals (experience, expertise, authoritativeness, trust) underperforms in Google rankings as of 2025 Helpful Content Updates.
- "Prompt and publish" without human review creates factual errors, outdated statistics, and brand-inconsistent phrasing at scale.
- AI tools trained on web data produce content that sounds like averaged internet output — differentiation requires human expert input layered on top.
- Surfer/MarketMuse SEO optimization recommendations may conflict with brand voice; blindly following them produces keyword-stuffed awkward content.
- Multi-channel repurposing via AI often produces versions that are too similar to each other, losing channel-native feel (Twitter vs. LinkedIn vs. newsletter have different expectations).

## Agentic workflow
A content pipeline agent receives a topic brief and persona target, runs keyword research (Semrush API or similar), generates an outline, produces a draft, applies SEO optimization metadata, and writes channel-specific variants. A human editor reviews and approves before scheduling. The agent can also analyze published content performance and feed insights back into the next brief. For high-volume pipelines, multiple agents run in parallel on different topics, coordinated by a queue file.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps content generation tasks in a quality gate that checks: outline reviewed, draft length within target, SEO metadata present, human approval flag set before scheduling.

### Prompt pattern
```
You are a content strategist. Topic: <topic>. Target audience: <persona>. Brand voice: <voice guide excerpt>.
Step 1: Generate 5 headline options for this topic.
Step 2: Write a 500-word outline with H2/H3 structure.
Step 3: Identify 3 differentiating angles (data, case study, contrarian) that generic AI content would miss.
Output as JSON: {"headlines": [], "outline": "", "differentiating_angles": []}.
```

```
You are an expert editor. Review this AI draft for: (1) factual claims that need source verification, (2) generic statements replaceable with specific data, (3) brand voice deviations from the style guide. Output: {"fact_check_required": [], "generic_statements": [], "voice_issues": []}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `semrush-api` (Python client) | Keyword research, content gap analysis | https://developer.semrush.com |
| `clearscope` (API) | Real-time SEO content optimization scoring | https://www.clearscope.io/api |
| `n8n` | No-code workflow to chain AI content generation steps with approval gates | https://n8n.io |
| `pandoc` | Convert AI-generated markdown to HTML/DOCX for CMS upload | https://pandoc.org |
| `claude --print` | Generate content drafts in automated pipeline | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jasper | SaaS | Partial — REST API | Content generation with brand voice training |
| Copy.ai | SaaS | Yes — REST API | Workflow automation with agentic content flows |
| Surfer SEO | SaaS | Yes — REST API | Real-time content scoring and optimization |
| MarketMuse | SaaS | Yes — REST API | Topic authority and content gap analysis |
| Clearscope | SaaS | Yes — REST API | Keyword and semantic SEO recommendations |
| Blaze.ai | SaaS | Yes — REST API | Multi-channel distribution from single source |
| Persado | SaaS | Yes — REST API | AI copy optimization for ads and email subject lines |
| n8n | OSS | Yes — native workflow | Chain AI content steps with approval nodes |

## Templates & scripts
See templates.md for content brief template, repurposing workflow, and SEO metadata checklist.

Inline pipeline snippet (n8n-style pseudocode for content workflow):

```
[Trigger: Google Sheet new row (topic brief)]
  → Claude: Generate outline (system: brand voice guide)
  → Human approval: Slack notification with approve/reject
  → IF approved: Claude: Generate full draft (1000-1500 words)
  → Surfer API: Score draft, get optimization suggestions
  → Claude: Apply top 3 SEO suggestions without altering voice
  → Human approval: Email draft review
  → IF approved: Schedule to CMS via API
  → Notify team in Slack
```

## Best practices
- Always add a "human layer" above AI output: expert quotes, first-hand data, proprietary statistics, or strong opinions. These are the elements AI cannot generate and that Google E-E-A-T rewards.
- Define brand voice in a written guide before training or prompting AI tools; "conversational but authoritative" means nothing without examples.
- Use AI for volume and speed, human for differentiation and trust. The ratio matters: 80% AI draft, 20% human expert enrichment is a workable baseline.
- Build a content asset library of approved expert quotes, proprietary data points, and case studies that agents pull from when generating drafts — this mechanically raises content quality.
- Repurposing should be channel-native, not format-swap: a 1500-word blog post does not become a good Twitter thread by cutting sentences; it needs restructuring for the format's conventions.
- Set measurable quality gates before any content is published: reading level, keyword density, E-E-A-T signal count, fact-check status, human approval.

## AI-agent gotchas
- AI content pipelines can publish at a rate that exceeds human review capacity. Always design the queue with a human approval bottleneck before the publish step — never fully autonomous publication.
- AI tools hallucinate statistics. Every quantitative claim in AI-generated content must be verified against a primary source before publishing. Include this as a required checklist item.
- SEO tools (Surfer, Clearscope) grade content by keyword density; an agent following their recommendations blindly can produce keyword-stuffed content that ranks but reads poorly. Human must balance.
- Brand voice drift occurs when multiple AI sessions produce content independently without a consistent system prompt containing the voice guide. The guide must be injected in every content generation call.
- Content repurposing agents that summarize for social media tend to pick the least differentiated points (generic takeaways) rather than the most differentiated (specific data points). Explicitly instruct agents to prioritize proprietary or specific insights.

## References
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content — Google E-E-A-T guidelines
- https://www.semrush.com/blog/ — Semrush AI content strategy research
- https://blog.hubspot.com/marketing/ai-trends — HubSpot AI marketing trends
- https://www.gartner.com/en/marketing/topics/ai-in-marketing — Gartner AI in marketing report
- https://clearscope.io/blog — Clearscope content optimization research
