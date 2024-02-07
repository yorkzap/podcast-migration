import json
import subprocess
import re

# Set your desired widths here
ID_WIDTH = 10
TITLE_WIDTH = 50
STATUS_WIDTH = 10
MESSAGE_WIDTH = 20

def fetch_current_content(post_id):
    command = ['wp', 'post', 'get', post_id, '--field=content', '--skip-plugins', '--skip-themes']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None

def update_post(post_id, updated_content):
    command = ['wp', 'post', 'update', post_id, '--post_content=' + updated_content, '--skip-plugins', '--skip-themes']
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0

def reformat_iframe(iframe_content):
    # Simply remove backslashes, no alteration to the src attribute
    new_content = iframe_content.replace('\\', '')  # Remove backslashes
    return new_content



def replace_libsyn_iframe(current_content, libsyn_iframe, redcircle_iframe):
    libsyn_iframe_pattern = re.escape(libsyn_iframe)
    updated_content = re.sub(libsyn_iframe_pattern, redcircle_iframe, current_content, flags=re.DOTALL)
    return updated_content

def verify_update(post_id, redcircle_iframe):
    updated_content = fetch_current_content(post_id)
    return redcircle_iframe in updated_content

def log_undone(post_id):
    with open('undone.log', 'a') as log_file:
        log_file.write(f'{post_id}\n')

def print_summary(results):
    success_count = sum(result['status'] == 'Success' for result in results)
    print("\nUpdate Summary:\n")
    print("{:<5} {:<{id_width}} {:<{title_width}} {:<{status_width}} {:<{message_width}}".format(
        'No.', 'Post ID', 'Title', 'Status', 'Message', id_width=ID_WIDTH, title_width=TITLE_WIDTH, status_width=STATUS_WIDTH, message_width=MESSAGE_WIDTH))
    print('-' * (5 + ID_WIDTH + TITLE_WIDTH + STATUS_WIDTH + MESSAGE_WIDTH + 4))  # Adjust for spaces between columns
    
    for index, result in enumerate(results, start=1):
        print("{:<5} {:<{id_width}} {:<{title_width}} {:<{status_width}} {:<{message_width}}".format(
            index, result['post_id'], result['title'], result['status'], result['message'], id_width=ID_WIDTH, title_width=TITLE_WIDTH, status_width=STATUS_WIDTH, message_width=MESSAGE_WIDTH))
    
    print(f"\nTotal posts updated: {success_count} out of {len(results)} processed")

def main():
    try:
        max_process = int(input("Enter the number of posts to update (0 for all posts): "))
    except ValueError:
        print("Please enter a valid number.")
        return

    results = []
    print("Starting post update process...\n", flush=True)

    with open('matched_data.json', 'r') as file:
        posts = json.load(file)

    if max_process == 0:
        max_process = len(posts)

    for count, post in enumerate(posts, start=1):
        if max_process != 0 and count > max_process:
            print(f"Reached the requested number of processed posts: {max_process}. Stopping.", flush=True)
            break

        post_id = post.get('post_id')
        title = post.get('title', 'No Title')
        redcircle_iframe = post.get('redcircle_iframe', '')
        libsyn_iframe = post.get('libsyn_iframe', '')

        current_content = fetch_current_content(post_id)
        if current_content is None:
            print(f"Failed to fetch content for post {post_id}.", flush=True)
            results.append({'post_id': post_id, 'title': title, 'status': 'Failed', 'message': 'Failed to fetch content'})
            continue

        formatted_iframe = reformat_iframe(redcircle_iframe)

        # Perform the replacement
        updated_content = replace_libsyn_iframe(current_content, libsyn_iframe, formatted_iframe)

        print(f"Updating Post {count}/{'∞' if max_process == 0 else max_process}: '{title}' (ID: {post_id})", flush=True)
        if update_post(post_id, updated_content):
            # Verify the update
            if verify_update(post_id, formatted_iframe):
                results.append({'post_id': post_id, 'title': title, 'status': 'Success', 'message': 'Updated successfully'})
                print("Success!", flush=True)
            else:
                results.append({'post_id': post_id, 'title': title, 'status': 'Failed', 'message': 'Verification failed'})
                print("Verification failed.", flush=True)
                log_undone(post_id)
        else:
            results.append({'post_id': post_id, 'title': title, 'status': 'Failed', 'message': 'Update failed'})
            print("Failed to update.", flush=True)

    print_summary(results)
    print("\nOperation complete.", flush=True)

if __name__ == "__main__":
    main()
