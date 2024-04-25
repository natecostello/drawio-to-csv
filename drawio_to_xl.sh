#!/bin/bash

# Check if the correct number of arguments were provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

# Assign the arguments to variables
input_file="$1"
output_file="$2"

# Run the Python scripts in a pipeline, passing the output of each command directly to the next
drawio_to_csv.py -i "$input_file" frontmatter.txt | \
csv_strip_frontmatter.py | \
csv_delete_height_width.py | \
csv_rename_ids.py | \
csv_strip_xl_ids.py | \
csv_rename_shapes.py | \
csv_parse_decisions.py | \
csv_insert_newlines.py | \
csv_rename_headers.py | \
csv_reorder_headers.py > "$output_file"