#!/bin/bash

# Check if the correct number of arguments were provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

# Assign the arguments to variables
input_file="$1"
output_file="$2"
frontmatter_file="frontmatter.txt"

# Run the Python scripts in a pipeline, passing the output of each command directly to the next
xl_fix_shape_case.py "$input_file" | \
xl_fix_status_case.py | \
xl_replace_newlines.py | \
xl_save_id.py | \
xl_to_csv.py | \
add_frontmatter.py "$frontmatter_file" | \
csv_to_drawio.sh > "$output_file"