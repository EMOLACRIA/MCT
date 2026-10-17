#!/usr/bin/env bash
set -euo pipefail
style_path="$HOME/.config/desktop-style"
choice=$(printf '%s\n' 'Network' 'Audio' 'Notification history' 'Session' | wofi --dmenu --conf "$style_path/wofi/config" --style "$style_path/wofi/style.css" --prompt Settings --cache-file /dev/null) || exit 0
case "$choice" in
    Network) command -v nm-connection-editor >/dev/null && exec nm-connection-editor ;;
    Audio) command -v pavucontrol >/dev/null && exec pavucontrol ;;
    'Notification history') exec dunstctl history-pop ;;
    Session) exec bash "$style_path/scripts/power.sh" ;;
esac
