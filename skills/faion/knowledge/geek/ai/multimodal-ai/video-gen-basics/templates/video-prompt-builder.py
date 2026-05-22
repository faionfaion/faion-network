# purpose: Fluent VideoPromptBuilder enforcing explicit camera + style + lighting per rule r1.
# consumes: brief fields (subject, action, setting, camera, style, lighting, details).
# produces: structured comma-joined prompt string ready for provider submission.
# depends-on: nothing (pure Python); used by generate() in video-gen-basics + video-gen-tools.
# token-budget-impact: zero (no LLM call); ~30-60 prompt tokens depending on detail count.
"""VideoPromptBuilder fluent API enforcing closed camera vocabulary."""


class VideoPromptBuilder:
    """Build structured prompts for video generation."""

    CAMERA_MOVEMENTS = {
        "static": "static camera, locked shot",
        "pan_left": "smooth pan left",
        "pan_right": "smooth pan right",
        "dolly_in": "dolly in, moving closer",
        "dolly_out": "dolly out, pulling back",
        "tracking": "tracking shot, following subject",
        "crane": "crane shot, rising up",
        "handheld": "handheld camera, slight shake",
        "drone": "aerial drone shot",
        "orbit": "orbiting around subject"
    }

    STYLES = {
        "cinematic": "cinematic, film quality, 35mm",
        "documentary": "documentary style, natural",
        "commercial": "commercial quality, polished",
        "artistic": "artistic, stylized",
        "anime": "anime style, animation",
        "realistic": "photorealistic, lifelike"
    }

    def __init__(self):
        self.components: dict[str, str | list] = {
            "subject": "", "action": "", "setting": "",
            "camera": "", "style": "", "lighting": "", "details": []
        }

    def set_subject(self, subject: str) -> "VideoPromptBuilder":
        self.components["subject"] = subject
        return self

    def set_action(self, action: str) -> "VideoPromptBuilder":
        self.components["action"] = action
        return self

    def set_setting(self, setting: str) -> "VideoPromptBuilder":
        self.components["setting"] = setting
        return self

    def set_camera(self, camera: str) -> "VideoPromptBuilder":
        self.components["camera"] = self.CAMERA_MOVEMENTS.get(camera, camera)
        return self

    def set_style(self, style: str) -> "VideoPromptBuilder":
        self.components["style"] = self.STYLES.get(style, style)
        return self

    def set_lighting(self, lighting: str) -> "VideoPromptBuilder":
        self.components["lighting"] = lighting
        return self

    def add_detail(self, detail: str) -> "VideoPromptBuilder":
        self.components["details"].append(detail)
        return self

    def build(self) -> str:
        parts = []
        for key in ("subject", "action"):
            if self.components[key]:
                parts.append(self.components[key])
        if self.components["setting"]:
            parts.append(f"in {self.components['setting']}")
        for key in ("camera", "style", "lighting"):
            if self.components[key]:
                parts.append(self.components[key])
        parts.extend(self.components["details"])
        return ", ".join(parts)
