#!/usr/bin/env python3

import csv
import sys

def insert_newlines(input_stream, output_stream):
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Create a CSV writer
    writer = csv.writer(output_stream)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Replace "<b>" with newline characters in each cell
        modified_row = [cell.replace('<br>', '\n') for cell in row]

        # Write the modified row to the new CSV file
        writer.writerow(modified_row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            insert_newlines(file, sys.stdout)
    else:
        # No file specified, use stdin
        insert_newlines(sys.stdin, sys.stdout)