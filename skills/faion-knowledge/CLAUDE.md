# Faion Knowledge

**Entry Point:** `/faion-knowledge`

Umbrella knowledge skill: 52 domain knowledge bases, 1300+ methodologies. No sub-skill invocation — load content from `knowledge/<group>/<name>/` on demand with Read.

## Structure

```
knowledge/
├── dev/           Python, JS, Go, Rust, Java, C#, backend, frontend, API, testing, architecture, automation, code quality (13)
├── ai/            ML, AI agents, RAG, ML ops, multimodal, LLM integration, Claude Code (7)
├── infra/         DevOps, CI/CD, infrastructure, server craft (4)
├── product/       PM, planning, operations (3)
├── pm/            Project, Agile, Traditional (3)
├── ba/            BA, core, modeling (3)
├── ux/            UX/UI, UI, UX research, user research, accessibility (5)
├── marketing/     Marketing, GTM, content, growth, CRO, SEO, PPC, SMM (8)
├── research/      Researcher, market research (2)
├── comms/         Communicator, HR recruiter (2)
└── sdd/           SDD, SDD planning (2)
```

Each skill = folder with `SKILL.md` + methodology subfolders. Each methodology = 5-file pattern (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`).

## How to Use

```
User task → Identify domain → Read knowledge/<group>/<name>/README.md → Apply
```

No `Skill(faion-X)` calls — sub-skills no longer exist as separate invocable skills.

**Full routing:** [SKILL.md](SKILL.md)

---

*Faion Network v4.0*
