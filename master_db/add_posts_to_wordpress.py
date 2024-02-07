import json
import subprocess
import logging

# Configuration
JSON_DB_PATH = './output.json'

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to load JSON data: {e}")
        return None

def update_wordpress_post(post_id, title, episode_number, human_post_html, gpt_summary):
    try:
        # Update 'post_body' field with HTML content
        subprocess.run(['wp', 'post', 'meta', 'update', str(post_id), 'post_body', human_post_html], check=True)

        # Check if gpt_summary is not None before updating
        if gpt_summary is not None:
            subprocess.run(['wp', 'post', 'meta', 'update', str(post_id), 'podcast_summary', gpt_summary], check=True)
        else:
            logging.warning(f"Skipped updating summary for Post ID {post_id} as gpt_summary is None")
        
        print(f"\nUpdated Post ID: {post_id}")
        print(f"Title: {title}")
        print(f"Episode Number: {episode_number}")
        if gpt_summary:
            print("Summary Added:\n" + gpt_summary)
        print("-------------------------------------------------\n")

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to update post ID {post_id}: {e}")

def main():
    json_data = load_json_data(JSON_DB_PATH)
    if not json_data:
        return

    num_entries = input("Enter the number of entries to update (0 for all): ")
    num_entries = int(num_entries)

    skipped_entries_titles = []

    if num_entries == 0:
        num_entries = len(json_data)

    for entry in json_data[:num_entries]:
        if 'human_post_html' in entry and entry['human_post_html']:
            update_wordpress_post(entry['post_id'], entry['title'], entry['episode_number'], entry['human_post_html'], entry['gpt_summary'])
        else:
            skipped_entries_titles.append(entry['title'])

    if skipped_entries_titles:
        print("\nSkipped Entries Titles:")
        for title in skipped_entries_titles:
            print(title)

if __name__ == "__main__":
    main()
