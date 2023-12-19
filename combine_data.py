import csv
import json
import re
from collections import Counter

def read_csv(file_path):
    """Reads a CSV file and returns a list of dictionaries."""
    data = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_json(file_path, data):
    """Writes a list of dictionaries to a JSON file."""
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def clean_title(title):
    """Cleans the title for comparison."""
    title = re.sub(r'^(Episode\s+\d+[:\s-]+\s+)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[^\w\s]', '', title).lower()
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def jaccard_similarity(str1, str2):
    """Calculate the Jaccard Similarity between two strings."""
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

# File paths
redcircle_file = 'get_redcircle_data/updated_data_redcircle.csv'
wordpress_file = 'get_wordpress_data/post_details.csv'
matched_file = 'matched_data.json'
unmatched_file = 'unmatched_data.json'

# Read CSV files
redcircle_data = read_csv(redcircle_file)
wordpress_data = read_csv(wordpress_file)

# Match and combine data
matched_data = []
unmatched_data = []

# Similarity threshold
similarity_threshold = 0.6

# Set to keep track of matched WordPress Post IDs
matched_wordpress_ids = set()

# Check RedCircle entries against WordPress
for redcircle_row in redcircle_data:
    redcircle_title_cleaned = clean_title(redcircle_row['title'])
    match_found = False

    for wordpress_row in wordpress_data:
        wordpress_title_cleaned = clean_title(wordpress_row['Title'])
        similarity = jaccard_similarity(redcircle_title_cleaned, wordpress_title_cleaned)
        
        if similarity >= similarity_threshold and wordpress_row['Post ID'] not in matched_wordpress_ids:
            combined_row = {
                'title': redcircle_row['title'],  # Original title from RedCircle
                'published_on': redcircle_row['published_on'],
                'post_id': wordpress_row['Post ID'],
                'redcircle_iframe': redcircle_row['iframe'],
                'libsyn_iframe': wordpress_row['Libsyn Iframe']
            }
            matched_data.append(combined_row)
            matched_wordpress_ids.add(wordpress_row['Post ID'])
            match_found = True
            break

    if not match_found:
        unmatched_data.append({'Title': redcircle_row['title'], 'Link': redcircle_row['link'], 'Source': 'RedCircle'})

# Check WordPress entries against RedCircle for unmatched
for wordpress_row in wordpress_data:
    if wordpress_row['Post ID'] not in matched_wordpress_ids:
        unmatched_data.append({'Title': wordpress_row['Title'], 'Post ID': wordpress_row['Post ID'], 'Source': 'WordPress'})

# Write the matched data to a new JSON file
write_json(matched_file, matched_data)
# Write the unmatched data to another JSON file
write_json(unmatched_file, unmatched_data)

print(f"Total RedCircle entries processed: {len(redcircle_data)}")
print(f"Total WordPress entries processed: {len(wordpress_data)}")
print(f"Found matches: {len(matched_data)}")
print(f"Unmatched entries: {len(unmatched_data)}")
