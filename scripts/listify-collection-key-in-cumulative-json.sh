#!/bin/bash

# Check if an input directory argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_directory>"
    exit 1
fi

INPUT_DIR="$1"
# Define the output file in the directory where the script is executed
OUTPUT_FILE="$(pwd)/media-objects.html"

# 1. cd into directory
cd "$INPUT_DIR" || { echo "Error: Cannot cd into $INPUT_DIR"; exit 1; }

# Enable nullglob to safely check if the JSON files exist before running jq
shopt -s nullglob
json_files=(*cumulative.json)
if [ ${#json_files[@]} -eq 0 ]; then
    echo "Error: No *cumulative.json files found in $INPUT_DIR"
    exit 1
fi

# 2. set molist to output from: jq -r '.collection_key' *cumulative.json
molist=$(jq -r '.collection_key' "${json_files[@]}")

# 3. insert "<ul>" to return file
echo "<ul>" > "$OUTPUT_FILE"

# 4. for each member of molist, add "<li>" + molist item + "</li>"
# We use a while read loop to safely handle keys that might contain spaces
while IFS= read -r item; do
    # Only add non-empty lines
    if [ -n "$item" ]; then
        echo "  <li>$item</li>" >> "$OUTPUT_FILE"
    fi
done <<< "$molist"

# 5. insert "</ul>" to return file
echo "</ul>" >> "$OUTPUT_FILE"

# 6. return file (print the path to the user)
echo "Success! File generated at: $OUTPUT_FILE"

