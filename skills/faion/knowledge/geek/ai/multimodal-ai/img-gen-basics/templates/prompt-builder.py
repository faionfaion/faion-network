"""ImagePromptBuilder fluent API with style/lighting/composition/technical fields."""


class ImagePromptBuilder:
    """Build structured image generation prompts from typed components."""

    STYLES = {
        "photorealistic": "photorealistic, highly detailed photograph",
        "digital_art": "digital art, vibrant colors",
        "oil_painting": "oil painting, textured brushstrokes",
        "watercolor": "watercolor painting, soft edges, fluid",
        "anime": "anime style, cel shading",
        "3d_render": "3D render, octane render, highly detailed",
        "sketch": "pencil sketch, hand-drawn",
        "minimalist": "minimalist, clean lines, simple"
    }

    LIGHTING = {
        "golden_hour": "golden hour lighting, warm tones",
        "studio": "professional studio lighting",
        "dramatic": "dramatic lighting, high contrast",
        "soft": "soft diffused lighting",
        "neon": "neon lighting, cyberpunk atmosphere",
        "natural": "natural daylight"
    }

    TECHNICAL = {
        "4k": "4K resolution, ultra detailed",
        "8k": "8K resolution, extremely detailed",
        "depth_of_field": "shallow depth of field, bokeh",
        "wide_angle": "wide angle lens",
        "macro": "macro photography, extreme detail",
        "cinematic": "cinematic composition, film grain"
    }

    def __init__(self):
        self.components: dict[str, str | list] = {
            "subject": "", "style": "", "lighting": "",
            "composition": "", "mood": "", "details": [], "technical": []
        }

    def set_subject(self, subject: str) -> "ImagePromptBuilder":
        self.components["subject"] = subject
        return self

    def set_style(self, style: str) -> "ImagePromptBuilder":
        self.components["style"] = self.STYLES.get(style, style)
        return self

    def set_lighting(self, lighting: str) -> "ImagePromptBuilder":
        self.components["lighting"] = self.LIGHTING.get(lighting, lighting)
        return self

    def set_composition(self, composition: str) -> "ImagePromptBuilder":
        self.components["composition"] = composition
        return self

    def set_mood(self, mood: str) -> "ImagePromptBuilder":
        self.components["mood"] = mood
        return self

    def add_detail(self, detail: str) -> "ImagePromptBuilder":
        self.components["details"].append(detail)
        return self

    def add_technical(self, spec: str) -> "ImagePromptBuilder":
        self.components["technical"].append(self.TECHNICAL.get(spec, spec))
        return self

    def build(self) -> str:
        parts = []
        for key in ("subject", "style", "lighting", "composition"):
            if self.components[key]:
                parts.append(self.components[key])
        if self.components["mood"]:
            parts.append(f"{self.components['mood']} mood")
        parts.extend(self.components["details"])
        parts.extend(self.components["technical"])
        return ", ".join(parts)
