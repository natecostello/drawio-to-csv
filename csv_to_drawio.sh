#!/bin/bash

# If a filename is provided as an argument, use that. Otherwise, read from standard input.
if [[ -n "$1" ]]; then
    input="$1"
else
    temp=$(mktemp -t tmp.XXXXXXXXXX)
    input="${temp}.csv"
    cat > "$input"
    trap 'rm -f "$input"' EXIT
fi

# Check if the input file exists and is not empty
if [[ ! -s "$input" ]]; then
    echo "Error: Input file does not exist or is empty" >&2
    exit 1
fi

# Check if draw.io is installed at the expected location
drawio_path="/Applications/draw.io.app/Contents/MacOS/draw.io"
if [[ ! -x "$drawio_path" ]]; then
    echo "Error: draw.io not found at $drawio_path" >&2
    exit 1
fi

# Use a temporary file for the output of draw.io
tempfile=$(mktemp)
trap 'rm -f "$tempfile"' EXIT

# Run draw.io on the input and save the output to the temporary file
"$drawio_path" -x "$input" -f xml -o "$tempfile" > /dev/null 2>&1
#"$drawio_path" -x "$input" -f xml -o final.xml > /dev/null 2>&1

# Check if draw.io was successful
if [[ $? -ne 0 ]]; then
    echo "Error: draw.io failed" >&2
    echo "Input file was: $input"
    echo "Temporary file was: $tempfile"
    exit 1
fi

# Copy the temporary file to standard output
cat "$tempfile"