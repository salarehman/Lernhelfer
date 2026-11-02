#!/usr/bin/env bash
# Kurzform für den Build: ./bau.sh [--offen|--nur-theorie|--nur-loesungen]
set -euo pipefail
exec python3 "$(dirname "$0")/werkzeuge/build.py" "$@"
