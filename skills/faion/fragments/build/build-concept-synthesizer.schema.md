{
  "type": "object",
  "required": ["title", "core", "catalog_entries_used", "rationale", "runner_up",
               "commercial_findings"],
  "properties": {
    "title": { "type": "string" },
    "core": { "type": "string" },
    "catalog_entries_used": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": ["catalog", "entry"],
        "properties": {
          "catalog": { "type": "string" },
          "entry": { "type": "string" }
        }
      }
    },
    "rationale": {
      "type": "object",
      "required": ["envelope_fit", "evidence", "build_cost", "value"],
      "properties": {
        "envelope_fit": { "type": "number" },
        "evidence": { "type": "number" },
        "build_cost": { "type": "number" },
        "value": { "type": "number" }
      }
    },
    "runner_up": {
      "type": "object",
      "required": ["title", "why_it_lost"],
      "properties": {
        "title": { "type": "string" },
        "why_it_lost": { "type": "string" }
      }
    },
    "commercial_findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "lever", "disposition", "lands_in", "reason",
                     "decline_class"],
        "properties": {
          "id": { "type": "string" },
          "lever": { "type": "string" },
          "disposition": { "type": "string", "enum": ["applied", "declined"] },
          "lands_in": { "type": "string" },
          "reason": { "type": "string" },
          "decline_class": {
            "type": "string",
            "enum": ["dark-pattern", "envelope", "evidence", "economics",
                     "dependency", "not-declined"]
          }
        }
      }
    },
    "sacrificed": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
