#!/usr/bin/env bash
# Build the static Soulsolid demo.
#
# Generates a fictional library, runs a real Soulsolid instance against it,
# seeds it through the API and crawls it into a static site (default: ./dist-demo).
# Soulsolid is built from $SOULSOLID_DIR (default: .soulsolid, see
# scripts/fetch-soulsolid.sh).
#
# Requires: go, node/npm, ffmpeg, fpcalc (chromaprint), git, python3.
# Usage: [SOULSOLID_DIR=...] demo/build.sh [out_dir]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEMO="$ROOT/demo"
SRC="$(realpath -m "${SOULSOLID_DIR:-$ROOT/.soulsolid}")"
OUT="$(realpath -m "${1:-$ROOT/dist-demo}")"
PORT="${DEMO_PORT:-3939}"
BASE="http://127.0.0.1:$PORT"
WORK="$(mktemp -d -t soulsolid-demo.XXXXXX)"
PID=""

cleanup() {
  # wait reports the server's SIGTERM status (143); don't let set -e turn it into ours.
  if [[ -n "$PID" ]]; then kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null || true; fi
  rm -rf "$WORK"
}
trap cleanup EXIT

[[ -f "$SRC/go.mod" ]] || { echo "no soulsolid checkout at $SRC (run scripts/fetch-soulsolid.sh)" >&2; exit 1; }

# The server finds views/, public/ and (for plugin builds) go.mod relative to its cwd.
cd "$SRC"

echo "==> Building assets"
[[ -d node_modules ]] || npm ci
npm run build --silent

echo "==> Generating demo library in $WORK"
# Duplicates go in the download path, where queued items normally live (and can stream from).
python3 "$DEMO/gen_library.py" "$WORK/incoming" --dupes "$WORK/downloads"
mkdir -p "$WORK/music" "$WORK/logs"

# demo/config.yaml placeholders: @WORK@ (stripped from the output later) and @PORT@.
sed -e "s|@WORK@|$WORK|g" -e "s|@PORT@|$PORT|g" "$DEMO/config.yaml" >"$WORK/config.yaml"

echo "==> Starting Soulsolid on :$PORT"
go build -o "$WORK/soulsolid" ./src/main.go
IMAGE_TAG="${IMAGE_TAG:-demo}" SOULSOLID_CONFIG_PATH="$WORK/config.yaml" \
  "$WORK/soulsolid" >"$WORK/logs/server.log" 2>&1 &
PID=$!
for _ in $(seq 1 180); do
  curl -fs "$BASE/health" >/dev/null 2>&1 && break
  kill -0 "$PID" 2>/dev/null || { cat "$WORK/logs/server.log"; exit 1; }
  sleep 1
done
curl -fs "$BASE/health" >/dev/null || { echo "server did not start"; cat "$WORK/logs/server.log"; exit 1; }

echo "==> Seeding"
python3 "$DEMO/seed.py" "$BASE" "$WORK/library.db" "$WORK/incoming" "$WORK/downloads"

echo "==> Crawling into $OUT"
# Stripping $WORK makes paths read /music/..., /downloads/... in the demo.
python3 "$DEMO/crawl.py" "$BASE" "$OUT" --public "$SRC/public" --strip "$WORK"

echo "==> Done: $(find "$OUT" -type f | wc -l) files, $(du -sh "$OUT" | cut -f1)"
