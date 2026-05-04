---
name: resolve-github-alerts
description: >-
  Resolve GitHub security alerts (Dependabot, code scanning, secret
  scanning). Fixes failing Dependabot PRs, remediates remaining
  vulnerability/code/secret alerts, and submits PRs for manual review.
---

# Resolve GitHub Alerts

This skill resolves all GitHub security alerts: Dependabot alerts,
code scanning alerts, and secret scanning alerts.

## Constants

- **Label**: `automated/resolve-github-alerts`
- **Branch**: `automated/resolve-github-alerts`
- **Base branch**: `main`

### Setup

At the start of execution, derive the GitHub owner and repo. Use
`git remote get-url origin` from the **current working directory**
(works in both the main checkout and git worktrees):

```bash
OWNER_REPO=$(git remote get-url origin | sed -E 's#.*(github\.com[:/])##;s/\.git$//')
OWNER=${OWNER_REPO%/*}
REPO=${OWNER_REPO#*/}
```

Use `$OWNER` and `$REPO` in all `gh` CLI commands below.

### Worktree Awareness

This skill may run inside a git worktree. Observe these rules:

- **Derive repo root** from `git rev-parse --show-toplevel`, never
  hard-code a path.
- **All file reads/edits** must use paths relative to the worktree
  root, not the main checkout.
- `git remote`, `git fetch`, `git push`, and `gh` commands work
  unchanged in a worktree because they share the main repo's
  remote configuration.
- **Do not run** `git worktree add/remove` — the caller manages the
  worktree lifecycle.

## Resolution Priority

1. **Fix the root cause in code** — All fixes must be committed as code
   changes: dependency upgrades in `requirements*.in`/`requirements*.txt`,
   Dockerfile base image tags, GitHub Actions versions, or application
   code fixes in `src/`. Never apply ad hoc fixes via manual steps.
   Never add lint exclusions or scanner ignores.
2. **Dismiss only for confirmed false positives** — Only dismiss alerts
   for test credentials, false positives, or transitive dependencies
   with no available patch.
3. **Create GitHub issues as last resort** — Only when the fix requires
   human judgment or access you don't have.

## PR Management Pattern

Maintain **at most ONE** open PR at a time for non-Dependabot fixes.
Identified by the `automated/resolve-github-alerts` label.

### Before creating or updating a PR

1. Search for an existing open PR:

   ```bash
   gh pr list --repo $OWNER/$REPO --label automated/resolve-github-alerts --state open --json number,title
   ```

2. **If PR exists**: Push additional commits to the existing
   `automated/resolve-github-alerts` branch and update the PR body.
3. **If no PR exists**: Create the branch from `main`, push fixes,
   create the PR, and add labels/assignee:
   - **Labels**: `automated/resolve-github-alerts`, `security`, `dependencies`
   - **Assignees**: `$OWNER`

## Execution Phases

Run all four phases in order. Track results for the final summary.

---

### Phase 1: Triage Dependabot PRs

**Goal**: List open Dependabot PRs, check CI status, and fix ones with
CI failures if possible. Never auto-merge — leave merging to the user.

#### Step 1.1: List open Dependabot PRs

```bash
gh pr list --repo $OWNER/$REPO --state open --author "app/dependabot" --json number,title,headRefName
```

#### Step 1.2: Check CI status for each Dependabot PR

For each Dependabot PR, check CI status:

```bash
gh pr checks <PR_NUMBER> --repo $OWNER/$REPO
```

Categorize each PR:

- **Passing**: All required checks are successful — ready for manual merge
- **Failing**: One or more checks failed
- **Pending**: Checks still running

#### Step 1.3: Fix failing Dependabot PRs

For each failing Dependabot PR:

1. Get the PR diff to understand the dependency change:

   ```bash
   gh pr diff <PR_NUMBER> --repo $OWNER/$REPO
   ```

