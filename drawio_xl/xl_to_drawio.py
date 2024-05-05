import io
import csv
import subprocess
import tempfile
import os
import argparse


if __name__ == '__main__':
    from utils import delete_column
    from utils import delete_non_utf8
    from utils import delete_empty_cols
    from utils import delete_empty_rows
    from utils import get_max_decision_count_from_headers
    from utils import get_max_decision_count_from_rows
    from utils import get_connect_frontmatter
    from utils import get_ignore_frontmatter
    from config import Config

else:
    from drawio_xl.utils import delete_column
    from drawio_xl.utils import delete_non_utf8
    from drawio_xl.utils import delete_empty_cols
    from drawio_xl.utils import delete_empty_rows
    from drawio_xl.utils import get_max_decision_count_from_headers
    from drawio_xl.utils import get_max_decision_count_from_rows
    from drawio_xl.utils import get_connect_frontmatter
    from drawio_xl.utils import get_ignore_frontmatter
    from drawio_xl.config import Config



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

def lower_shape_case(input_stream):
    """
    Converts the 'shape' column values to lowercase in the input CSV stream.

    This function reads a CSV from the input stream, finds the 'shape' column, and converts all its values to lowercase.
    The modified CSV is written to a new output stream, which is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with 'shape' column values converted to lowercase.
    """
    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "shape" column
    shape_type_index = headers.index("shape")

    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Convert the "shape" entry to lowercase
        row[shape_type_index] = row[shape_type_index].lower()
        # Write the modified row to the new CSV file
        writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def lower_status_case(input_stream):
    """
    Converts the 'status' column values to lowercase in the input CSV stream.

    This function reads a CSV from the input stream, finds the 'status' column, and converts all its values to lowercase.
    The modified CSV is written to a new output stream, which is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with 'status' column values converted to lowercase.
    """
    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "status" column
    status_index = headers.index("status")

    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows in the original CSV file and change case
    for row in reader:
        row[status_index] = row[status_index].lower()
        writer.writerow(row)

    output_stream.seek(0)
    return output_stream

def replace_newlines(input_stream):
    """
    Replaces newline and carriage return characters in the input CSV stream with "<br>".

    This function reads a CSV from the input stream, finds any fields that contain newline or carriage return characters, 
    and replaces them with "<br>". The modified CSV is written to a new output stream, which is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with newline and carriage return characters replaced with "<br>".
    """
    output_stream = io.StringIO()
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Replace newline and carriage return characters with "<br>" in each cell
        modified_row = [cell.replace('\n', '<br>').replace('\r', '<br>') for cell in row]
        # Write the modified row to the new CSV file
        writer.writerow(modified_row)
    
    output_stream.seek(0)
    return output_stream

