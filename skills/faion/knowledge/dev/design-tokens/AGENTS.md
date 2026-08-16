# Design Tokens

## Summary

**One-sentence:** Author primitive → semantic → component design tokens as one JSON source of truth that emits per-platform outputs via Style Dictionary.

**One-paragraph:** Design tokens are the atomic values of a design system stored as structured data with a three-tier hierarchy: primitive (raw values: colors, spacing scales), semantic (purpose-based aliases: text/primary, surface/raised), component (usage-specific: button/text/hover). One JSON source emits per-platform outputs (CSS vars, JS constants, iOS Swift, Android XML) via Style Dictionary. Output is the token spec + build pipeline that designers and engineers consume from one source.

**Ефективно для:**

- Building or extending a design system across web + mobile.
- Introducing dark mode or white-label theming.
- Bridging Figma to code so design and engineering stay in sync.
- Standardising brand across multiple apps in a monorepo.

## Applies If (ALL must hold)

- Design system spans more than one product or platform.
- Theming (dark mode, white-label, brand variants) is on the roadmap.
- Designers work in Figma and engineering needs the values in code.
- Token churn is bounded (not hourly iteration on a prototype).

## Skip If (ANY kills it)

- Single one-off marketing page — overhead beats payoff.
- Apps fully delegating to a UI library (Material, Mantine) with no re-skinning.
- Prototype work where designers iterate hourly — token churn outpaces pipeline cost.
- Pure server-rendered emails using external template SaaS that owns tokens.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Figma file with frames + variables (or equivalent design source) | Figma URL | design lead |
| Target platforms list (web, iOS, Android, email) | list | tech-lead |
| Style Dictionary or similar emitter chosen + version pinned | config | platform |
| Brand identity decisions (primary, neutral, semantic colour roles) | ADR | design lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[tailwind-architecture]] | Token output often consumed by Tailwind config. |
| [[ui-component-library]] | Components consume the component-tier tokens. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (3-tier hierarchy, one source of truth, semantic aliases, no hex in components, per-platform emission, Figma parity) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for token spec artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: primitives → semantics → components → emit → audit | 800 |
| `content/05-examples.xml` | essential | Worked example: dark-mode-ready button tokens | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primitive_extraction` | sonnet | Mechanical: pull values from Figma variables. |
| `semantic_mapping` | opus | Naming semantic aliases requires deep design synthesis. |
| `component_token_authoring` | sonnet | Component-tier names follow predictable conventions. |
| `emitter_pipeline` | sonnet | Wire Style Dictionary build to CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/primitive.json` | Primitive-tier raw values (colors, spacing, type scale) |
| `templates/semantic.json` | Semantic-tier aliases referencing primitives |
| `templates/build-tokens.mjs` | Style Dictionary build pipeline |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-tokens.py` | Validate the token spec artefact metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tailwind-architecture]]
- [[ui-component-library]]
- [[frontend-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps platform count, theming need, and design-source authority to a rule from `01-core-rules.xml`, telling the agent whether to invoke the full token pipeline or skip when overhead exceeds value. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/primitive.json`

```json
{
  "color": {
    "blue": {
      "500": {
        "value": "#3b82f6"
      },
      "600": {
        "value": "#2563eb"
      },
      "700": {
        "value": "#1d4ed8"
      }
    },
    "gray": {
      "50": {
        "value": "#f9fafb"
      },
      "100": {
        "value": "#f3f4f6"
      },
      "200": {
        "value": "#e5e7eb"
      },
      "300": {
        "value": "#d1d5db"
      },
      "400": {
        "value": "#9ca3af"
      },
      "500": {
        "value": "#6b7280"
      },
      "600": {
        "value": "#4b5563"
      },
      "700": {
        "value": "#374151"
      },
      "800": {
        "value": "#1f2937"
      },
      "900": {
        "value": "#111827"
      }
    },
    "red": {
      "600": {
        "value": "#dc2626"
      }
    },
    "green": {
      "600": {
        "value": "#16a34a"
      }
    },
    "white": {
      "value": "#ffffff"
    }
  },
  "spacing": {
    "1": {
      "value": "0.25rem"
    },
    "2": {
      "value": "0.5rem"
    },
    "4": {
      "value": "1rem"
    },
    "6": {
      "value": "1.5rem"
    },
    "8": {
      "value": "2rem"
    },
    "12": {
      "value": "3rem"
    },
    "16": {
      "value": "4rem"
    }
  },
  "fontSize": {
    "sm": {
      "value": "0.875rem"
    },
    "base": {
      "value": "1rem"
    },
    "lg": {
      "value": "1.125rem"
    },
    "xl": {
      "value": "1.25rem"
    },
    "2xl": {
      "value": "1.5rem"
    }
  },
  "borderRadius": {
    "sm": {
      "value": "0.125rem"
    },
    "md": {
      "value": "0.375rem"
    },
    "lg": {
      "value": "0.5rem"
    },
    "full": {
      "value": "9999px"
    }
  },
  "shadow": {
    "sm": {
      "value": "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    },
    "md": {
      "value": "0 4px 6px -1px rgb(0 0 0 / 0.1)"
    },
    "lg": {
      "value": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    }
  }
}
```

### `templates/semantic.json`

```json
{
  "color": {
    "action": {
      "primary": {
        "value": "{color.blue.600}"
      },
      "primaryHover": {
        "value": "{color.blue.700}"
      },
      "secondary": {
        "value": "{color.gray.100}"
      },
      "secondaryHover": {
        "value": "{color.gray.200}"
      }
    },
    "text": {
      "primary": {
        "value": "{color.gray.900}"
      },
      "secondary": {
        "value": "{color.gray.600}"
      },
      "tertiary": {
        "value": "{color.gray.500}"
      },
      "inverse": {
        "value": "{color.white}"
      },
      "disabled": {
        "value": "{color.gray.400}"
      }
    },
    "bg": {
      "primary": {
        "value": "{color.white}"
      },
      "secondary": {
        "value": "{color.gray.50}"
      },
      "inverse": {
        "value": "{color.gray.900}"
      }
    },
    "border": {
      "default": {
        "value": "{color.gray.200}"
      },
      "hover": {
        "value": "{color.gray.300}"
      },
      "focus": {
        "value": "{color.blue.500}"
      }
    },
    "status": {
      "success": {
        "value": "{color.green.600}"
      },
      "error": {
        "value": "{color.red.600}"
      }
    }
  },
  "_darkThemeOverrides": {
    "_note": "Copy this block to semantic-dark.json, replacing values with dark primitives.",
    "color": {
      "bg": {
        "primary": {
          "value": "{color.gray.900}"
        },
        "secondary": {
          "value": "{color.gray.800}"
        }
      },
      "text": {
        "primary": {
          "value": "{color.gray.50}"
        },
        "secondary": {
          "value": "{color.gray.300}"
        }
      }
    }
  }
}
```

### `templates/build-tokens.mjs`

```javascript
// build-tokens.mjs — Style Dictionary pipeline
// Input:  tokens/primitive.json + tokens/semantic.json
// Output: dist/css/tokens.css, dist/js/tokens.js, dist/ios/Tokens.swift
import StyleDictionary from 'style-dictionary';

const sd = new StyleDictionary({
  source: ['tokens/primitive.json', 'tokens/semantic.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }],
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/js/',
      files: [{ destination: 'tokens.js', format: 'javascript/es6' }],
    },
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'dist/ios/',
      files: [{
        destination: 'Tokens.swift',
        format: 'ios-swift/class.swift',
        className: 'Tokens',
      }],
    },
  },
});

await sd.buildAllPlatforms();
```
