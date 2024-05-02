import csv
import io

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

