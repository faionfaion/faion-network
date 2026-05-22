<!--
purpose: filled SASSCL template with provider-specific overlay slot
consumes: brand-style.yaml + creative brief
produces: spec (prompt text for video provider)
depends-on: prompt-template.yaml schema
token-budget-impact: ~200 tokens per generation
-->

# SASSCL Template

| Field | Value |
|-------|-------|
| Subject | {character_name}, mid-30s, wearing {wardrobe}, {distinguishing_features} |
| Action | walking confidently / running / sitting / etc. + manner |
| Setting | {location} + {time_of_day} |
| Style | brand X aesthetic: 35mm film grain, slight desaturation |
| Camera | {camera_movement} + {lens} |
| Lighting | {natural light + direction} |

## Provider overlay slot
Append per provider-quirks.md notes:
- Runway: "tracking shot from {direction}, {speed} dolly forward, motion blur on {part}"
- Luma: "the air feels warm; light dances on the surface; subject moves with quiet purpose"
- Sora: "starting with {first state}, gradually transitioning to {second state} over the clip"
- Veo: "ambient {audio cue}; subtle {sound}; 4K resolution"

## Concatenated prompt
{Subject}, {Action}, in {Setting}. Style: {Style}. Camera: {Camera}. Lighting: {Lighting}. {Provider overlay}
