# Video Generation

AI video generation: text-to-video, image-to-video APIs, production workflows.

## Overview

Video generation has evolved rapidly with commercial APIs from Runway, Luma, OpenAI Sora, and Google Veo providing production-ready solutions.

## Providers Comparison (2025-2026)

| Provider | Model | Max Duration | Resolution | API Status | Pricing |
|----------|-------|--------------|------------|------------|---------|
| **Runway** | Gen-3 Alpha | 10s | 1080p | Public API | $15/mo + credits |
| **Luma AI** | Dream Machine | 5s extendable | 1080p | Public API | Credits-based |
| **OpenAI** | Sora 2 | 60s | 1080p | Limited API | ChatGPT Plus/Pro |
| **Google** | Veo 3 | 8s | 4K | Limited API | Vertex AI |
| **Replicate** | Various | Varies | Varies | Public API | Per-generation |
| **Kling** | Kling 1.5 | 10s | 1080p | Public API | Credits-based |

## Capabilities Matrix

| Feature | Runway | Luma | Sora 2 | Veo 3 |
|---------|--------|------|--------|-------|
| Text-to-video | Yes | Yes | Yes | Yes |
| Image-to-video | Yes | Yes | Yes | Yes |
| Video-to-video | Yes | No | Limited | Yes |
| Video extension | Yes | Yes | No | Yes |
| Lip-sync | Yes | No | No | No |
| Native audio | No | No | Yes | Yes |
| Motion control | Yes | Limited | Limited | Yes |
| Character consistency | Good | Good | Excellent | Excellent |

## Provider Selection

**Choose Runway Gen-3 when:**
- Need reliable production API
- Video-to-video transformations
- Lip-sync for talking head videos
- Precise motion control

**Choose Luma Dream Machine when:**
- Simple text-to-video workflow
- Image animation
- Need video extension capabilities
- Budget-conscious projects

**Choose Sora 2 when:**
- Highest quality is priority
- Long-form content (up to 60s)
- Photorealistic output required
- Have ChatGPT Pro subscription

**Choose Veo 3 when:**
- Need 4K resolution
- Native audio/dialogue required
- Google Cloud infrastructure
- Enterprise scale

**Choose Replicate when:**
- Need open-source models
- Custom model fine-tuning
- Cost optimization via self-hosting
- Experimental workflows

## Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples for all providers |
| [templates.md](templates.md) | Production service templates |
| [llm-prompts.md](llm-prompts.md) | Video prompt engineering |

## Market Context

- Text-to-video market: $0.4B (2025) projected to $1.18B (2029)
- Global AI video generator market: $2.56B by 2032 (19.5% CAGR)
- Key trend: Native audio integration (Sora 2, Veo 3)
- Key trend: 4K resolution becoming standard

## References

- [Runway ML API](https://runwayml.com/api)
- [Luma AI API](https://lumalabs.ai/api)
- [OpenAI Sora](https://openai.com/index/sora/)
- [Google Veo](https://deepmind.google/technologies/veo/)
- [Replicate Video Models](https://replicate.com/collections/video-generation)

## Related

- [image-generation/](../image-generation/README.md) - Image generation (DALL-E, Stable Diffusion)
- [text-to-speech/](../text-to-speech/README.md) - TTS and voice synthesis
- [faion-multimodal-ai](../../faion-multimodal-ai/CLAUDE.md) - Multimodal AI routing
