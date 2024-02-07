import json
import openpyxl

def get_number_of_posts():
    while True:
        try:
            number = input("Enter the number of posts to process (0 for all): ")
            number = int(number)
            if number >= 0:
                return number
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input, please enter a number.")

# Load JSON data
with open('full_db.json', 'r') as file:
    data = json.load(file)

# Load Excel data
wb = openpyxl.load_workbook('database.xlsx')
sheet = wb.active

# Function to find the human_post content for an episode number
def find_human_post_for_episode(episode_number):
    for row in range(2, sheet.max_row + 1):  # Assuming the first row is the header
        excel_episode_number = sheet['H' + str(row)].value
        # Convert float to int then to string for comparison
        if excel_episode_number is not None:
            excel_episode_number = str(int(excel_episode_number)).strip()

        if excel_episode_number == str(episode_number).strip():
            return sheet['N' + str(row)].value
    return None

# Get the number of posts to process
num_posts = get_number_of_posts()

# Update JSON data
for index, item in enumerate(data):
    if num_posts != 0 and index >= num_posts:
        break

    episode_number = item.get('episode_number')
    if item.get('human_post') is None:
        human_post_content = find_human_post_for_episode(episode_number)
        if human_post_content:
            item['human_post'] = human_post_content
            print(f"Updated episode {episode_number} with human_post: {human_post_content[:30]}...")  # Debugging information

# Save updated JSON data
with open('full_db_final.json', 'w') as file:
    json.dump(data, file, indent=4)

print("JSON file updated successfully.")
