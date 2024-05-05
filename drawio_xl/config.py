from dataclasses import dataclass, field

# Define your large string here
STATIC_FRONTMATTER = """## ******Static Frontmatter*******
# label: %description%<br><b>%xl_id%</b> - <i>%owner%</i><br>%estimated_completion_date%
# styles: { \\
# "todo" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;html=1;", \\
# "doing" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#fff2cc;strokeColor=#d6b656;html=1;", \\
# "waiting" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#f5f5f5;strokeColor=#666666;html=1;", \\
# "done" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#d5e8d4;strokeColor=#82b366;html=1;", \\
# "stop" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;fillColor=#f8cecc;strokeColor=#b85450;html=1;", \\
# "" : "whiteSpace=wrap;shape=mxgraph.flowchart.%shape%;html=1;" }
# stylename: status
# namespace: csvimport-
# width: @width
# height: @height
# padding: 5
# link: url
# nodespacing: 100
# levelspacing: 200
# edgespacing: 40
# layout: horizontalflow
"""

@dataclass
class Config:
    static_frontmatter: str = STATIC_FRONTMATTER
    connector_style: str = "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"
    shape_dimensions: dict = field(default_factory=lambda: {
        'process': ('200', '100'),
        'decision': ('100', '100'),
        'data': ('200', '100'),  
        'predefined_process': ('200', '100'),
        'terminator': ('100', '50'),
        'document': ('200', '100'),
        'or': ('100', '100'),
        'summing_function': ('100', '100'),
        'start': ('100', '100'),
    })
    xl_to_drawio_shape_mapping: dict = field(default_factory=lambda: {
        'process': 'process',
        'decision': 'decision',
        'data': 'data',
        'document': 'document',
        'subprocess': 'predefined_process',
        'start': 'start_1',
        'end': 'terminator',
        'custom 1': 'summing_function',
        'custom 2': 'or',
    })
    drawio_to_xl_shape_mapping: dict = field(default_factory=lambda: {
        'process': 'process',
        'decision': 'decision',
        'data': 'data',
        'document': 'document',
        'predefined_process': 'subprocess',
        'start_1': 'start',
        'terminator': 'end',
        'summing_function': 'custom 1',
        'or': 'custom 2',
    })