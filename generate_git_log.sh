#!/bin/bash

# Author to filter commits for
AUTHOR="psmardz"

# Output file
OUTPUT_FILE="git_activity.csv"

# Write the header for the CSV file
echo "Date,Activity/Task" > "$OUTPUT_FILE"

# Extract relevant information from git log
git log --author="$AUTHOR" --pretty=format:"%cd,%s" --date=format:'%Y-%m-%d %H:%M:%S' >> "$OUTPUT_FILE"

# Print a success message
echo "Activity log saved to $OUTPUT_FILE. Open it in Google Sheets for further use."

