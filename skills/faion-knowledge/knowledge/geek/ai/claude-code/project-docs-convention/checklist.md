# Documentation Convention Checklist

## New Directory Setup

- [ ] Create `CLAUDE.md` with content `@AGENTS.md`
- [ ] Create `AGENTS.md` with essential context (20-80 lines)
- [ ] If dir has reference docs → create `.agents/INDEX.md`
- [ ] If dir is project root → ensure `.aidocs/INDEX.md` exists
- [ ] AGENTS.md mentions `.agents/INDEX.md` path (if exists)
- [ ] AGENTS.md mentions `.aidocs/INDEX.md` path (if exists)

## AGENTS.md Quality Check

- [ ] Answers: what IS this directory?
- [ ] Includes: how to build/test/deploy (if applicable)
- [ ] Includes: current gotchas or active issues
- [ ] Lists key subdirectories with one-line descriptions
- [ ] Under 80 lines (move excess to .agents/)
- [ ] No @-refs (those belong only in CLAUDE.md)
- [ ] No detailed API specs (move to .agents/)
- [ ] No historical decisions (move to .agents/)

## Audit Existing Project

- [ ] Run `bash ~/workspace/scripts/audit-claude-md.sh <root>`
- [ ] All CLAUDE.md show as `@-REF` (zero `CONTENT`)
- [ ] Every AGENTS.md has a corresponding CLAUDE.md
- [ ] .agents/ has INDEX.md if it exists
- [ ] .aidocs/ has INDEX.md if it exists
- [ ] No orphan docs (referenced in AGENTS.md but file missing)

## Converting Existing Project

- [ ] For each CLAUDE.md with content: `cp CLAUDE.md AGENTS.md && echo '@AGENTS.md' > CLAUDE.md`
- [ ] Move detailed docs from AGENTS.md to `.agents/`
- [ ] Create `.agents/INDEX.md`
- [ ] Create `.aidocs/INDEX.md` if .aidocs/ exists
- [ ] Update links in AGENTS.md (CLAUDE.md refs → AGENTS.md refs)
- [ ] Run audit script to verify
