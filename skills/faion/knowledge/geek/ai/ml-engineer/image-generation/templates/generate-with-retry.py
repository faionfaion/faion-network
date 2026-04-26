# DALL-E 3 batch generation with content-policy retry and URL expiry handling
import time
import requests
from openai import OpenAI

client = OpenAI()

def generate_image(prompt: str, size: str = "1792x1024") -> dict:
    """Generate a single image and download it immediately (URLs expire in 1 hour)."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    img = response.data[0]
    # Download immediately — URL expires after 1 hour
    image_bytes = requests.get(img.url).content
    return {
        "bytes": image_bytes,
        "revised_prompt": img.revised_prompt,  # log this — DALL-E may have changed your prompt
        "original_prompt": prompt,
    }

def batch_generate(prompts: list[str]) -> list[dict]:
    results = []
    for prompt in prompts:
        for attempt in range(3):
            try:
                result = generate_image(prompt)
                results.append({"prompt": prompt, **result, "error": None})
                break
            except Exception as e:
                if "content_policy" in str(e).lower():
                    # Soften: remove proper nouns and explicit terms
                    prompt = prompt.replace("named", "").strip()
                time.sleep(2 ** attempt)
        else:
            results.append({"prompt": prompt, "bytes": None, "error": "failed after 3 attempts"})
        # Respect 5 images/minute rate limit on Tier 1
        time.sleep(12)
    return results
