#!/bin/bash

echo "Configuring ASHES environment variables..."

# Define the target file
BASHRC="$HOME/.bashrc"

# Define the exact export commands (using single quotes so $USER evaluates at runtime)
ASHES_CMD="export ASHESPATH=/home/$USER/ashes"
RASP_CMD="export RASPPATH=/home/$USER/ashes/rasp30"

# Check and append ASHESPATH
if grep -q "export ASHESPATH=" "$BASHRC"; then
    echo " -> ASHESPATH is already configured in $BASHRC. Skipping."
else
    echo "$ASHES_CMD" >> "$BASHRC"
    echo " -> Added ASHESPATH to $BASHRC."
fi

# Check and append RASPPATH
if grep -q "export RASPPATH=" "$BASHRC"; then
    echo " -> RASPPATH is already configured in $BASHRC. Skipping."
else
    echo "$RASP_CMD" >> "$BASHRC"
    echo " -> Added RASPPATH to $BASHRC."
fi

echo ""
echo "Configuration complete! To apply these changes immediately, run:"
echo "source ~/.bashrc"
