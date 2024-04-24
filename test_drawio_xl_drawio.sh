#!/bin/bash

# Check if the correct number of arguments were provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

# Assign the arguments to variables
input_file="$1"
output_file="$2"

# Create a temporary file for the intermediate output
intermediate_file=$(mktemp)

# Run drawio_to_xl.sh on the input file
./drawio_to_xl.sh "$input_file" "$intermediate_file"

# Run xl_to_drawio.sh on the intermediate file
./xl_to_drawio.sh "$intermediate_file" "$output_file"

# Delete the intermediate file
rm "$intermediate_file"