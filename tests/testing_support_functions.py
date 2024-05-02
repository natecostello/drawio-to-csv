import xml.etree.ElementTree as ET
import io


def normalize_csv(csv_string):
        
    """
    Sort the columns in a CSV string.  This is intended for csv formatted for conversion to draw.io diagrams.

    Args:
        csv_string (str): The input string containing the CSV data.

    Returns:
        str: The output string with the columns in the CSV data sorted.
    """
    # Create a StringIO object from the input string
    stream = io.StringIO(csv_string)
    # Read the CSV data from the input stream
    reader = csv.reader(stream)

    # Store all lines beginning with a '#' character in the frontmatter
    frontmatter = []
    line = next(reader)
    while line[0].startswith('#'):
        frontmatter.append(line)
        line = next(reader)
    # the first line that is not a comment is the header
    headers = line

    # Read the remaining rows
    rows = list(reader)

    # Alphabetize the headers and get the new order
    new_order = sorted(range(len(headers)), key=lambda i: headers[i])
    headers = [headers[i] for i in new_order]

    # Rearrange the columns in the rows to match the new order of the headers
    rows = [[row[i] for i in new_order] for row in rows]

    # Write the CSV data to the output stream
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, lineterminator='\n')
    for line in frontmatter:
        writer.writerow(line)
    writer.writerow(headers)
    writer.writerows(rows)

    # convert the output stream to a string
    output_string = output_stream.getvalue()
    # Return the output string
    return output_string

def normalize_xml(xml_string):
    # Parse the XML string into an ElementTree object
    root = ET.fromstring(xml_string)

    # Find the <root> element
    root_element = root.find('.//root')

    def normalize_element(element):
        # Sort the properties
        element.attrib = dict(sorted(element.attrib.items()))

        if element.tag == 'UserObject':
            element.attrib.pop('label', None)
            for child in element.findall('mxCell'):
                style = child.get('style', '')
                style_dict = dict(item.split('=') for item in style.split(';') if item)
                child.set('style', 'shape=' + style_dict.get('shape', '') + ';')
                for grandchild in list(child):
                    child.remove(grandchild)
                return
        elif element.tag == 'mxCell':
            element.attrib.pop('style', None)
            for child in list(element):
                element.remove(child)
            return
        # Sort the children
        element[:] = sorted(element, key=lambda child: (child.tag, str(sorted(child.attrib.items()))))

        for child in element:
            normalize_element(child)

    normalize_element(root_element)

    return ET.tostring(root_element, encoding='unicode')