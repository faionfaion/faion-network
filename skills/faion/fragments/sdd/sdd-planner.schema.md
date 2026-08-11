{
  "type": "object",
  "required": ["feature_id", "tasks"],
  "properties": {
    "feature_id": { "type": "string" },
    "tasks": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "title", "summary", "feature_folder", "depends_on"],
        "properties": {
          "id": { "type": "string" },
          "title": { "type": "string" },
          "summary": { "type": "string" },
          "feature_folder": { "type": "string" },
          "depends_on": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  }
}
