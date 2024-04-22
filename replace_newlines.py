#!/usr/bin/env python3

import csv
import sys

def process_csv(input_stream, output_stream):
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Create a CSV writer
    writer = csv.writer(output_stream)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Replace newline and carriage return characters with "<b>" in each cell
        modified_row = [cell.replace('\n', '<br>').replace('\r', '<br>') for cell in row]
        # Write the modified row to the new CSV file
        writer.writerow(modified_row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            process_csv(file, sys.stdout)
    else:
        # No file specified, use stdin
        process_csv(sys.stdin, sys.stdout)