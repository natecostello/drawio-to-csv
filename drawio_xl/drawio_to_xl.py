import argparse
import csv
import xml.etree.ElementTree as ET
import sys
import io
import os

if __name__ == '__main__':
    from utils import delete_column
    from utils import get_max_decision_count_from_headers
    from config import Config
else:
    from drawio_xl.utils import delete_column
    from drawio_xl.utils import get_max_decision_count_from_headers
    from drawio_xl.config import Config


def convert_to_csv(input_stream):
    """
    Convert a .drawio (XML) file to a draw.io formatted CSV string.

    This function parses a draw.io (XML) file from the provided input stream, 
    extracts shapes, shape properties, and relationships.  It returns a draw.io 
    formatted CSV string without frontmatter.

    Parameters:
    input_stream (io.TextIOWrapper): The input stream from which to read the draw.io XML file.
    
    The function uses the xml.etree.ElementTree module to parse the XML file. 

    Returns:
    io.StringIO: The draw.io formatted CSV stream without frontmatter.
    """
    # Load and parse the XML
    tree = ET.parse(input_stream)
    root = tree.getroot()
    
    #create config instance
    config = Config()
    shape_dimensions = config.shape_dimensions
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
    # for i in range(max_decision_count):
    #     fieldnames.add(f'decision{i}_id')
    #     fieldnames.add(f'decision{i}_label')

    # Function to parse the shape from the style string
    def parse_shape(style):
        prefix = "shape="
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
                shape = parse_shape(style)

                # add some required fields
                details = {
                    'id': element.get('id'),
                    'shape': shape,
                    'width': shape_dimensions.get(shape, ('100', '100'))[0], # default to 100 if the shape is not found
                    'height': shape_dimensions.get(shape, ('100', '100'))[1], # default to 100 if the shape is not found
                    'xl_id': element.get('xl_id', element.get('id')), # default to the id if no xl_id is present
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

    # Determine max_decision_count based on connections to decision nodes
    max_decision_count = 0
    for node in nodes:
        connected_edges = [edge for edge in edges if edge['source'] == node['id']]
        decision_count = 0
        for edge in connected_edges:
            if node['shape'] == 'mxgraph.flowchart.decision':
                decision_count += 1
        # Update max_decision_count if necessary
        max_decision_count = max(max_decision_count, decision_count)

    # Add decision fields to fieldnames
    for i in range(max_decision_count):
        fieldnames.add(f'decision{i}_id')
        fieldnames.add(f'decision{i}_label')

    # Assign relationships
    for node in nodes:
        connected_edges = [edge for edge in edges if edge['source'] == node['id']]
        decision_count = 0
        for edge in connected_edges:
            if node['shape'] == 'mxgraph.flowchart.decision' and decision_count < max_decision_count:
                decision_key_id = f'decision{decision_count}_id'
                decision_key_label = f'decision{decision_count}_label'
                node[decision_key_id] = edge['target']
                node[decision_key_label] = edge['label']
                decision_count += 1
            elif node['shape'] != 'mxgraph.flowchart.decision':
                if 'next_step_id' in node and node['next_step_id']:
                    node['next_step_id'] += ',' + edge['target']
                else:
                    node['next_step_id'] = edge['target']

    output = io.StringIO()
    # Sort the fieldnames for consistency in the output for testing
    fieldnames = sorted(list(fieldnames))
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    for node in nodes:
        writer.writerow({key: node.get(key, '') for key in fieldnames})
    # Add a newline
    #output.write('\n') #deleted because this is not needed.
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
    Replace the 'id' column values with the 'xl_id' column values in the CSV content.  If the 'xl_id' column is empty in ANY row, the 'id' column values are retained.

    This function reads the CSV content from the given input stream,
    replaces the 'id' column values with the 'xl_id' column values, and returns the modified
    CSV content as a stream.

    Args:
    input_stream (io.StringIO): The input stream containing the CSV content.

    Returns:
    io.StringIO: The CSV content with the 'id' column renamed to 'xl_id' and 'id' column values with 'xl_id' column values.
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

    # Iterate over the rows in the original CSV file if ANY xl_id is empty, set xl_id_empty = true
    xl_id_empty = False
    for row in reader:
        if not row[xl_id_index]:
            xl_id_empty = True
        rows.append(row)
    
    # If any xl_id is empty, keep the original id for all rows
    # otherwise, replace the id with the corresponding xl_id
    if xl_id_empty:
        for row in rows:
            id_to_xl_id[row[id_index]] = row[id_index]
            #row[id_index] = row[id_index]
    else:
        for row in rows:
            id_to_xl_id[row[id_index]] = row[xl_id_index]
            #row[id_index] = row[xl_id_index]

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
    Rename shapes in the CSV content to maintain correspondence between Drawio and Visio shapes.  If the shape is not found in the mapping, the shape is left unchanged.

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
    
    writer.writeheader()

    config = Config()
    drawio_to_xl_shape_mapping = config.drawio_to_xl_shape_mapping

    for row in reader:
        if row['shape'] in drawio_to_xl_shape_mapping:
            row['shape'] = drawio_to_xl_shape_mapping[row['shape']]
        writer.writerow(row)

    output_stream.seek(0)
    return output_stream
    
def parse_decisions(input_stream):
    """
    This function parses decision-related fields in a CSV data stream. It combines decision_id and decision_label fields
    into a single field, and removes the original decision_id and decision_label fields. The number of decision fields 
    is determined by the max_decision_count variable.

    Parameters:
    input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
    io.StringIO: A new stream with the parsed decision fields.
    """
    
    # first pass
    reader = csv.reader(input_stream)
    output = io.StringIO()
    writer = csv.writer(output)

    headers = next(reader)
    max_decision_count = get_max_decision_count_from_headers(headers)
    shape_index = headers.index('shape')
    next_step_id_index = headers.index('next_step_id')

    decision_id_indices = [headers.index(f'decision{i}_id') for i in range(max_decision_count)]
    decision_label_indices = [headers.index(f'decision{i}_label') for i in range(max_decision_count)]

    headers.append('connector_label')
    connector_label_index = headers.index('connector_label')
    
    writer.writerow(headers)

    for row in reader:
        row.append('') # Append the connector_label field to the row
        # Handle decision-specific fields
        if row[shape_index] == "mxgraph.flowchart.decision":
            decision_ids = [row[index] for index in decision_id_indices]
            decision_labels = [row[index] for index in decision_label_indices]
            row[next_step_id_index] = ', '.join(filter(None, decision_ids))
            row[connector_label_index] = ', '.join(filter(None, decision_labels))
        else:
            row[connector_label_index] = ''

        writer.writerow(row)
    
    # second pass
    output.seek(0)

    for i in range(max_decision_count):
        output = delete_column(output, f'decision{i}_id')
        output = delete_column(output, f'decision{i}_label')

    return output

def insert_newlines(input_stream):
    """
    This function replaces '<br>' tags with newline characters ('\n') in each cell of the CSV data read from the input stream.

    Parameters:
    input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
    io.StringIO: A new stream with '<br>' tags replaced by newline characters in each cell.
    """
    reader = csv.reader(input_stream)
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, lineterminator='\n')
    for row in reader:
        modified_row = [cell.replace('<br>', '\n') for cell in row]
        writer.writerow(modified_row)

    output_stream.seek(0)
    return output_stream

