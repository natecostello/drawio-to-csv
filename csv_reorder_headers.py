#!/usr/bin/env python3

import csv
import sys

def reorder_headers(input_stream, output_stream):

    header_order = ["Process Step ID","Owner","Description","Status","Function","Phase","Estimated Duration","Estimated Completion Date","Notes","Wbs","Oqe","Next Step ID","Shape Type","Connector Label"]

    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    # reorder the headers and row elements to match the header_order list
    original_headers = next(reader)
    ordered_headers = [header for header in header_order if header in original_headers]
    remaining_headers = [header for header in original_headers if header not in header_order]
    headers = ordered_headers + remaining_headers

    writer.writerow(headers)

    # reorder the row elements to match the header_order list
    for row in reader:
        row_dict = dict(zip(original_headers, row))
        row = [row_dict[header] for header in headers]
        writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            reorder_headers(file, sys.stdout)
    else:
        reorder_headers(sys.stdin, sys.stdout)



