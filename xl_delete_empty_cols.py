#!/usr/bin/env python3

import csv
import sys

def delete_empty_cols(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)
    indices = [i for i, h in enumerate(headers) if h]

    # Write the non-empty headers to the output
    writer.writerow([headers[i] for i in indices])

    for row in reader:
        writer.writerow([row[i] for i in indices])

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            delete_empty_cols(file, sys.stdout)
    else:
        # No file specified, use stdin
        delete_empty_cols(sys.stdin, sys.stdout)