#!/usr/bin/env python3

import argparse
import csv
import xml.etree.ElementTree as ET
import sys
import io

def convertToCSV(input_stream, frontmatter_file):
    # Load and parse the XML
    tree = ET.parse(input_stream)
    root = tree.getroot()

    # Define shape dimensions based on shapes for accurate dimension assignment
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

    # Define the full list of field names for the CSV

    pre_fixed_fields = ['id', 'owner', 'description', 'status']
    post_fixed_fields = ['shape', 'width', 'height', 'next_step_id', 'decision0_id', 'decision0_label', 'decision1_id', 'decision1_label', 'decision2_id', 'decision2_label', 'xl_id']
    ignored_properties = ['label', 'placeholders']

    # Initialize an empty set to store all fieldnames
    arbitrary_fieldnames = set()

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

                # add the initial fixed fields
                details = {
                    'id': element.get('id'),                    
                    'owner': element.get('owner', ''),
                    'description': element.get('description', ''),
                    'status': element.get('status', ''),
                }

                # add all the other properties from the element
                for property in element.keys():
                    if property not in pre_fixed_fields and property not in post_fixed_fields and property not in ignored_properties:
                        details[property] = element.get(property)
                        arbitrary_fieldnames.add(property)
                
                # add some remaining fixed fields
                details['shape'] = shape
                details['width'] = shape_dimensions.get(shape, ('100', '100'))[0]
                details['height'] = shape_dimensions.get(shape, ('100', '100'))[1]
                details['xl_id'] = element.get('xl_id', '')
                
                nodes.append(details)

    # Build fieldnames
    fieldnames = list(pre_fixed_fields)
    arbitrary_fieldnames_list = list(arbitrary_fieldnames)
    fieldnames.extend(arbitrary_fieldnames_list)
    fieldnames.extend(post_fixed_fields)
    

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
            if node['shape'] == 'decision' and decision_count < 3:
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
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for node in nodes:
        writer.writerow({key: node.get(key, '') for key in fieldnames})

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('frontmatter', help='Path to the frontmatter.txt file')
    parser.add_argument('-p', '--pipe', action='store_true', help='Read input from stdin')
    parser.add_argument('-i', '--input', help='Path to the input file')

    args = parser.parse_args()

    if args.pipe and args.input:
        print("Error: Cannot use both -p and -i options at the same time", file=sys.stderr)
        return

    if args.pipe:
        input_stream = sys.stdin
    elif args.input:
        input_stream = open(args.input, 'r')
    else:
        print("Error: Either -p or -i option must be used", file=sys.stderr)
        return

    output = convertToCSV(input_stream, args.frontmatter)
    sys.stdout.write(output)

if __name__ == "__main__":
    main()