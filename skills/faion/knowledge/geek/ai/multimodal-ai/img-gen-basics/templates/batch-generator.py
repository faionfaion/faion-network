"""BatchImageGenerator with ThreadPoolExecutor and rate-limit-safe variant."""
import time
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI, RateLimitError


class BatchImageGenerator:
    """Generate multiple images. Use safe_batch_generate for DALL-E tier-1."""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.client = OpenAI()

    def generate_batch(self, prompts: list[str], **kwargs) -> list[dict]:
        """Parallel generation. Risk: hits rate limits on tier-1 keys."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [(p, executor.submit(self._generate_single, p, **kwargs))
                       for p in prompts]
        for prompt, future in futures:
            try:
                results.append({"prompt": prompt, "success": True, **future.result()})
            except Exception as e:
                results.append({"prompt": prompt, "success": False, "error": str(e)})
        return results

    def _generate_single(self, prompt: str, **kwargs) -> dict:
        response = self.client.images.generate(
            model="dall-e-3", prompt=prompt, **kwargs
        )
        return {"url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt}


def safe_batch_generate(prompts: list[str], size: str = "1024x1024",
                        delay: float = 12.0) -> list[dict]:
    """
    Rate-limit-safe batch generation for DALL-E tier-1 (5 img/min = 12s/img).
    Retries up to 3 times on RateLimitError with exponential backoff.
    """
    client = OpenAI()
    results = []
    for i, prompt in enumerate(prompts):
        for attempt in range(3):
            try:
                resp = client.images.generate(
                    model="dall-e-3", prompt=prompt, size=size, n=1)
                results.append({
                    "prompt": prompt,
                    "url": resp.data[0].url,
                    "revised": resp.data[0].revised_prompt
                })
                break
            except RateLimitError:
                time.sleep(delay * (2 ** attempt))
        else:
            results.append({"prompt": prompt, "error": "rate_limit"})
        # Inter-image delay — respect 5 img/min limit
        if i < len(prompts) - 1:
            time.sleep(delay)
    return results
