# CLAUDE.md

## Project Overview

MCP server providing multi-LLM tools (ask_chatgpt, ask_claude, ask_gemini, ask_deepseek).
Python 3.13+, src layout with `PYTHONPATH=src`.

## Key Commands

- `make test` - Run tests (pytest, parallel via xdist)
- `make lint` - Run all linters via pre-commit (33 hooks including black, ruff, mypy, bandit, vulture)
- `make format` - Auto-format code
- `make compile-requirements` - Recompile requirements.txt from requirements.in (uses pip-compile with hashes)
- `make all` - format + lint + test
- `make publish` - **ALWAYS use this to release.** Runs tests, lint, commits version bump, creates git tag, pushes, and creates GitHub release. Never create releases or tags manually.

## Project Structure

- `src/mcp_server/server.py` - MCP server with tool definitions and handlers
- `src/context_manager/` - LLM client implementations (openai, anthropic, gemini, deepseek)
- `tests/` - pytest tests with asyncio auto mode; mock all API clients

## Code Style

- Line length: 140 (black, ruff, isort all configured)
- Strict mypy with `explicit_package_bases = true`
- Google-style docstrings (pydocstyle)
- Error messages use `msg = "..."; raise ValueError(msg)` pattern (ruff EM rules)
- Markdown line length: 240 (markdownlint MD013) — wrap long paragraphs manually; the hook fails, it doesn't auto-wrap
- Avoid `+` at the start of continuation lines in markdown — markdownlint MD004 silently rewrites it to `-`

## Testing

- Tests run with `PYTHONPATH=src` (set in Makefile/pytest config)
- All LLM API calls are mocked via `unittest.mock.patch` on the client classes
- MCP server tests patch at `mcp_server.server.ClientClass` level
- pytest markers: unit, integration, slow

## Claude Code plugins

This repo's `.claude-plugin/marketplace.json` ships four plugins. Install via `/plugin marketplace add taylorleese/mcp-toolz` from any session.

- `mcp-toolz-server` - wraps `uvx --from mcp-toolz python -m mcp_server` as an installable MCP server config; one-step install of the multi-LLM tools for Claude Code users (other MCP clients still configure manually).
- `precommit-detect` - SessionStart/PostToolUse hooks that detect whether the repo's pre-commit setup is wired up and walk through approval-gated installs.
- `revise-all-docs` - `/revise-all-docs` command + skill for syncing CLAUDE.md, README.md, and docs/**/*.md with session learnings (depends on `claude-md-management@anthropics`).
- `resolve-github-alerts` - `/resolve-github-alerts` triages and resolves GitHub security alerts across pip/pip-tools/poetry/uv/npm/cargo/go/docker/actions ecosystems and opens a single PR for review.

## Dependencies

- After changing requirements.in, run `make compile-requirements` to regenerate hashed requirements.txt
- google.generativeai is deprecated (FutureWarning) but still functional
