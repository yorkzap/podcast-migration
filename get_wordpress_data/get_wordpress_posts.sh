#!/bin/bash

# Path to the file containing post IDs
POST_ID_FILE="posts_id.txt"

# Store the original directory
ORIGINAL_DIR=$(pwd)
echo "Original Directory: $ORIGINAL_DIR" # Debug line

# JSON file to store the results
JSON_FILE="$ORIGINAL_DIR/post_details.json"
echo "Writing to $JSON_FILE" # Debug line

# Check if POST_ID_FILE exists
if [ ! -f "$POST_ID_FILE" ]; then
    echo "Post ID file not found: $POST_ID_FILE" # Debug line
    exit 1
fi

# Start the JSON array
echo "[" > "$JSON_FILE"
if [ $? -ne 0 ]; then
    echo "Failed to write to $JSON_FILE" # Debug line
    exit 1
fi

# Variable to handle comma separation in JSON
first_entry=true

# Change directory to the WordPress installation
cd ~/www/staging17.podcast.susanmcvea.com/public_html
echo "Changed directory to $(pwd)" # Debug line

# Loop through each post ID in the file
while read -r post_id; do 
    echo "Processing Post ID: $post_id" # Debug line

    # Fetch the title and permalink of the post
    title=$(wp post get "$post_id" --field=post_title | sed 's/"/\\"/g')
    permalink=$(wp post list --post__in="$post_id" --post_type=post --field=url)

    # Add a comma before each entry after the first
    if [ "$first_entry" = true ]; then
        first_entry=false
    else
        echo "," >> "$JSON_FILE"
    fi

    # Append the post details to JSON file
    echo "{\"Post ID\": \"$post_id\", \"Title\": \"$title\", \"Link\": \"$permalink\"}" >> "$JSON_FILE"
    if [ $? -ne 0 ]; then
        echo "Failed to append data for Post ID $post_id to $JSON_FILE" # Debug line
    fi

    # Print the post ID, title, and permalink
    echo "Post ID: $post_id"
    echo "Title: $title"
    echo "Link: $permalink"
    echo ""
done < "$ORIGINAL_DIR/$POST_ID_FILE"

# End the JSON array
echo "]" >> "$JSON_FILE"
if [ $? -ne 0 ]; then
    echo "Failed to finalize $JSON_FILE" # Debug line
    exit 1
fi

echo "Script execution completed." # Debug line
