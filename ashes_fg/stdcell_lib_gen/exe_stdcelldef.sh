#!/bin/bash

# 1. Ask for the folder path
read -p "Enter the GDS file path to convert them to std cell defs (e.g., ./data or /home/user/files): " folder

# 2. Ask for the extension
read -p "Enter extension (e.g., txt): " ext

# 3. Loop through files in THAT specific folder
# We use "${folder%/}/" to ensure there isn't a double slash //
for file in "${folder%/}"/*."$ext"; do
    echo "Processing: $file"
    # This runs the python script using the full path to the file
    python3 ./../gds_to_celldef/gen_stdcell_defs.py "$file" -json ./cells.json -pydef ./cells.py -pn 22 -foundry gfN

    echo "Finished $file"
    echo "----------------"
done
