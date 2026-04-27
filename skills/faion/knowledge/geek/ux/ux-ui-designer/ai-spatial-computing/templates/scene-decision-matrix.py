"""Scene-type to UI state decision matrix generator.

Produces a mapping from AI-detected scene type to UI layout parameters.
Includes explicit confidence threshold and fallback for unknown scenes.
"""

SCENE_TYPES = ["living_room", "office", "kitchen", "outdoor", "unknown"]

DECISION_MATRIX = {
    "living_room": {"layout": "relaxed",    "info_density": "low",    "voice": True},
    "office":      {"layout": "compact",    "info_density": "high",   "voice": False},
    "kitchen":     {"layout": "glanceable", "info_density": "low",    "voice": True},
    "outdoor":     {"layout": "minimal",    "info_density": "low",    "voice": True},
    "unknown":     {"layout": "default",    "info_density": "medium", "voice": True},
}

CONFIDENCE_THRESHOLD = 0.75  # below this → fall back to "unknown"


def get_ui_state(scene: str, confidence: float) -> dict:
    """Return UI state for detected scene type, applying confidence threshold."""
    if confidence < CONFIDENCE_THRESHOLD:
        scene = "unknown"
    return {
        "scene": scene,
        "confidence": confidence,
        "ui": DECISION_MATRIX.get(scene, DECISION_MATRIX["unknown"]),
    }


if __name__ == "__main__":
    examples = [
        ("office", 0.92),
        ("living_room", 0.60),   # below threshold → falls back to default
        ("outdoor", 0.88),
    ]
    for scene, conf in examples:
        state = get_ui_state(scene, conf)
        print(f"Scene: {state['scene']} (conf={state['confidence']}) → {state['ui']}")
