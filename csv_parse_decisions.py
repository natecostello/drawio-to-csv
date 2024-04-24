#!/usr/bin/env python3

import csv
import sys
import io

def parse_decisions(input_stream, output_stream):
    # first pass
    reader = csv.reader(input_stream)
    intermediate = io.StringIO()
    writer = csv.writer(intermediate)

    headers = next(reader)
    shape_index = headers.index('shape')
    next_step_id_index = headers.index('next_step_id')
    decision0_id_index = headers.index('decision0_id')
    decision0_label_index = headers.index('decision0_label')
    decision1_id_index = headers.index('decision1_id')
    decision1_label_index = headers.index('decision1_label')
    decision2_id_index = headers.index('decision2_id')
    decision2_label_index = headers.index('decision2_label')

    # Remove the decision-specific fields
    # headers.remove('decision0_id')
    # headers.remove('decision0_label')
    # headers.remove('decision1_id')
    # headers.remove('decision1_label')
    # headers.remove('decision2_id')
    # headers.remove('decision2_label')

    # Add the connector_label field
    headers.append('connector_label')
    connector_label_index = headers.index('connector_label')
    
    writer.writerow(headers)
    

    for row in reader:
        # Append the connector_label field to the row
        row.append('')
        # Handle decision-specific fields
        if row[shape_index] == "decision":
            decision_ids = [row[decision0_id_index], row[decision1_id_index], row[decision2_id_index]]
            decision_labels = [row[decision0_label_index], row[decision1_label_index], row[decision2_label_index]]
            row[next_step_id_index] = ', '.join(filter(None, decision_ids))
            row[connector_label_index] = ', '.join(filter(None, decision_labels))
        else:
            row[connector_label_index] = ''

        # Delete the decision-specific fields
        # del row[decision0_id_index]
        # del row[decision0_label_index]
        # del row[decision1_id_index]
        # del row[decision1_label_index]
        # del row[decision2_id_index]
        # del row[decision2_label_index]

        writer.writerow(row)
    
    # second pass
    intermediate.seek(0)
    reader = csv.reader(intermediate)
    writer = csv.writer(output_stream)
    headers = next(reader)

    decision0_id_index = headers.index('decision0_id')
    decision0_label_index = headers.index('decision0_label')
    decision1_id_index = headers.index('decision1_id')
    decision1_label_index = headers.index('decision1_label')
    decision2_id_index = headers.index('decision2_id')
    decision2_label_index = headers.index('decision2_label')

    # Remove the decision-specific fields
    headers.remove('decision0_id')
    headers.remove('decision0_label')
    headers.remove('decision1_id')
    headers.remove('decision1_label')
    headers.remove('decision2_id')
    headers.remove('decision2_label')

    writer.writerow(headers)

    for row in reader:
        # Delete the decision-specific fields in reverse order of their indices
        del row[decision2_label_index]
        del row[decision2_id_index]
        del row[decision1_label_index]
        del row[decision1_id_index]
        del row[decision0_label_index]
        del row[decision0_id_index]

        writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            parse_decisions(file, sys.stdout)
    else:
        parse_decisions(sys.stdin, sys.stdout)