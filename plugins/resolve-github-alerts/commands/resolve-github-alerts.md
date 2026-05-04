---
description: Resolve GitHub security alerts (Dependabot, code scanning, secret scanning) across pip / pip-tools / poetry / uv / npm / yarn / pnpm / cargo / go / docker / GitHub Actions ecosystems. Opens a single PR for manual review.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Skill
---

Invoke the `resolve-github-alerts` skill via the Skill tool. The skill runs all four phases — triage Dependabot PRs, fix remaining Dependabot
vulnerability alerts, resolve code-scanning alerts, handle secret-scanning alerts — using the project's existing toolchain (auto-detects Makefile
targets, pre-commit, ruff/pytest, npm scripts) and opens a single labeled PR with all fixes for manual review. Never auto-merges.
