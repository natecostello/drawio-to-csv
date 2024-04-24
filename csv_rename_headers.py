#!/usr/bin/env python3

import csv
import sys

def rename_headers(input_stream, output_stream):

    fixed_headers = ['id', 'shape', 'connector_label', 'next_step_id']

    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)

    # for all headers not in fixed_headers, replace underscores with spaces and capitalize the first letter of each word
    headers = [header.replace('_', ' ').title() if header not in fixed_headers else header for header in headers]
    
    # rename fixed headers
    headers[headers.index('id')] = 'Process Step ID'
    headers[headers.index('shape')] = 'Shape Type'
    headers[headers.index('connector_label')] = 'Connector Label'
    headers[headers.index('next_step_id')] = 'Next Step ID'
    
    writer.writerow(headers)

    for row in reader:
        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            rename_headers(file, sys.stdout)
    else:
        rename_headers(sys.stdin, sys.stdout)