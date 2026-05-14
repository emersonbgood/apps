#!/bin/bash

# Use zenity to display a graphical input dialog box and store the result
filename=$(zenity --entry --title="Create New File" --text="Enter the desired file name:")

# Check if the user cancelled the dialog (zenity returns non-zero status)
if [ $? -eq 0 ] && [ -n "$filename" ]; then
    # Create the file on the desktop using the entered name
    touch ~/Desktop/"$filename"
    zenity --info --title="Success" --text="File '$filename' created on the desktop."
else
    zenity --warning --title="Cancelled" --text="File creation cancelled or no name entered."
fi

