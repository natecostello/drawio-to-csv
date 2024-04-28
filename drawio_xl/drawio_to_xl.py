# Run the Python scripts in a pipeline, passing the output of each command directly to the next
# drawio_to_csv.py -i "$input_file" frontmatter.txt | \
# csv_strip_frontmatter.py | \
# csv_delete_height_width.py | \
# csv_rename_ids.py | \
# csv_strip_xl_ids.py | \
# csv_rename_shapes.py | \
# csv_parse_decisions.py | \
# csv_insert_newlines.py | \
# csv_rename_headers.py | \
# csv_reorder_headers.py > "$output_file"

import argparse
import csv
import xml.etree.ElementTree as ET
import sys
import io


def convert_to_csv(input_stream, frontmatter_file):
    """
    Convert a .drawio (XML) file to a draw.io formatted CSV string.

    This function parses a draw.io (XML) file from the provided input stream, 
    extracts relevant data based on predefined shape dimensions, and returns 
    the data as a draw.io formatted CSV string.

    Parameters:
    input_stream (io.TextIOWrapper): The input stream from which to read the draw.io XML file.
    frontmatter_file (str): The path to the frontmatter file.

    The function uses the xml.etree.ElementTree module to parse the XML file. 
    It defines shape dimensions based on shapes for accurate dimension assignment. 
    The shape dimensions are currently hardcoded in the function, but there's a TODO 
    to move this to a config object that reads a config file.

    Returns:
    io.StringIO: The draw.io formatted CSV stream.
    """
    # Load and parse the XML
    tree = ET.parse(input_stream)
    root = tree.getroot()

    # Define shape dimensions based on shapes for accurate dimension assignment
    # TODO move this to a config object that reads a config file
    shape_dimensions = {
        'process': ('200', '100'),
        'decision': ('100', '100'),
        'data': ('200', '100'),  # Example shapes, adjust as necessary
        'predefined_process': ('200', '100'),
        'terminator': ('100', '50'),
        'document': ('200', '100'),
        'or': ('100', '100'),
        'summing_function': ('100', '100'),
        'start': ('100', '100'),   
        # Add other shapes as necessary
    }

    # TODO generalize to number provided in config
    max_decision_count = 3

    # Required fields that will be built from any diagram are
    # id, shape, width, height, next_step_id, decisionN_id, decisionN_label, xl_id

    ignored_properties = ['label', 'placeholders']

    # Initialize a set to store all fieldnames and add some required fields
    fieldnames = set()
    fieldnames.add('id')
    fieldnames.add('shape')
    fieldnames.add('width')
    fieldnames.add('height')
    fieldnames.add('next_step_id')
    fieldnames.add('xl_id')
    for i in range(max_decision_count):
        fieldnames.add(f'decision{i}_id')
        fieldnames.add(f'decision{i}_label')

    # Function to parse the shape from the style string
    def refined_parse_shape(style):
        prefix = "mxgraph.flowchart."
        start = style.find(prefix)
        if start != -1:
            start += len(prefix)
            end = style.find(';', start)
            if end == -1:
                end = len(style)
            return style[start:end]
        return 'unknown'

    # Extract nodes
    nodes = []
    for element in root.iter():
        if element.tag.endswith('UserObject'):
            mxcell = element.find('.//mxCell')
            if mxcell is not None and 'style' in mxcell.attrib:
                style = mxcell.get('style', '')
                shape = refined_parse_shape(style)

                # add some required fields
                details = {
                    'id': element.get('id'),
                    'shape': shape,
                    'width': shape_dimensions.get(shape, ('100', '100'))[0], # default to 100 if the shape is not found
                    'height': shape_dimensions.get(shape, ('100', '100'))[1], # default to 100 if the shape is not found
                    'xl_id': element.get('xl_id', element.get('id')), # default to the id if no xl_id is present                   
                    # 'owner': element.get('owner', ''),
                    # 'description': element.get('description', ''),
                    # 'status': element.get('status', ''),
                }

                # add all the other properties from the element
                for property in element.keys():
                    if property not in ['id', 'shape', 'width', 'height', 'xl_id'] and property not in ignored_properties:
                        details[property] = element.get(property)
                        fieldnames.add(property)
                
                nodes.append(details)

    # Extract edges
    edges = []
    for element in root.iter():
        if element.tag.endswith('mxCell') and 'edge' in element.attrib:
            edges.append({
                'source': element.get('source'),
                'target': element.get('target'),
                'label': element.get('value', '').strip()
            })

    # Assign relationships
    for node in nodes:
        connected_edges = [edge for edge in edges if edge['source'] == node['id']]
        decision_count = 0
        for edge in connected_edges:
            if node['shape'] == 'decision' and decision_count < max_decision_count:
                decision_key_id = f'decision{decision_count}_id'
                decision_key_label = f'decision{decision_count}_label'
                node[decision_key_id] = edge['target']
                node[decision_key_label] = edge['label']
                decision_count += 1
            elif node['shape'] != 'decision':
                if 'next_step_id' in node and node['next_step_id']:
                    node['next_step_id'] += ',' + edge['target']
                else:
                    node['next_step_id'] = edge['target']

    # Read the front matter from the provided file
    with open(frontmatter_file, 'r') as f:
        front_matter = f.read()

    # Write the final CSV with hardcoded front matter
    output = io.StringIO()
    output.write(front_matter)
    # Sort the fieldnames for consistency in the output for testing
    fieldnames = sorted(list(fieldnames))
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    for node in nodes:
        writer.writerow({key: node.get(key, '') for key in fieldnames})
    # Add a newline
    output.write('\n')
    output.seek(0)
    return output

