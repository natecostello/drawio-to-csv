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
drawio_to_csv_flex.py -i "$input_file" frontmatter.txt | tee data/0drawio_to_csv_flex.csv | \
csv_strip_frontmatter.py | tee data/1csv_strip_frontmattery.csv | \
csv_delete_height_width.py | tee data/2csv_delete_height_width.csv | \
csv_rename_ids.py | tee data/3csv_rename_ids.csv | \
csv_strip_xl_ids.py | tee data/4csv_strip_xl_ids.csv | \
csv_rename_shapes.py | tee data/5csv_rename_shapes.csv | \
csv_parse_decisions.py | tee data/6csv_parse_decisions.csv | \
csv_insert_newlines.py | tee data/7csv_insert_newlines.csv | \
csv_rename_headers.py | tee data/8csv_rename_headers.csv | \
csv_reorder_headers.py > "$output_file"
#csv_rename_headers.py > "$output_file"

#csv_to_xl.py > "$output_file"