def save_id(input_stream):
    """
    Copies the 'id' column to a new 'xl_id' column in the input CSV stream.

    This function reads a CSV from the input stream, finds the 'id' column, 
    and copies its values to a new 'xl_id' column. The modified CSV is written 
    to a new output stream, which is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with the added 'xl_id' column.
    """

    output_stream = io.StringIO()
    # Create a CSV reader
    reader = csv.reader(input_stream)
    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "id" column
    id_index = headers.index("id")

    # Add the new "xl_id" header
    headers.append("xl_id")

    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')
    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Copy the value from "id" to "xl_id"
        row.append(row[id_index])
        # Write the modified row to the new CSV file
        writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def rename_shapes(input_stream):
    """
    Renames certain 'shape' values in the input CSV to maintain correspondence with between Visio and draw.io.

    The modified CSV is written to a new output stream, which is then returned.

    The mapping of 'shape' values from Visio to draw.io is as follows:
    - 'custom 1' is renamed to 'summing_junction'.
    - 'custom 2' is renamed to 'or'.
    - 'end' is renamed to 'terminator'.
    - 'start' is renamed to 'start_1'.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with the renamed 'shape' values.
    """
    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    headers = next(reader)
    shape_index = headers.index('shape')
    
    writer.writerow(headers)

    for row in reader:
        if row[shape_index] == "custom 2":
            row[shape_index] = "or"
        elif row[shape_index] == "custom 1":
            row[shape_index] = "summing_function"
        elif row[shape_index] == "end":
            row[shape_index] = "terminator"
        elif row[shape_index] == "start":
            row[shape_index] = "start_1"
        writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def insert_height_width(input_stream):
    """
    Inserts 'width' and 'height' columns into the input CSV stream based on the 'shape' column.

    This function reads a CSV from the input stream, finds the 'shape' column, and inserts 'width' 
    and 'height' columns based on the 'shape' value. The dimensions for each shape are defined in 
    the `shape_dimensions` dictionary. If a shape is not found in the dictionary, default dimensions 
    of '100' (width) and '100' (height) are used. The modified CSV is written to a new output stream, 
    which is then returned.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: The output stream with the added 'width' and 'height' columns.
    """
    output_stream = io.StringIO()
    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator='\n')

    headers = next(reader)
    shape_index = headers.index('shape')

    headers.extend(['width', 'height'])
    writer.writerow(headers)

    config = Config()
    shape_dimensions = config.shape_dimensions

    for row in reader:
        shape = row[shape_index]
        width, height = shape_dimensions.get(shape, ('100', '100'))
        row.extend([width, height])

        writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def parse_decisions(input_stream):
    """
    Parses a CSV file containing decision data and transforms it into a format suitable for further processing.

    The function reads from an input stream, which should be a CSV file with headers. The CSV file should contain columns named 'shape', 'next_step_id', and 'connector_label'. Rows where 'shape' is 'decision' are treated specially.

    For each 'decision' row, the 'next_step_id' and 'connector_label' fields are split into multiple fields. The number of fields is determined by the `max_decision_count` variable. The split fields are appended to the row, and the original 'next_step_id' field is cleared.

    For non-'decision' rows, the same number of empty fields are appended.

    The function then removes the 'connector_label' column from the CSV data.

    The transformed CSV data is returned as a string.

    Args:
        input_stream (io.TextIOWrapper): The input stream to read the CSV data from.

    Returns:
        io.StringIO: A stream containing the transformed CSV data.
    """
    # first pass
    reader = csv.reader(input_stream)
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, lineterminator='\n')
    
    headers = next(reader)
    shape_index = headers.index('shape')
    next_step_id_index = headers.index('next_step_id')
    connector_label_index = headers.index('connector_label')
    rows = list(reader)

    # Find the max number of decision branches
    max_decision_count = get_max_decision_count_from_rows(rows, headers)

    # Second Pass
    input_stream.seek(0)
    next(reader) # skip the headers

    headers.extend([f'decision{i}_{suffix}' for i in range(max_decision_count) for suffix in ['id', 'label']])
    
    writer.writerow(headers)

    for row in reader:
        if row[shape_index] == "decision":
            decision_ids = [id.strip() for id in row[next_step_id_index].replace('"', '').split(',')]
            decision_labels = [label.strip() for label in row[connector_label_index].replace('"', '').split(',')]
            decision_fields = list(zip(decision_ids + [None]*max_decision_count, decision_labels + [None]*max_decision_count))[:max_decision_count]
            row[next_step_id_index] = ""
        else:
            decision_fields = [(None, None)] * max_decision_count

        row.extend([item for sublist in decision_fields for item in sublist])

        writer.writerow(row)
    
    # delete 'connector_label'
    output_stream.seek(0)
    output_stream = delete_column(output_stream, 'connector_label')
    
    return output_stream

def add_frontmatter(input_stream):
    """
    This function takes an input stream, extracts the max_decision_count from the stream data using 
    get_max_decision_count from utils, assembles a frontmatter string composed of static frontmatter 
    from config.py, connector frontmatter from utils, and ignore frontmatter from utils. 
    It returns a stream that consists of the input stream with the frontmatter string prepended to it.

    Parameters:
    input_stream (io.StringIO): The input stream to read from.

    Returns:
    output_stream (io.StringIO): The output stream with the frontmatter content prepended.
    """
    
    # read the first line of the input stream
    reader = csv.reader(input_stream)
    headers = next(reader)

    # reset the input stream
    input_stream.seek(0)

    # Extract max_decision_count from input_stream data
    max_decision_count = get_max_decision_count_from_headers(headers)

    # Assemble frontmatter string
    config = Config()
    connector_style = config.connector_style
    frontmatter_content = config.static_frontmatter + \
                        get_connect_frontmatter(max_decision_count, connector_style) + \
                        get_ignore_frontmatter(max_decision_count)
    # Create an output stream
    output_stream = io.StringIO()

    # Write the frontmatter to the output stream
    output_stream.write(frontmatter_content)

    # Write the input stream
    output_stream.write(input_stream.read())

    output_stream.seek(0)
    return output_stream

