# Adobe Firefly Integration

## Summary

Use Adobe Firefly Services REST API to batch-generate commercial-safe images, apply Generative Fill to placeholder regions, and produce vector assets from text prompts. Firefly is trained on licensed content with clear generative-credit accounting — it is the correct tool when commercial IP safety is required. All generated assets require a human brand-alignment review before production promotion.

## Why

Firefly's commercial licensing framework removes IP ambiguity that affects other generative image tools. Integration via the Firefly Services REST API enables automated batch generation pipelines (prompt → download → staging), but the API requires an Adobe enterprise plan and OAuth2 machine-to-machine auth. Generated outputs are starting points, not finals.

## When To Use

- Generating commercial-safe image assets for UI mockups, marketing banners, or product visuals
- Creating vector assets in Illustrator via text-to-vector prompts for icon sets
- Removing or replacing image backgrounds in Photoshop for product shots or hero images
- Producing asset variations (color, style, format) from a single source for A/B testing
- Applying AI-generated text effects and typography variations at scale

## When NOT To Use

- Design requires a coherent custom illustration style — Firefly outputs generic aesthetics
- Iterating on UI layout or component design — Figma is the correct tool
- Team has no Adobe CC enterprise licenses — generative credits are consumed per generation and the API requires enterprise plan
- Output must strictly match an established illustration system — Firefly cannot learn custom styles
- Speed is critical and assets must integrate directly into Figma without round-trips

## Content

| File | What's inside |
|------|---------------|
| `content/01-firefly-rules.xml` | Firefly capabilities per CC app, commercial framework, API rules, limitations |
| `content/02-agent-integration.xml` | Agent workflow, prompt patterns, service catalog, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/batch-generate.py` | Batch image generation script via Firefly Services REST API |
| `templates/firefly-prompt.txt` | Approved prompt template for hero image generation |
