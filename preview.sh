#!/usr/bin/env bash
set -euo pipefail
package_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if (($#)); then
    exec python3 "$package_dir/theme_preview.py" "$@"
fi
exec quickshell -p "$package_dir/payload/style/shell/preview.qml"
