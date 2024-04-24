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
        # Transform 'shape' and corresponding 'description'
        if row[shape_index] == "start_1":
            row[shape_index] = "start"
        elif row[shape_index] == "terminator":
            row[shape_index] = "end"
        elif row[shape_index] == "summing_function":
            row[shape_index] = "process"
            row[description_index] = "OR"
        elif row[shape_index] == "or":
            row[shape_index] = "process"
            row[description_index] = "AND"
        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            rename_shapes(file, sys.stdout)
    else:
        rename_shapes(sys.stdin, sys.stdout)