def rename_headers(input_stream):
    """
    This function renames the headers of the CSV data read from the input stream. 

    The headers 'id', 'shape', 'connector_label', and 'next_step_id' are renamed to 'Process Step ID', 'Shape Type', 'Connector Label', and 'Next Step ID', respectively. 

    All other headers are transformed by replacing underscores with spaces and capitalizing the first letter of each word.

    Parameters:
    input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
    io.StringIO: A new stream with renamed headers.
    """

    #TODO naming should be pulled from a config file
    fixed_headers = ['id', 'shape', 'connector_label', 'next_step_id']

    reader = csv.reader(input_stream)
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, lineterminator='\n')

    headers = next(reader)

    # for all headers not in fixed_headers, replace underscores with spaces and capitalize the first letter of each word
    headers = [header.replace('_', ' ').title() if header not in fixed_headers else header for header in headers]
    
    # rename fixed headers
    # TODO add to config file
    headers[headers.index('id')] = 'Process Step ID'
    headers[headers.index('shape')] = 'Shape Type'
    headers[headers.index('connector_label')] = 'Connector Label'
    headers[headers.index('next_step_id')] = 'Next Step ID'
    
    writer.writerow(headers)

    for row in reader:
        writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def reorder_headers(input_stream):
    """
    This function reorders the headers of the CSV data read from the input stream. 

    The headers are reordered according to a hardcoded predefined list. Headers not in this list are sorted alphabetically and appended after the ordered headers.

    Parameters:
    input_stream (io.StringIO): The input stream containing the CSV data.

    Returns:
    io.StringIO: A new stream with reordered headers.
    """

    #TODO This should be pulled from a config file
    header_order = ["Process Step ID","Owner","Description","Status","Function","Phase","Estimated Duration","Estimated Completion Date","Notes","Wbs","Oqe","Next Step ID","Shape Type","Connector Label"]

    reader = csv.reader(input_stream)
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, lineterminator='\n')

    # reorder the headers and row elements to match the header_order list
    original_headers = next(reader)
    ordered_headers = [header for header in header_order if header in original_headers]
    
    remaining_headers = [header for header in original_headers if header not in header_order]
    remaining_headers.sort() # sort any remaining headers alphabetically
    headers = ordered_headers + remaining_headers

    writer.writerow(headers)

    # reorder the row elements to match the header_order list
    for row in reader:
        row_dict = dict(zip(original_headers, row))
        row = [row_dict[header] for header in headers]
        writer.writerow(row)
    
    output_stream.seek(0)
    return output_stream