2. Get the failure details from the checks output.
3. Determine if the failure is fixable:
   - **Lint failures** (ruff, mypy, type errors): Read the failing
     files, determine the fix, and push a commit to the Dependabot
     branch.
   - **Test failures**: Read the test files, understand the breakage,
     fix the tests, and push.
   - **Security check failures**: Do NOT attempt to fix. Skip and
     report as "unfixable - security check failure".
4. After pushing fixes, re-check CI status and report result.

#### Step 1.4: Report Phase 1 results

Track counts: passing (ready to merge), fixed (ready to merge),
attempted fix (still failing), pending, skipped.

---

### Phase 2: Fix Remaining Dependabot Alerts

**Goal**: Resolve open Dependabot vulnerability alerts that don't have
associated PRs.

#### Step 2.1: Discover open alerts

```bash
gh api repos/$OWNER/$REPO/dependabot/alerts --jq '[.[] | select(.state == "open")] | length'
```

Get full alert details:

```bash
gh api repos/$OWNER/$REPO/dependabot/alerts \
  --jq '[.[] | select(.state == "open")] | .[] | {
    number, state,
    dependency: .dependency.package.name,
    ecosystem: .dependency.package.ecosystem,
    manifest: .dependency.manifest_path,
    severity: .security_advisory.severity,
    summary: .security_advisory.summary,
    fixed_in: .security_vulnerability.first_patched_version.identifier
  }'
```

If no open alerts, skip to Phase 3.

#### Step 2.2: Map alerts to files

Based on ecosystem, identify which files to modify:

| Ecosystem | Files |
| ----------- | ------- |
| pip | `requirements.in`, `requirements.txt`, `requirements-dev.in`, `requirements-dev.txt` |
| docker | `Dockerfile`, `Dockerfile.glama` |
| github-actions | `.github/workflows/*.yml` |

#### Step 2.3: Apply fixes

For each alert:

1. Read the affected manifest file.
2. Determine the fix:
   - **Direct pip dependency**: Bump the version in `requirements.in`
     (or `requirements-dev.in`), then run `make compile-requirements`
     to regenerate the hashed `.txt` files.
   - **Docker base image**: Update the image tag in the Dockerfile.
   - **GitHub Actions**: Update the action version reference.
3. Apply the fix using the Edit tool.

#### Step 2.4: Push fixes as a PR

Follow the PR Management Pattern above. Commit all Dependabot alert
fixes together with a clear message describing what was bumped and why.

#### Guardrails for Phase 2

- After touching any `requirements*.in` file, **always** run
  `make compile-requirements` to regenerate the hashed `.txt` files.
- Run `make lint` after changes to verify no breakage.
- Run `make test` after dependency changes to verify compatibility.

---

### Phase 3: Resolve Code Scanning Alerts

**Goal**: Fix SAST/code scanning findings in source code.

#### Step 3.1: Discover open alerts

```bash
gh api repos/$OWNER/$REPO/code-scanning/alerts --jq '[.[] | select(.state == "open")] | length'
```

Get full alert details:

```bash
gh api repos/$OWNER/$REPO/code-scanning/alerts \
  --jq '[.[] | select(.state == "open")] | .[] | {
    number, state,
    rule: .rule.id,
    severity: .rule.severity,
    description: .rule.description,
    path: .most_recent_instance.location.path,
    start_line: .most_recent_instance.location.start_line,
    end_line: .most_recent_instance.location.end_line
  }'
```

If no open alerts, skip to Phase 4.

#### Step 3.2: Analyze each alert

Read the affected source file at the identified line range to
understand the context and determine the correct fix.

#### Step 3.3: Fix each alert

Apply the appropriate fix based on the alert type:

| Alert Type | Fix Pattern |
| ------------ | ------------- |
| SQL injection | Use parameterized queries |
| Command injection | Use `subprocess.run()` with list args, never `shell=True` with user input |
| Path traversal | Validate and sanitize paths, use `os.path.realpath()` + prefix check |
| XSS | Escape output, use safe templating |
| Insecure deserialization | Replace `pickle.loads` with JSON or safe alternatives |
| Hardcoded credentials | Move to environment variables |
| Weak cryptography | Upgrade to strong algorithms (AES-256, SHA-256+) |

