# Agent Integration — Product Explainability

## When to use
- Pre-launch: producing or auditing the product knowledge base (KB) that will represent the product to ChatGPT, Claude, Perplexity, Gemini, and on-site search.
- Migrating from human-only marketing copy to AI-mediated discovery: home page, product page, docs, pricing page need machine-readable purpose, capabilities, and limits.
- After a model update or major SEO/AEO shift, when traffic from AI answer engines starts displacing classical organic search.
- When customers report wrong answers from AI assistants ("ChatGPT said your tool can do X but it can't") — explainability gap, not a marketing gap.
- When integrating product into agent toolchains (MCP servers, OpenAI custom GPT actions, Claude skills) — the same metadata serves both surfaces.
- Compliance contexts (EU AI Act Art. 13, FTC AI guidance, regulated B2B): documented purpose + scope + limits is required, not optional.

## When NOT to use
- Pre-PMF products with <100 users — fix the product, not its representation.
- Internal-only tools that no AI will ever index or recommend.
- One-page landing pages with a single CTA: schema markup is overkill; standard Open Graph is enough.
- Products whose purpose changes monthly — KB will be stale faster than it ships; stabilize positioning first.
- Hyper-niche enterprise sales where buyers reach the product only through human channels (RFP, channel partner) — AEO investment has ~zero return.

## Where it fails / limitations
- **KB drift is the default.** Marketing site, docs, pricing page, schema feed, and `llms.txt` diverge within weeks. AI assistants will pick whichever source they crawled last; contradictions become hallucinations attributed to the brand.
- **Limits get watered down.** Product teams write aspirational capability statements; "honest scope" gets edited out by marketing review. AI then over-promises.
- **Schema theater.** Teams add `Product` JSON-LD to look compliant, but `description`/`audience`/`feature` fields repeat the marketing tagline. No retrieval system gets new signal.
- **`llms.txt` is not yet a standard.** As of 2026, only ~15-20% of major LLM crawlers (Anthropic, OpenAI, Perplexity tested) honor it; assuming coverage is wrong.
- **Hallucination floor.** Even a perfectly aligned KB cannot prevent an LLM from confabulating. Explainability lowers the rate; it does not zero it.
- **No measurement primitive.** "How well does AI represent us?" has no off-the-shelf metric — teams skip the monitoring loop, KB rots silently.
- **Localization explosion.** Each language doubles surface area; agents conflate locales when retrieval is multilingual.
- **Capability-version skew.** Capability statements rarely carry `validFrom`/`validUntil`; deprecated features keep getting recommended.

## Agentic workflow
Drive product explainability as a four-stage agent pipeline that re-runs on every release: (1) an extractor agent reads the live product (website, docs, OpenAPI spec, changelog, in-app strings) and emits a structured `product-kb.json` (purpose, capabilities, limits, use cases, audience, prerequisites); (2) a generator agent renders that JSON into the public surfaces — `llms.txt`, schema.org JSON-LD, sitemap with `lastmod`, and a docs section "What this product is / is not"; (3) a probe agent runs canonical questions against ChatGPT, Claude, Perplexity, and Gemini and diffs answers against the KB to score representation accuracy; (4) a drift agent runs on a cron, comparing the live site, docs, and KB, opening tickets when fields disagree. Wire stages 1–2 into CI so a release cannot ship without an updated KB; stages 3–4 run weekly. Persist the KB at `.aidocs/product_docs/product-kb.json` so other faion-net agents (research, marketing, SDD) consume the same source of truth.

### Recommended subagents
- `faion-research-agent` (`skills/faion/knowledge/pro/research/researcher/`) — runs the AI-probe stage: queries each AI surface with the canonical question set, captures responses, structures the diff. Reuse the existing `competitive-intelligence` mode template.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts drift-agent findings into SDD `todo/` tasks (each KB ↔ site contradiction becomes a fix ticket with owner).
- `faion-market-researcher` (sub-skill of researcher) — supplies the audience/JTBD vocabulary that feeds the KB's "for whom" section; without this, capability statements lack a buyer-language anchor.
- `faion-marketing-manager` skill methodologies (`solo/marketing/`, `pro/marketing/`) — own the public-surface copy generated from the KB; explainability is upstream of GTM messaging.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub the KB before publishing `llms.txt` or pushing to a third-party retrieval index; capability docs frequently leak internal endpoints, vendor names, beta-only flags.
- A purpose-built **AI-answer probe agent** (not yet in repo, worth creating): given a question set, queries each frontier LLM via API, normalizes responses, scores against ground truth.

### Prompt pattern
KB extraction pass:
```
You extract a structured product KB. Inputs: <homepage url>, <docs root>,
<openapi spec>, <changelog>. Output JSON with fields: purpose (1 sentence,
no marketing adjectives), capabilities[] (each: name, description, example,
status: ga|beta|deprecated, since_version), limits[] (each: scope, rationale,
workaround_or_null), use_cases[] (each: persona, job, success_signal),
audience (industry, role, company_size), prerequisites[]. Refuse to invent
fields. If a source is missing, write "unknown" — never fabricate.
```

