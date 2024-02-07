import json
import subprocess

def update_post(post_id, iframe_link, episode, title):
    # Update the iframe link in ACF
    subprocess.run(["wp", "post", "meta", "update", post_id, "iframe_link", iframe_link])

    # Update the episode number in ACF
    subprocess.run(["wp", "post", "meta", "update", post_id, "episode", episode])

    # Update the title in ACF
    subprocess.run(["wp", "post", "meta", "update", post_id, "title", title])

def main():
    # Load JSON data from db.json
    with open('db.json', 'r') as file:
        data = json.load(file)

    # Ask the user for the number of entries they want to process
    try:
        num_entries = int(input("Enter the number of entries to process (0 for all): "))
        if num_entries == 0:
            num_entries = len(data)  # Set to total number of entries if 0 is entered
    except ValueError:
        print("Please enter a valid number.")
        return

    # Ensure the number of entries does not exceed the data length
    num_entries = min(num_entries, len(data))

    # Iterate over the specified number of entries and update the posts
    for i in range(num_entries):
        entry = data[i]
        post_id = entry.get("post_id")
        iframe_link = entry.get("redcircle_iframe")  # Or the appropriate iframe link field
        episode = entry.get("episode_number")
        title = entry.get("title")

        if post_id and iframe_link and episode and title:
            update_post(post_id, iframe_link, episode, title)
            print(f"Updated post {post_id} with title '{title}', episode number {episode}, and iframe link.")

if __name__ == "__main__":
    main()
