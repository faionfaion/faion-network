"""MultiProviderImageService with ordered provider fallback."""
import logging
from openai import OpenAI


class MultiProviderImageService:
    """Image generation with provider fallback. Result always includes provider field."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate(self, prompt: str,
                 providers: list[str] | None = None, **kwargs) -> dict:
        """
        Try providers in order; return first success.
        providers: ["dalle3", "flux", "sdxl"]
        Always include provider in result — silent fallback must be visible.
        """
        providers = providers or ["dalle3", "flux"]
        errors = {}
        for provider in providers:
            try:
                self.logger.info(f"Trying {provider}")
                result = self._dispatch(provider, prompt, **kwargs)
                result["provider"] = provider  # always expose which provider was used
                return result
            except Exception as e:
                self.logger.warning(f"{provider} failed: {e}")
                errors[provider] = str(e)
        raise RuntimeError(f"All providers failed: {errors}")

    def _dispatch(self, provider: str, prompt: str, **kwargs) -> dict:
        if provider == "dalle3":
            return self._dalle3(prompt, **kwargs)
        elif provider == "sdxl":
            return self._sdxl(prompt, **kwargs)
        elif provider == "flux":
            return self._flux(prompt, **kwargs)
        raise ValueError(f"Unknown provider: {provider}")

    def _dalle3(self, prompt: str, size: str = "1024x1024",
                quality: str = "standard", style: str = "vivid") -> dict:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size=size, quality=quality,
            style=style, n=1
        )
        return {"url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt}

    def _sdxl(self, prompt: str, size: str = "1024x1024", **_) -> dict:
        import replicate
        width, height = map(int, size.split("x"))
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": prompt, "width": width, "height": height}
        )
        return {"url": output[0]}

    def _flux(self, prompt: str, **_) -> dict:
        import replicate
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt, "output_format": "webp"}
        )
        return {"url": str(next(iter(output)))}
