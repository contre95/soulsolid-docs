#!/usr/bin/env bash
# Put a soulsolid checkout at .soulsolid/, which the docs (Hugo mounts) and the
# demo (demo/build.sh) are built from.
#
#   SOULSOLID_DIR=../soulsolid scripts/fetch-soulsolid.sh   # symlink a local working copy
#   SOULSOLID_REF=v0.28.2 scripts/fetch-soulsolid.sh        # clone a specific tag/branch
#   scripts/fetch-soulsolid.sh                              # clone the latest release tag
#
# The resolved ref is written to .soulsolid-ref.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="${SOULSOLID_REPO:-https://github.com/contre95/soulsolid}"
DEST="$ROOT/.soulsolid"

rm -rf "$DEST"

if [[ -n "${SOULSOLID_DIR:-}" ]]; then
  src="$(realpath "$SOULSOLID_DIR")"
  ln -s "$src" "$DEST"
  ref="$(git -C "$src" describe --tags --always --dirty 2>/dev/null || echo local)"
  echo "Linked $src as .soulsolid ($ref)"
else
  ref="${SOULSOLID_REF:-}"
  if [[ -z "$ref" ]]; then
    # Release tags only (vX.Y.Z), newest first.
    ref="$(git ls-remote --tags --refs --sort=-v:refname "$REPO" 'v*' |
      sed 's|.*refs/tags/||' | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -1)"
    [[ -n "$ref" ]] || { echo "no release tag found in $REPO" >&2; exit 1; }
  fi
  git clone --quiet --depth 1 --branch "$ref" "$REPO" "$DEST"
  echo "Cloned $REPO at $ref into .soulsolid"
fi

echo "$ref" >"$ROOT/.soulsolid-ref"
