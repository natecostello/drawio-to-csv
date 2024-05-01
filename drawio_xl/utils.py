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