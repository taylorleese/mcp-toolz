# Pre-commit setup protocol

When the `precommit-detect.sh` hook reports unchecked items, follow this protocol exactly. **Never install or run anything without explicit user approval.**

## Rules

1. **One AskUserQuestion per missing item.** Do not bundle multiple installs into a single yes/no. Each unchecked item gets its own question with options "Install" / "Skip".
2. **Order matters.** Ask about prerequisites before dependents:
   - pre-commit binary → before → `pre-commit install`
   - Docker → no install action; only ask user to start daemon and re-check
3. **If a prerequisite is skipped, do not ask about its dependents.** Skipping the binary install means `pre-commit install` is impossible — don't even ask.
4. After every approved action, re-run `bash ${CLAUDE_PLUGIN_ROOT}/hooks/precommit-detect.sh` and report the final state to the user.

## Per-item commands (run only on Install)

| Missing item | Command |
| --- | --- |
| pre-commit binary | `pipx install pre-commit` (preferred) — fall back to `python3 -m pip install --user pre-commit` if pipx is unavailable |
| `.git/hooks/pre-commit` | `(cd <repo-root> && pre-commit install)` |
| Docker daemon | **never auto-install**; instruct the user to start Docker Desktop / colima / orbstack manually, then re-run detection |
| Python 3.9+ missing | **never auto-install**; tell the user their Python is too old and let them upgrade manually |

## Question phrasing examples

- "The `pre-commit` binary isn't available. Install it with `pipx install pre-commit`?" — options: Install / Skip
- "Wire up `.git/hooks/pre-commit` for `<repo-root>` by running `pre-commit install`?" — options: Install / Skip. **Ask this as a separate question, even when the binary install just succeeded.**
- "Docker daemon isn't reachable but this repo's pre-commit config needs it. Start it now (manually) and I'll re-check?" — options: Re-check / Skip

## Edge cases

- **User declines binary install but the git hook is also missing:** stop. Do not ask about `pre-commit install`. Note in your reply that nothing was changed.
- **Binary install succeeds but user declines `pre-commit install`:** that's fine. The binary remains available for future use; the hook just isn't wired up for this repo. Don't undo the binary install.
- **Detection re-run still shows missing items:** report them plainly. Don't re-ask the user about items they just declined.
