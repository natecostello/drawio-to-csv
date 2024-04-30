import io
import csv

# Run the Python scripts in a pipeline, passing the output of each command directly to the next
# xl_delete_non_utf8.py "$input_file" | \
# xl_delete_empty_cols.py | \
# xl_delete_empty_rows.py | \
# xl_rename_headers.py | \
# xl_fix_shape_case.py | \
# xl_fix_status_case.py | \
# xl_replace_newlines.py | \
# xl_save_id.py | \
# xl_rename_shapes.py | \
# xl_add_height_width.py | \
# xl_parse_decisions.py | \
# csv_add_frontmatter.py "$frontmatter_file" | \
# csv_to_drawio.sh > "$output_file"

def delete_non_utf8(input_stream):
    """
    Deletes non-UTF-8 characters from the input stream.

    This function reads each line from the input stream, decodes it as UTF-8 while ignoring any errors,
    and writes the line to a new output stream. The output stream is then returned.

    Args:
        input_stream (io.StringIO): The input stream.

    Returns:
        io.StringIO: The output stream with non-UTF-8 characters deleted.
    """
    output_stream = io.StringIO()
    for line in input_stream:
        line = line.decode('utf-8', 'ignore') # Decode the line as UTF-8, ignoring any errors
        output_stream.write(line)

    output_stream.seek(0)
    return output_stream

def delete_empty_cols(input_stream):
    """
    Deletes empty columns from the input CSV stream.

    This function reads a CSV from the input stream, removes any columns where the header is empty,
    and writes the remaining columns to a new output stream. The output stream is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with empty columns deleted.

    Note:
        This function assumes that the first row of the CSV contains the headers.
    """
    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    headers = next(reader)
    indices = [i for i, h in enumerate(headers) if h]

    # Write the non-empty headers to the output
    writer.writerow([headers[i] for i in indices])

    for row in reader:
        writer.writerow([row[i] for i in indices])
    
    output_stream.seek(0)
    return output_stream

def delete_empty_rows(input_stream):
    """
    Deletes empty rows from the input CSV stream.

    This function reads a CSV from the input stream, removes any rows that are empty or contain only whitespace,
    and writes the remaining rows to a new output stream. The output stream is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with empty rows deleted.
    """
    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    for row in reader:
        # Check if the row is not empty
        if any(field.strip() for field in row):
            writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def rename_headers(input_stream):
    """
    Renames headers in the input CSV stream.

    This function reads a CSV from the input stream, renames the headers according to a predefined mapping,
    and writes the renamed headers to a new output stream. The output stream is then returned.

    The headers 'Process Step ID', 'Shape Type', 'Connector Label', and 'Next Step ID' are renamed to 'id', 'shape', 
    'connector_label', and 'next_step_id' respectively. All other headers are converted to lowercase and spaces are 
    replaced with underscores.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with renamed headers.

    Note:
        This function assumes that the first row of the CSV contains the headers.
    """

    #TODO these should come from a config file
    fixed_headers = ['Process Step ID', 'Shape Type', 'Connector Label', 'Next Step ID']

    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    headers = next(reader)

    # for all headers not in fixed_headers, replace spaces with underscores and lowercase the header
    headers = [header.replace(' ', '_').lower() if header not in fixed_headers else header for header in headers]

    # rename fixed headers
    headers[headers.index('Process Step ID')] = 'id'
    headers[headers.index('Shape Type')] = 'shape'
    headers[headers.index('Connector Label')] = 'connector_label'
    headers[headers.index('Next Step ID')] = 'next_step_id'

    writer.writerow(headers)

    for row in reader:
        writer.writerow(row)

    output_stream.seek(0)
    return output_stream

def fix_shape_case(input_stream):
    pass

def fix_status_case(input_stream):
    pass

def replace_newlines(input_stream):
    pass

def save_id(input_stream):
    pass

def rename_shapes(input_stream):
    pass

def add_height_width(input_stream):
    pass

def parse_decisions(input_stream):
    pass

def add_frontmatter(input_stream, frontmatter_file):
    pass

def csv_to_drawio(input_stream):
    pass

