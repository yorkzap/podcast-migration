import json
import markdown2
from bs4 import BeautifulSoup

def convert_markdown_to_html(markdown_text):
    # Convert Markdown to HTML
    html = markdown2.markdown(markdown_text)
    return html

def add_blog_structure_to_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Add custom classes to headers
    for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        header['class'] = header.name + '-class'

    # Add custom classes to paragraphs
    for paragraph in soup.find_all('p'):
        paragraph['class'] = 'paragraph-class'

    return str(soup)

def process_json_file(json_file, num_entries):
    with open(json_file, 'r') as file:
        data = json.load(file)
        processed_count = 0
        missing_posts = []

        for entry in data:
            if 'human_post' in entry and entry['human_post'] is not None:
                markdown_content = entry['human_post']
                html_content = convert_markdown_to_html(markdown_content)
                html_content = add_blog_structure_to_html(html_content)
                entry['human_post_html'] = html_content
                processed_count += 1
            else:
                if 'title' in entry:
                    missing_posts.append(entry['title'])
                else:
                    missing_posts.append("Unknown Title")

            if num_entries != 0 and processed_count >= num_entries:
                break

        return data, missing_posts

def save_json_file(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# User input for the number of entries to process
num_entries = int(input("Enter the number of entries to process (0 for all): "))

# File paths (can be modified as needed)
input_json_file = 'db_new.json'  # Replace with your JSON file path
output_json_file = 'output.json'  # Replace with your desired output file path

print(f"Processing {num_entries if num_entries != 0 else 'all'} entries...")
processed_data, missing_posts = process_json_file(input_json_file, num_entries)
print("Conversion completed.")

if missing_posts:
    print("Entries with missing 'human_post' field:")
    for title in missing_posts:
        print(title)

save_json_file(processed_data, output_json_file)
print(f"Data saved to {output_json_file}")
