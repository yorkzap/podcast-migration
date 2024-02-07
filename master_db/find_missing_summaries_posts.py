import json
import subprocess

def update_custom_field(post_id, field_name, field_value):
    """ Update a custom field value using WP-CLI. """
    try:
        subprocess.check_output(
            ['wp', 'post', 'meta', 'update', str(post_id), field_name, field_value],
            stderr=subprocess.STDOUT,  # Capture standard error in the output
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        return e.output

def process_posts(file_path, num_posts):
    with open(file_path, 'r') as file:
        data = json.load(file)

    count = 0
    skipped_posts = []

    for item in data:
        if num_posts != 0 and count >= num_posts:
            break

        post_id = item.get('post_id')
        gpt_summary = item.get('gpt_summary')

        if not post_id or not gpt_summary:
            skipped_posts.append((post_id, 'Missing post_id or gpt_summary'))
            continue

        result = update_custom_field(post_id, 'podcast_body', gpt_summary)

        if result is True:
            count += 1
            print(f"Updated post {post_id} successfully.")
        else:
            skipped_posts.append((post_id, result))

    print(f"Processed {count} posts.")
    if skipped_posts:
        print("Posts not updated due to errors:")
        for post_id, error in skipped_posts:
            print(f"Post ID {post_id}: {error}")

# Main execution
file_path = 'full_db.json'  # Replace with your actual file path
try:
    num_posts = int(input("Enter the number of posts to process (0 for all): "))
    process_posts(file_path, num_posts)
except ValueError:
    print("Invalid input. Please enter a valid number.")
