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
drawio_to_csv.py "$input_file" | \
strip_frontmatter.py | \
csv_to_xl.py > "$output_file"