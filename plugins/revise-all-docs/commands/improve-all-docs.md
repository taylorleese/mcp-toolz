---
description: Audit CLAUDE.md, README.md, and docs/**/*.md for quality, currency, and actionability
allowed-tools: Read, Edit, Glob, Grep, Bash, Skill
---

Run a static quality audit of the project's documentation — independent of the current session's work. Unlike `/revise-all-docs` (which captures
learnings from *this* session), this command scores each doc file against type-appropriate rubrics and proposes targeted fixes.

Invoke the `revise-all-docs:all-docs-improver` skill via the Skill tool. It owns the full workflow:

1. **Discovery** — find every `CLAUDE.md`, `README.md`, and `docs/**/*.md` in the repo.
2. **Quality Assessment** — score each file against criteria appropriate to its type (delegates `CLAUDE.md` audits to the `claude-md-management:claude-md-improver` skill).
3. **Quality Report** — print a unified per-file score table with specific issues.
4. **Targeted Updates** — propose concrete diffs, one concept per line, no filler.
5. **Apply** — only after explicit user approval; use `Edit` (never `Write`).

After the skill returns, summarize: which files changed, how many lines added/removed per file, and any learnings the user declined.
