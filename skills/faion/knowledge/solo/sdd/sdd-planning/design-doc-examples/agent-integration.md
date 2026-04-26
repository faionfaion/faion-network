# Agent Integration — Design Document Examples

## When to use
- Onboarding a new agent or team member to the expected design doc format — examples calibrate output quality faster than abstract descriptions
- Reviewing a generated design doc against a known-good reference to spot structural gaps
- Bootstrapping a design for a feature similar to authentication, file handling, or payment (the example domains)
- Teaching an agent the AD (Architecture Decision) format by pointing at concrete, correct instances

## When NOT to use
- Example-copying without adapting to project constitution — auth examples use JWT/bcrypt defaults that may not match your stack
- Using frontend component examples (RegisterForm props) in a backend-only project
- Treating example file structures as required layouts rather than illustrative patterns
- Running examples through automated tooling that expects live code — examples are documentation, not executable code

## Where it fails / limitations
- Examples are static snapshots; they don't reflect how a real design evolves through review cycles
- The authentication example uses TypeScript/Node conventions; Python/Django projects need different file structures
- Component hierarchy examples assume React; agent will confuse these with backend component diagrams
- Examples demonstrate correct structure but cannot show incorrect structure being caught and fixed
- File change tables in examples omit migration rollback files, which are required in production

## Agentic workflow
Examples serve as few-shot prompts for design generation subagents. When invoking a design-writer agent, inject the relevant example (auth for user features, payment for transactional features) as a reference in the prompt. The agent uses the example's AD structure, FR coverage table format, and file change table as a template. A reviewer subagent then compares the generated design against the example's structural completeness using the FR coverage table as a checklist proxy.

### Recommended subagents
- `faion-sdd-reviewer-agent (mode: design)` — uses example structure as implicit rubric for structural review
- Any design-writing Sonnet agent — inject example as few-shot context before generating new design

### Prompt pattern
```
Generate design.md for feature: {feature_name}
Spec requirements: {fr_list}
Constitution constraints: {tech_stack}

Use this example as structural reference — match the AD format, FR coverage table,
and file change table exactly. Adapt content, not structure.

EXAMPLE:
{paste relevant sections from design-doc-examples/README.md}
```

```
Review the generated design.md against the structural checklist:
- FR coverage table present and complete?
- Each AD has: Context, Decision, Rationale, Alternatives Considered, Consequences, Traces to?
- File changes table has Action (CREATE/MODIFY/DELETE), File, Description, FR, AD columns?
- Testing strategy covers unit and integration?
- Risks table has Impact, Probability, Mitigation?
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `diff design.md design-reference.md` | Compare generated design against example structure | built-in |
| `grep -c "AD-"` | Count AD entries; complex features should have 3-7 ADs | built-in |
| `grep "Traces to"` | Verify all ADs have FR traceability links | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub | SaaS | Yes | Store design examples as gist templates; `gh gist create` |
| Backstage | OSS | Partial | Tech docs plugin renders design docs; requires TechDocs setup |
| Notion | SaaS | Partial | Template gallery for design doc examples; API push is possible |

## Templates & scripts
The examples in `README.md` are the primary artifact. No additional script needed.

Inline FR coverage validator:
```python
import re

def check_fr_coverage(spec_text: str, design_text: str) -> dict:
    """Verify every FR in spec appears in design's FR coverage table."""
    spec_frs = set(re.findall(r"FR-\d+", spec_text))
    design_frs = set(re.findall(r"FR-\d+", design_text))
    missing = spec_frs - design_frs
    return {
        "spec_frs": sorted(spec_frs),
        "design_frs": sorted(design_frs),
        "missing_in_design": sorted(missing),
        "coverage_pct": round(len(design_frs & spec_frs) / len(spec_frs) * 100) if spec_frs else 100,
    }
```

## Best practices
- Keep examples in their own methodology directory — do not inline them in templates or README files that agents load automatically (adds token cost every session)
- Annotate example ADs with why each alternative was rejected, not just what was rejected — this is where agents learn decision-making, not just structure
- Include a "wrong" example alongside each "right" example showing common mistakes (missing Consequences section, no traceability, vague Rationale)
- Version examples when the template format changes — agents referencing stale examples produce outdated structure
- Use the authentication example as a baseline for any user-identity feature; payment example for any transactional feature; do not remix across domains

## AI-agent gotchas
- Agents treat examples as specifications: if the example has `bcrypt cost 12`, agents will use cost 12 for every project regardless of constitution
- Component hierarchy trees (e.g., `<AuthLayout>` tree) are ASCII art — avoid in docs per project rules; use directory tree or table format instead
- TypeScript interface examples cause agents to generate TypeScript even in Python projects if example is injected without domain filtering
- The `Alternatives Considered` table in examples has 2-3 rows; agents generate exactly 2-3 alternatives even when more options exist
- Example file structure trees imply directory layout; agents create the exact tree structure even when the project has a different convention

## References
- [Architecture Decision Records examples — GitHub](https://github.com/joelparkerhenderson/architecture-decision-record)
- [Real-world system design examples — System Design Primer](https://github.com/donnemartin/system-design-primer)
- [The Twelve-Factor App — concrete design patterns](https://12factor.net/)
- [Microsoft Azure Architecture Center — worked examples](https://learn.microsoft.com/en-us/azure/architecture/)
