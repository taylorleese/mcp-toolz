---
name: all-docs-improver
description: Audit and improve CLAUDE.md, README.md, and docs/**/*.md across a repo. Use when the user asks to audit, check, score, improve, or fix the project's documentation as a whole — not just CLAUDE.md. Scans all doc files, scores each against type-appropriate rubrics, outputs a unified quality report, then makes targeted updates after approval. Delegates CLAUDE.md audits to the `claude-md-management:claude-md-improver` skill.
allowed-tools: Read, Edit, Glob, Grep, Bash, Skill
---

# All-Docs Improver

Audit, score, and improve the documentation surface of a repository — `CLAUDE.md`, `README.md`, and `docs/**/*.md` — to keep contributors and Claude sessions oriented.

**This skill writes to doc files.** It always presents a quality report and waits for explicit approval before applying any edits.

## Workflow

### Phase 1: Discovery

Find every relevant doc file. Skip vendored / generated / build directories.

```bash
# CLAUDE.md family (handled by claude-md-improver)
find . -name "CLAUDE.md" -o -name ".claude.md" -o -name ".claude.local.md" 2>/dev/null \
  | grep -v -E "/(node_modules|\.git|venv|\.venv|dist|build|target)/" | head -50

# READMEs at any depth (skip vendored)
find . -name "README.md" 2>/dev/null \
  | grep -v -E "/(node_modules|\.git|venv|\.venv|dist|build|target)/" | head -50

# Everything under docs/
find docs -type f -name "*.md" 2>/dev/null | head -100
```

If none of the three sets has any files, stop and tell the user there are no docs to audit.

### Phase 2: Quality Assessment

Score each file against the rubric appropriate to its type. See [references/quality-criteria.md](references/quality-criteria.md) for the full rubrics.

| File type | Rubric source | Owner |
| --- | --- | --- |
| `CLAUDE.md` / `.claude.local.md` | `claude-md-management:claude-md-improver` rubric | Delegate via the Skill tool — pass through its quality report verbatim |
| `README.md` | README rubric (this skill) | This skill |
| `docs/**/*.md` | Docs rubric (this skill) | This skill |

**Delegation rule:** if any `CLAUDE.md` files were found, invoke `claude-md-management:claude-md-improver` via the Skill tool *before* assessing
READMEs and `docs/`. Capture its quality report and merge it into the unified report in Phase 3. Do not re-score CLAUDE.md files yourself.

**Cross-reference with the actual repo:**

- Run (or mentally run) any documented commands; verify they exist in `Makefile`, `package.json`, `pyproject.toml`, etc.
- Check that referenced file paths exist (`ls` / `Read`).
- Compare claimed versions against `pyproject.toml` / `package.json` / lockfiles.
- Compare badge URLs and screenshots against current state.
- For docs/ contributor guides, spot-check that referenced commands and file paths are still valid.

### Phase 3: Quality Report

**Always print the unified report before any edits.**

```
## Documentation Quality Report

### Summary
- Files audited: X (CLAUDE.md: A, README.md: B, docs/: C)
- Average score: X/100
- Files needing update: X

### CLAUDE.md family
[verbatim from claude-md-improver — do not re-score]

### README.md files

#### ./README.md
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Install / quickstart works | X/20 | ... |
| Public surface complete | X/20 | ... |
| Currency (versions / paths / commands) | X/20 | ... |
| Examples runnable | X/15 | ... |
| Conciseness | X/15 | ... |
| Onboarding clarity | X/10 | ... |

**Issues:**
- [Specific, file:line where possible]

**Recommended changes:**
- [Concrete, one line each]

### docs/

#### ./docs/architecture.md
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Accuracy vs current code | X/25 | ... |
| Structure / discoverability | X/20 | ... |
| Currency | X/20 | ... |
| Conciseness | X/15 | ... |
| Links resolve | X/10 | ... |
| Non-duplication with README/CLAUDE.md | X/10 | ... |

**Issues:** ...
**Recommended changes:** ...
```

### Phase 4: Targeted Updates

After the report, propose concrete edits. **Do not apply yet.**

**Update guidelines:**

1. **One concept per line** — same density as `revise-all-docs`. No filler, no restating obvious code.
2. **Edit existing files only** — never create new doc files in this skill. If a finding doesn't fit anywhere, list it under "Unfiled findings" and let the user decide.
3. **Show diffs per file**, grouped. For each file that gets edits, output a `### Update: ./<path>` heading, a one-line `**Why:** <reason>`, then
   a standard ```` ```diff ```` fenced block with the `-` / `+` lines. Example for `./README.md` where the quickstart references a removed
   `make dev` target:

   ```diff
   - make dev
   + make serve
   ```

4. **Surface deletions too** — outdated sections, dead links, references to removed features. These often matter more than additions.
5. **Do not duplicate** — if the same fact belongs in both README and a docs file, pick the canonical home and link from the other.

### Phase 5: Apply

Wait for explicit user approval ("yes" / "apply" / per-file selection). Then:

- Use `Edit` (never `Write` — we're amending, not replacing).
- Apply only the edits the user approved.
- After applying, summarize: files changed, lines added/removed per file, and any findings deferred or declined.

## Common Issues to Flag

**README.md:**

- Install commands that no longer work (wrong tool, wrong path, missing step)
- Screenshots / badges referencing prior versions or deleted features
- Tool / command listings missing newly added or removed entries
- Version mismatch with `pyproject.toml` / `package.json`
- Quickstart that skips a required env-var or auth step
- Marketing prose that's drifted from what the project actually does

**docs/**/*.md:**

- Architecture diagrams referencing deleted modules
- Contributor guides citing dead `make` targets or scripts
- Duplicate content also covered (more accurately) in README or CLAUDE.md
- Orphan files no longer linked from anywhere
- Broken intra-doc links (`](./other.md)`)
- "TODO" / "WIP" markers older than the file's most recent commit

## What this skill does *not* do

- **Session learnings** — that's `/revise-all-docs`. This skill audits the static state of docs, not what was learned this session.
- **CLAUDE.md scoring** — delegated to `claude-md-management:claude-md-improver`.
- **Creating new doc files** — only edits existing ones. New files are a human decision.
- **Code or config edits** — only doc files (`*.md`).
