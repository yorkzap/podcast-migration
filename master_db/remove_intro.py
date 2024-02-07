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

def main():
    json_data = load_json_data('full_db.json')

    num_posts = input("Enter the number of posts to update (0 for all): ")
    num_posts = int(num_posts)

    posts_processed = 0
    for record in json_data:
        if num_posts != 0 and posts_processed >= num_posts:
            break

        post_id = record.get("post_id")
        if not post_id:
            continue

        original_content = get_wp_post_content(post_id)
        # Regex to match the script tag
        script_tag_pattern = re.compile(r'<script async defer onload=".*?</script>', re.IGNORECASE | re.DOTALL)
        # Regex to match "<b>Biggest Takeaways:</b>" with variations
        takeaway_pattern = re.compile(r'<b>Biggest Takeaways:\s*</b>', re.IGNORECASE)

        script_tag_match = list(script_tag_pattern.finditer(original_content))
        takeaway_match = takeaway_pattern.search(original_content)

        if takeaway_match and script_tag_match:
            last_script_tag = script_tag_match[-1]
            new_content_start = max(last_script_tag.end(), takeaway_match.start())
            new_content = original_content[new_content_start:]

            # Ensure shortcodes are not removed
            shortcode_pattern = re.compile(r'\[et_pb_[^\]]*\]')
            shortcodes = shortcode_pattern.findall(original_content[:new_content_start])
            new_content = ''.join(shortcodes) + new_content

            update_wp_post(post_id, new_content)
            print(f'Updated Post ID: {post_id}')
        else:
            print(f'Pattern not found in Post ID: {post_id}')

        posts_processed += 1

if __name__ == '__main__':
    main()
