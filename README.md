# MCP Toolz

mcp-name: io.github.taylorleese/mcp-toolz

[![CI](https://github.com/taylorleese/mcp-toolz/actions/workflows/ci.yml/badge.svg)](https://github.com/taylorleese/mcp-toolz/actions/workflows/ci.yml)
[![GitHub issues](https://img.shields.io/github/issues/taylorleese/mcp-toolz)](https://github.com/taylorleese/mcp-toolz/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/taylorleese/mcp-toolz)](https://github.com/taylorleese/mcp-toolz/commits/main)
[![codecov](https://codecov.io/gh/taylorleese/mcp-toolz/branch/main/graph/badge.svg)](https://codecov.io/gh/taylorleese/mcp-toolz)
[![PyPI version](https://img.shields.io/pypi/v/mcp-toolz.svg)](https://pypi.org/project/mcp-toolz/)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.26.0-blue)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/11358/badge)](https://www.bestpractices.dev/projects/11358)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/taylorleese/mcp-toolz/badge)](https://scorecard.dev/viewer/?uri=github.com/taylorleese/mcp-toolz)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-blue?logo=dependabot)](https://github.com/taylorleese/mcp-toolz/blob/main/.github/dependabot.yml)

MCP server for Claude Code that provides multi-LLM feedback tools.

## Features

- **Multi-LLM Feedback**: Get second opinions from ChatGPT (OpenAI), Gemini (Google), and DeepSeek
- **MCP Integration**: Works with Claude Code via the Model Context Protocol

## Quick Start

### Installation

#### From PyPI (Recommended)

```bash
pip install mcp-toolz
```

#### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/taylorleese/mcp-toolz.git
cd mcp-toolz

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Configuration

```bash
# Set your API keys as environment variables (at least one required for AI feedback tools)
export OPENAI_API_KEY=sk-...           # For ChatGPT
export GOOGLE_API_KEY=...              # For Gemini
export DEEPSEEK_API_KEY=sk-...         # For DeepSeek

# Or create a .env file (if installing from source)
cp .env.example .env
# Edit .env and add your API keys
```

### MCP Server Setup

Add to your Claude Code MCP settings:

**If installed via pip:**

```json
{
  "mcpServers": {
    "mcp-toolz": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "GOOGLE_API_KEY": "...",
        "DEEPSEEK_API_KEY": "sk-..."
      }
    }
  }
}
```

**If installed from source:**

```json
{
  "mcpServers": {
    "mcp-toolz": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "cwd": "/absolute/path/to/mcp-toolz",
      "env": {
        "PYTHONPATH": "/absolute/path/to/mcp-toolz/src"
      }
    }
  }
}
```

Restart Claude Code to load the MCP server.

## MCP Server Tools

### AI Feedback Tools

Get second opinions from multiple LLMs on code, architecture decisions, and implementation plans:

- `ask_chatgpt` - Get ChatGPT's analysis (supports custom questions)
- `ask_gemini` - Get Gemini's analysis (supports custom questions)
- `ask_deepseek` - Get DeepSeek's analysis (supports custom questions)

## Claude Code plugins

This repo doubles as a Claude Code plugin marketplace. Install all four with:

```text
/plugin marketplace add taylorleese/mcp-toolz
/plugin install mcp-toolz-server@mcp-toolz
/plugin install precommit-detect@mcp-toolz
/plugin install revise-all-docs@mcp-toolz
/plugin install resolve-github-alerts@mcp-toolz
```

### `mcp-toolz-server`

Installs the mcp-toolz MCP server in Claude Code without manual editing of `~/.claude.json`. Once installed, the three tools (`ask_chatgpt`, `ask_gemini`,
`ask_deepseek`) are available to the model in any Claude Code session. The plugin runs the server via `uvx --from mcp-toolz python -m mcp_server`, so PyPI
is still the underlying distribution channel — this is purely an installation-ergonomics layer for Claude Code users.

Required env vars (set in your shell or via direnv/`.envrc`): `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`. Each is independently optional — the
corresponding tool just returns an error if its key is unset.

For Cursor / Zed / Claude Desktop users: keep configuring the MCP server manually via your client's standard mechanism. Claude Code plugins don't propagate
to other clients.

### `precommit-detect`

Read-only check for pre-commit setup state. Registers `SessionStart` and `PostToolUse:EnterWorktree` hooks that detect whether the current repo's
`.pre-commit-config.yaml` is wired up — pre-commit binary present, `.git/hooks/pre-commit` installed, Docker daemon reachable when the config requires it.
When something is missing, the hook surfaces the gap as `additionalContext` so Claude can walk you through approval-gated installs (one prompt per missing
item — never auto-installs).

### `revise-all-docs`

Two ways to keep **CLAUDE.md**, **README.md**, and **`docs/**/*.md`** in sync — pick by intent.

#### `/revise-all-docs` — *"I just finished some work. Capture what we learned."*

Reads the current conversation, pulls out commands discovered, gotchas hit, and patterns enforced, and proposes additions to the right doc file
for each finding (project-internal context → `CLAUDE.md`, user-facing onboarding → `README.md`, deeper how-to → `docs/`). Run this at the end of
a session that uncovered something worth recording.

#### `/improve-all-docs` — *"Forget the session. Audit the docs as they stand today."*

Statically scans every doc file, scores each against type-appropriate rubrics (install steps actually work? public command/API surface
complete? versions and paths current? intra-doc links resolve? duplicated content?), then proposes targeted fixes — including **deletions** of
stale or duplicated content, not just additions. Run this during cleanup passes, before a release, or when docs feel out of sync with the code.

The `all-docs-improver` skill is the same audit auto-invoked when you ask in plain language ("are my docs up to date?", "check the README and
docs"). The slash command is explicit; the skill is hands-free.

#### Required dependency

Both surfaces delegate `CLAUDE.md` work to the official `claude-md-management` plugin:

```text
/plugin install claude-md-management@anthropics
```

### `resolve-github-alerts`

Triages and resolves GitHub security alerts (Dependabot, code scanning, secret scanning) across **pip / pip-tools / poetry / uv / npm / yarn / pnpm / cargo / go-modules / Docker / GitHub Actions** ecosystems. Run it in any repo to:

- Fix failing Dependabot PRs (lint/test issues)
- Bump vulnerable dependencies and recompile lockfiles
- Remediate code scanning and secret scanning alerts
- Submit a single PR with all fixes for manual review

Auto-detects the project's verify commands (Makefile targets, pre-commit, ruff, pytest, npm scripts) — no per-project configuration required.

```text
/resolve-github-alerts
```

## Usage Examples

### Get Multiple AI Perspectives

```text
I'm deciding between Redis and Memcached for caching user sessions.
Ask ChatGPT for their analysis.
```

Follow up with:

- "Ask Gemini for another perspective"
- "What does DeepSeek think about this?"

### Debug with Multiple Perspectives

```text
I'm getting "TypeError: Cannot read property 'map' of undefined" in my React component.
The error occurs in UserList.jsx when rendering the users array.
Ask ChatGPT and Gemini for debugging suggestions.
```

## Environment Variables

```bash
# Required (at least one for AI feedback tools)
OPENAI_API_KEY=sk-...                              # Your OpenAI API key
GOOGLE_API_KEY=...                                 # Your Google API key (for Gemini)
DEEPSEEK_API_KEY=sk-...                            # Your DeepSeek API key

# Optional
MCP_TOOLZ_MODEL=gpt-5                                         # OpenAI model (default: gpt-5)
MCP_TOOLZ_GEMINI_MODEL=gemini-2.0-flash-thinking-exp-01-21   # Gemini model
MCP_TOOLZ_DEEPSEEK_MODEL=deepseek-chat                        # DeepSeek model
```

## Troubleshooting

### "Error 401: Invalid API key"

- Verify API keys are set in `.env` or environment variables
- Check billing is enabled on your API provider account

### "No module named context_manager"

- Use `PYTHONPATH=src` before running Python directly
- Or install via pip: `pip install mcp-toolz`

## Project Structure

```text
mcp-toolz/
├── src/
│   ├── mcp_server/              # MCP server for Claude Code
│   │   └── server.py            # MCP tools and handlers
│   └── context_manager/         # Client implementations
│       ├── openai_client.py     # ChatGPT API client
│       ├── gemini_client.py     # Gemini API client
│       └── deepseek_client.py   # DeepSeek API client
├── tests/                       # pytest tests
├── requirements.in
└── requirements.txt
```

## Development

### Setup for Contributors

```bash
# Clone and install
git clone https://github.com/taylorleese/mcp-toolz.git
cd mcp-toolz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Install pre-commit hooks (IMPORTANT!)
pre-commit install

# Copy and configure .env
cp .env.example .env
# Edit .env with your API keys
```

### Running Tests

```bash
source venv/bin/activate
pytest
```

### Code Quality

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)
[![isort](https://img.shields.io/badge/imports-isort-blue)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

<a href="https://glama.ai/mcp/servers/@taylorleese/mcp-toolz">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@taylorleese/mcp-toolz/badge" alt="mcp-toolz MCP server" />
</a>

```bash
# Run all checks (runs automatically on commit after pre-commit install)
pre-commit run --all-files

# Individual tools
black .
ruff check .
mypy src/
```

## License

MIT
