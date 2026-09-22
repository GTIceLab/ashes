#!/bin/bash

# 1. Ask for the folder path
read -p "Enter the GDS file path to add direction notation to their pins (e.g., ./data or /home/user/files): " folder

# 2. Ask for the extension
read -p "Enter extension (e.g., txt): " ext

# 3. Loop through files in THAT specific folder
# We use "${folder%/}/" to ensure there isn't a double slash //
for file in "${folder%/}"/*."$ext"; do
    echo "Processing: $file"
    # This runs the python script using the full path to the file
     python3 fix_gds.py -o ../gds/ "$file"

    echo "Finished $file"
    echo "----------------"
done
