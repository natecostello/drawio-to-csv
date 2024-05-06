import csv
import io
import re

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

def get_front_matter():
    """
    Returns:
        str: The front matter as a string.
    """
    front_matter = """##
## **********************************************************
## Example description
## **********************************************************
## This example shows how you can use styles for shapes. There are three styles configured in the "styles" array: the first two are static styles, while "style3" uses the fill and stroke columns as parameters for fillColor and strokeColor. This shows how you can use a single style with varying parameters (see Cell C and Cell D). All these principles work the same for connectors.
## **********************************************************
## Configuration
## **********************************************************
# label: %description%<br><b>%xl_id%</b> - <i>%owner%</i><br>%estimated_completion_date%
##
##
# styles: { \
# "todo" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;html=1;", \
# "doing" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#fff2cc;strokeColor=#d6b656;html=1;", \
# "waiting" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#f5f5f5;strokeColor=#666666;html=1;", \
# "done" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#d5e8d4;strokeColor=#82b366;html=1;", \
# "stop" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#f8cecc;strokeColor=#b85450;html=1;", \
# "" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;html=1;" }
# stylename: status
# namespace: csvimport-
# connect: {"from": "next_step_id", "to": "id", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}
# connect: {"from": "decision0_id", "to": "id", "fromlabel": "decision0_label", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}
# connect: {"from": "decision1_id", "to": "id", "fromlabel": "decision1_label", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}
# connect: {"from": "decision2_id", "to": "id", "fromlabel": "decision2_label", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}
# width: @width
# height: @height
# padding: 5
# ignore: id, next_step_id, shape, width, height, decision0_id, decision0_label, decision1_id, decision1_label, decision2_id, decision2_label
# link: url
# nodespacing: 100
# levelspacing: 200
# edgespacing: 40
# layout: horizontalflow
## **********************************************************
## CSV Data
##
##
## status is one of: todo, doing, waiting, done, stop
## shape is one of: or(and), data, decision, document, terminator (end), summing_function(or), predefined_process (subprocess), process, start_1 (start)
## next_step_id can be a comma separated list of ids
## decision0_id, decision1_id, decision2_id are the ids of the next steps following a decision
## decision0_label, decision1_label, decision2_label are the labels for the decisions
## width and height are the dimensions of the shape
## xl_id is the original process step id from excel
## **********************************************************"""
    
    return front_matter

def get_max_decision_count_from_rows(rows, headers):
    """
    This function calculates the maximum decision count from the given rows of CSV data. 
    The decision count for a row is defined as the number of next steps for rows where the shape is 'decision'.
    
    The function first identifies the indices of 'shape', 'next_step_id', and 'connector_label' in the headers list.
    It then iterates over each row in the rows list. For each row, if the shape is 'decision', 
    it splits the 'next_step_id' field by comma to get a list of next steps. 
    If the number of next steps is greater than the current maximum decision count, 
    it updates the maximum decision count.
    
    Finally, it returns the maximum decision count found.

    Args:
        rows (list): A list of lists where each inner list represents a row of CSV data. 
                     Each inner list contains string elements.
        headers (list): A list of strings where each string is a header of the CSV data.

    Returns:
        int: The maximum decision count found among the rows where the shape is 'decision'. 
             If no such rows are found, it returns 0.
    """
    max_decision_count = 0

    shape_index = headers.index('shape')
    next_step_id_index = headers.index('next_step_id')
    connector_label_index = headers.index('connector_label')

    # Iterate over rows and find the maximum number of next steps for rows with shape 'decision'
    for row in rows:
        if row[shape_index] == 'mxgraph.flowchart.decision':
            next_steps = row[next_step_id_index].split(',')
            
            if len(next_steps) > max_decision_count:
                max_decision_count = len(next_steps)

    return max_decision_count
    
def get_max_decision_count_from_headers(headers):
    """
    This function takes a list of csv headers and determines the value of max_decision_count 
    based on the presence of fields of the form "decisionN_id" and "decisionN_label".

    Parameters:
    headers (list): The list of headers.

    Returns:
    max_decision_count (int): The maximum decision count found in the headers.
    """
    # Initialize max_decision_count to 0
    max_decision_count = 0

    # Check each header
    for header in headers:
        # If the header matches the pattern "decisionN_id" or "decisionN_label"
        match = re.match(r'decision(\d+)_(id|label)', header)
        if match:
            # Extract N from the header and convert it to an integer
            N = int(match.group(1))
            # If N+1 is greater than the current max_decision_count, update max_decision_count
            if N+1 > max_decision_count:
                max_decision_count = N+1

    return max_decision_count

def get_connect_frontmatter(max_decision_count, connector_style):
    """
    This function generates a string of connection instructions based on the provided max_decision_count and connector_style.  Each line of the string is terminated with a newline character.

    Parameters:
    max_decision_count (int): The maximum decision count.
    connector_style (str): The style of the connector.

    Returns:
    connect_string (str): The generated string of connection instructions.
    """
    # Initialize the connect string with the connection for "next_step_id"
    connect_string = f'# connect: {{"from": "next_step_id", "to": "id", "style": "{connector_style}"}}\n'

    # Add the connections for "decisionN_id" and "decisionN_label" for each N from 0 to max_decision_count - 1
    for N in range(max_decision_count):
        connect_string += f'# connect: {{"from": "decision{N}_id", "to": "id", "fromlabel": "decision{N}_label", "style": "{connector_style}"}}\n'

    return connect_string

def get_ignore_frontmatter(max_decision_count):
    """
    This function generates a string of frontmatter instructions based on the provided max_decision_count.  The string terminates with a newline character.

    Parameters:
    max_decision_count (int): The maximum decision count.

    Returns:
    ignore_string (str): The generated string of frontmatter instructions.
    """
    # Initialize the ignore string with the fixed fields
    # TODO this should be driven by config maybe
    ignore_string = '# ignore: id, next_step_id, shape, width, height'

    # Add the fields for "decisionN_id" and "decisionN_label" for each N from 0 to max_decision_count - 1
    for N in range(max_decision_count):
        ignore_string += f', decision{N}_id, decision{N}_label'

    return ignore_string + '\n'    