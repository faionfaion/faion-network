{
  "type": "object",
  "required": ["verdict", "blockers", "nits"],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": ["PASS", "FAIL-WITH-NITS", "FAIL"]
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["finding", "citation"],
        "properties": {
          "finding": { "type": "string" },
          "citation": { "type": "string" }
        }
      }
    },
    "nits": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
