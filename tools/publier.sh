#!/usr/bin/env bash
# Publie la sortie Drive d'une cohorte sur la branche « publication ».
# Le script Google Apps Script « synchroniser » la recopie ensuite dans Drive, sans action manuelle.
# Usage : tools/publier.sh [cohorte-1]
set -euo pipefail
COHORTE="${1:-cohorte-1}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/build.py" >/dev/null
W="$(mktemp -d)"
git -C "$ROOT" fetch -q origin publication
git -C "$ROOT" worktree add -q "$W" origin/publication -B publication
rm -rf "$W/drive/$COHORTE" && mkdir -p "$W/drive" && cp -r "$ROOT/out/drive/$COHORTE" "$W/drive/"
git -C "$W" add -A
git -C "$W" commit -qm "publication : $COHORTE" || echo "publier : rien de nouveau"
git -C "$W" push -q origin publication
git -C "$ROOT" worktree remove --force "$W"
echo "publier : $COHORTE publié sur la branche publication"
