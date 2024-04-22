#!/usr/bin/env python3
import csv
import sys

# Define shape dimensions
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

# Function to reverse process each row of the output CSV to reconstruct the original input format
def reverse_process_csv(input_file):
    input_data = []
    reader = csv.reader(input_file)
    next(reader)  # Skip header row

    for row in reader:
        if len(row) < 14:  # Ensure row has sufficient data
            continue

        id, owner, description, status, function, phase, \
        estimated_duration, estimated_completion_date, notes, \
        wbs, oqe, next_step_id, shape, connector_label, xl_id = row

        if shape == "start":
            shape = "start_1"
        elif shape == "end":
            shape = "terminator"
        elif shape == "process" and description == "AND":
            shape = "summing_function"
            description = ""
        elif shape == "process" and description == "OR":
            shape = "or"
            description = ""

        width, height = shape_dimensions.get(shape, ('100', '100'))

        if shape in ["decision"]:
            decision_ids = next_step_id.split(', ')
            decision_labels = connector_label.split(', ')
            decision_fields = list(zip(decision_ids + [None]*3, decision_labels + [None]*3))[:3]
            next_step_id = ""
        else:
            decision_fields = [(None, None)] * 3

        input_row = [
            id, owner, description, status, function, phase,
            estimated_duration, estimated_completion_date, notes,
            wbs, oqe, next_step_id, shape, width, height
        ] + [item for sublist in decision_fields for item in sublist] + [xl_id]

        input_data.append(input_row)

    return input_data

# Function to write the reversed data to a CSV file
def write_output_to_csv(output_data, output_file):
    writer = csv.writer(output_file)
    
    writer.writerow(['id', 'owner', 'description', 'status', 'function', 'phase',
                     'estimated_duration', 'estimated_completion_date', 'notes',
                     'wbs', 'oqe', 'next_step_id', 'shape', 'width', 'height',
                     'decision0_id', 'decision0_label', 'decision1_id', 'decision1_label', 
                     'decision2_id', 'decision2_label', 'xl_id'])
    
    writer.writerows(output_data)

# Function to convert the input CSV file to the output CSV file
def convertToDrawioCSV(input_file, output_file):
    processed_data = reverse_process_csv(input_file)
    write_output_to_csv(processed_data, output_file)

def main(argv):
    if len(argv) > 2:
        print('Usage: xl_to_csv.py [<path_to_your_input_file.csv>]\n'
              'If no input file is provided, the script will read from standard input.\n'
              'The output will be written to standard output.')
        return
    elif len(argv) == 2:
        with open(argv[1], 'r') as input_file:
            convertToDrawioCSV(input_file, sys.stdout)
    else:
        convertToDrawioCSV(sys.stdin, sys.stdout)

# Run the main function
if __name__ == "__main__":
    import sys
    main(sys.argv)