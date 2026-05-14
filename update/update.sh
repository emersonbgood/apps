#!/bin/bash

# 1. Update the local package list
sudo apt update -qq

# 2. Extract names of upgradable packages
upgradable_pkgs=$(apt list --upgradable 2>/dev/null | grep 'upgradable' | cut -d/ -f1)

# 3. Check if any updates exist and show a pop-up for each
if [ -n "$upgradable_pkgs" ]; then
    for pkg in $upgradable_pkgs; do
        zenity --info --title="Update Available" --text="Package needs to be upgraded: $pkg" --width=300
    done
else
    echo "No updates needed."
fi

