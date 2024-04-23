#!/usr/bin/env python3

"""
Takes a CSV file or piped CSV file, checks for the required input headers, 
and renames them as follows (the format below is Input Required Header, Renamed Header):
Process Step ID,id
Owner,owner
Description,description
Status,status
Next Step ID,next_step_id
Shape Type,shape
Connector Label,connector_label
"""


import csv
import sys

def rename_headers(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)
    header_mapping = {
        'Process Step ID': 'id',
        'Owner': 'owner',
        'Description': 'description',
        'Status': 'status',
        'Next Step ID': 'next_step_id',
        'Shape Type': 'shape',
        'Connector Label': 'connector_label',
    }

    new_headers = [header_mapping.get(header, header) for header in headers]
    writer.writerow(new_headers)

    for row in reader:
        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            rename_headers(file, sys.stdout)
    else:
        rename_headers(sys.stdin, sys.stdout)