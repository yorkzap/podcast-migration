#!/bin/bash

# Change directory to the WordPress installation
cd ~/www/staging17.podcast.susanmcvea.com/public_html

# Path to the file containing post IDs
POST_ID_FILE="./podcast-migration/post_ids.txt"

# Loop through each post ID in the file
while read -r post_id; do 
    # Fetch the title and permalink of the post
    title=$(wp post get "$post_id" --field=post_title)
    permalink=$(wp post get "$post_id" --field=permalink)

    # Print the post ID, title, and permalink
    echo "Post ID: $post_id"
    echo "Title: $title"
    echo "Link: $permalink"
    echo ""
done < "$POST_ID_FILE"
