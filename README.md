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

- **Multi-LLM Feedback**: Get second opinions from ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google), and DeepSeek
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
export ANTHROPIC_API_KEY=sk-ant-...    # For Claude
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
        "ANTHROPIC_API_KEY": "sk-ant-...",
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
- `ask_claude` - Get Claude's analysis (supports custom questions)
- `ask_gemini` - Get Gemini's analysis (supports custom questions)
- `ask_deepseek` - Get DeepSeek's analysis (supports custom questions)

## Claude Code Skills

### `/resolve-github-alerts`

Automatically triages and resolves GitHub security alerts (Dependabot, code scanning, secret scanning). Run it in Claude Code to:

- Fix failing Dependabot PRs (lint/test issues)
- Bump vulnerable dependencies and recompile requirements
- Remediate code scanning and secret scanning alerts
- Submit a single PR with all fixes for manual review

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

- "Ask Claude the same question for comparison"
- "Ask Gemini for another perspective"
- "What does DeepSeek think about this?"

### Debug with Multiple Perspectives

```text
I'm getting "TypeError: Cannot read property 'map' of undefined" in my React component.
The error occurs in UserList.jsx when rendering the users array.
Ask ChatGPT and Claude for debugging suggestions.
```

## Environment Variables

```bash
# Required (at least one for AI feedback tools)
OPENAI_API_KEY=sk-...                              # Your OpenAI API key
ANTHROPIC_API_KEY=sk-ant-...                       # Your Anthropic API key
GOOGLE_API_KEY=...                                 # Your Google API key (for Gemini)
DEEPSEEK_API_KEY=sk-...                            # Your DeepSeek API key

# Optional
MCP_TOOLZ_MODEL=gpt-5                                         # OpenAI model (default: gpt-5)
MCP_TOOLZ_CLAUDE_MODEL=claude-sonnet-4-5-20250929             # Claude model
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
│       ├── anthropic_client.py  # Claude API client
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
