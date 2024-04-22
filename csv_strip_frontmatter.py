#!/usr/bin/env python3

import sys

def strip_frontmatter(input_stream):
    output_content = []
    try:
        # Read the input stream line by line and accumulate lines that do not start with "#"
        for line in input_stream:
            if not line.strip().startswith('#'):
                output_content.append(line)

        # Output all content at once to stdout
        sys.stdout.write(''.join(output_content))
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Check if there's an input file specified, otherwise use stdin
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as file:
            strip_frontmatter(file)
    else:
        # No file specified, use stdin
        strip_frontmatter(sys.stdin)
