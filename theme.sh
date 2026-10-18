#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "menu" ]]; then
    shift
    exec python3 "$(dirname -- "$(readlink -f -- "$0")")/theme_picker.py" menu "$@"
fi
exec python3 "$(dirname -- "$(readlink -f -- "$0")")/theme_core.py" "$@"
