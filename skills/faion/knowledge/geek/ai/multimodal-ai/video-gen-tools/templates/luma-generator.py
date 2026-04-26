"""LumaVideoGenerator: generate, extend, image-to-video via Luma REST API."""
import requests
import time


class LumaVideoGenerator:
    """Generate videos using Luma AI Dream Machine (no official Python SDK)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate(self, prompt: str, aspect_ratio: str = "16:9",
                 loop: bool = False) -> dict:
        response = requests.post(f"{self.base_url}/generations",
                                 headers=self.headers,
                                 json={"prompt": prompt, "aspect_ratio": aspect_ratio,
                                       "loop": loop})
        return self._wait_for_completion(response.json()["id"])

    def generate_from_image(self, prompt: str, image_url: str) -> dict:
        payload = {"prompt": prompt, "keyframes": {
            "frame0": {"type": "image", "url": image_url}
        }}
        response = requests.post(f"{self.base_url}/generations",
                                 headers=self.headers, json=payload)
        return self._wait_for_completion(response.json()["id"])

    def extend_video(self, video_id: str, prompt: str) -> dict:
        """Extend using generation ID (not video URL) in keyframes."""
        payload = {"prompt": prompt, "keyframes": {
            "frame0": {"type": "generation", "id": video_id}  # ID, not URL
        }}
        response = requests.post(f"{self.base_url}/generations",
                                 headers=self.headers, json=payload)
        return self._wait_for_completion(response.json()["id"])

    def _wait_for_completion(self, generation_id: str, timeout: int = 300) -> dict:
        """Fixed version with timeout — original would loop infinitely."""
        start = time.time()
        while time.time() - start < timeout:
            response = requests.get(f"{self.base_url}/generations/{generation_id}",
                                    headers=self.headers)
            gen = response.json()
            if gen["state"] == "completed":
                return {"status": "success",
                        "video_url": gen["assets"]["video"], "id": generation_id}
            elif gen["state"] == "failed":
                return {"status": "failed",
                        "error": gen.get("failure_reason"), "id": generation_id}
            time.sleep(5)
        return {"status": "timeout", "id": generation_id}
