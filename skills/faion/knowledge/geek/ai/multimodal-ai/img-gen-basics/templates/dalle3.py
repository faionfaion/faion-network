"""DALL-E 3 generation: generate_image, generate_and_save, DALL-E 2 variations/edit."""
import base64
import requests
from openai import OpenAI

client = OpenAI()


def generate_image(prompt: str, size: str = "1024x1024",
                   quality: str = "standard", style: str = "vivid") -> dict:
    """
    Generate with DALL-E 3. Always log revised_prompt.
    size: "1024x1024" | "1792x1024" | "1024x1792"
    quality: "standard" | "hd"
    style: "vivid" (creative) | "natural" (photorealistic products)
    """
    response = client.images.generate(
        model="dall-e-3", prompt=prompt,
        size=size, quality=quality, style=style, n=1
    )
    return {
        "url": response.data[0].url,
        "revised_prompt": response.data[0].revised_prompt  # log — can diverge from input
    }


def generate_and_save(prompt: str, output_path: str, **kwargs) -> str:
    """Generate and download immediately. URLs expire in ~1 hour."""
    result = generate_image(prompt, **kwargs)
    response = requests.get(result["url"], timeout=30)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def generate_variations(image_path: str, n: int = 3) -> list[str]:
    """DALL-E 2 only. Requires PNG with alpha channel — JPEG causes 400 error."""
    with open(image_path, "rb") as f:
        response = client.images.create_variation(
            image=f, n=n, size="1024x1024", model="dall-e-2"
        )
    return [img.url for img in response.data]


def edit_image(image_path: str, mask_path: str, prompt: str) -> str:
    """DALL-E 2 only. Both image and mask must be PNG with alpha channel."""
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = client.images.edit(
            image=img, mask=mask, prompt=prompt,
            n=1, size="1024x1024", model="dall-e-2"
        )
    return response.data[0].url


def describe_image(image_path: str) -> str:
    """Describe image using GPT-4o Vision for describe-then-generate cycle."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Describe this image in detail for image generation."},
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        ]}]
    )
    return response.choices[0].message.content
