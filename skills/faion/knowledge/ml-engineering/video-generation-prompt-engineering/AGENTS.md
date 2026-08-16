# AI Video Generation Prompt Engineering

## Summary

**One-sentence:** Composes video gen prompts with the SASSCL formula (Subject + Action + Setting + Style + Camera + Lighting) and gates promotion behind a per-prompt human-rated eval on 5 generations.

**One-paragraph:** Naive prompts ("a dog running") produce wobbly, off-model output. SASSCL gives consistent results: Subject (precisely described), Action (concrete verb + manner), Setting (location + time of day), Style (cinematic / anime / hyperreal / etc.), Camera (POV / dolly / static / handheld), Lighting (golden hour / overcast / neon). Provider quirks matter: Runway loves detailed camera moves; Luma wants prose; Veo handles longer prompts; Sora needs structured. Output: a `prompt-template.yaml` + a 5-gen eval that gates promotion.

**Ефективно для:**

- Media pipelines що автоматично генерують роліки — стандартизована prompt structure дає predictable якість.
- A/B prompt iteration — формула + eval гейт показує, який варіант кращий.
- Multi-provider strategy — той самий SASSCL шаблон з провайдер-специфічними corner adjustments.
- Brand consistency — Style + Camera + Lighting залишаються фіксованими, лише Subject + Action міняються.

## Applies If (ALL must hold)

- Using AI video gen in production OR running &gt;100 generations
- Have a way to rate output (human OR LLM-judge)
- Goal is consistent quality across many generations

## Skip If (ANY kills it)

- One-off creative exploration — formula constrains creativity
- &lt;10 generations total — investment not paid back
- Single-shot use, no iteration — eval gate has no purpose

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `brand-style.yaml` | YAML | brand / style guide |
| `eval-rubric.yaml` | YAML | per-prompt rating criteria |
| `provider-quirks.md` | Markdown | provider-specific notes |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `video-generation-async-api` | Underlying primitive |
| `video-generation-production-service` | Where prompts are consumed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: SASSCL formula, provider-quirk overlay, 5-gen eval gate, max-prompt-length per provider, brand style locked | 1100 |
| `content/02-output-contract.xml` | essential | prompt-template.yaml schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: terse prompt, generic style, no eval, no provider quirks, brand drift | 900 |
| `content/04-procedure.xml` | essential | 5 steps: draft prompt with SASSCL → apply provider quirks → 5-gen eval → promote OR iterate → audit | 700 |
| `content/05-examples.xml` | essential | Worked example: 30s cinematic walk-cycle prompt for Runway | 500 |
| `content/06-decision-tree.xml` | essential | Routes by provider to prompt-style adjustments | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prompt_drafting` | sonnet | Creative + structured |
| `eval_judgement` | sonnet | Cross-shot consistency |
| `prompt_template_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/sasscl-template.md.j2` | Filled-in SASSCL example |
| `templates/sasscl-template.md` | Filled-in SASSCL example Generated from `templates/sasscl-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/prompt-template.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable spec |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-generation-prompt-engineering.py` | Lint prompt-template.yaml | Pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[video-generation-async-api]] · [[video-generation-production-service]]
- external: [Runway prompt guide](https://help.runwayml.com/) · [Luma prompts](https://lumalabs.ai/learn) · [Sora system card](https://openai.com/sora)

## Decision tree

See `content/06-decision-tree.xml`. Routes prompt-style adjustments by chosen provider (Runway / Luma / Veo / Sora).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-template.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [provider, sasscl, provider_overlay, max_chars, eval, brand_locks]
properties:
  provider: {type: string, enum: [runway, luma, veo, sora, kling]}
  sasscl:
    type: object
    required: [subject_slot, action_slot, setting, style, camera, lighting]
    properties:
      subject_slot: {type: string}
      action_slot: {type: string}
      setting: {type: string}
      style: {type: string}
      camera: {type: string}
      lighting: {type: string}
  provider_overlay: {type: string, minLength: 5}
  max_chars: {type: integer, minimum: 100, maximum: 4000}
  eval:
    type: object
    required: [rubric_path, sample_size, promotion_threshold]
    properties:
      sample_size: {type: integer, minimum: 5}
      promotion_threshold: {type: number, minimum: 0.8, maximum: 1.0}
  brand_locks:
    type: array
    items: {type: string, enum: [style, camera, lighting]}
    minItems: 3
```

### `templates/_smoke-test.yaml`

```yaml
provider: runway
provider_overlay: "tracking shot from right, slow dolly, motion blur"
max_chars: 480
sasscl:
  subject_slot: "character X mid-30s wearing brand wardrobe"
  action_slot: "walking confidently looking forward"
  setting: "Lisbon riverside late afternoon"
  style: "cinematic 35mm slight desaturation"
  camera: "tracking right 24mm wide"
  lighting: "golden hour warm rim light"
eval:
  rubric_path: evals/brand-x-rubric.yaml
  sample_size: 5
  promotion_threshold: 0.8
brand_locks: [style, camera, lighting]
```
