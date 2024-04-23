#!/usr/bin/env python3

import csv
import sys

def delete_empty_rows(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    for row in reader:
        # Check if the row is not empty
        if any(field.strip() for field in row):
            writer.writerow(row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            delete_empty_rows(file, sys.stdout)
    else:
        # No file specified, use stdin
        delete_empty_rows(sys.stdin, sys.stdout)