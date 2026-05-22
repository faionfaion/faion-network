"""
purpose: Upload a video to Gemini Files API and query it with ACTIVE polling.
consumes: video file path + Gemini client
produces: text response from the model
depends-on: content/01-core-rules.xml r1, r2
token-budget-impact: per-call; video size dominates context tokens

analyze_video — upload a video to Gemini and query it with a polling guard.

Usage:
    text = analyze_video("presentation.mp4", "Summarize the key points")
"""
import time
import google.generativeai as genai


def analyze_video(
    path: str,
    query: str,
    model_name: str = "gemini-1.5-pro",
    max_wait_iterations: int = 60,  # 60 * 5s = 5-minute max
) -> str:
    """Upload video, poll until ACTIVE, run query. Raises on FAILED or timeout."""
    file = genai.upload_file(path)

    for _ in range(max_wait_iterations):
        file = genai.get_file(file.name)
        if file.state.name == "ACTIVE":
            break
        if file.state.name == "FAILED":
            raise RuntimeError(f"Video processing failed: {file.name}")
        time.sleep(5)
    else:
        raise TimeoutError(f"Video processing timed out after {max_wait_iterations * 5}s")

    model = genai.GenerativeModel(model_name)
    response = model.generate_content([query, file])
    return response.text
