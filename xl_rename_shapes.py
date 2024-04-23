#!/usr/bin/env python3

import csv
import sys

def rename_shapes(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)
    shape_index = headers.index('shape')
    description_index = headers.index('description')

    writer.writerow(headers)

    for row in reader:
        if row[shape_index] == "process" and row[description_index] == "AND":
            row[shape_index] = "or"
            row[description_index] = ""
        elif row[shape_index] == "process" and row[description_index] == "OR":
            row[shape_index] = "summing_function"
            row[description_index] = ""
        elif row[shape_index] == "end":
            row[shape_index] = "terminator"
        elif row[shape_index] == "start":
            row[shape_index] = "start_1"
        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            rename_shapes(file, sys.stdout)
    else:
        rename_shapes(sys.stdin, sys.stdout)