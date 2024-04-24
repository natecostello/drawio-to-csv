#!/usr/bin/env python3

import csv
import sys

def remove_dimensions(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)
    height_index = headers.index('height')
    width_index = headers.index('width')
    
    # Remove the height and width from the headers without using index
    headers.remove('height')
    headers.remove('width')

    writer.writerow(headers)

    for row in reader:
        # Delete the height and width from the row but account for the fact that the indices 
        # will change and we don't know which index is where
        if height_index > width_index:
            del row[height_index]
            del row[width_index]
        else:
            del row[width_index]
            del row[height_index]

        
        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            remove_dimensions(file, sys.stdout)
    else:
        remove_dimensions(sys.stdin, sys.stdout)