# purpose: VideoProcessor — ffmpeg/ffprobe wrapper for validation, concat, resize, audio merge.
# consumes: local mp4 paths; ffmpeg + ffprobe binaries on host.
# produces: validated mp4 outputs; ffprobe metadata JSON.
# depends-on: ffmpeg (apt install ffmpeg); subprocess module from stdlib.
# token-budget-impact: zero.
"""VideoProcessor: ffmpeg utilities + ffprobe validation per rule r3."""
import subprocess
import json
from pathlib import Path


class VideoProcessor:
    """ffmpeg/ffprobe utilities for video post-processing."""

    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """Get video metadata. Always call on output before downstream use."""
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_format", "-show_streams", video_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)

    @staticmethod
    def validate_output(video_path: str) -> bool:
        """Return True if file exists, size > 0, and has valid video stream."""
        p = Path(video_path)
        if not p.exists() or p.stat().st_size == 0:
            return False
        try:
            info = VideoProcessor.get_video_info(video_path)
            streams = info.get("streams", [])
            return any(s.get("codec_type") == "video" for s in streams)
        except Exception:
            return False

    @staticmethod
    def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> list[str]:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-i", video_path, "-vf", f"fps={fps}",
               f"{output_dir}/frame_%04d.png"]
        subprocess.run(cmd, check=True)
        return sorted(str(p) for p in Path(output_dir).glob("frame_*.png"))

    @staticmethod
    def concatenate_videos(video_paths: list[str], output_path: str) -> None:
        list_path = "/tmp/video_list.txt"
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0",
               "-i", list_path, "-c", "copy", output_path]
        subprocess.run(cmd, check=True)
        Path(list_path).unlink()

    @staticmethod
    def add_audio(video_path: str, audio_path: str, output_path: str) -> None:
        cmd = ["ffmpeg", "-i", video_path, "-i", audio_path,
               "-c:v", "copy", "-c:a", "aac", "-shortest", output_path]
        subprocess.run(cmd, check=True)

    @staticmethod
    def resize_video(video_path: str, output_path: str,
                     width: int, height: int) -> None:
        cmd = ["ffmpeg", "-i", video_path, "-vf", f"scale={width}:{height}",
               "-c:a", "copy", output_path]
        subprocess.run(cmd, check=True)