Apply fixes using the Edit tool.

#### Step 3.4: Push fixes

Add code scanning fixes to the same PR branch (following PR Management
Pattern). If no PR exists yet, create one.

---

### Phase 4: Resolve Secret Scanning Alerts

**Goal**: Handle exposed secrets detected by GitHub secret scanning.

#### Step 4.1: Discover open alerts

```bash
gh api repos/$OWNER/$REPO/secret-scanning/alerts --jq '[.[] | select(.state == "open")] | length'
```

If no open alerts, skip to Summary.

#### Step 4.2: Triage each alert

```bash
gh api repos/$OWNER/$REPO/secret-scanning/alerts \
  --jq '[.[] | select(.state == "open")] | .[] | {
    number, state,
    secret_type: .secret_type_display_name,
    created_at
  }'
```

#### Step 4.3: Handle each alert

**For false positives** (test keys, example values, already-rotated
secrets):

- Verify the secret is not real/active.
- Note in the summary as "false positive" for manual resolution.

**For real credentials**:

1. **Always create a GitHub issue** with:
   - Title: `[Secret Scanning] Rotate exposed <secret_type>`
   - Body: Details of what was exposed, where, and what rotation steps
     are needed
   - Labels: `security`, `automated/resolve-github-alerts`
   - Assignees: `$OWNER`
2. Remove the secret from code if still present:
   - Replace with environment variable reference
   - Add the file pattern to `.gitignore` if it's a credentials file
3. Push the code fix to the PR branch

#### Guardrails for Phase 4

- **Always create a GitHub issue** for confirmed real credentials,
  even after rotation.
- Never log or echo the actual secret value in any output.
- Check if the secret is referenced in other files before removing.

---

## Summary Report

After all phases complete, output a summary table:

```markdown
## Security Alert Resolution Summary

### Phase 1: Dependabot PRs
| PR | Title | CI Status | Action |
| ---- | ------- | ---------- | -------- |
| #XX | Bump foo from 1.0 to 1.1 | Passing | Ready to merge |
| #YY | Bump bar from 2.0 to 2.1 | Fixed | Ready to merge |

### Phase 2: Dependabot Alerts
| Alert | Package | Severity | Action | Result |
| ------- | --------- | ---------- | -------- | -------- |
| #NN | package-name | high | Version bump | Fixed in PR #ZZ |

### Phase 3: Code Scanning Alerts
| Alert | Rule | File | Action | Result |
| ------- | ------ | ------ | -------- | -------- |
| #NN | rule-id | src/file.py | Fixed pattern | Fixed in PR #ZZ |

### Phase 4: Secret Scanning Alerts
| Alert | Type | Action | Result |
| ------- | ------ | -------- | -------- |
| #NN | secret-type | False positive | Noted for manual review |

### Totals
- Dependabot PRs ready to merge: X
- Dependabot alerts fixed: X
- Code scanning alerts fixed: X
- Secret scanning alerts handled: X
- Items requiring manual attention: X
```

If no issues were found across all phases, report:

```markdown
## All Clear

No open security alerts found.
- Dependabot PRs checked: 0 open
- Dependabot alerts: 0 open
- Code scanning alerts: 0 open
- Secret scanning alerts: 0 open
```

End the summary with: **Generated by `/resolve-github-alerts`**

---

## PR Format

When creating or updating the fix PR, use this format:

**Title**: `fix: resolve GitHub security alerts`

**Body**:

```markdown
## Summary

Automated resolution of GitHub security alerts.

<insert summary table from above>

## Changes

<bulleted list of specific changes made>

## Test Plan

- [ ] CI checks pass
- [ ] No new security alerts introduced
- [ ] Dependency compatibility verified

Generated by `/resolve-github-alerts`
```
