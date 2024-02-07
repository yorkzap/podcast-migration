import json
import subprocess

def check_acf_fields(post_id, field_name, empty_fields_list):
    command = f"wp post meta get {post_id} {field_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        empty_fields_list.append(post_id)

# Load JSON data
with open('full_db.json', 'r') as file:
    data = json.load(file)

empty_post_body_posts = []
empty_podcast_summary_posts = []

# Check ACF fields for each WordPress post
for item in data:
    post_id = item.get('post_id')
    if post_id:
        check_acf_fields(post_id, 'post_body', empty_post_body_posts)
        check_acf_fields(post_id, 'podcast_summary', empty_podcast_summary_posts)

# Print the results
if empty_post_body_posts:
    print("Posts with empty 'post_body' field:", empty_post_body_posts)
else:
    print("No posts with empty 'post_body' field found.")

if empty_podcast_summary_posts:
    print("Posts with empty 'podcast_summary' field:", empty_podcast_summary_posts)
else:
    print("No posts with empty 'podcast_summary' field found.")

print("Completed checking posts.")
