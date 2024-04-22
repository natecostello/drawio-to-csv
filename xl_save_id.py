#!/usr/bin/env python3

import csv
import sys

def process_csv(input_stream, output_stream):
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "Process Step ID" column
    process_step_id_index = headers.index("Process Step ID")

    # Add the new "xl_id" header
    headers.append("xl_id")

    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')
    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Copy the value from "Process Step ID" to "xl_id"
        row.append(row[process_step_id_index])
        # Write the modified row to the new CSV file
        writer.writerow(row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            process_csv(file, sys.stdout)
    else:
        # No file specified, use stdin
        process_csv(sys.stdin, sys.stdout)