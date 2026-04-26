"""RunwayVideoGenerator: text-to-video and image-to-video via Runway SDK."""
import runwayml
import time
from typing import Optional


class RunwayVideoGenerator:
    """Generate videos using Runway Gen-3 Alpha Turbo."""

    def __init__(self):
        self.client = runwayml.RunwayML()

    def generate_from_text(self, prompt: str, duration: int = 5,
                           aspect_ratio: str = "16:9",
                           seed: Optional[int] = None) -> dict:
        task = self.client.image_to_video.create(
            model="gen3a_turbo", prompt_text=prompt,
            duration=duration, ratio=aspect_ratio, seed=seed
        )
        return self._wait_for_completion(task.id)

    def generate_from_image(self, image_url: str, prompt: str,
                            duration: int = 5) -> dict:
        task = self.client.image_to_video.create(
            model="gen3a_turbo", prompt_image=image_url,
            prompt_text=prompt, duration=duration
        )
        return self._wait_for_completion(task.id)

    def _wait_for_completion(self, task_id: str, timeout: int = 300) -> dict:
        """Poll for task completion. Runway tasks can take 3-5 minutes."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.client.tasks.retrieve(task_id)
            if task.status == "SUCCEEDED":
                return {"status": "success", "video_url": task.output[0],
                        "task_id": task_id}
            elif task.status == "FAILED":
                # Content policy failures return terse error — do not retry same prompt
                return {"status": "failed", "error": task.failure, "task_id": task_id}
            time.sleep(5)
        return {"status": "timeout", "task_id": task_id}
