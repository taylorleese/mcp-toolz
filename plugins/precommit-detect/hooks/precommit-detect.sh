#!/usr/bin/env bash
# precommit-detect.sh — read-only check for pre-commit setup state.
# Emits a JSON envelope with hookSpecificOutput.additionalContext when any
# dependency or hook installation is missing. Never installs anything.
# Always exits 0.

set -u

# Resolve repo root. Bail silently if not in a git repo.
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$repo_root" ]; then
  echo '{}'
  exit 0
fi

config="$repo_root/.pre-commit-config.yaml"
if [ ! -f "$config" ]; then
  echo '{}'
  exit 0
fi

report="$(mktemp -t precommit-detect.XXXXXX)"
missing=0

check() {
  local label="$1" detail="$2"
  printf -- '- [ ] %s%s\n' "$label" "${detail:+ — $detail}" >>"$report"
  missing=1
}
ok() {
  local label="$1"
  printf -- '- [x] %s\n' "$label" >>"$report"
}

# Python 3.9+
py_ver="$(python3 -c 'import sys; print(".".join(map(str,sys.version_info[:3])))' 2>/dev/null || true)"
if [ -z "$py_ver" ]; then
  check "Python 3" "python3 not found on PATH"
else
  py_major="$(printf '%s' "$py_ver" | cut -d. -f1)"
  py_minor="$(printf '%s' "$py_ver" | cut -d. -f2)"
  if [ "$py_major" -lt 3 ] || { [ "$py_major" -eq 3 ] && [ "$py_minor" -lt 9 ]; }; then
    check "Python 3.9+" "have $py_ver"
  else
    ok "Python $py_ver"
  fi
fi

# pre-commit binary or module — accepts either a PATH binary or `python3 -m pre_commit`.
pc_ver="$(pre-commit --version 2>/dev/null | awk '{print $2}')"
if [ -z "$pc_ver" ]; then
  pc_ver="$(python3 -m pre_commit --version 2>/dev/null | awk '{print $2}')"
fi
if [ -n "$pc_ver" ]; then
  ok "pre-commit $pc_ver available"
  pc_present=1
else
  pc_present=0
  # Don't report missing pre-commit yet — only flag if the git hook is also missing.
fi

# .git/hooks/pre-commit installed by pre-commit framework.
# This is the load-bearing check: if the hook is installed, the repo is wired up,
# even when the binary lives in a venv that isn't on PATH.
hook_path="$repo_root/.git/hooks/pre-commit"
if [ -f "$hook_path" ] && grep -q 'pre-commit' "$hook_path" 2>/dev/null; then
  ok ".git/hooks/pre-commit installed"
else
  if [ "$pc_present" -eq 1 ]; then
    check ".git/hooks/pre-commit not installed" "run \`pre-commit install\` in $repo_root"
  else
    check "pre-commit binary not available" "install with \`pipx install pre-commit\` (or \`python3 -m pip install --user pre-commit\`); needed before \`pre-commit install\` can run"
    check ".git/hooks/pre-commit not installed" "depends on the pre-commit binary above"
  fi
fi

# Docker — only flagged if config references docker-based hooks.
if grep -Eq '^[[:space:]]*language:[[:space:]]*docker(_image)?[[:space:]]*$|-docker$' "$config"; then
  if docker info >/dev/null 2>&1; then
    ok "Docker daemon reachable (required by docker-based hooks)"
  else
    check "Docker daemon not reachable" "required by docker-based hooks in this config — start Docker Desktop / colima / orbstack manually (do NOT auto-install)"
  fi
fi

# Note: we deliberately do NOT scan `entry:` lines for external binaries.
# Most pre-commit hooks use `language: python|node|go|ruby` and the framework
# installs them in isolated envs, so the entry command is never expected to
# be on the user's PATH. Genuine `language: system` failures surface clearly
# at run time — earlier flagging here is too noisy.

# Emit. If nothing is missing, stay silent.
if [ "$missing" -eq 0 ]; then
  rm -f "$report"
  echo '{}'
  exit 0
fi

body="## pre-commit setup check ($repo_root)

$(cat "$report")

**Action required:** read \`\$HOME/.claude/hooks/PRECOMMIT_INSTRUCTIONS.md\` and follow the per-item AskUserQuestion protocol. Do not install anything without explicit user approval for each item."
rm -f "$report"

python3 - "$body" <<'PY'
import json, sys
body = sys.argv[1]
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": body,
    }
}))
PY

exit 0