AI-answer probe pass:
```
For each question in <question_set>, query <model> with no system prompt,
plain user role. Capture the full answer. Then score against <product-kb.json>
on three axes: factually_correct (0|1), capability_in_scope (0|1),
limit_acknowledged (0|1). Output a markdown table sorted by total score asc.
Flag any answer that recommends a capability with status=deprecated.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `schema-dts` + `tsc` | Type-checked schema.org JSON-LD generation | `npm i schema-dts` ; https://github.com/google/schema-dts |
| Google Rich Results Test | Validate `Product`, `SoftwareApplication`, `FAQPage` markup | https://search.google.com/test/rich-results |
| `structured-data-testing-tool` (CLI) | Lint JSON-LD in CI | `npm i -g structured-data-testing-tool` |
| `llms.txt` generators (e.g. `llmstxt-cli`) | Emit `/llms.txt` and `/llms-full.txt` from docs | https://llmstxt.org/ ; npm/pypi packages |
| `screaming-frog` CLI | Crawl public site, extract title/description/schema diff | https://www.screamingfrog.co.uk/seo-spider/ |
| `gh` CLI | File drift findings as labeled issues (`label:explainability-drift`) | https://cli.github.com |
| `claude` (Anthropic CLI) | Run extractor + probe prompts headless against Claude | https://docs.anthropic.com |
| `openai` CLI / `perplexity` API | Probe ChatGPT and Perplexity from CI | https://platform.openai.com ; https://docs.perplexity.ai |
| `jq` + `ajv-cli` | Validate `product-kb.json` against a JSON Schema | `npm i -g ajv-cli` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Algolia / Typesense | SaaS / OSS search | API yes | Best surface for "AI-mediated on-site discovery"; index the KB, not just docs HTML. |
| Mintlify / GitBook / Docusaurus | Docs platform | API yes | Mintlify ships first-class `llms.txt` and AI-answer telemetry as of 2026. |
| Inkeep / Kapa.ai / Mendable | RAG-as-a-service | API yes | Hosts a chat agent grounded in your KB; useful as the canonical "what we say" reference for probe agents. |
| OpenAI Custom GPT / Anthropic Skill | Agent surface | API yes | Same KB renders as MCP server tool descriptions and capability cards. |
| Profound / Athena AI / SE Ranking AEO | AEO monitoring SaaS | API limited | Track brand mentions and capability accuracy across LLMs over time. |
| schema.org + Google Merchant Center | Standard / SaaS | API yes | Required for any e-commerce or SaaS surfaced via Google AI Overviews. |
| ProductHunt / G2 / Capterra | Discovery SaaS | API limited | Their LLM-readable feeds influence AI buying guidance; keep capability statements identical to your KB. |
| Notion / Airtable | KB host | API yes | Pragmatic place to author `product-kb` if devs do not own it; export to JSON via API. |
| Linear / GitHub Issues | Drift tickets | API yes | Drift agent files explainability-drift issues; mitigations = subtasks. |
| Tracecat / OSS pipelines | Workflow | yes | Self-hosted scheduling for the four-stage pipeline. |

## Templates & scripts

The methodology ships only `README.md` (54 lines) — `templates.md`, `examples.md`, `llm-prompts.md`, `checklist.md` are empty. The biggest immediate gap is the lack of a canonical KB shape. Inline drop-in (≤50 lines) — JSON Schema for `product-kb.json` plus a one-shot validator:

```bash
#!/usr/bin/env bash
# product-kb-validate.sh — validate product-kb.json against schema.
# Usage: product-kb-validate.sh path/to/product-kb.json
set -euo pipefail
kb="${1:?usage: product-kb-validate.sh KB.json}"
schema="$(dirname "$0")/product-kb.schema.json"
cat > "$schema" <<'JSON'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["purpose","capabilities","limits","use_cases","audience"],
  "properties": {
    "purpose": {"type":"string","minLength":20,"maxLength":240},
    "capabilities": {"type":"array","minItems":3,"items":{
      "type":"object",
      "required":["name","description","status","since_version"],
      "properties":{
        "name":{"type":"string"},
        "description":{"type":"string","minLength":20},
        "example":{"type":"string"},
        "status":{"enum":["ga","beta","deprecated"]},
        "since_version":{"type":"string"}}}},
    "limits": {"type":"array","minItems":3,"items":{
      "type":"object",
      "required":["scope","rationale"],
      "properties":{
        "scope":{"type":"string"},
        "rationale":{"type":"string"},
        "workaround":{"type":["string","null"]}}}},
    "use_cases": {"type":"array","minItems":2},
    "audience": {"type":"object",
      "required":["industry","role"],
      "properties":{"industry":{"type":"string"},"role":{"type":"string"},
                    "company_size":{"type":"string"}}}
  }
}
JSON
ajv validate -s "$schema" -d "$kb" --strict=true
```

Wire this into pre-commit so a release cannot ship a KB missing limits, deprecated-status flags, or audience anchoring.

## Best practices
- **Single source of truth, multiple renders.** `product-kb.json` is canonical; `llms.txt`, JSON-LD, FAQ page, MCP tool descriptions, marketing one-liners are all generated from it. No hand-edits downstream.
- **Limits are first-class.** Every capability ships with at least one `limits[]` entry. A KB with no limits is a KB nobody trusts.
- **Version every capability.** `status: ga|beta|deprecated` + `since_version` lets agents avoid recommending sunset features. Without this, AI keeps surfacing yesterday's product.
- **Probe weekly across ≥3 frontier models.** Single-model probing is biased; rotate Claude, GPT, Gemini, Perplexity at minimum, score the diff.
- **Track answer accuracy as a real metric.** Treat "AI representation accuracy" as you would NPS — set a target (e.g. ≥85%), put it on a dashboard, regress on it after each release.
- **Co-locate KB with code.** `product-kb.json` lives in the product repo, not the marketing repo; release pipeline rebuilds renders. This is the only way to prevent capability-version skew.
- **Write purpose in customer language, not marketing language.** Strip adjectives ("powerful", "intuitive", "next-gen"); LLMs and humans both ignore them. State who, what, in one sentence.
- **Publish an "is not" section.** A docs page titled "What this product is not" cuts AI miscategorization more than any positive statement. List 3–5 things customers commonly assume but are false.
- **Keep `llms.txt` short.** ≤200 lines, links to `llms-full.txt` for depth. Bloat reduces retrieval quality.
- **Localize structurally, not as translation.** Each locale has its own KB rendering pipeline; never machine-translate capability statements without review — limits and prerequisites mistranslate dangerously.

## AI-agent gotchas
- **Marketing-tone leakage.** Generator agents default to adjective-heavy copy; force a "no adjectives, no superlatives" constraint in the system prompt and lint generated output for banned tokens (`best`, `leading`, `revolutionary`, `seamless`).
- **Capability invention.** Extractor agents will fabricate capabilities to fill empty fields ("AI-powered analytics" when there's no analytics module). Refuse-on-unknown must be enforced via prompt + post-hoc validator that grep's capability names against the source code or feature flag registry.
- **Limit erosion across passes.** Multi-step pipelines lose limits because each pass summarizes; preserve the `limits[]` array verbatim, never re-summarize.
- **Probe agents anchor on prior answers.** Same prompt + same model = cached or anchored response across runs. Vary phrasing, vary user role, vary timing. Otherwise the accuracy score is artificially stable.
- **Hallucinated `since_version`.** Agents will guess versions if not given a changelog. Hard requirement: extractor must read a real changelog or refuse.
- **Schema bloat.** Generator agents produce maximalist JSON-LD with every optional field. AI retrieval prefers small, dense, accurate. Cap field count; lint with `structured-data-testing-tool`.
- **Confidentiality leak.** Capability statements often reveal unlaunched features, internal infra (vendor names, region IDs, partner SKUs). Run `password-scrubber-agent` before any external publish.
- **No human checkpoint on `deprecated` flips.** Marking a capability `deprecated` removes it from AI-mediated discovery and impacts revenue. Always require a product-owner sign-off before status changes; never let the agent flip status autonomously.
- **Cross-locale drift via auto-translation.** Translation agents will helpfully translate "limit" as a synonym that loses legal precision. Limits and disclaimers go through human review per locale; non-negotiable.
- **`llms.txt` echo chamber.** Many sites copy each other's `llms.txt`; the agent will follow the herd and produce a generic file. Force a pre-publish diff against the top-3 competitors' `llms.txt`; if similarity >0.7, regenerate.
- **Probe-set staleness.** Canonical question sets calcify; the product evolves but the questions don't, so accuracy looks flat. Refresh the question set whenever a new capability ships or a customer reports a wrong AI answer.

## References
- "llms.txt — a proposal" — https://llmstxt.org/
- schema.org `Product` / `SoftwareApplication` / `FAQPage` — https://schema.org/Product
- Google Search Central, "AI Overviews and your site" — https://developers.google.com/search
- Anthropic, "Building tools and skills" — https://docs.anthropic.com/en/docs/build-with-claude
- OpenAI, "Custom GPT actions and metadata" — https://platform.openai.com/docs/actions
- EU AI Act Article 13 — Transparency obligations — https://artificialintelligenceact.eu/article/13/
- Profound, "AEO benchmark report 2026" — https://tryprofound.com/research
- Mintlify, "llms.txt and AI-answer telemetry" — https://mintlify.com/docs
- Sibling methodologies: `pro/product/product-operations/product-led-growth/`, `pro/product/product-operations/experimentation-at-scale/`, `solo/product/product-operations/`.