def drawio_to_xl(input_stream):
    """
    This function processes a draw.io XML file and converts it to an Excel file.

    The function performs the following steps:
    1. Convert the draw.io XML file to a CSV file.
    2. Strip the front matter from the CSV file.
    3. Delete the 'height' and 'width' columns from the CSV file.
    4. Rename the 'id' column to 'xl_id' in the CSV file.
    5. Delete the 'xl_id' column from the CSV file.
    6. Rename the shapes in the CSV file.
    7. Parse decision-related fields in the CSV file.
    8. Insert newlines in the CSV file.
    9. Rename the headers in the CSV file.
    10. Reorder the headers in the CSV file.

    Parameters:
    input_stream (io.StringIO): The input stream containing the draw.io XML data.

    Returns:
    io.StringIO: The output stream containing the processed Excel data.
    """

    output_stream = convert_to_csv(input_stream) # Call the convert_to_csv function
    with open('tests/debug_output/0_convert_to_csv.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = strip_front_matter(output_stream)
    with open('tests/debug_output/1_strip_front_matter.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = delete_height_width(output_stream)
    with open('tests/debug_output/2_delete_height_width.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = replace_ids_with_xl_ids(output_stream)
    with open('tests/debug_output/3_replace_ids_with_xl_ids.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = delete_xl_ids(output_stream)
    with open('tests/debug_output/4_delete_xl_ids.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = parse_decisions(output_stream)
    with open('tests/debug_output/5_parse_decisions.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = rename_shapes(output_stream)
    with open('tests/debug_output/6_rename_shapes.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = insert_newlines(output_stream)
    with open('tests/debug_output/7_insert_newlines.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = rename_headers(output_stream)
    with open('tests/debug_output/8_rename_headers.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    output_stream = reorder_headers(output_stream)
    with open('tests/debug_output/9_reorder_headers.csv', 'w') as f:
        f.write(output_stream.getvalue())
    output_stream.seek(0)

    return output_stream

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Convert a drawio file to a CSV file.')
    parser.add_argument('input_file', help='The input drawio file.')
    parser.add_argument('output_file', help='The output CSV file.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Read the input file
    with open(args.input_file, 'r') as f:
        input_data = f.read()
    input_stream = io.StringIO(input_data)

    # Call the drawio_to_xl function
    output_stream = drawio_to_xl(input_stream)

    # Write the output to the output file
    with open(args.output_file, 'w') as f:
        f.write(output_stream.getvalue())

if __name__ == '__main__':
    main()