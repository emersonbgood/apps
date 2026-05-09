#!/bin/bash

FOLDER_TO_MONITOR="/home/emersonberry/.local/share/Trash/files" # Match the folder in trash.sh
TRASH_SCRIPT="/home/emersonberry/trash.sh" # Point to your main script

echo "Starting monitoring of $FOLDER_TO_MONITOR..."

# Loop forever, waiting for file events (create, delete, modify, etc.)
while inotifywait -e modify,create,delete,move "$FOLDER_TO_MONITOR"; do
    # When an event happens, execute the main script
    bash "$TRASH_SCRIPT"
done

