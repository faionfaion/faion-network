"""PromptTemplates static methods: product_photo, logo, social_media, ui_mockup."""


class PromptTemplates:
    """Reusable prompt templates. Use as single source of truth — avoid ad-hoc strings."""

    @staticmethod
    def product_photo(product: str,
                      background: str = "white studio background",
                      lighting: str = "professional studio lighting") -> str:
        return (f"{product}, {background}, {lighting}, "
                "product photography, high quality, commercial, 4K")

    @staticmethod
    def logo(concept: str, style: str = "minimalist",
             colors: str = "modern color palette") -> str:
        return (f"{style} logo design, {concept}, {colors}, "
                "vector art, clean, professional")

    @staticmethod
    def social_media(content: str, platform: str = "instagram",
                     mood: str = "vibrant") -> str:
        return (f"{content}, {mood} mood, social media post, "
                f"eye-catching, {platform} style")

    @staticmethod
    def ui_mockup(screen: str, style: str = "modern",
                  platform: str = "web") -> str:
        return (f"{style} {platform} interface, {screen}, "
                "clean design, professional UI/UX, Figma style")


def select_provider(use_case: str) -> str:
    """Provider selection heuristic by use case."""
    return {
        "product_photo": "dalle3",   # best photorealism
        "logo": "dalle3",            # clean vector-like output
        "social_media": "flux",      # fast and cheap for volume
        "mockup": "sdxl",            # controllable composition
    }.get(use_case, "dalle3")
