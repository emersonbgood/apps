#!/bin/bash

# 1. Setup
DEST_DIR="$HOME/Desktop/scripts"
mkdir -p "$DEST_DIR"
COMMAND_LIST=()
COUNT=0

# 2. Main Builder Loop
while true; do
    # Simple list is more stable on Pi 500
    ADD_TYPE=$(zenity --list --title="Zenity Master Builder" \
        --column="Feature" \
        "Text Entry" "Password" "Calendar" "File Picker" "Color Picker" \
        "Scale (Slider)" "Question Box" "Notification" "FINISH" \
        --width=350 --height=450 2>/dev/null)

    [[ -z "$ADD_TYPE" || "$ADD_TYPE" == "FINISH" ]] && break

    LABEL=$(zenity --entry --title="Label" --text="Question/Label for $ADD_TYPE:" 2>/dev/null)
    [[ -z "$LABEL" ]] && continue

    # 3. Store the correct standalone command for each feature
    case "$ADD_TYPE" in
        "Text Entry")    COMMAND_LIST+=("zenity --entry --text='$LABEL'") ;;
        "Password")      COMMAND_LIST+=("zenity --password --text='$LABEL'") ;;
        "Calendar")      COMMAND_LIST+=("zenity --calendar --text='$LABEL'") ;;
        "File Picker")   COMMAND_LIST+=("zenity --file-selection --title='$LABEL'") ;;
        "Color Picker")  COMMAND_LIST+=("zenity --color-selection --title='$LABEL'") ;;
        "Scale (Slider)") COMMAND_LIST+=("zenity --scale --text='$LABEL'") ;;
        "Question Box")  COMMAND_LIST+=("zenity --question --text='$LABEL'") ;;
        "Notification")  COMMAND_LIST+=("zenity --notification --text='$LABEL'") ;;
    esac
    
    ((COUNT++))
done

# 4. Save and Generate
[[ $COUNT -eq 0 ]] && exit 1

FILE_NAME=$(zenity --entry --title="Save" --text="Filename:" 2>/dev/null)
[[ -z "$FILE_NAME" ]] && FILE_NAME="my_pi_tool"

DEST_PATH="$DEST_DIR/${FILE_NAME}.sh"

# Create a bash script instead of a .desktop for better stability
{
    echo "#!/bin/bash"
    for cmd in "${COMMAND_LIST[@]}"; do
        echo "$cmd 2>/dev/null"
    done
    echo "zenity --info --text='All tasks complete!' 2>/dev/null"
} > "$DEST_PATH"

chmod +x "$DEST_PATH"

# 5. Create a desktop launcher that points to the new script
cat <<EOF > "$DEST_DIR/${FILE_NAME}.desktop"
[Desktop Entry]
Name=$FILE_NAME
Type=Application
Exec=$DEST_PATH
Icon=system-run
Terminal=false
EOF

chmod +x "$DEST_DIR/${FILE_NAME}.desktop"
zenity --info --text="Created $COUNT-step script at:\n$DEST_PATH" 2>/dev/null
