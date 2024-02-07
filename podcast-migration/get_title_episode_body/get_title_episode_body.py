import json
import subprocess
import re
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_wordpress_post_info(post_id):
    try:
        title_output = subprocess.check_output(f"wp post get {post_id} --field=title", shell=True)
        title = title_output.decode().strip()

        body_output = subprocess.check_output(f"wp post get {post_id} --field=content", shell=True)
        body = strip_tags(body_output.decode().strip())

        return title, body
    except subprocess.CalledProcessError as e:
        print(f"  Error: Could not fetch post info for ID {post_id}. {e}")
        return None, None

def extract_episode_number_and_title(title):
    pattern = r'Episode (\d+):?\s*(.+)'
    match = re.match(pattern, title, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2).strip()
    else:
        print(f"  Debug: No match found for pattern '{pattern}' in title '{title}'")
        return None, None

def titles_similar(json_title, extracted_title):
    # Normalize the titles by removing punctuation, converting to lower case and stripping leading '- '
    normalize = lambda t: re.sub(r'^[-\s]+', '', re.sub(r'[^\w\s]', '', t)).lower()
    return normalize(json_title) == normalize(extracted_title)

def print_divider():
    print("-" * 50)

def main():
    try:
        with open('../matched_data.json', 'r') as file:
            data_list = json.load(file)
    except FileNotFoundError:
        print("Error: matched_data.json file not found.")
        return
    except json.JSONDecodeError:
        print("Error: JSON format error in matched_data.json.")
        return

    try:
        num_entries = int(input("Enter the number of entries to process (0 for all): "))
        if num_entries == 0:
            num_entries = len(data_list)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    updated_data_list = []
    successful_updates = 0
    unsuccessful_updates = 0

    for index, data in enumerate(data_list[:num_entries]):
        post_id = data.get('post_id')
        print_divider()
        print(f"Processing post ID: {post_id}")

        if post_id:
            wp_title, wp_body = get_wordpress_post_info(post_id)
            if wp_title and wp_body:
                print(f"  WordPress Title: {wp_title}")
                print(f"  WordPress Body (Preview): {wp_body[:200]}...")

                episode_number, separated_title = extract_episode_number_and_title(wp_title)
                json_title = data.get('title')
                print(f"  JSON Title: {json_title}")
                print(f"  Extracted Episode Number: {episode_number}")
                print(f"  Separated Title: {separated_title}")

                data['full_wordpress_title'] = wp_title
                data['episode_number'] = episode_number if episode_number else "Not Found"
                data['full_wordpress_body'] = wp_body

                title_match = titles_similar(json_title, separated_title)
                data['title_match_discrepancy'] = not title_match

                if title_match:
                    successful_updates += 1
                else:
                    unsuccessful_updates += 1
                    print(f"  Title Discrepancy: JSON Title - '{json_title}', Extracted Title - '{separated_title}'")

                print(f"  Title Match Discrepancy: {data['title_match_discrepancy']}")
                updated_data_list.append(data)
            else:
                print("  Could not retrieve post info.")
        else:
            print("  Post ID not found in JSON item.")

    with open('db.json', 'w') as outfile:
        json.dump(updated_data_list, outfile, indent=4)

    print_divider()
    print("\nData updated and saved to db.json")
    print(f"Total Entries Processed: {num_entries}")
    print(f"Successful Updates (No Discrepancy): {successful_updates}")
    print(f"Unsuccessful Updates (Discrepancy Found): {unsuccessful_updates}")

if __name__ == "__main__":
    main()
