# All-Docs Quality Criteria

Per-type rubrics for the `all-docs-improver` skill. `CLAUDE.md` is delegated to `claude-md-management:claude-md-improver` and uses *its* rubric — not duplicated here.

## README.md Rubric (100 points)

### 1. Install / Quickstart Works (20 points)

**20**: Every install/quickstart command is copy-pasteable and currently passes on a clean machine.

- Tool prerequisites listed
- All required env vars / config mentioned
- The minimum-viable "run the thing" path is end-to-end runnable

**15**: Mostly works; one minor missing prereq or assumed step.

**10**: Works after manual fixup the reader has to figure out.

**5**: Outdated commands or missing steps in the critical path.

**0**: Quickstart no longer reflects how the project is run.

### 2. Public Surface Complete (20 points)

**20**: Every user-facing entrypoint is documented:

- Commands / CLI flags / subcommands match current code
- Public APIs / exported functions match current code
- For plugins: every shipped command, skill, hook, and tool is listed
- Configuration / env vars listed match the implementation

**15**: One or two minor entrypoints undocumented.

**10**: Several entrypoints undocumented or stale.

**5**: Documents a surface that no longer matches the code.

**0**: Major undocumented surface or describes a surface that's been removed.

### 3. Currency (20 points)

**20**: Versions, paths, screenshots, and badges match current state.

- Version numbers in README ↔ `pyproject.toml` / `package.json` agree
- Referenced paths exist
- Screenshots / badges reflect current UI / build status

**15**: Mostly current; one or two stale references.

**10**: Several stale references (old version, renamed paths).

**5**: Significantly out of date.

**0**: README describes a previous era of the project.

### 4. Examples Runnable (15 points)

**15**: Every code block in the README runs as written.

**10**: Most run; one or two need a missing import / path tweak.

**5**: Examples are illustrative but not runnable.

**0**: No examples, or examples are broken.

### 5. Conciseness (15 points)

**15**: Dense and skim-friendly. No filler, no redundancy, no marketing prose that doesn't help a user decide.

**10**: Mostly tight; a section or two of bloat.

**5**: Verbose; reader has to hunt for the actionable parts.

**0**: Wall of text or duplicated content.

### 6. Onboarding Clarity (10 points)

**10**: Reader knows in <30 seconds: what this project does, who it's for, and how to try it.

**5**: One of the three is unclear.

**0**: Reader leaves confused about scope or audience.

## docs/**/*.md Rubric (100 points)

### 1. Accuracy vs Current Code (25 points)

**25**: Every claim about the codebase matches what's in `main`.

- Architecture diagrams reflect actual modules
- File paths and module names exist
- Behavior described matches behavior implemented
- Cited versions, deps, and config match the lockfile / config

**18**: Mostly accurate; one or two stale specifics.

**12**: Several inaccuracies — confusing if used as a reference.

**6**: Doc describes a prior architecture.

**0**: Doc actively misleads.

### 2. Structure / Discoverability (20 points)

**20**: Reader can find what they need:

- Title and intro state scope clearly
- Sections / headings match what they actually contain
- Linked from a discoverable place (root README, `docs/index.md`, etc.)
- Doesn't require reading top-to-bottom

**15**: Reasonable structure with minor gaps.

**10**: Findable but disorganized.

**5**: Hidden / orphan / no internal structure.

**0**: Title doesn't match content; reader can't tell what they're reading.

### 3. Documentation Currency (20 points)

**20**: Reflects current state, not a snapshot from N months ago.

- No `TODO` / `WIP` items older than the file's last meaningful commit
- No references to deprecated tools / paths / processes
- "Last updated" claims (if present) match git log

**15**: Mostly current, minor staleness.

**10**: Several outdated specifics.

**5**: Significantly stale.

**0**: Snapshot from a previous era.

### 4. Conciseness (15 points)

**15**: Dense, single-purpose. No padding, no obvious info.

**10**: Mostly tight.

**5**: Verbose.

**0**: Wall of filler.

### 5. Links Resolve (10 points)

**10**: Every intra-doc link (`](./other.md)`) and external link points to something that exists.

**5**: A few broken links.

**0**: Many broken links / dead refs.

### 6. Non-Duplication (10 points)

**10**: This file is the canonical home for its topic. No content lives more accurately in README or CLAUDE.md.

**5**: Some duplication, but this version adds depth.

**0**: Pure duplication of content owned elsewhere.

## Grading Scale

- **A (90–100)**: Comprehensive, current, actionable
- **B (70–89)**: Good coverage, minor gaps
- **C (50–69)**: Basic info, missing key sections
- **D (30–49)**: Sparse or outdated
- **F (0–29)**: Missing, severely outdated, or actively misleading

## Red Flags (Both File Types)

- Commands that fail or reference removed scripts / make targets
- Paths or modules that no longer exist
- Versions, badges, or screenshots from a previous era
- "TODO" items left over from prior contributors
- Sections that contradict the actual code
- Duplicate content drifting between README, CLAUDE.md, and `docs/`
- Files no longer linked from anywhere — orphans
- Marketing copy that no longer matches the project's actual scope
