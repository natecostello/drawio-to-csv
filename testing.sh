#!/bin/bash

set -x
# Define the directory where the Python scripts are located
script_dir="/Users/ncos/GithubRepos/drawio-visio-excel-planning"

# Add the script directory to the PATH
export PATH="$PATH:$script_dir"

# Define the input and output files
input_file="input.drawio"
final_file="final.drawio"
frontmatter_file="frontmatter.txt"

# Run the Python scripts in a pipeline, creating temporary files at each stage
#drawio_to_csv.py "$input_file" > temp1.csv
#cat temp1.csv | strip_frontmatter.py > temp2.csv
#cat temp2.csv | csv_to_xl.py > temp3.csv
#cat temp3.csv | xl_to_csv.py > temp4.csv
#cat temp4.csv | add_frontmatter.py "$frontmatter_file" > temp5.csv
#cat temp5.csv | csv_to_drawio.sh > "$final_file"

# Run the Python scripts in a pipeline, passing the output of each command directly to the next
drawio_to_csv.py "$input_file" | \
strip_frontmatter.py | \
csv_to_xl.py | \
xl_to_csv.py | \
add_frontmatter.py "$frontmatter_file" | \
csv_to_drawio.sh > "$final_file"

# Compare the original and final files
#diff "$input_file" "$final_file"