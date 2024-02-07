import os
import shlex
import re

# Function to replace the src URL in the iframe_link ACF field
def replace_src_in_acf(post_id, new_src):
    # Use shlex to properly escape the content within the command
    wp_cli_command = f'wp post meta update {post_id} iframe_link {shlex.quote(new_src)}'
    os.system(wp_cli_command)

# Function to iterate through posts with "iframe_link" ACF field and update iframe src
def process_posts(num_posts):
    # Get a list of post IDs with "iframe_link" ACF field content
    acf_query = 'wp post list --fields=ID --format=ids --meta_key=iframe_link --meta_compare=EXISTS'
    post_ids = os.popen(acf_query).read().strip().split()

    # If num_posts is 0, process all posts; otherwise, process a specified number of posts
    if num_posts == 0:
        num_posts = len(post_ids)

    # Define the old src pattern for the "iframe_link" ACF field
    old_src_pattern = r'https://api\.podcache\.net/embedded-player/sh/([^\s/]+)/ep/([^\s"]+)'

    # Define the base of the new src URL structure
    new_src_base = 'https://api.podcache.net/embedded-player/sh/edb1ac3c-440b-4633-ace3-4abc3b29eb9e/ep/'

    # Initialize counters
    total_posts = len(post_ids)
    successful_updates = 0
    unsuccessful_updates = 0

    for post_id in post_ids[:num_posts]:
        # Get the current content of the "iframe_link" ACF field without specifying 'format'
        wp_cli_command_get = f'wp post meta get {post_id} iframe_link'
        acf_content_before = os.popen(wp_cli_command_get).read().strip()

        # Extract the episode identifier from the old src URL
        match = re.search(old_src_pattern, acf_content_before)
        if match:
            episode_id = match.group(2)
            new_src = new_src_base + episode_id

            # Replace the old src URLs in the ACF field with the new src URL
            updated_acf_content = re.sub(old_src_pattern, new_src, acf_content_before)

            # Update the content of the "iframe_link" ACF field with the new URL
            replace_src_in_acf(post_id, updated_acf_content)

            # Increment successful update count
            successful_updates += 1
        else:
            # Increment unsuccessful update count
            unsuccessful_updates += 1

    # Print the results
    print(f"Total Posts Processed: {total_posts}")
    print(f"Successful Updates: {successful_updates}")
    print(f"Unsuccessful Updates: {unsuccessful_updates}")

if __name__ == '__main__':
    num_posts = int(input("Enter the number of posts to process (0 for all): "))
    process_posts(num_posts)
