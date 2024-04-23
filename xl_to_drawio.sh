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
xl_delete_non_utf8.py "$input_file" | tee data/0xl_delete_non_utf8.csv | \
xl_delete_empty_cols.py | tee data/0xl_delete_empty_cols.csv | \
xl_delete_empty_rows.py | tee data/1xl_delete_empty_rows.csv | \
xl_rename_headers.py | tee data/2xl_rename_headers.csv | \
xl_fix_shape_case.py | tee data/3xl_fix_shape_case.csv | \
xl_fix_status_case.py | tee data/4xl_fix_status_case.csv | \
xl_replace_newlines.py | tee data/5xl_replace_newlines.csv | \
xl_save_id.py | tee data/6xl_save_id.csv | \
#xl_to_csv.py | tee data/xl_to_csv.csv| \
xl_rename_shapes.py | tee data/7xl_rename_shapes.csv| \
xl_add_height_width.py | tee data/8xl_add_height_width.csv | \
xl_parse_decisions.py | tee data/9xl_parse_decisions.csv | \
# end of functionality that was xl_to_csv.py
csv_add_frontmatter.py "$frontmatter_file" | \
csv_to_drawio.sh > "$output_file"