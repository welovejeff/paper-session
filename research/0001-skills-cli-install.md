Status: Implemented
Date: 2026-08-11
Outcome: same PR as this status change — README §Install now documents `npx skills add welovejeff/paper-session`

# skills.sh / `skills` CLI research results

## Scope

Research whether this repository can support installation through the `skills` CLI (the ecosystem behind skills.sh), and what would be required.

## Sources

- https://github.com/vercel-labs/skills (primary CLI documentation)
- https://skills.sh (registry/marketplace referenced by the CLI project)
- Local repository files:
  - `paper-session/SKILL.md`
  - `scan-back/SKILL.md`
  - `build.sh`

## Key findings

1. **The install CLI is `npx skills` (from `vercel-labs/skills`)** and supports adding skills from:
   - GitHub shorthand (`owner/repo`)
   - full Git URLs
   - direct skill paths in repos
   - local directories
   - direct `SKILL.md`/archive download URLs

   Example commands from upstream docs:

   ```bash
   npx skills add vercel-labs/agent-skills
   npx skills add https://github.com/vercel-labs/agent-skills
   npx skills add ./my-local-skills
   npx skills add vercel-labs/agent-skills --list
   ```

2. **Cross-agent support is broad** (README currently says OpenCode, Claude Code, Codex, Cursor, and many more), including explicit agent flags like:
   - `-a claude-code`
   - `-a github-copilot`
   - `-a cursor`

3. **The required skill format matches this repo’s structure**:
   - Skills are directory-based and require a `SKILL.md` with YAML frontmatter (`name`, `description`).
   - This repository already has:
     - `paper-session/SKILL.md` with `name: paper-session`
     - `scan-back/SKILL.md` with `name: scan-back`
   - `build.sh` already enforces the same name/directory alignment rule.

4. **This repo’s existing `.skill` artifacts are compatible with the current model**:
   - The repository is source-first (`paper-session/`, `scan-back/`) and already generates distributable `.skill` archives via `build.sh`.
   - The `skills` CLI can install from repos/directories and (per upstream docs) direct archive/`SKILL.md` URLs, so both source and packaged distribution patterns can coexist.

## Practical integration options for `welovejeff/paper-session`

### Option A (lowest friction): document CLI install from repo source

Add usage docs showing:

```bash
# install discovered skills from this repo
npx skills add welovejeff/paper-session

# or target specific agents
npx skills add welovejeff/paper-session -a claude-code -a github-copilot -a cursor

# inspect before install
npx skills add welovejeff/paper-session --list
```

### Option B: document local/dev install

```bash
npx skills add ./paper-session
npx skills add ./scan-back
```

Useful for contributors editing skills locally before publishing.

### Option C: optional future publishing enhancements

- Add a dedicated section in `README.md` for `npx skills` installation.
- Optionally evaluate `skills.json`/ecosystem metadata only if needed by team workflows.

## Risks / unknowns to validate

1. **Live registry/discovery behavior can change quickly**; verify commands against the latest `vercel-labs/skills` README before release messaging.
2. **Repository-level discovery details** (which directories are auto-discovered first) should be tested once against this repo layout.
3. **Agent-specific install paths** differ by tool; docs should focus on CLI commands and let the CLI route files.

## Recommended next step

If we decide to proceed, the smallest follow-up change is a README update with a `skills` install section using `npx skills add welovejeff/paper-session` plus a `--list` example.

---

## Validation — 2026-08-11, implementation PR

Everything above this line is the brief as accepted. The implementation PR
tested its three flagged unknowns against the live CLI and the upstream source
before documenting anything. All three resolved; two details in the brief
needed correcting.

### Confirmed by live test

- **Discovery works on this exact layout (unknown #2, resolved).**
  `npx skills add welovejeff/paper-session --list` — run against the real
  GitHub repo — found both skills with their full descriptions. The mechanism,
  confirmed in upstream source (`src/skills.ts`): with no root `SKILL.md`, the
  CLI walks every *immediate* root-level subdirectory looking for one. The
  root-level position of `paper-session/` and `scan-back/` is therefore
  load-bearing for CLI discovery — moving them deeper would require a
  `skills/` container directory or the `--full-depth` flag.
- **End-to-end install is faithful.**
  `npx skills add welovejeff/paper-session -a claude-code -g -y` into an
  isolated `$HOME` installed both skills to `~/.claude/skills/`,
  **byte-identical to the source directories** (`diff -r` clean), including
  `references/`, `scripts/`, and the fonts with their OFL license. The CLI
  keeps a canonical copy under `~/.agents/skills/`. Without `-g`, installs are
  project-level (`.claude/skills/` in the working directory).
- **The committed `.skill` archives install directly (finding 4, confirmed
  with a caveat).**
  `npx skills add https://raw.githubusercontent.com/welovejeff/paper-session/main/paper-session.skill`
  works — the CLI detects the zip by magic bytes, so the nonstandard `.skill`
  extension is fine, and the archive's single top-level directory is unwrapped
  correctly. **Caveat:** a plain `github.com` blob URL will *not* install;
  only `/archive/`, `/raw/`, and `/releases/download/` paths on `github.com` —
  plus `raw.githubusercontent.com` — are treated as downloads.
- **Command surface (unknown #1, resolved as of this date).** `--list`, `-a`,
  `-s/--skill`, `-g`, `-y`, `--copy`, `--all`, and `--full-depth` all exist as
  the brief described. Upstream can still change; the README documents only
  the stable core (`add`, `--list`, `-a`, `-g`).

### Corrections to the brief

- **There is no `skills.json`** (Option C). The registry's optional
  customization file is `skills.sh.json`, and it is not required for listing.
- **skills.sh listing needs no submission at all**: repos appear automatically
  through the CLI's anonymous install telemetry once someone installs from
  them, ranked by install counts. At validation time this repo was not yet
  listed (its skills.sh pages 404) — expected, since listing follows installs,
  not the other way around.

### What was implemented

README §Install now leads with `npx skills add welovejeff/paper-session`, keeps
the clone-and-unzip and claude.ai upload paths, and notes that a CLI install
does not bring `requirements.txt`, so the Python dependencies get one explicit
line. No repository restructuring, no metadata files, no build changes were
needed — the source-first layout already satisfied the CLI's format.
