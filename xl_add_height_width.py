#!/usr/bin/env python3

import csv
import sys

def insert_dimensions(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)
    shape_index = headers.index('shape')

    headers.extend(['width', 'height'])
    writer.writerow(headers)

    shape_dimensions = {
        'decision': ('100', '100'),
        'process': ('200', '100'),
        'or': ('100', '100'),
        'start_1': ('100', '100'),
        'terminator': ('100', '50'),
        'predefined_process': ('200', '100'),
        'data': ('200', '100'),
        'document': ('200', '100'),
    }

    for row in reader:
        shape = row[shape_index]
        width, height = shape_dimensions.get(shape, ('100', '100'))
        row.extend([width, height])

        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            insert_dimensions(file, sys.stdout)
    else:
        insert_dimensions(sys.stdin, sys.stdout)