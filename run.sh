#!/usr/bin/env bash
# Backup & IRE Discovery Tool — single-command launcher (macOS / Linux)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

PYTHON="${PYTHON:-python3}"

if [ ! -d ".venv" ]; then
  echo "[setup] creating local virtualenv (.venv)…"
  "$PYTHON" -m venv .venv
  . .venv/bin/activate
  pip install --quiet --upgrade pip
  pip install --quiet -r requirements.txt
else
  . .venv/bin/activate
fi

if [ ! -f "data/seed.json" ]; then
  echo "[setup] ingesting source artifacts…"
  python ingest.py
fi

exec python app.py "$@"
