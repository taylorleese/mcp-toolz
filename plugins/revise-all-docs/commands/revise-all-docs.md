---
description: Revise CLAUDE.md, README.md, and docs/**/*.md with session learnings
allowed-tools: Read, Edit, Glob, Grep, Skill
---

Review this session for context worth recording in the project's docs. Update **CLAUDE.md**, **README.md**, and any **docs/**/*.md** files with what would help future contributors and Claude sessions.

## Step 1: Reflect

What context was missing or out-of-date this session? Capture:

- Bash commands used or discovered (build, test, lint, deploy, debug)
- Code style patterns enforced
- Testing approaches that worked
- Environment / config quirks
- Warnings or gotchas
- User-facing changes (install / quickstart / public commands) — these belong in README, not CLAUDE.md
- Architecture or contributor-guide drift — these belong in `docs/`

## Step 2: Delegate CLAUDE.md updates

Invoke the `claude-md-management:revise-claude-md` skill via the Skill tool. It owns all `CLAUDE.md` and `.claude.local.md` updates. Wait for it to finish before continuing.

## Step 3: Discover other docs

```bash
# Project-level READMEs (skip vendored / build dirs)
find . -name "README.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/dist/*" 2>/dev/null

# All markdown under docs/
find docs -name "*.md" 2>/dev/null
```

If neither exists, skip to Step 5 with an empty change set.

## Step 4: Categorize each candidate addition

For each piece of context surfaced in Step 1, decide where it belongs:

| Destination | What goes there |
| --- | --- |
| `CLAUDE.md` | (handled in Step 2 — skip if Step 2 already covered it) |
| `README.md` | User-facing onboarding, install, quickstart, public command surface, badges, top-level project description |
| `docs/<file>.md` | Deeper how-to, architecture, contributor guides — match each addition to the most topical existing file |

**Do not create new doc files.** Only update existing ones. If a learning doesn't fit any existing file, leave it out and call that out explicitly to the user.

**One line per concept** — same density as `revise-claude-md`. No filler.

## Step 5: Show & apply

Group proposed changes by file. For each file that receives updates, show:

```
### <relative path>
+ <one-line addition>
+ <one-line addition>
```

Files with zero changes: omit entirely.

Ask the user to approve. On approval, use `Edit` to apply (never `Write` — we're amending, not replacing). After applying, summarize: which files changed, how many lines added per file.
