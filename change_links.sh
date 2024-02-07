#!/bin/bash

CSV_FILE="matched_data.csv"
SUCCESS_FILE="changed_links.json"
FAIL_FILE="failed_links.json"
MAX_PROCESS=5
COUNT=0

echo "[" > "$SUCCESS_FILE"
echo "[" > "$FAIL_FILE"

{
    read  # skip header line
    while IFS= read -r line; do
        # Extract post_id from the line
        post_id=$(echo "$line" | cut -d ',' -f3 | tr -d '"')
        # Read next lines to get the iframes
        IFS= read -r redcircle_iframe
        IFS= read -r libsyn_iframe
        # Read additional lines till the next record
        while IFS= read -r next_line && [[ ! $next_line =~ ^[^,]+,[^,]+,[^,]+ ]]; do
            redcircle_iframe+=$'\n'"$next_line"
        done

        ((++COUNT > MAX_PROCESS)) && break

        # Fetch current post content
        current_content=$(wp post get "$post_id" --field=content --skip-plugins --skip-themes)

        # Replace Libsyn iframe with RedCircle iframe
        updated_content=${current_content//$libsyn_iframe/$redcircle_iframe}

        # Update the post
        if wp post update "$post_id" --post_content="$updated_content" --skip-plugins --skip-themes; then
            echo "{\"post_id\": \"$post_id\", \"status\": \"success\"}," >> "$SUCCESS_FILE"
            echo "Updated post $post_id successfully."
        else
            echo "{\"post_id\": \"$post_id\", \"status\": \"failed\"}," >> "$FAIL_FILE"
            echo "Failed to update post $post_id."
        fi

        unset IFS
    done
} < "$CSV_FILE"

# Finalize JSON files
sed -i '$ s/,$//' "$SUCCESS_FILE"  # Remove trailing comma
echo "]" >> "$SUCCESS_FILE"
sed -i '$ s/,$//' "$FAIL_FILE"
echo "]" >> "$FAIL_FILE"

echo "Operation complete."
