#!/usr/bin/env python3

import csv
import sys

# Function to process each row of the CSV based on the specified rules
def process_csv(input_file):
    output_data = []
    reader = csv.reader(input_file)
    
    for row in reader:
        # skip rows that begin with #
        if row[0].startswith('#'):
            continue

        # skip the header row by checking the first element of the row is 'id' ingoring case
        if row[0].lower() == 'id':
            continue

        # Unpack the row into variables for clarity and easier handling
        id, owner, description, status, function, phase, estimated_duration, \
        estimated_completion_date, notes, wbs, oqe, next_step_id, shape, \
        width, height, decision0_id, decision0_label, decision1_id, \
        decision1_label, decision2_id, decision2_label = row

        # Transform 'shape' and corresponding 'description'
        if shape == "start_1":
            shape = "start"
        elif shape == "terminator":
            shape = "end"
        elif shape == "summing_function":
            shape = "process"
            description = "AND"
        elif shape == "or":
            shape = "process"
            description = "OR"

        # Handle decision-specific fields
        if shape == "decision":
            decision_ids = [decision0_id, decision1_id, decision2_id]
            decision_labels = [decision0_label, decision1_label, decision2_label]
            next_step_id = ', '.join(filter(None, decision_ids))
            connector_label = ', '.join(filter(None, decision_labels))
        else:
            connector_label = ''

        # Compile the transformed row
        output_row = [
            id, owner, description, status, function, phase,
            estimated_duration, estimated_completion_date, notes,
            wbs, oqe, next_step_id, shape, connector_label
        ]
        output_data.append(output_row)

    return output_data

# Function to write the processed data to a CSV file
def write_output_to_csv(output_data, output_file):
    writer = csv.writer(output_file)
    # Write the header
    writer.writerow(['Process Step ID', 'Owner', 'Description', 'Status', 'Function', 'Phase',
                     'Estimated Duration', 'Estimated Completion Date', 'Notes',
                     'WBS', 'OQE', 'Next Step ID', 'Shape Type', 'Connector Label'])
    # Write the data
    writer.writerows(output_data)

def main(argv):
    if len(argv) > 2:
        print('Usage: csv_to_xl.py [<path_to_your_drawio_file.csv>]')
        return
    elif len(argv) == 2:
        input_path = argv[1]
        processed_data = process_csv(input_path)
    else:
        processed_data = process_csv(sys.stdin)
    
    write_output_to_csv(processed_data, sys.stdout)

if __name__ == '__main__':
    import sys
    main(sys.argv)