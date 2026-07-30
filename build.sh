#!/usr/bin/env bash
# Package each skill source directory into a distributable .skill bundle.
#
# A .skill file is a zip whose single top-level directory is the skill name,
# containing SKILL.md at its root. The source directories in this repo are
# authoritative; the .skill files are build artifacts (committed so people can
# install without cloning).
#
# Usage: ./build.sh [skill-name ...]      # default: all skills

set -euo pipefail
cd "$(dirname "$0")"

SKILLS=("${@:-}")
[[ -z "${SKILLS[0]:-}" ]] && SKILLS=(paper-session scan-back)

# unzip is needed too, for the file count and the font-license check below.
# Check both up front: discovering it after the first bundle is rewritten leaves
# the tree half-built.
for tool in zip unzip; do
  command -v "$tool" >/dev/null || { echo "error: $tool not found" >&2; exit 1; }
done

for skill in "${SKILLS[@]}"; do
  if [[ ! -f "$skill/SKILL.md" ]]; then
    echo "error: $skill/SKILL.md not found — is '$skill' a skill directory?" >&2
    exit 1
  fi

  # SKILL.md must declare a name matching the directory, or the bundle installs
  # under one name and describes itself as another.
  declared=$(awk -F': *' '/^name:/ {gsub(/"/, "", $2); print $2; exit}' "$skill/SKILL.md")
  if [[ "$declared" != "$skill" ]]; then
    echo "error: $skill/SKILL.md declares name '$declared' but lives in '$skill/'" >&2
    exit 1
  fi

  find "$skill" -name '.DS_Store' -delete
  rm -f "$skill.skill"
  # -X drops extra file attributes (uid/gid, Finder metadata) for a cleaner,
  # more reproducible archive.
  zip -q -r -X "$skill.skill" "$skill" -x '*.DS_Store' '*__pycache__*' '*.pyc'

  files=$(unzip -Z1 "$skill.skill" | grep -vc '/$' || true)
  size=$(du -h "$skill.skill" | cut -f1)
  echo "built $skill.skill — $files files, $size"
done

# The fonts' license must travel with the fonts (SIL OFL 1.1). Fail loudly if a
# build would ship them without it.
if [[ -f paper-session.skill ]]; then
  # Capture first: `... | grep -q` exits early, and under `pipefail` the SIGPIPE
  # on unzip would make this check fail even when the file is present.
  listing=$(unzip -Z1 paper-session.skill)
  if [[ "$listing" != *"assets/fonts/LICENSE-IBMPlex.txt"* ]]; then
    echo "error: paper-session.skill ships fonts without LICENSE-IBMPlex.txt" >&2
    exit 1
  fi
fi

echo "ok"
