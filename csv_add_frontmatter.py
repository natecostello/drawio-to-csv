#!/usr/bin/env python3

import sys

def add_frontmatter(frontmatter_filename, input_stream=sys.stdin):
    try:
        # Read and store the frontmatter
        with open(frontmatter_filename, 'r') as frontmatter_file:
            frontmatter_content = frontmatter_file.read()
        
        # Output the frontmatter first
        sys.stdout.write(frontmatter_content)
        
        # Then output the piped input content
        for line in input_stream:
            sys.stdout.write(line)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <frontmatter_file> [input_file]", file=sys.stderr)
        sys.exit(1)
    
    frontmatter_file = sys.argv[1]
    if len(sys.argv) == 3:
        with open(sys.argv[2], 'r') as input_file:
            add_frontmatter(frontmatter_file, input_file)
    else:
        add_frontmatter(frontmatter_file)