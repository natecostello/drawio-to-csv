#!/usr/bin/env python3

import csv
import sys

def parse_decisions(input_stream, output_stream):
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream)

    headers = next(reader)
    shape_index = headers.index('shape')
    next_step_id_index = headers.index('next_step_id')
    connector_label_index = headers.index('connector_label')

    headers.extend(['decision0_id', 'decision0_label', 'decision1_id', 'decision1_label', 'decision2_id', 'decision2_label'])
    writer.writerow(headers)

    for row in reader:
        if row[shape_index] == "decision":
            decision_ids = row[next_step_id_index].split(',')
            decision_labels = row[connector_label_index].split(',')
            decision_fields = list(zip(decision_ids + [None]*3, decision_labels + [None]*3))[:3]
            row[next_step_id_index] = ""
        else:
            decision_fields = [(None, None)] * 3

        row.extend([item for sublist in decision_fields for item in sublist])

        writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            parse_decisions(file, sys.stdout)
    else:
        parse_decisions(sys.stdin, sys.stdout)