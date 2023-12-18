import json

# Load your JSON data from a file
with open('./data_redcircle.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Base URL for the iframe source
base_url = "https://api.podcache.net/embedded-player/sh/"

# Initialize a list to store the updated JSON data
updated_data = []

# Iterate through the JSON data and add the "iframe" field
for entry in data:
    episode_id = entry["link"].split("/")[-1]

    iframe_html = (
        f'<script async defer onload="redcircleIframe();" src="{base_url}{episode_id}/ep/{episode_id}"></script>\n'
        f'<div class="redcirclePlayer-{episode_id}"></div>\n'
        '<style>\n'
        '.redcircle-link:link {\n'
        '    color: #ea404d;\n'
        '    text-decoration: none;\n'
        '}\n'
        '.redcircle-link:hover {\n'
        '    color: #ea404d;\n'
        '}\n'
        '.redcircle-link:active {\n'
        '    color: #ea404d;\n'
        '}\n'
        '.redcircle-link:visited {\n'
        '    color: #ea404d;\n'
        '}\n'
        '</style>\n'
        '<p style="margin-top:3px;margin-left:11px;font-family: sans-serif;font-size: 10px; color: gray;">'
        'Powered by <a class="redcircle-link" href="https://redcircle.com?utm_source=rc_embedded_player&utm_medium=web&utm_campaign=embedded_v1">RedCircle</a></p>'
    )

    entry["iframe"] = iframe_html
    updated_data.append(entry)

# Print the updated JSON data
print(json.dumps(updated_data, indent=4))

# Write the updated JSON data to a file
with open('./updated_data_redcircle.json', 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, indent=4)
