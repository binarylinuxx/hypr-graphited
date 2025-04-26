#!/bin/bash

# Config
MAX_LENGTH=50

# Get metadata
artist=$(playerctl metadata artist 2>/dev/null)
title=$(playerctl metadata title 2>/dev/null)
status=$(playerctl status 2>/dev/null)

if [[ "$status" == "Playing" ]]; then
    icon=""
elif [[ "$status" == "Paused" ]]; then
    icon=""
else
    echo '{"text": "", "tooltip": "No media playing"}'
    exit 0
fi

# Fallback text
artist=${artist:-Unknown Artist}
title=${title:-Unknown Title}
full_text="$icon $artist - $title"

# Truncate if necessary
if [ ${#full_text} -gt $MAX_LENGTH ]; then
    short_text="${full_text:0:$MAX_LENGTH}…"
else
    short_text="$full_text"
fi

# Output
echo "{\"text\": \"$short_text\", \"tooltip\": \"$artist - $title\"}"
