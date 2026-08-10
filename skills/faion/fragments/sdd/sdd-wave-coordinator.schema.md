{
  "type": "object",
  "required": ["verdict", "wave", "findings"],
  "properties": {
    "verdict": { "type": "string", "enum": ["CLEAR", "HOLD", "ABORT"] },
    "wave": { "type": "integer", "minimum": 1 },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["feature_id", "citation"],
        "properties": {
          "feature_id": { "type": "string" },
          "citation": { "type": "string" },
          "remediation": { "type": "string" }
        }
      }
    }
  }
}
