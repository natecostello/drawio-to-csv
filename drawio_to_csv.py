#!/usr/bin/env python3

import csv
import xml.etree.ElementTree as ET
import sys

def convertToCSV(filename):
    # Load and parse the XML
    tree = ET.parse(filename)
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
    full_fieldnames = [
        'id', 'owner', 'description', 'status', 'function', 'phase',
        'estimated_duration', 'estimated_completion_date', 'notes', 'wbs', 'oqe',
        'next_step_id', 'shape', 'width', 'height',
        'decision0_id', 'decision0_label', 'decision1_id', 'decision1_label',
        'decision2_id', 'decision2_label', 'xl_id'
    ]

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
                details = {
                    'id': element.get('id'),
                    'owner': element.get('owner', ''),
                    'description': element.get('description', ''),
                    'status': element.get('status', ''),
                    'function': element.get('function', ''),
                    'phase': element.get('phase', ''),
                    'estimated_duration': element.get('estimated_duration', ''),
                    'estimated_completion_date': element.get('estimated_completion_date', ''),
                    'notes': element.get('notes', ''),
                    'wbs': element.get('wbs', ''),
                    'oqe': element.get('oqe', ''),
                    'shape': shape,
                    'width': shape_dimensions.get(shape, ('100', '100'))[0],
                    'height': shape_dimensions.get(shape, ('100', '100'))[1],
                    'xl_id': element.get('xl_id', '')
                }
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

    # Hardcoded front matter as a string
    front_matter = """##
## **********************************************************
## Example description
## **********************************************************
## This example shows how you can use styles for shapes. There are three styles configured in the "styles" array: the first two are static styles, while "style3" uses the fill and stroke columns as parameters for fillColor and strokeColor. This shows how you can use a single style with varying parameters (see Cell C and Cell D). All these principles work the same for connectors.
## **********************************************************
## Configuration
## **********************************************************
# label: %description%<br><br><i>%owner%</i>
##
##
# styles: { \\
# "todo" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;html=1;", \\
# "doing" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#fff2cc;strokeColor=#d6b656;html=1;", \\
# "waiting" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#f5f5f5;strokeColor=#666666;html=1;", \\
# "done" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#d5e8d4;strokeColor=#82b366;html=1;", \\
# "stop" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#f8cecc;strokeColor=#b85450;html=1;", \\
# "" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;html=1;" }
# stylename: status
# namespace: csvimport-
# connect: {"from": "next_step_id", "to": "id"}
# connect: {"from": "decision0_id", "to": "id", "fromlabel": "decision0_label"}
# connect: {"from": "decision1_id", "to": "id", "fromlabel": "decision1_label"}
# connect: {"from": "decision2_id", "to": "id", "fromlabel": "decision2_label"}
# width: @width
# height: @height
# padding: 5
# ignore: id, next_step_id, shape, width, height, decision0_id, decision0_label, decision1_id, decision1_label, decision2_id, decision2_label
# link: url
# nodespacing: 60
# levelspacing: 60
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
##
## **********************************************************
"""

    # Write the final CSV with hardcoded front matter
    sys.stdout.write(front_matter)
    writer = csv.DictWriter(sys.stdout, fieldnames=full_fieldnames)
    writer.writeheader()
    for node in nodes:
        writer.writerow({key: node.get(key, '') for key in full_fieldnames})

def main(argv):
    if len(argv) != 2:
        print('Usage: drawio2csv.py <path_to_your_drawio_file.drawio>', file=sys.stderr)
        return
    convertToCSV(argv[1])

if __name__ == '__main__':
    main(sys.argv)