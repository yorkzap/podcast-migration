import json
import re
import subprocess

def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def update_wp_post(post_id, new_content):
    subprocess.run(['wp', 'post', 'update', str(post_id), '--post_content=' + new_content], check=True)

def get_wp_post_content(post_id):
    result = subprocess.run(['wp', 'post', 'get', str(post_id), '--field=content'], capture_output=True, text=True)
    return result.stdout.strip()

def remove_section(content, start_marker, end_marker):
    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)

    if start_index != -1 and end_index != -1:
        # Adjust end_index to include the end_marker
        end_index += len(end_marker)
        return content[:start_index] + content[end_index:]
    else:
        return None

def main():
    json_data = load_json_data('full_db.json')

    num_posts = input("Enter the number of posts to update (0 for all): ")
    num_posts = int(num_posts)

    posts_processed = 0
    string_start_marker = "<b>Find out more about me here: </b>"
    string_end_marker = "<span style=\"font-weight: 400;\">Website:</span>"
    regex_pattern = re.compile(r"<strong>Find out more about me here:.*?<span style=\"font-weight: 400;\"> </span></p>", re.DOTALL | re.IGNORECASE)

    for record in json_data:
        if num_posts != 0 and posts_processed >= num_posts:
            break

        post_id = record.get("post_id")
        if not post_id:
            continue

        original_content = get_wp_post_content(post_id)
        new_content = remove_section(original_content, string_start_marker, string_end_marker)

        if not new_content:
            new_content, num_replacements = regex_pattern.subn('', original_content)

        if new_content and new_content != original_content:
            update_wp_post(post_id, new_content)
            print(f'Updated Post ID: {post_id}')
        else:
            print(f'Section not found in Post ID: {post_id}')
            print(f'Original Content (first 500 chars): {original_content[:500]}...')

        posts_processed += 1

if __name__ == '__main__':
    main()
