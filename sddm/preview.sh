#!/usr/bin/env bash
set -euo pipefail
package_path=$(dirname "$(readlink -f "$0")")
if command -v sddm-greeter-qt6 >/dev/null; then
    greeter=sddm-greeter-qt6
elif command -v sddm-greeter >/dev/null && ldd "$(command -v sddm-greeter)" | rg -q 'libQt6'; then
    greeter=sddm-greeter
else
    echo 'A Qt6 SDDM greeter is required. Check pacman -Q sddm qt6-declarative.' >&2
    exit 1
fi
preview_help=$("$greeter" --help 2>&1) || {
    printf '%s\n' "$preview_help" >&2
    exit 1
}
legacy_test_pattern='(^|[[:space:]])--test([[:space:],=]|$)'
if [[ "$preview_help" == *"--test-mode"* ]]; then
    preview_option=--test-mode
elif [[ "$preview_help" =~ $legacy_test_pattern ]]; then
    preview_option=--test
else
    echo 'This greeter does not advertise a supported test option. Run sddm-greeter-qt6 --help.' >&2
    exit 1
fi
exec "$greeter" "$preview_option" --theme "$package_path/theme"
