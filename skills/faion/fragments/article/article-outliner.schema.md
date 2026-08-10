{
  "type": "object",
  "required": ["title", "description", "sections"],
  "properties": {
    "title": { "type": "string" },
    "description": { "type": "string", "maxLength": 160 },
    "sections": {
      "type": "array",
      "minItems": 6,
      "maxItems": 14,
      "items": {
        "type": "object",
        "required": ["n", "heading", "target_words", "key_points"],
        "properties": {
          "n": { "type": "integer", "minimum": 1 },
          "heading": { "type": "string" },
          "target_words": { "type": "integer", "minimum": 1 },
          "key_points": {
            "type": "array",
            "minItems": 2,
            "maxItems": 5,
            "items": { "type": "string" }
          }
        }
      }
    }
  }
}
