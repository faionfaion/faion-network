# Instagram Basics

## Summary

**One-sentence:** Instagram setup + content strategy that allocates ≥80% of effort to Reels, mandates on-screen text, enforces hashtag minimalism, and restricts DM automation to approved partners.

**One-paragraph:** Reels deliver ~2× the reach of photos by pushing to non-followers; accounts that ignore Reels get ~1/4 the reach. The first 1.5 seconds decide reach, 80% of viewers watch muted, and hashtag density no longer correlates with topical understanding. This methodology pins those mechanics into testable rules: 80/15/5 effort split, three-line bio formula, pillar tags on every draft, banned TikTok-watermark cross-posts, ManyChat-only DM automation. Output: a weekly content pack of 5-12 Reels + Stories + carousels validated against the contract.

**Ефективно для:**

- Reels-first контент стратегії (80% effort на Reels).
- Mandatory on-screen text — 80% дивиться без звуку.
- Hashtag minimalism 3-5 mixed tiers, не 30.
- DM automation тільки через ManyChat / approved partners.
- Pillar discipline + bigram rotation у тижневому контент-паку.

## Applies If (ALL must hold)

- Setting up an Instagram presence (founder, brand, creator) and configuring profile, highlights, and content pillars.
- Reels-first content strategy where the team can shoot/edit but needs scripts, hooks, and carousel scripts.
- Auditing an underperforming Instagram account to identify whether decline is reach, engagement, or conversion.
- Drafting carousel scripts (10 slides) and Story sequences for product launches.
- Pairing with Meta Ads where organic posts feed retargeting audiences.

## Skip If (ANY kills it)

- Audience is purely B2B enterprise — LinkedIn and email outperform; do not invest cycles here.
- Team cannot shoot or edit video; Instagram without Reels gets roughly 1/4 the reach of a Reels-led account.
- Brand requires text-heavy, long-form content (use blog + LinkedIn).
- Regulated industries where every visual claim needs compliance review incompatible with Instagram's posting velocity.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Content pillars (5 pillars + ratios) | YAML / sheet | operator's strategy doc |
| Brand voice guide | Markdown | operator's brand book |
| Recent Instagram insights export | CSV | Instagram Business account |
| Top-5 winners library | Markdown | operator's archive of past hits |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/smm-manager/threads-basics` | Sibling — Threads pack often piggy-backs on the Instagram Reels brief. |
| `pro/marketing/growth-social-media-strategy` | Upstream strategy: which platforms to invest in. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules (Reels 80%, on-screen text, hashtag minimalism, bio formula, no TikTok watermark, DM automation, pillar) + self-routing anchors | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for a weekly content pack + valid / invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (emoji-heavy captions, stale trending hashtags, listicle overuse, voiceover-only, TikTok watermark, broad DM automation) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-reel-script` | sonnet | Per-script judgment: hook scoring, on-screen text composition. |
| `score-hook` | haiku | Mechanical 1-5 rating against the rubric. |
| `weekly-pack-synthesis` | opus | Cross-pillar synthesis across 7-10 drafts; pillar-balance check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/instagram-basics.md.j2` | Markdown skeleton (5-line header) for the weekly content pack artefact. |
| `templates/instagram-basics.md` | Markdown skeleton (5-line header) for the weekly content pack artefact. Generated from `templates/instagram-basics.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/instagram-basics.json` | JSON Schema (draft-07) for the output contract. |
| `templates/bio-template.txt` | Three-line bio formula (what / credibility / CTA). |
| `templates/reel-script.txt` | Hook + body + CTA Reel script template. |
| `templates/carousel-template.txt` | 10-slide carousel narrative structure. |
| `templates/prompt-reels.txt` | Prompt for generating 5 Reels scripts with pillar tags and hook scores. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-instagram-basics.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/smm-manager/`
- sibling: [[threads-basics]]
- sibling: [[growth-twitter-x-growth]]
- sibling: [[growth-linkedin-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (audience-on-Instagram, video capacity, brand voice compatibility, regulatory load) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the SMM operator opens a fresh weekly brief and must decide whether to invest the Reels-first pack this week or route to a text-first channel.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/instagram-basics.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/instagram-basics.json",
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

### `templates/bio-template.txt`

```text
Line 1: [What you do] for [who you help]
Line 2: [Credibility/proof point]
Line 3: [CTA - what to do next]
Link: [Link description]

Example:
Helping developers ship faster
Built 5 products | 50K+ downloads
FREE startup checklist below
```

### `templates/reel-script.txt`

```text
HOOK (0-2 sec):
[On-screen text: Bold statement or question — max 8 words]
[Action: match the hook visually]

BODY BEAT 1 (3-10 sec):
[On-screen text: Point 1]
[Visual supporting beat 1]

BODY BEAT 2 (11-18 sec):
[On-screen text: Point 2]
[Visual supporting beat 2]

BODY BEAT 3 / RETENTION SPIKE (19-25 sec):
[On-screen text: Point 3 — make viewer rewatch]
[Visual supporting beat 3]

CTA (26-30 sec):
[Follow for more [topic]] OR [Save this for later]
[Point to follow button or save gesture]
```

### `templates/carousel-template.txt`

```text
Slide 1 (Cover):
[Hook headline — max 8 words, make them stop scrolling]
[Eye-catching visual]

Slides 2-8 (One point per slide):
[Point N — large text, max 10 words per slide]
[Supporting visual or icon]

Slide 9 (Summary):
[Recap 3 key points as bullets]

Slide 10 (CTA):
[Save + Share + Follow]
[Your handle]
```

### `templates/prompt-reels.txt`

```text
Pillar mix: educational 40%, behind-scenes 30%, results 20%, inspirational 10%.
Brand voice: <attached>.

Output 5 Reels scripts. For each:
- Hook (<2s): on-screen text only, max 8 words, score it 1-5
- 3 body beats with on-screen text (max 10 words per beat)
- Mark the retention spike beat (the moment that triggers a rewatch)
- CTA (1 line)
- Total length: 15-30 seconds
- No emojis
- Tag with pillar (educational/behind-scenes/results/inspirational)

Only include scripts where hook score >= 4.
```
