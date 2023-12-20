import json
import subprocess

JSON_FILE = 'matched_data.json'
MAX_PROCESS = 5

def reformat_iframe(iframe_content):
    # Add the missing part to the iframe src URL
    new_content = iframe_content.replace('/embedded-player/sh/', '/embedded-player/sh/edb1ac3c-440b-4633-ace3-4abc3b29eb9e/ep/')
    # Remove unnecessary escape characters for quotes
    new_content = new_content.replace('\\"', '"')
    return new_content

def update_post(post_id, new_content):
    command = ['wp', 'post', 'update', post_id, '--post_content=' + new_content, '--skip-plugins', '--skip-themes']
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("Starting post update process...")

    with open(JSON_FILE, 'r') as file:
        posts = json.load(file)

    for count, post in enumerate(posts, start=1):
        if count > MAX_PROCESS:
            print(f"Reached maximum of {MAX_PROCESS} processed posts. Stopping.")
            break

        post_id = post.get('post_id')
        redcircle_iframe = post.get('redcircle_iframe', '')

        formatted_iframe = reformat_iframe(redcircle_iframe)

        print(f"\nProcessing Post {count}:")
        print(f"Post ID: {post_id}")
        print("Formatted iframe content:")
        print(formatted_iframe)

        if update_post(post_id, formatted_iframe):
            print(f"Successfully updated post {post_id}.")
        else:
            print(f"Failed to update post {post_id}.")

    print("\nOperation complete.")

if __name__ == "__main__":
    main()
