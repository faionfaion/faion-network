#!/usr/bin/env python3
"""validate-healthtech-fhir-ba-pack.py

Validate the artefact produced by the healthtech-fhir-ba-pack methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only, self-contained:
`faion get-content` ships this file alone, so the schema and the checker live
here rather than in a shared module.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid / invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "faion://healthtech-fhir-ba-pack/output.schema.json",
  "title": "HealthTech FHIR BA pack",
  "type": "object",
  "required": [
    "feature_name",
    "regimes",
    "fhir_version",
    "profile",
    "element_map",
    "data_flows",
    "processors",
    "consent",
    "audit_trail",
    "encryption",
    "blocking_findings"
  ],
  "additionalProperties": False,
  "definitions": {
    "handle": {
      "type": "string",
      "pattern": "^[a-z-]+:[a-z0-9._-]+$"
    },
    "date": {
      "type": "string",
      "format": "date",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    },
    "matrix_row": {
      "type": "object",
      "required": [
        "hipaa_position",
        "gdpr_position",
        "design_decision",
        "stricter_clock_honoured"
      ],
      "additionalProperties": False,
      "properties": {
        "hipaa_position": {
          "type": "string",
          "minLength": 10
        },
        "gdpr_position": {
          "type": "string",
          "minLength": 10
        },
        "design_decision": {
          "type": "string",
          "minLength": 10
        },
        "stricter_clock_honoured": {
          "type": "string",
          "minLength": 3
        }
      }
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "feature_name": {
      "type": "string",
      "minLength": 3
    },
    "regimes": {
      "type": "object",
      "required": [
        "hipaa",
        "gdpr",
        "nhs"
      ],
      "additionalProperties": False,
      "properties": {
        "hipaa": {
          "type": "boolean"
        },
        "gdpr": {
          "type": "boolean"
        },
        "nhs": {
          "type": "boolean"
        }
      }
    },
    "fhir_version": {
      "type": "string",
      "enum": [
        "R4",
        "R5"
      ]
    },
    "profile": {
      "type": "string",
      "minLength": 3,
      "description": "US Core, UK Core, or the customer's named profile"
    },
    "element_map": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "clinical_element",
          "resource",
          "element_path",
          "coded"
        ],
        "additionalProperties": False,
        "properties": {
          "clinical_element": {
            "type": "string",
            "minLength": 2
          },
          "resource": {
            "type": "string",
            "enum": [
              "Patient",
              "Encounter",
              "Observation",
              "Condition",
              "MedicationRequest",
              "MedicationStatement",
              "Procedure",
              "AllergyIntolerance",
              "Immunization",
              "DiagnosticReport",
              "DocumentReference",
              "Consent",
              "AuditEvent",
              "Practitioner",
              "Organization",
              "CarePlan",
              "Device",
              "Coverage"
            ]
          },
          "element_path": {
            "type": "string",
            "pattern": "^[A-Z][A-Za-z]+\\.[A-Za-z0-9\\[\\]\\.]+$",
            "description": "e.g. Observation.value[x], Condition.clinicalStatus"
          },
          "coded": {
            "type": "boolean"
          },
          "binding": {
            "type": "object",
            "required": [
              "code_system",
              "system_uri"
            ],
            "additionalProperties": False,
            "properties": {
              "code_system": {
                "type": "string",
                "enum": [
                  "LOINC",
                  "SNOMED CT",
                  "ICD-10-CM",
                  "ICD-10",
                  "RxNorm",
                  "dm+d",
                  "UCUM",
                  "CPT",
                  "HL7 v3",
                  "other-standard"
                ]
              },
              "system_uri": {
                "type": "string",
                "format": "uri"
              },
              "value_set": {
                "type": "string"
              }
            }
          }
        },
        "if": {
          "properties": {
            "coded": {
              "const": True
            }
          }
        },
        "then": {
          "required": [
            "binding"
          ]
        }
      }
    },
    "data_flows": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "from",
          "to",
          "phi_elements",
          "purpose",
          "de_identification"
        ],
        "additionalProperties": False,
        "properties": {
          "from": {
            "type": "string",
            "minLength": 2
          },
          "to": {
            "type": "string",
            "minLength": 2
          },
          "phi_elements": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string",
              "minLength": 2
            }
          },
          "purpose": {
            "type": "string",
            "enum": [
              "treatment",
              "payment",
              "operations",
              "analytics",
              "model-training",
              "research",
              "patient-access",
              "support",
              "other"
            ]
          },
          "de_identification": {
            "type": "string",
            "enum": [
              "none",
              "safe-harbor",
              "expert-determination"
            ]
          },
          "de_identification_method": {
            "type": "string",
            "minLength": 10,
            "description": "safe-harbor: which of the 18 identifier classes are stripped and how; expert-determination: who certified and when"
          },
          "excluded_elements": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "allOf": [
          {
            "if": {
              "properties": {
                "purpose": {
                  "enum": [
                    "analytics",
                    "model-training"
                  ]
                }
              }
            },
            "then": {
              "properties": {
                "de_identification": {
                  "enum": [
                    "safe-harbor",
                    "expert-determination"
                  ]
                }
              },
              "required": [
                "de_identification_method"
              ]
            }
          }
        ]
      }
    },
    "processors": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "service_kind",
          "phi_in_scope",
          "baa_signed",
          "status"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "minLength": 2
          },
          "service_kind": {
            "type": "string",
            "enum": [
              "cloud-host",
              "database-saas",
              "search-saas",
              "llm-api",
              "ml-api",
              "email-gateway",
              "sms-gateway",
              "analytics",
              "error-tracking",
              "support-desk",
              "backup",
              "other"
            ]
          },
          "phi_in_scope": {
            "type": "boolean"
          },
          "baa_signed": {
            "type": "boolean"
          },
          "baa_signed_on": {
            "$ref": "#/definitions/date"
          },
          "dpa_art28_signed": {
            "type": "boolean"
          },
          "agreement_evidence": {
            "type": "string",
            "format": "uri"
          },
          "status": {
            "type": "string",
            "enum": [
              "cleared",
              "blocking"
            ]
          }
        },
        "allOf": [
          {
            "if": {
              "properties": {
                "phi_in_scope": {
                  "const": True
                },
                "baa_signed": {
                  "const": False
                }
              }
            },
            "then": {
              "properties": {
                "status": {
                  "const": "blocking"
                }
              }
            }
          },
          {
            "if": {
              "properties": {
                "baa_signed": {
                  "const": True
                }
              }
            },
            "then": {
              "required": [
                "baa_signed_on",
                "agreement_evidence"
              ]
            }
          }
        ]
      }
    },
    "overlap_matrix": {
      "type": "object",
      "required": [
        "lawful_basis",
        "breach_notification_clock",
        "individual_access",
        "retention_and_deletion",
        "cross_border_transfer"
      ],
      "properties": {
        "lawful_basis": {
          "$ref": "#/definitions/matrix_row"
        },
        "breach_notification_clock": {
          "$ref": "#/definitions/matrix_row"
        },
        "individual_access": {
          "$ref": "#/definitions/matrix_row"
        },
        "retention_and_deletion": {
          "$ref": "#/definitions/matrix_row"
        },
        "cross_border_transfer": {
          "$ref": "#/definitions/matrix_row"
        }
      },
      "additionalProperties": {
        "$ref": "#/definitions/matrix_row"
      }
    },
    "consent": {
      "type": "object",
      "required": [
        "model",
        "research_use",
        "records"
      ],
      "additionalProperties": False,
      "properties": {
        "model": {
          "type": "string",
          "enum": [
            "fhir-consent",
            "equivalent-record"
          ]
        },
        "research_use": {
          "type": "boolean"
        },
        "records": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "kind",
              "scope",
              "provision",
              "period",
              "text_version",
              "capture"
            ],
            "additionalProperties": False,
            "properties": {
              "kind": {
                "type": "string",
                "enum": [
                  "treatment",
                  "research",
                  "marketing",
                  "data-sharing"
                ]
              },
              "scope": {
                "type": "string",
                "minLength": 3
              },
              "provision": {
                "type": "array",
                "minItems": 1,
                "items": {
                  "type": "object",
                  "required": [
                    "action",
                    "data_category",
                    "purpose"
                  ],
                  "additionalProperties": False,
                  "properties": {
                    "action": {
                      "type": "string",
                      "enum": [
                        "permit",
                        "deny"
                      ]
                    },
                    "data_category": {
                      "type": "string",
                      "minLength": 2
                    },
                    "purpose": {
                      "type": "string",
                      "minLength": 2
                    }
                  }
                }
              },
              "period": {
                "type": "object",
                "required": [
                  "start"
                ],
                "additionalProperties": False,
                "properties": {
                  "start": {
                    "$ref": "#/definitions/date"
                  },
                  "end": {
                    "$ref": "#/definitions/date"
                  }
                }
              },
              "text_version": {
                "type": "string",
                "minLength": 1
              },
              "capture": {
                "type": "object",
                "required": [
                  "timestamp_field",
                  "channel"
                ],
                "additionalProperties": False,
                "properties": {
                  "timestamp_field": {
                    "type": "string",
                    "minLength": 2
                  },
                  "channel": {
                    "type": "string",
                    "enum": [
                      "web",
                      "mobile",
                      "paper",
                      "verbal-witnessed",
                      "kiosk",
                      "api"
                    ]
                  }
                }
              }
            }
          }
        },
        "irb": {
          "type": "object",
          "required": [
            "protocol_number",
            "approval_date",
            "waiver_of_consent"
          ],
          "additionalProperties": False,
          "properties": {
            "protocol_number": {
              "type": "string",
              "minLength": 3
            },
            "approval_date": {
              "$ref": "#/definitions/date"
            },
            "waiver_of_consent": {
              "type": "boolean"
            },
            "committee": {
              "type": "string"
            }
          }
        }
      },
      "if": {
        "properties": {
          "research_use": {
            "const": True
          }
        }
      },
      "then": {
        "required": [
          "irb"
        ]
      }
    },
    "audit_trail": {
      "type": "object",
      "required": [
        "model",
        "fields",
        "append_only",
        "retention_years",
        "per_patient_query"
      ],
      "additionalProperties": False,
      "properties": {
        "model": {
          "type": "string",
          "enum": [
            "fhir-auditevent",
            "equivalent-schema"
          ]
        },
        "fields": {
          "type": "array",
          "minItems": 6,
          "uniqueItems": True,
          "items": {
            "type": "string",
            "enum": [
              "actor",
              "subject_id",
              "action",
              "timestamp",
              "source_system",
              "purpose"
            ]
          }
        },
        "append_only": {
          "type": "boolean",
          "const": True
        },
        "application_roles_with_update_or_delete": {
          "type": "array",
          "maxItems": 0,
          "items": {
            "type": "string"
          }
        },
        "retention_years": {
          "type": "integer",
          "minimum": 6
        },
        "per_patient_query": {
          "type": "boolean",
          "const": True
        },
        "storage": {
          "type": "string"
        }
      }
    },
    "encryption": {
      "type": "object",
      "required": [
        "stores",
        "hops"
      ],
      "additionalProperties": False,
      "properties": {
        "stores": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "name",
              "kind",
              "encrypted_at_rest",
              "key_management_separated",
              "status"
            ],
            "additionalProperties": False,
            "properties": {
              "name": {
                "type": "string",
                "minLength": 2
              },
              "kind": {
                "type": "string",
                "enum": [
                  "database",
                  "backup",
                  "object-storage",
                  "log",
                  "search-index",
                  "queue",
                  "cache",
                  "other"
                ]
              },
              "encrypted_at_rest": {
                "type": "boolean"
              },
              "key_management_separated": {
                "type": "boolean"
              },
              "status": {
                "type": "string",
                "enum": [
                  "cleared",
                  "blocking"
                ]
              }
            },
            "if": {
              "properties": {
                "encrypted_at_rest": {
                  "const": False
                }
              }
            },
            "then": {
              "properties": {
                "status": {
                  "const": "blocking"
                }
              }
            }
          }
        },
        "hops": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": [
              "from",
              "to",
              "tls_min"
            ],
            "additionalProperties": False,
            "properties": {
              "from": {
                "type": "string",
                "minLength": 2
              },
              "to": {
                "type": "string",
                "minLength": 2
              },
              "tls_min": {
                "type": "string",
                "enum": [
                  "1.2",
                  "1.3"
                ]
              }
            }
          }
        }
      }
    },
    "blocking_findings": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 10
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "regimes": {
            "properties": {
              "hipaa": {
                "const": True
              },
              "gdpr": {
                "const": True
              }
            }
          }
        }
      },
      "then": {
        "required": [
          "overlap_matrix"
        ]
      }
    }
  ]
}

OK = {
  "feature_name": "Remote blood-pressure monitoring dashboard",
  "regimes": {
    "hipaa": True,
    "gdpr": True,
    "nhs": False
  },
  "fhir_version": "R4",
  "profile": "US Core 6.1.0",
  "element_map": [
    {
      "clinical_element": "patient MRN",
      "resource": "Patient",
      "element_path": "Patient.identifier",
      "coded": False
    },
    {
      "clinical_element": "monitoring encounter",
      "resource": "Encounter",
      "element_path": "Encounter.period",
      "coded": False
    },
    {
      "clinical_element": "systolic blood pressure",
      "resource": "Observation",
      "element_path": "Observation.component.value[x]",
      "coded": True,
      "binding": {
        "code_system": "LOINC",
        "system_uri": "http://loinc.org",
        "value_set": "8480-6"
      }
    },
    {
      "clinical_element": "diastolic blood pressure",
      "resource": "Observation",
      "element_path": "Observation.component.value[x]",
      "coded": True,
      "binding": {
        "code_system": "LOINC",
        "system_uri": "http://loinc.org",
        "value_set": "8462-4"
      }
    },
    {
      "clinical_element": "hypertension diagnosis",
      "resource": "Condition",
      "element_path": "Condition.code",
      "coded": True,
      "binding": {
        "code_system": "SNOMED CT",
        "system_uri": "http://snomed.info/sct",
        "value_set": "38341003"
      }
    },
    {
      "clinical_element": "antihypertensive prescription",
      "resource": "MedicationRequest",
      "element_path": "MedicationRequest.medication[x]",
      "coded": True,
      "binding": {
        "code_system": "RxNorm",
        "system_uri": "http://www.nlm.nih.gov/research/umls/rxnorm"
      }
    }
  ],
  "data_flows": [
    {
      "from": "home cuff app",
      "to": "ingest-api",
      "phi_elements": [
        "Patient.identifier",
        "Observation.component.value[x]",
        "Observation.effective[x]"
      ],
      "purpose": "treatment",
      "de_identification": "none"
    },
    {
      "from": "ingest-api",
      "to": "clinician dashboard",
      "phi_elements": [
        "Patient.name",
        "Patient.identifier",
        "Observation.component.value[x]",
        "Condition.code"
      ],
      "purpose": "treatment",
      "de_identification": "none"
    },
    {
      "from": "ingest-api",
      "to": "analytics warehouse",
      "phi_elements": [
        "Observation.component.value[x]",
        "Observation.effective[x]",
        "Patient.birthDate"
      ],
      "purpose": "analytics",
      "de_identification": "safe-harbor",
      "de_identification_method": "All 18 Safe Harbor identifier classes removed at the ETL step: name, MRN, dates shifted to year only for ages 89 and under, zip truncated to 3 digits; pipeline job deid-v3",
      "excluded_elements": [
        "Patient.name",
        "Patient.identifier",
        "Patient.address"
      ]
    },
    {
      "from": "ingest-api",
      "to": "error tracker",
      "phi_elements": [
        "Patient.identifier"
      ],
      "purpose": "operations",
      "de_identification": "none"
    }
  ],
  "processors": [
    {
      "name": "AWS (us-east-1)",
      "service_kind": "cloud-host",
      "phi_in_scope": True,
      "baa_signed": True,
      "baa_signed_on": "2025-11-04",
      "dpa_art28_signed": True,
      "agreement_evidence": "https://contracts.example.health/aws-baa-2025.pdf",
      "status": "cleared"
    },
    {
      "name": "Twilio SMS reminders",
      "service_kind": "sms-gateway",
      "phi_in_scope": True,
      "baa_signed": True,
      "baa_signed_on": "2026-01-12",
      "dpa_art28_signed": True,
      "agreement_evidence": "https://contracts.example.health/twilio-baa.pdf",
      "status": "cleared"
    },
    {
      "name": "Sentry error tracking",
      "service_kind": "error-tracking",
      "phi_in_scope": True,
      "baa_signed": False,
      "dpa_art28_signed": False,
      "status": "blocking"
    },
    {
      "name": "Snowflake analytics",
      "service_kind": "analytics",
      "phi_in_scope": False,
      "baa_signed": False,
      "status": "cleared"
    }
  ],
  "overlap_matrix": {
    "lawful_basis": {
      "hipaa_position": "Permitted use for treatment under 45 CFR §164.506",
      "gdpr_position": "Art. 6(1)(e) or (b) plus Art. 9(2)(h) provision of health care",
      "design_decision": "Record the Art. 9(2)(h) condition per EU tenant; no marketing use without separate consent",
      "stricter_clock_honoured": "n/a - basis documented per tenant"
    },
    "breach_notification_clock": {
      "hipaa_position": "Individuals without unreasonable delay, no later than 60 days, 45 CFR §164.404",
      "gdpr_position": "Supervisory authority within 72 hours, Art. 33",
      "design_decision": "Incident runbook targets authority notice within 72 hours for every tenant",
      "stricter_clock_honoured": "72 hours"
    },
    "individual_access": {
      "hipaa_position": "Right of access within 30 days, 45 CFR §164.524",
      "gdpr_position": "Art. 15, one month",
      "design_decision": "Patient export endpoint returns a FHIR bundle within 30 days for all tenants",
      "stricter_clock_honoured": "30 days"
    },
    "retention_and_deletion": {
      "hipaa_position": "Documentation retained six years, 45 CFR §164.316(b)(2)",
      "gdpr_position": "Erasure on request, Art. 17, subject to Art. 17(3)(c) health exception",
      "design_decision": "Clinical records retained six years; marketing and analytics derivatives erased on request",
      "stricter_clock_honoured": "six-year retention for clinical records; erasure for derivatives"
    },
    "cross_border_transfer": {
      "hipaa_position": "No transfer restriction",
      "gdpr_position": "Chapter V; SCCs or adequacy required for EU to US",
      "design_decision": "EU tenants pinned to eu-central-1; no EU PHI in us-east-1",
      "stricter_clock_honoured": "GDPR Chapter V - regional pinning"
    }
  },
  "consent": {
    "model": "fhir-consent",
    "research_use": True,
    "records": [
      {
        "kind": "treatment",
        "scope": "remote monitoring by the care team",
        "provision": [
          {
            "action": "permit",
            "data_category": "vital signs",
            "purpose": "treatment"
          }
        ],
        "period": {
          "start": "2026-02-01"
        },
        "text_version": "treatment-consent-v3",
        "capture": {
          "timestamp_field": "Consent.dateTime",
          "channel": "mobile"
        }
      },
      {
        "kind": "research",
        "scope": "hypertension outcomes study",
        "provision": [
          {
            "action": "permit",
            "data_category": "de-identified vital signs",
            "purpose": "research"
          },
          {
            "action": "deny",
            "data_category": "free-text notes",
            "purpose": "research"
          }
        ],
        "period": {
          "start": "2026-02-01",
          "end": "2028-01-31"
        },
        "text_version": "research-consent-v1",
        "capture": {
          "timestamp_field": "Consent.dateTime",
          "channel": "mobile"
        }
      }
    ],
    "irb": {
      "protocol_number": "IRB-2026-0142",
      "approval_date": "2026-01-20",
      "waiver_of_consent": False,
      "committee": "Example Health IRB"
    }
  },
  "audit_trail": {
    "model": "fhir-auditevent",
    "fields": [
      "actor",
      "subject_id",
      "action",
      "timestamp",
      "source_system",
      "purpose"
    ],
    "append_only": True,
    "application_roles_with_update_or_delete": [],
    "retention_years": 6,
    "per_patient_query": True,
    "storage": "append-only Postgres partition with row-level security; indexed on subject_id"
  },
  "encryption": {
    "stores": [
      {
        "name": "postgres.clinical",
        "kind": "database",
        "encrypted_at_rest": True,
        "key_management_separated": True,
        "status": "cleared"
      },
      {
        "name": "s3.backups",
        "kind": "backup",
        "encrypted_at_rest": True,
        "key_management_separated": True,
        "status": "cleared"
      },
      {
        "name": "opensearch.notes",
        "kind": "search-index",
        "encrypted_at_rest": True,
        "key_management_separated": True,
        "status": "cleared"
      },
      {
        "name": "cloudwatch.app-logs",
        "kind": "log",
        "encrypted_at_rest": True,
        "key_management_separated": True,
        "status": "cleared"
      }
    ],
    "hops": [
      {
        "from": "home cuff app",
        "to": "ingest-api",
        "tls_min": "1.2"
      },
      {
        "from": "ingest-api",
        "to": "postgres.clinical",
        "tls_min": "1.2"
      },
      {
        "from": "ingest-api",
        "to": "analytics warehouse",
        "tls_min": "1.2"
      }
    ]
  },
  "blocking_findings": [
    "Sentry receives Patient.identifier in request bodies with no BAA: scrub identifiers from error payloads or sign the BAA before launch"
  ]
}

BAD = {
  "feature_name": "Symptom checker chat",
  "regimes": {
    "hipaa": True,
    "gdpr": True,
    "nhs": False
  },
  "fhir_version": "R4",
  "profile": "US Core 6.1.0",
  "element_map": [
    {
      "clinical_element": "reported symptoms",
      "resource": "Observation",
      "element_path": "Observation.code",
      "coded": True
    },
    {
      "clinical_element": "diagnosis",
      "resource": "Condition",
      "element_path": "Condition.code",
      "coded": True,
      "binding": {
        "code_system": "ICD-10-CM",
        "system_uri": "http://hl7.org/fhir/sid/icd-10-cm"
      }
    }
  ],
  "data_flows": [
    {
      "from": "chat-api",
      "to": "OpenAI API",
      "phi_elements": [
        "Patient.name",
        "Observation.code",
        "Observation.note"
      ],
      "purpose": "treatment",
      "de_identification": "none"
    },
    {
      "from": "chat-api",
      "to": "model-training bucket",
      "phi_elements": [
        "Patient.name",
        "Observation.note"
      ],
      "purpose": "model-training",
      "de_identification": "none"
    }
  ],
  "processors": [
    {
      "name": "OpenAI API",
      "service_kind": "llm-api",
      "phi_in_scope": True,
      "baa_signed": False,
      "status": "cleared"
    }
  ],
  "consent": {
    "model": "equivalent-record",
    "research_use": True,
    "records": [
      {
        "kind": "treatment",
        "scope": "I agree to the terms",
        "provision": [
          {
            "action": "permit",
            "data_category": "all",
            "purpose": "any"
          }
        ],
        "period": {
          "start": "2026-03-01"
        },
        "text_version": "1",
        "capture": {
          "timestamp_field": "accepted_at",
          "channel": "web"
        }
      }
    ]
  },
  "audit_trail": {
    "model": "equivalent-schema",
    "fields": [
      "actor",
      "action",
      "timestamp"
    ],
    "append_only": False,
    "retention_years": 1,
    "per_patient_query": False
  },
  "encryption": {
    "stores": [
      {
        "name": "s3.chat-transcripts",
        "kind": "object-storage",
        "encrypted_at_rest": False,
        "key_management_separated": False,
        "status": "cleared"
      }
    ],
    "hops": [
      {
        "from": "chat-api",
        "to": "s3.chat-transcripts",
        "tls_min": "1.0"
      }
    ]
  },
  "blocking_findings": []
}

_FORMATS = {
    "date-time": re.compile(
        r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
        r"(?:Z|[+-]\d{2}:?\d{2})?$"
    ),
    "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "email": re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"),
    "uri": re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:\S*$"),
    "uri-reference": re.compile(r"^\S+$"),
}

_PY_TYPES = {"object": dict, "array": list, "string": str, "null": type(None)}


def _type_ok(value, declared) -> bool:
    names = declared if isinstance(declared, list) else [declared]
    for name in names:
        if name == "integer":
            ok = isinstance(value, int) and not isinstance(value, bool)
        elif name == "number":
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        elif name == "boolean":
            ok = isinstance(value, bool)
        elif name in _PY_TYPES:
            ok = isinstance(value, _PY_TYPES[name])
        else:
            ok = True
        if ok:
            return True
    return False


def _label(path: str) -> str:
    return path or "<root>"


def _resolve(ref: str):
    """Local `#/definitions/<name>` references only (draft-07 `$ref` replaces its siblings)."""
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported $ref: {ref}")
    node = SCHEMA
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _valid(value, schema) -> bool:
    errs: list[str] = []
    _check(value, schema, "", errs)
    return not errs


def _check(value, schema, path: str, errs: list) -> None:
    """Draft-07 subset: required, type, enum, const, pattern, format, minimum /
    maximum (+exclusive), minLength / maxLength, minItems / maxItems,
    uniqueItems, items, properties, additionalProperties, allOf / anyOf /
    oneOf / not, if / then / else, local $ref."""
    if schema is True or schema == {}:
        return
    if schema is False:
        errs.append(f"{_label(path)}: schema forbids any value here")
        return
    if "$ref" in schema:
        schema = _resolve(schema["$ref"])
    declared = schema.get("type")
    if declared is not None and not _type_ok(value, declared):
        errs.append(f"{_label(path)}: expected type {declared}, got {type(value).__name__}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{_label(path)}: {value!r} not in allowed enum {schema['enum']!r}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{_label(path)}: {value!r} is not the required const {schema['const']!r}")

    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errs.append(f"{_label(path)}: {value!r} does not match pattern {pattern!r}")
        rx = _FORMATS.get(schema.get("format"))
        if rx is not None and not rx.match(value):
            errs.append(f"{_label(path)}: {value!r} is not a valid {schema['format']}")
        low, high = schema.get("minLength"), schema.get("maxLength")
        if isinstance(low, int) and len(value) < low:
            errs.append(f"{_label(path)}: length {len(value)} is under minLength {low}")
        if isinstance(high, int) and len(value) > high:
            errs.append(f"{_label(path)}: length {len(value)} is over maxLength {high}")

    if isinstance(value, list):
        low, high = schema.get("minItems"), schema.get("maxItems")
        if isinstance(low, int) and len(value) < low:
            errs.append(f"{_label(path)}: {len(value)} items is under minItems {low}")
        if isinstance(high, int) and len(value) > high:
            errs.append(f"{_label(path)}: {len(value)} items is over maxItems {high}")
        if schema.get("uniqueItems"):
            seen = [json.dumps(v, sort_keys=True) for v in value]
            if len(set(seen)) != len(seen):
                errs.append(f"{_label(path)}: items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, element in enumerate(value):
                _check(element, item_schema, f"{_label(path)}[{i}]", errs)
        elif isinstance(item_schema, list):
            for i, (element, sub) in enumerate(zip(value, item_schema)):
                _check(element, sub, f"{_label(path)}[{i}]", errs)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        for key, test, word in (
            ("minimum", lambda v, b: v < b, "is below minimum"),
            ("maximum", lambda v, b: v > b, "is above maximum"),
            ("exclusiveMinimum", lambda v, b: v <= b, "is not above exclusiveMinimum"),
            ("exclusiveMaximum", lambda v, b: v >= b, "is not below exclusiveMaximum"),
        ):
            bound = schema.get(key)
            if isinstance(bound, (int, float)) and test(value, bound):
                errs.append(f"{_label(path)}: {value} {word} {bound}")

    if isinstance(value, dict):
        props = schema.get("properties") or {}
        for key in schema.get("required") or []:
            if key not in value:
                errs.append(f"{_label(path)}: missing required field: {key}")
        extra = schema.get("additionalProperties", True)
        for key in value:
            if key in props:
                continue
            if extra is False:
                errs.append(f"{_label(path)}: unknown field {key!r} (additionalProperties: false)")
            elif isinstance(extra, dict):
                _check(value[key], extra, f"{path}.{key}" if path else key, errs)
        for key, sub in props.items():
            if key in value and isinstance(sub, (dict, bool)):
                _check(value[key], sub, f"{path}.{key}" if path else key, errs)

    for sub in schema.get("allOf") or []:
        _check(value, sub, path, errs)
    any_of = schema.get("anyOf")
    if any_of and not any(_valid(value, s) for s in any_of):
        errs.append(f"{_label(path)}: matches none of the anyOf alternatives")
    one_of = schema.get("oneOf")
    if one_of:
        hits = sum(1 for s in one_of if _valid(value, s))
        if hits != 1:
            errs.append(f"{_label(path)}: matches {hits} oneOf alternatives, need exactly 1")
    if "not" in schema and _valid(value, schema["not"]):
        errs.append(f"{_label(path)}: matches the forbidden `not` schema")
    if "if" in schema:
        branch = "then" if _valid(value, schema["if"]) else "else"
        if branch in schema:
            _check(value, schema[branch], path, errs)


def validate(obj: object) -> list[str]:
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    errs: list[str] = []
    _check(obj, SCHEMA, "", errs)
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-healthtech-fhir-ba-pack.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
