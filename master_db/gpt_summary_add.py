import json
import subprocess

def get_number_of_iterations():
    while True:
        try:
            number = input("Enter the number of iterations to process (0 for all): ")
            number = int(number)
            if number >= 0:
                return number
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input, please enter a number.")

def update_wp_post(post_id, summary):
    # Escape single quotes in the summary
    summary = summary.replace("'", "'\\''")
    
    # Check if the "podcast_summary" field is empty
    check_cmd = f"wp post meta get {post_id} podcast_summary --skip-plugins --skip-themes"
    check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)

    if check_result.stdout.strip() == '':
        # Update the "podcast_summary" field if it's empty
        update_cmd = f"wp post meta update {post_id} podcast_summary '{summary}' --skip-plugins --skip-themes"
        subprocess.run(update_cmd, shell=True)
        print(f"Updated post {post_id} with new summary.")
    else:
        print(f"Post {post_id} already has a summary, skipping.")

# Load JSON data
with open('full_db_final.json', 'r') as file:
    data = json.load(file)

num_iterations = get_number_of_iterations()
processed = 0

for item in data:
    if processed == num_iterations:
        break

    post_id = item.get("post_id")
    summary = item.get("gpt_summary")

    if summary:
        print(f"Processing post {post_id}...")
        update_wp_post(post_id, summary)
        processed += 1
    else:
        print(f"No summary for post {post_id}, skipping.")

print("Finished processing posts.")