def strip_front_matter(input_stream):
    """
    Strip the front matter from the input stream.

    This function reads the input stream line by line and accumulates lines that do not start with "#".

    Parameters:
    input_stream (io.TextIOWrapper): The input stream from which to read the front matter.

    Returns:
    io.StringIO: The content without the front matter.
    """
    output_stream = io.StringIO()
    for line in input_stream:
        if not line.strip().startswith('#'):
            output_stream.write(line)
    output_stream.seek(0)
    return output_stream

def delete_column(input_stream, column_name):
    """
    Remove a column from the CSV content.

    Args:
    input_stream (io.StringIO): The input stream from which to read the CSV content.
    column_name (str): The name of the column to remove.

    Returns:
    io.StringIO: The CSV content without the specified column.
    """
    reader = csv.reader(input_stream)
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, lineterminator='\n')

    headers = next(reader)
    if column_name in headers:
        column_index = headers.index(column_name)
        headers.remove(column_name)

        writer.writerow(headers)

        for row in reader:
            del row[column_index]
            writer.writerow(row)
    else:
        input_stream.seek(0)
        return input_stream

    output_stream.seek(0)
    return output_stream

def delete_height_width(input_stream):
    """
    Remove the 'height' and 'width' columns from the CSV content.

    This function reads the CSV content from the given input stream,
    removes the 'height' and 'width' columns, and returns the modified
    CSV content as a new stream.

    Args:
    input_stream (io.StringIO): The input stream containing the CSV content.

    Returns:
    io.StringIO: The CSV content without the 'height' and 'width' columns.
    """
    csv_content = delete_column(input_stream, "height")
    csv_content = delete_column(csv_content, "width")
    return csv_content

def replace_ids_with_xl_ids(input_stream):
    """
    Replace the 'id' column values with the 'xl_id' column values in the CSV content.

    This function reads the CSV content from the given input stream,
    replaces the 'id' column values with the 'xl_id' column values, and returns the modified
    CSV content as a stream.

    Args:
    input_stream (io.StringIO): The input stream containing the CSV content.

    Returns:
    io.StringIO: The CSV content with the 'id' column renamed to 'xl_id'.
    """
    reader = csv.reader(input_stream)
    output_stream = io.StringIO()
    
    # Get the headers from the first row
    headers = next(reader)
    # Find the index of the "id" and "xl_id" columns
    id_index = headers.index("id")
    xl_id_index = headers.index("xl_id")

    # Create a dictionary to map "id" to "xl_id"
    id_to_xl_id = {}

    # Create a list to store the rows
    rows = []

    # Iterate over the rows in the original CSV file
    for row in reader:
        # Add the mapping from "id" to "xl_id"
        id_to_xl_id[row[id_index]] = row[xl_id_index]
        # Add the row to the list of rows
        rows.append(row)

    # Create a CSV writer
    writer = csv.writer(output_stream, lineterminator='\n')
    # Write the headers to the output
    writer.writerow(headers)

    # Iterate over the rows again
    for row in rows:
        # Replace the "id" with the corresponding "xl_id"
        row[id_index] = id_to_xl_id[row[id_index]]

        # Replace the "next_step_id", "decision0_id", "decision1_id", and "decision2_id" with the corresponding "xl_id"
        for header in ["next_step_id", "decision0_id", "decision1_id", "decision2_id"]:
            if header in headers:
                index = headers.index(header)
                # Handle the case where the cell contains a comma-separated list of ids
                ids = row[index].split(',')
                xl_ids = [id_to_xl_id[id] for id in ids if id in id_to_xl_id]
                row[index] = ','.join(xl_ids)

        # Write the modified row to the new CSV file
        writer.writerow(row)
    
    output_stream.seek(0)

    return output_stream

def delete_xl_ids(input_stream):
    """
    Remove the 'xl_id' column from the CSV content.

    This function reads the CSV content from the given input stream,
    removes the 'xl_id' column, and returns the modified CSV content as a new stream.

    Args:
    input_stream (io.StringIO): The input stream containing the CSV content.

    Returns:
    io.StringIO: The CSV content without the 'xl_id' column.
    """
    return delete_column(input_stream, "xl_id")

def rename_shapes(input_stream):
    """
    Rename shapes in the CSV content.

    This function reads the CSV content from the given input stream,
    renames shapes based on predefined mappings, and returns the modified
    CSV content as a new stream.

    Args:
    input_stream (io.StringIO): The input stream containing the CSV content.

    Returns:
    io.StringIO: The CSV content with shapes renamed.
    """
    reader = csv.DictReader(input_stream)
    output_stream = io.StringIO()
    writer = csv.DictWriter(output_stream, fieldnames=reader.fieldnames, lineterminator='\n')
    #TODO this function depends on a non-required column 'description' which is not present in the input file
    #TODO consider if there is a better way to do this
    
    # Check if 'description' column is present in the input file and  create it if not
    if 'description' not in reader.fieldnames:
        reader.fieldnames.append('description')
        writer.writeheader()
    else:
        writer.writeheader()

    for row in reader:
        if row['shape'] == 'start_1':
            row['shape'] = 'start'
        elif row['shape'] == 'terminator':
            row['shape'] = 'end'
        elif row['shape'] == 'summing_function':
            row['shape'] = 'process'
            row['description'] = 'OR'
        elif row['shape'] == 'or':
            row['shape'] = 'process'
            row['description'] = 'AND'
        writer.writerow(row)

    output_stream.seek(0)
    return output_stream
    