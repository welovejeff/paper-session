# skills.sh / `skills` CLI research results

## Scope

Research whether this repository can support installation through the `skills` CLI (the ecosystem behind skills.sh), and what would be required.

## Sources

- https://github.com/vercel-labs/skills (primary CLI documentation)
- https://skills.sh (registry/marketplace referenced by the CLI project)
- Local repository files:
  - `/home/runner/work/paper-session/paper-session/paper-session/SKILL.md`
  - `/home/runner/work/paper-session/paper-session/scan-back/SKILL.md`
  - `/home/runner/work/paper-session/paper-session/build.sh`

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

