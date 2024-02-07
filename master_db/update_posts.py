import json
import subprocess

def escape_special_characters(text):
    if text is None:
        return ''
    # Replace single quotes with an escaped version and handle other special characters as needed
    return text.replace("'", "'\\''")

def update_wordpress_post(post_id, gpt_summary):
    print(f"Starting update for post ID {post_id}...")

    if not gpt_summary.strip():
        print(f"Skipped update for post ID {post_id} as gpt_summary is empty.")
        return

    gpt_summary_escaped = escape_special_characters(gpt_summary)

    update_podcast_summary_cmd = f"wp post meta update {post_id} podcast_summary '{gpt_summary_escaped}'"
    print(f"Executing command for podcast_summary: {update_podcast_summary_cmd}")

    try:
        result = subprocess.run(update_podcast_summary_cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"podcast_summary updated for post ID {post_id}. Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update podcast_summary for post ID {post_id}. Error: {e.stderr}")

with open('full_db.json', 'r') as file:
    data = json.load(file)

post_data_mapping = {str(post['post_id']): post for post in data}

post_ids_to_process = [
    875, 638, 632, 769, 1100, 391, 881, 895, 1116, 1224, 835, 736, 352, 1108, 
    751, 689, 1358, 949, 411, 760, 934, 915, 888, 849, 842, 651, 812, 921, 726, 
    659, 1279, 342, 682, 861, 855, 744, 1339, 902, 928, 672, 1157, 626, 782, 
    776, 790, 909, 1165, 799, 1195, 665, 1340, 1273, 712, 1186, 943, 1321, 1350, 
    819, 806, 869, 1380, 825, 1215, 319, 369, 312, 377, 316, 324, 360, 365, 328, 
    332, 396, 348, 384, 337
]

for post_id in post_ids_to_process:
    post_id_str = str(post_id)
    if post_id_str in post_data_mapping:
        post_data = post_data_mapping[post_id_str]
        gpt_summary = post_data.get('gpt_summary', '')
        update_wordpress_post(post_id, gpt_summary)
    else:
        print(f"No data found for post ID {post_id}. Skipping...")

print("Completed processing specified posts.")
