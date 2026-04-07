# CLAUDE.md

## Project Overview

MCP server providing multi-LLM tools (ask_chatgpt, ask_claude, ask_gemini, ask_deepseek) and clipboard image capture (paste_image).
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
- `src/context_manager/` - LLM client implementations (openai, anthropic, gemini, deepseek) and clipboard image capture
- `tests/` - pytest tests with asyncio auto mode; mock all API clients

## Code Style

- Line length: 140 (black, ruff, isort all configured)
- Strict mypy with `explicit_package_bases = true`
- Google-style docstrings (pydocstyle)
- Error messages use `msg = "..."; raise ValueError(msg)` pattern (ruff EM rules)

## Testing

- Tests run with `PYTHONPATH=src` (set in Makefile/pytest config)
- All LLM API calls are mocked via `unittest.mock.patch` on the client classes
- MCP server tests patch at `mcp_server.server.ClientClass` level
- pytest markers: unit, integration, slow

## Skills

- `/resolve-github-alerts` - Automatically triages and resolves GitHub security alerts (Dependabot, code scanning, secret scanning). Fixes failing Dependabot PRs, bumps vulnerable dependencies, and submits PRs for manual review.

## Dependencies

- After changing requirements.in, run `make compile-requirements` to regenerate hashed requirements.txt
- google.generativeai is deprecated (FutureWarning) but still functional
