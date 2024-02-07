import json
import subprocess

# Load JSON data
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Update WordPress post
def update_wp_post(post_id, tags):
    try:
        # Ensure tags are comma-separated without new lines or extra spaces
        formatted_tags = ','.join(tag.strip() for tag in tags.split(','))
        update_tags_command = f"wp post term set {post_id} post_tag {formatted_tags}"
        result = subprocess.run(update_tags_command, shell=True, check=True, capture_output=True, text=True)
        print(f"Success: Set term for post ID {post_id} with tags: {formatted_tags}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update post ID {post_id}: {e}")

# Get episode range from user
def get_episode_range():
    range_input = input("Enter episode range (e.g., 15-25): ")
    start, end = map(int, range_input.split('-'))
    return start, end

# Main function
def main():
    start_episode, end_episode = get_episode_range()
    print(f"Ok, updating episodes from {start_episode} to {end_episode}.")

    json_data = load_json_data('updated_db.json')  # Replace with your actual JSON file name
    for entry in json_data:
        episode_number = int(entry.get("episode_number", 0))
        if start_episode <= episode_number <= end_episode:
            post_id = entry.get("post_id")
            tags = entry.get("tags", "")
            if post_id and tags:
                update_wp_post(post_id, tags)

    print("Update process completed.")

if __name__ == "__main__":
    main()
