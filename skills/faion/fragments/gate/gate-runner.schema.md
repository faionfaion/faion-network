{
  "type": "object",
  "required": ["clean", "findings"],
  "properties": {
    "clean": { "type": "boolean" },
    "findings": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
