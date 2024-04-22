#!/usr/bin/env python3

import csv
import sys

def process_csv(input_stream, output_stream):
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')

    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "Shape Type" column
    shape_type_index = headers.index("Shape Type")

    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Convert the "Shape Type" cell to lowercase
        row[shape_type_index] = row[shape_type_index].lower()
        # Write the modified row to the new CSV file
        writer.writerow(row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            process_csv(file, sys.stdout)
    else:
        # No file specified, use stdin
        process_csv(sys.stdin, sys.stdout)