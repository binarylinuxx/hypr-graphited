#!/bin/bash

desktop_file="$1"

if [ -z "$desktop_file" ]; then
    echo "No desktop file specified"
    exit 1
fi

# Try to find the desktop file
if [ -f "$desktop_file" ]; then
    gtk-launch "$(basename "$desktop_file")"
elif [ -f "/usr/share/applications/$desktop_file" ]; then
    gtk-launch "$desktop_file"
elif [ -f "$HOME/.local/share/applications/$desktop_file" ]; then
    gtk-launch "$desktop_file"
else
    # Fallback to just executing the command if desktop file not found
    app_name=$(echo "$desktop_file" | cut -d. -f1)
    $app_name &
fi
