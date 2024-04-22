#!/usr/bin/env python3

import csv
import sys

def strip_xl_id(input_stream, output_stream):
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "xl_id" column
    xl_id_index = headers.index("xl_id")

    # Remove the "xl_id" header
    headers.pop(xl_id_index)

    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')
    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Remove the "xl_id" cell
        row.pop(xl_id_index)
        # Write the modified row to the new CSV file
        writer.writerow(row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            strip_xl_id(file, sys.stdout)
    else:
        # No file specified, use stdin
        strip_xl_id(sys.stdin, sys.stdout)