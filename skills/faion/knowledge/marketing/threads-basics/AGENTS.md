# Threads Basics

## Summary

**One-sentence:** Setup + content strategy for Meta Threads — text-first, leveraging Instagram audience, growth driven by conversational content + 7-10 posts/day + reply velocity, not volume alone.

**One-paragraph:** Threads crossed 100M users rapidly; early adopters get reach upside before competition densifies. Accounts that cross-post X verbatim underperform — Threads rewards a warmer conversational register. No stable scheduling API exists at the start of 2026; the operator posts manually from a ranked draft pool the agent produces. This methodology pins the mechanics into testable rules: 3-10 posts/day, ≤500 chars, banned engagement-bait phrases, pillar tags, hook bigram rotation, and a 50% cap on agent-generated drafts. Output: a daily content pack of 5-12 ranked drafts validated against the contract.

**Ефективно для:**

- Брендів з вже існуючою Instagram-аудиторією.
- High-cadence 7-10 постів/день з reply-velocity у першу годину.
- Drafts ≤500 chars + pillar tag + bigram rotation.
- Operator picks 7-10 з 20 agent-ranked candidates manually.
- Conversational-register rewrites замість X-verbatim cross-post.

## Applies If (ALL must hold)

- Standing up a brand or founder presence on Threads while leveraging an existing Instagram audience.
- Drafting daily content packs (5-12 posts) for a SMM operator who has defined voice guidelines.
- Auditing an account that cross-posts from X/Twitter verbatim and is underperforming.
- Hot-take and conversation-starter ideation for accounts where engagement bait is acceptable.
- Bootstrapping a new niche account that needs cadence and format scaffolding.

## Skip If (ANY kills it)

- Target audience does not overlap with Instagram demographics (e.g., enterprise security buyers — use LinkedIn).
- Brand voice forbids hot takes, personal stories, or unmoderated conversation.
- Team has zero capacity for replies — Threads' algorithm rewards reply velocity; posting alone plateaus within weeks.
- Regulated industries (finance, healthcare) where every post needs compliance review incompatible with the required cadence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Content pillars (Opinion / Value / Question / Personal / Curated) | YAML | operator's strategy doc |
| Banned-bigram + banned-phrase list | YAML | brand book + Meta moderation guidelines |
| Instagram audience export | CSV | Instagram Business account |
| Recent Threads insights | screenshots / CSV | Threads Insights tab |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/smm-manager/instagram-basics` | Sibling — Threads piggy-backs on Instagram audience + visual brand. |
| `pro/marketing/growth-social-media-strategy` | Upstream strategy: which platforms to invest in. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules (cadence, no X-verbatim, no auto-post, char cap, banned bait, bigram rotation, pillar) + self-routing anchors | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for a daily content pack + valid / invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (verbatim X cross-post, auto-post, identical hooks, engagement-bait, link-heavy, ignored replies) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-daily-pack` | sonnet | Per-draft judgment: pillar tag, hook score, register rewrite. |
| `score-hook` | haiku | Mechanical 1-5 rating against the rubric. |
| `weekly-trend-synthesis` | opus | Cross-pack synthesis across 7 days; bigram rotation and pillar-balance check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/threads-basics.md` | Markdown skeleton (5-line header) for the daily content pack artefact. |
| `templates/threads-basics.json` | JSON Schema (draft-07) for the output contract. |
| `templates/bio-templates.txt` | Founder, expert, and creator bio formulas. |
| `templates/daily-posts.txt` | Morning/afternoon/evening post templates and multi-post thread format. |
| `templates/prompt-ideation.txt` | Daily content pack ideation prompt with pillar tags and hook scoring. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-threads-basics.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/smm-manager/`
- sibling: [[instagram-basics]]
- sibling: [[growth-twitter-x-growth]]
- sibling: [[growth-linkedin-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (audience-overlap-Instagram, reply capacity, brand-voice compatibility, regulatory load) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the SMM operator opens a fresh daily brief and must decide whether to invest the Threads pack today or route to a text-first sibling channel.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/threads-basics.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/threads-basics.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 3
    },
    "decision": {
      "type": "string",
      "minLength": 3
    },
    "rationale": {
      "type": "string",
      "minLength": 30
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/bio-templates.txt`

```text
FOUNDER:
Building [product] in public
[What it does in <5 words]
Sharing wins, fails, and lessons

---

EXPERT:
[Topic] tips daily
[Credibility: X years, Y clients, etc.]
Let's chat in replies

---

CREATOR:
Making content about [topic]
[IG handle] for more
Ask me anything
```

### `templates/daily-posts.txt`

```text
MORNING POST (engagement driver):
"Starting the day with [activity].

What's your morning routine look like?"

---

AFTERNOON POST (value):
"One thing I learned this week about [topic]:

[Insight in 2-3 sentences]

Has anyone else experienced this?"

---

EVENING POST (conversation):
"Honest question for [your audience]:

[Question about their work/life]

I'll go first: [Your answer]"

---

THREAD FORMAT (multi-post):

POST 1:
"I've been building [product] for [X] months.

Here's what I've learned (thread):"

POST 2 (reply to self):
"1. [First lesson]

[2-3 sentence explanation]"

POST 3+ (reply to thread):
"2. [Second lesson]

[2-3 sentence explanation]"

FINAL POST:
"That's it for now. What would you add?

Drop your lessons below"
```

### `templates/prompt-ideation.txt`

```text
Brand voice: <attached>. Pillars: opinions (40%), value (30%), questions (20%), personal (10%).
Yesterday's top post: <text+stats>.
Today's trending topics: <list>.

Draft 12 candidate posts for today. For each:
- Tag with pillar (opinions/value/questions/personal)
- Keep under 500 characters (hard limit)
- Assign hook score 1-5 (5 = strongest)
- No emojis unless brand voice file explicitly allows them
- No engagement-bait phrases ("comment X for Y", "tag a friend", "follow for more")
- No links

Output 12 posts sorted by hook score descending.
Operator will select 7-10 to post manually within today's prime windows.
```