def csv_to_drawio(input_stream):
    """
    Converts a CSV file to a Draw.io diagram using the Draw.io command-line tool.

    This function creates temporary files for the input and output, writes the contents of the input stream to the input file,
    runs the Draw.io command-line tool to convert the input file to a Draw.io diagram, and writes the output to the output file.
    The function then reads the output file into a string stream and returns it.

    The temporary input and output files are automatically deleted when they are no longer needed.

    Args:
        input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
        io.StringIO: A string stream containing the Draw.io diagram.

    Raises:
        subprocess.CalledProcessError: If the Draw.io command fails.
    """
    # Create temporary files for the input and output
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=True, mode='w+') as temp_input, tempfile.NamedTemporaryFile(delete=True, mode='w+') as temp_output:
        # Write the contents of the input stream to the temporary input file
        temp_input.write(input_stream.read())
        temp_input.flush()  # Ensure all data is written to the file
        
        #TODO this path should come from a config file
        drawio_path = "/Applications/draw.io.app/Contents/MacOS/draw.io"
        command = [drawio_path, "-x", temp_input.name, "-f", "xml", "-o", temp_output.name]
        
        # Run the command
        subprocess.run(command, check=True)

        temp_output.seek(0)
        return io.StringIO(temp_output.read())    

def xl_to_drawio(input_stream):
    """
    This function processes an Excel CSV file and converts it to a draw.io (XML) .drawio file.

    The function performs the following steps:
    1. Removed as it is not needed: Deletes non-utf8 characters.
    2. Deletes empty columns.
    3. Deletes empty rows.
    4. Renames headers.
    5. Lowers the case of the 'shape' and 'status' columns.
    6. Replaces newline characters with '<br>'.
    7. Saves the 'id' column to a new 'xl_id' column.
    8. Renames shapes from Visio standard flowchart shapes to draw.io flowchart shapes.
    9. Adds 'width' and 'height' columns based on the 'shape' column.
    10. Parses decision data from Visio standard format to a format suitable for draw.io.
    11. Adds frontmatter to the CSV data.
    12. Converts the CSV data to a draw.io diagram using the draw.io command-line tool.

    Parameters:
    input_stream (io.StringIO): The input stream containing the Excel CSV data.

    Returns:
    io.StringIO: The output stream containing the processed draw.io data.
    """
    # Delete non-utf8 characters
    #input_stream = delete_non_utf8(input_stream)
    
    # input_stream = delete_empty_cols(input_stream)
    # input_stream = delete_empty_rows(input_stream)
    # input_stream = rename_headers(input_stream)
    # input_stream = lower_shape_case(input_stream)
    # input_stream = lower_status_case(input_stream)
    # input_stream = replace_newlines(input_stream)
    # input_stream = save_id(input_stream)
    # input_stream = rename_shapes(input_stream)
    # input_stream = insert_height_width(input_stream)
    # input_stream = parse_decisions(input_stream)
    # script_dir = os.path.dirname(os.path.realpath(__file__)) # Get the directory of this script
    # frontmatter_path = os.path.join(script_dir, 'frontmatter.txt') # Construct the path to the frontmatter file
    # input_stream = add_frontmatter(input_stream, frontmatter_path)
    # output_stream = csv_to_drawio(input_stream)
    
    input_stream = delete_empty_cols(input_stream)
    with open('tests/debug_output/0_delete_empty_cols.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = delete_empty_rows(input_stream)
    with open('tests/debug_output/1_delete_empty_rows.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = rename_headers(input_stream)
    with open('tests/debug_output/2_rename_headers.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = lower_shape_case(input_stream)
    with open('tests/debug_output/3_lower_shape_case.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = lower_status_case(input_stream)
    with open('tests/debug_output/4_lower_status_case.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = replace_newlines(input_stream)
    with open('tests/debug_output/5_replace_newlines.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = save_id(input_stream)
    with open('tests/debug_output/6_save_id.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = rename_shapes(input_stream)
    with open('tests/debug_output/7_rename_shapes.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = insert_height_width(input_stream)
    with open('tests/debug_output/8_insert_height_width.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    input_stream = parse_decisions(input_stream)
    with open('tests/debug_output/9_parse_decisions.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    script_dir = os.path.dirname(os.path.realpath(__file__)) # Get the directory of this script
    frontmatter_path = os.path.join(script_dir, 'frontmatter.txt') # Construct the path to the frontmatter file
    input_stream = add_frontmatter(input_stream)
    with open('tests/debug_output/10_add_frontmatter.csv', 'w') as f:
        f.write(input_stream.getvalue())
    input_stream.seek(0)

    output_stream = csv_to_drawio(input_stream)
    with open('tests/debug_output/11_csv_to_drawio.drawio', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    return output_stream

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Convert an Excel CSV file to a drawio.')
    parser.add_argument('input_file', help='The input CSV file.')
    parser.add_argument('output_file', help='The output drawio file.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Read the input file
    with open(args.input_file, 'r') as f:
        input_data = f.read()
    input_stream = io.StringIO(input_data)

    # Call the drawio_to_xl function
    output_stream = xl_to_drawio(input_stream)

    # Write the output to the output file
    with open(args.output_file, 'w') as f:
        f.write(output_stream.getvalue())

if __name__ == '__main__':
    main()