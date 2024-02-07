#!/bin/bash

# Define the CSV file to store the results
CSV_FILE="/home/u100-emjg4pwrmcun/www/staging17.podcast.susanmcvea.com/public_html/podcast-migration/post_details.csv"
TEMP_FILE="/home/u100-emjg4pwrmcun/www/staging17.podcast.susanmcvea.com/public_html/podcast-migration/temp_post_details.csv"

# Change directory to the WordPress installation
cd ~/www/staging17.podcast.susanmcvea.com/public_html
echo "Changed directory to $(pwd)"

# Fetch all post IDs including all types and statuses
post_ids=$(wp post list --post_type=any --post_status=any --format=ids --posts_per_page=-1)

# Create a temporary file and add headers
echo "Post ID,Title,Link,Libsyn Iframe" > "$TEMP_FILE"

# Initialize the iterator
iteration=0

# Loop through each post ID
for post_id in $post_ids; do 
    ((iteration++))
    echo "Processing iteration $iteration: Post ID $post_id"

    # Fetch the title, permalink, and content of the post
    title=$(wp post get "$post_id" --field=post_title)
    permalink=$(wp post list --post__in="$post_id" --post_type=post --field=url)
    content=$(wp post get "$post_id" --field=content --skip-plugins --skip-themes)

    # Extract the Libsyn iframe (either format)
    libsyn_iframe=$(echo "$content" | grep -o -E '<iframe[^>]*src="(//html5-player.libsyn.com/embed/episode/id/[^>]*|https://play.libsyn.com/embed/episode/id/[^>]*height/192[^>]*)></iframe>')

    # Handle posts without Libsyn iframes
    if [ -z "$libsyn_iframe" ]; then
        echo "No Libsyn Iframe found for Post ID $post_id. Including post with empty iframe field..."
        libsyn_iframe="N/A" # Or use any placeholder you prefer
        echo "Iteration $iteration: Post ID $post_id - Unmatched Link"
    else
        libsyn_iframe=$(echo "$libsyn_iframe" | sed 's/"/""/g')
        echo "Iteration $iteration: Post ID $post_id - Matched Link"
    fi

    # Print details being written to CSV file
    echo "Details for iteration $iteration: Post ID $post_id"
    echo "Title: $title"
    echo "Link: $permalink"
    echo "Libsyn Iframe: $libsyn_iframe"

    # Append the post details to the temporary file
    echo "$post_id,\"$title\",\"$permalink\",\"$libsyn_iframe\"" >> "$TEMP_FILE"
done

# Move the temporary file to the final CSV file
mv "$TEMP_FILE" "$CSV_FILE"
echo "Data written to $CSV_FILE"

echo "Script execution completed."
