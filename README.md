# Podcast Migration
This repository contains scripts to automate the generation of summaries for posts and their updates to a WordPress website. Additionally, it includes WordPress-related files and themes for integration with the scripts.


## Scripts

### 1. Update WordPress Post Script (`update_wordpress_post.py`)

This script updates WordPress posts with summaries fetched from a JSON file.

#### Dependencies
- `json`: for handling JSON data.
- `subprocess`: for running shell commands.
  
#### Functionality
- Reads data from a JSON file containing post details.
- Updates WordPress posts with corresponding summaries.
- Handles special characters in summaries.
- Allows skipping of posts with empty summaries.

### 2. Generate Summary Script (`generate_summary.py`)

This script generates summaries for posts using the OpenAI GPT model.

#### Dependencies
- `openpyxl`: for working with Excel files.
- `requests`: for making HTTP requests.
- `time`: for adding delays.
- `logging`: for logging messages.
- `json`: for handling JSON data.

#### Configuration
- `MAX_POSTS`: Maximum number of posts to process.
- `MAX_INPUT_TOKENS`: Maximum number of tokens for input data.
- `SLEEP_DURATION`: Duration to wait between API requests.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `FILE_PATH`: Path to the input Excel file.
- `NEW_FILE_PATH`: Path to the output Excel file.

#### Functionality
- Reads data from an Excel file.
- Generates summaries using the OpenAI GPT model.
- Writes summaries to a new Excel file.
- Supports different columns for data input.

### 3. Update WordPress Post Script 2 (`update_wp_post.py`)

This script updates WordPress posts with summaries fetched from a JSON file.

#### Dependencies
- `json`: for handling JSON data.
- `subprocess`: for running shell commands.

#### Functionality
- Prompts the user to enter the number of iterations.
- Updates WordPress posts with corresponding summaries.
- Handles special characters in summaries.
- Allows skipping of posts with empty summaries.

## Usage

To use these scripts, follow the run each python or shell file with their dependencies. Ensure that you have the necessary dependencies installed and configured correctly.
