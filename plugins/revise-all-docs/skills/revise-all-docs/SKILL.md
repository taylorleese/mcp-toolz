---
name: revise-all-docs
description: Revise CLAUDE.md plus README.md and docs/**/*.md based on session learnings. Use when the user asks to update docs, refresh README, or sync project docs after a feature/fix. Wraps claude-md-management:revise-claude-md and extends to public docs.
tools: Read, Edit, Glob, Grep, Skill
---

# revise-all-docs

Sync project docs (CLAUDE.md + README.md + docs/**/*.md) with what was learned this session.

This skill is the model-invocable version of the `/revise-all-docs` slash command. Use it when the user says things like "update the docs", "refresh the README", or "sync everything" after meaningful work.

## Workflow (5 steps)

### 1. Reflect

What context was missing or out-of-date this session? Categorize each item by audience:

- **CLAUDE.md** — internal context for Claude sessions (commands, gotchas, env quirks)
- **README.md** — user-facing onboarding (install, quickstart, public surface)
- **docs/<file>.md** — deeper guides (architecture, contributor docs)

### 2. Delegate CLAUDE.md

Invoke the `claude-md-management:revise-claude-md` skill via the Skill tool. Wait for completion.

### 3. Discover

```bash
find . -name "README.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/dist/*" 2>/dev/null
find docs -name "*.md" 2>/dev/null
```

### 4. Categorize

For each pending addition not handled in step 2, pick the right existing file. Match by topic. **Never create new doc files.** If nothing fits, drop the addition and tell the user.

### 5. Show & apply

Group diffs by file. Skip files with zero changes. Get user approval. Use `Edit` (never `Write`).

## Guardrails

- One line per concept.
- Don't create new doc files.
- Skip files with zero proposed changes.
- Don't duplicate additions across CLAUDE.md and README.md — pick the right home.
