#!/usr/bin/env python3

#!/usr/bin/env python3

import sys

def process_input(input_stream, output_stream):
    # Read the input stream line by line
    for line in input_stream:
        # Decode the line as UTF-8, ignoring any errors
        line = line.decode('utf-8', 'ignore')
        # Encode the line back to bytes and write it to the output stream
        output_stream.write(line.encode('utf-8'))

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'rb') as file:
            process_input(file, sys.stdout.buffer)
    else:
        # No file specified, use stdin
        process_input(sys.stdin.buffer, sys.stdout.buffer)