# purpose: Replicate adapter with pinned sha hashes for SVD / AnimateDiff / Zeroscope (rule r3).
# consumes: image_path or prompt, motion_bucket_id, fps, num_frames, pinned model hash.
# produces: dict {status, video_url or list[url], prediction_id, error}.
# depends-on: replicate SDK; env REPLICATE_API_TOKEN; never use name-only resolution.
# token-budget-impact: zero LLM tokens.
"""ReplicateVideoGenerator: SVD / AnimateDiff / Zeroscope with pinned hashes."""
import replicate


class ReplicateVideoGenerator:
    """Generate videos using Replicate open models."""

    # Pin version hashes — update intentionally, not automatically
    MODELS = {
        "svd": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        "animatediff": "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48c9f",
        "zeroscope": "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
    }

    def generate_stable_video(self, image_path: str,
                               motion_bucket_id: int = 127,
                               fps: int = 7, num_frames: int = 25) -> str:
        """Image-to-video with Stable Video Diffusion. Returns URL string."""
        output = replicate.run(
            self.MODELS["svd"],
            input={"input_image": open(image_path, "rb"),
                   "motion_bucket_id": motion_bucket_id,
                   "fps": fps, "num_frames": num_frames}
        )
        return output  # SVD returns URL string directly

    def generate_with_animatediff(self, prompt: str, negative_prompt: str = "",
                                   num_frames: int = 16,
                                   guidance_scale: float = 7.5) -> str:
        output = replicate.run(
            self.MODELS["animatediff"],
            input={"prompt": prompt, "negative_prompt": negative_prompt,
                   "num_frames": num_frames, "guidance_scale": guidance_scale}
        )
        # Some models return iterator; handle both
        if hasattr(output, "__iter__") and not isinstance(output, str):
            return next(iter(output))
        return output

    def generate_with_zeroscope(self, prompt: str, num_frames: int = 24,
                                 fps: int = 8, width: int = 576,
                                 height: int = 320) -> str:
        output = replicate.run(
            self.MODELS["zeroscope"],
            input={"prompt": prompt, "num_frames": num_frames,
                   "fps": fps, "width": width, "height": height}
        )
        if hasattr(output, "__iter__") and not isinstance(output, str):
            return next(iter(output))
        return output
