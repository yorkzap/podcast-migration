import json
import openpyxl

JSON_DB_PATH = './output.json'  # Path to your JSON file
EXCEL_DB_PATH = './database.xlsx'  # Path to your Excel file
OUTPUT_JSON_PATH = './updated_db.json'  # Path for the output JSON file

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def load_excel_data(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    excel_data = {}
    for row in sheet.iter_rows(min_row=2):
        episode_num = row[7].value  # Assuming episode number is in column H
        tags = row[15].value  # Assuming tags are in column P
        if episode_num is not None and tags is not None:
            # Convert float to int then to string for matching
            episode_num_str = str(int(episode_num))
            excel_data[episode_num_str] = str(tags).strip()
    return excel_data

def update_json_with_tags(json_data, excel_data):
    matched = 0
    for item in json_data:
        episode_num = str(item.get('episode_number', '')).strip()
        if episode_num in excel_data:
            item['tags'] = excel_data[episode_num]
            matched += 1
    print(f'Matched tags for {matched} episodes.')
    return json_data

def write_json_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    json_data = load_json_data(JSON_DB_PATH)
    excel_data = load_excel_data(EXCEL_DB_PATH)
    updated_json_data = update_json_with_tags(json_data, excel_data)
    write_json_data(OUTPUT_JSON_PATH, updated_json_data)
    print(f'Updated JSON data written to {OUTPUT_JSON_PATH}')

if __name__ == "__main__":
    main()
