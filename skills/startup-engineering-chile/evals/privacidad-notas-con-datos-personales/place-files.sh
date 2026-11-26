#!/usr/bin/env bash
set -eu
CASO="$(cd "$(dirname "$0")" && pwd)"
for PY in python3 python; do "$PY" -c "import sys" >/dev/null 2>&1 && break; done
"$PY" "$CASO/../../../../tools/armar_fixture.py" "$CASO" "$PWD"
