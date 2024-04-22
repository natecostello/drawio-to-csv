#!/usr/bin/env python3

import csv
import sys

def rename_ids(input_stream, output_stream):
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "id" and "xl_id" columns
    id_index = headers.index("id")
    xl_id_index = headers.index("xl_id")

    # Create a dictionary to map "id" to "xl_id"
    id_to_xl_id = {}

    # Create a list to store the rows
    rows = []

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Add the mapping from "id" to "xl_id"
        id_to_xl_id[row[id_index]] = row[xl_id_index]
        # Add the row to the list of rows
        rows.append(row)

    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')
    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows again
    for row in rows:
        # Replace the "id" with the corresponding "xl_id"
        row[id_index] = id_to_xl_id[row[id_index]]

        # Replace the "next_step_id", "decision0_id", "decision1_id", and "decision2_id" with the corresponding "xl_id"
        for header in ["next_step_id", "decision0_id", "decision1_id", "decision2_id"]:
            if header in headers:
                index = headers.index(header)
                # Handle the case where the cell contains a comma-separated list of ids
                ids = row[index].split(',')
                xl_ids = [id_to_xl_id[id] for id in ids if id in id_to_xl_id]
                row[index] = ','.join(xl_ids)

        # Write the modified row to the new CSV file
        writer.writerow(row)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            rename_ids(file, sys.stdout)
    else:
        # No file specified, use stdin
        rename_ids(sys.stdin, sys.stdout)