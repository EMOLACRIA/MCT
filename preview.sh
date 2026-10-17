#!/usr/bin/env bash
set -euo pipefail
package_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec quickshell -p "$package_dir/payload/style/shell/preview.qml"
