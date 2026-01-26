# Image Generation Checklist

## Pre-Generation Checklist

### 1. Requirements Analysis

- [ ] Define use case (marketing, product, social, UI)
- [ ] Identify target audience
- [ ] Determine required dimensions/aspect ratio
- [ ] Check content policy compliance
- [ ] Estimate budget (API costs)

### 2. Model Selection

| Factor | DALL-E 3 | Stable Diffusion | Flux | Midjourney |
|--------|----------|------------------|------|------------|
| Prompt adherence | Excellent | Good | Excellent | Good |
| Speed | Medium | Fast (Turbo) | Very Fast | Medium |
| Customization | Low | High (LoRA) | Medium | Low |
| Text rendering | Good | Poor | Medium | Poor |
| Anatomy accuracy | Good | Medium | Excellent | Good |
| Cost efficiency | Medium | Low/Free | Low | Medium |
| Local deployment | No | Yes | Yes | No |

**Decision:**
- [ ] Selected model: _______________
- [ ] Reason: _______________

### 3. Prompt Preparation

- [ ] Subject clearly defined
- [ ] Style/aesthetic specified
- [ ] Lighting described
- [ ] Composition/framing set
- [ ] Mood/atmosphere indicated
- [ ] Technical specs included (resolution, quality)
- [ ] Negative prompts prepared (if using SD)

### 4. Technical Setup

- [ ] API keys configured
- [ ] Rate limits understood
- [ ] Error handling implemented
- [ ] Caching strategy defined
- [ ] Output storage prepared

---

## Quality Gates

### Gate 1: Prompt Review

```
Before generating, verify prompt includes:
[ ] Clear subject (1 sentence)
[ ] 4-6 high-signal details
[ ] Style reference
[ ] No conflicting instructions
[ ] Content policy compliant
```

### Gate 2: Generation Review

```
After generation, check:
[ ] Subject matches request
[ ] Style is consistent
[ ] No artifacts or distortions
[ ] Text rendered correctly (if any)
[ ] Appropriate for use case
[ ] No copyright concerns
```

### Gate 3: Production Ready

```
Before deployment:
[ ] Resolution matches requirements
[ ] File format appropriate (PNG, WebP, JPEG)
[ ] File size optimized
[ ] Metadata stripped (if needed)
[ ] Backup/archive created
```

---

## Cost Optimization Checklist

### Before Batch Generation

- [ ] Test with single image first
- [ ] Use standard quality for drafts
- [ ] Cache successful generations
- [ ] Consider local alternatives for high volume
- [ ] Batch similar requests together

### Cost Comparison (per 1000 images)

| Model | Standard | HD/High Quality |
|-------|----------|-----------------|
| DALL-E 3 (1024x1024) | $40 | $80 |
| DALL-E 3 (1792x1024) | $80 | $120 |
| Flux.2 klein | ~$14 | - |
| Stable Diffusion (Replicate) | $5-20 | $10-40 |
| Self-hosted SD | ~$0 (compute only) | ~$0 |

---

## Content Safety Checklist

### Pre-Generation

- [ ] Review platform content policies
- [ ] Avoid prohibited content categories
- [ ] No real people without consent
- [ ] No copyrighted characters (use descriptions instead)
- [ ] No misleading/deceptive content

### Post-Generation

- [ ] Run safety classifier on output
- [ ] Review for unintended content
- [ ] Verify no identifiable faces (if unwanted)
- [ ] Check for brand/logo issues

---

## Production Deployment Checklist

### Infrastructure

- [ ] API rate limiting configured
- [ ] Retry logic with exponential backoff
- [ ] Timeout handling (images can take 10-60s)
- [ ] Queue system for batch requests
- [ ] Monitoring and alerting

### Storage

- [ ] Image storage configured (S3, GCS, etc.)
- [ ] CDN for delivery
- [ ] Backup strategy
- [ ] Retention policy

### Security

- [ ] API keys in secrets manager
- [ ] No keys in client-side code
- [ ] User input sanitization
- [ ] Rate limiting per user

---

## Troubleshooting Checklist

### Generation Failed

- [ ] Check API key validity
- [ ] Verify rate limits not exceeded
- [ ] Review prompt for policy violations
- [ ] Check network connectivity
- [ ] Try simpler prompt
- [ ] Try different model

### Poor Quality Output

- [ ] Add more specific details to prompt
- [ ] Try different style keywords
- [ ] Use HD/high quality setting
- [ ] Increase inference steps (SD)
- [ ] Try different seed values
- [ ] Iterate and refine prompt

### Inconsistent Results

- [ ] Use fixed seed for reproducibility
- [ ] Create detailed style guide in prompt
- [ ] Use reference images (Flux Kontext)
- [ ] Document successful prompts
- [ ] Build prompt templates
