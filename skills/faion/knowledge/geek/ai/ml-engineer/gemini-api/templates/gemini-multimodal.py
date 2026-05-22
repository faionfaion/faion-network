"""
purpose: Image / audio / video input variants.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for gemini-api
token-budget-impact: ≤500 tokens to fill
"""

"""
Gemini multimodal helpers: image analyzer, video analyzer, document processor.
Requires: pip install google-generativeai pillow
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


class ImageAnalyzer:
    """Analyze images with Gemini vision."""

    def __init__(self, model_name: str = "gemini-2.0-flash") -> None:
        import PIL.Image  # noqa: PLC0415
        self._pil = PIL.Image
        self.model = genai.GenerativeModel(model_name)

    def analyze(self, image_path: str, prompt: str) -> str:
        """Run arbitrary prompt against an image."""
        image = self._pil.open(image_path)
        response = self.model.generate_content([prompt, image])
        return response.text

    def describe(self, image_path: str) -> str:
        """Return detailed description of image contents."""
        return self.analyze(image_path, "Describe this image in detail. Include objects, colors, composition, and any text visible.")

    def extract_text(self, image_path: str) -> str:
        """OCR: extract all text from image."""
        return self.analyze(image_path, "Extract all text visible in this image. Return plain text, preserving line breaks.")

    def compare(self, image_paths: list[str], prompt: str) -> str:
        """Compare multiple images with a custom prompt."""
        images = [self._pil.open(p) for p in image_paths]
        response = self.model.generate_content([prompt, *images])
        return response.text


class VideoAnalyzer:
    """Analyze video files with Gemini (via File API)."""

    def __init__(self, model_name: str = "gemini-1.5-pro") -> None:
        self.model = genai.GenerativeModel(model_name)
        self._cache: dict[str, genai.File] = {}

    def upload(self, video_path: str) -> genai.File:
        """Upload video and wait for processing to complete."""
        if video_path in self._cache:
            return self._cache[video_path]

        video_file = genai.upload_file(video_path)
        while video_file.state.name == "PROCESSING":
            time.sleep(5)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name != "ACTIVE":
            raise RuntimeError(f"Video processing failed: {video_file.state.name}")

        self._cache[video_path] = video_file
        return video_file

    def analyze(self, video_file: genai.File, prompt: str) -> str:
        """Run prompt against uploaded video file."""
        response = self.model.generate_content([prompt, video_file])
        return response.text

    def summarize(self, video_path: str) -> str:
        """Upload and summarize video."""
        f = self.upload(video_path)
        return self.analyze(f, "Summarize this video. Include key points, main scenes, and overall message.")

    def transcribe(self, video_path: str) -> str:
        """Transcribe all spoken words in video."""
        f = self.upload(video_path)
        return self.analyze(f, "Transcribe all spoken words in this video. Include speaker labels if multiple speakers.")


class DocumentProcessor:
    """Process PDFs and documents with Gemini."""

    def __init__(self, model_name: str = "gemini-1.5-pro") -> None:
        self.model = genai.GenerativeModel(model_name)
        self._file_cache: dict[str, genai.File] = {}

    def upload(self, file_path: str) -> genai.File:
        """Upload document (caches by path)."""
        if file_path in self._file_cache:
            return self._file_cache[file_path]
        file = genai.upload_file(file_path)
        self._file_cache[file_path] = file
        return file

    def process(self, file_path: str, prompt: str) -> str:
        """Run custom prompt against document."""
        file = self.upload(file_path)
        response = self.model.generate_content([prompt, file])
        return response.text

    def summarize(self, file_path: str, length: str = "medium") -> str:
        """Summarize document. length: 'short'|'medium'|'long'."""
        lengths = {
            "short": "in 2-3 sentences",
            "medium": "in 1-2 paragraphs with key points",
            "long": "in detail covering all major sections",
        }
        instruction = lengths.get(length, lengths["medium"])
        return self.process(file_path, f"Summarize this document {instruction}.")

    def extract_structured(self, file_path: str, schema: dict[str, Any]) -> str:
        """Extract structured JSON from document per schema."""
        json_model = genai.GenerativeModel(
            model_name=self.model._model_name,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )
        file = self.upload(file_path)
        response = json_model.generate_content(["Extract the required fields from this document:", file])
        return response.text

    def answer(self, file_path: str, question: str) -> str:
        """Answer a question about the document."""
        return self.process(file_path, f"Based on this document, answer: {question}")


# Usage:
# img = ImageAnalyzer(); print(img.describe("photo.jpg"))
# vid = VideoAnalyzer(); print(vid.summarize("meeting.mp4"))
# doc = DocumentProcessor(); print(doc.summarize("report.pdf", length="short"))
