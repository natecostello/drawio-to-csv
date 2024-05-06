from dataclasses import dataclass, field

# Define your large string here
STATIC_FRONTMATTER = """## ******Static Frontmatter*******
# label: %description%<br><b>%xl_id%</b> - <i>%owner%</i><br>%estimated_completion_date%
# styles: { \\
# "todo" : "whiteSpace=wrap;shape=%shape%;html=1;", \\
# "doing" : "whiteSpace=wrap;shape=%shape%;fillColor=#fff2cc;strokeColor=#d6b656;html=1;", \\
# "waiting" : "whiteSpace=wrap;shape=%shape%;fillColor=#f5f5f5;strokeColor=#666666;html=1;", \\
# "done" : "whiteSpace=wrap;shape=%shape%;fillColor=#d5e8d4;strokeColor=#82b366;html=1;", \\
# "stop" : "whiteSpace=wrap;shape=%shape%;fillColor=#f8cecc;strokeColor=#b85450;html=1;", \\
# "" : "whiteSpace=wrap;shape=%shape%;html=1;" }
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
    drawio_path: str = "/Applications/draw.io.app/Contents/MacOS/draw.io"
    static_frontmatter: str = STATIC_FRONTMATTER
    connector_style: str = "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"
    shape_dimensions: dict = field(default_factory=lambda: {
        'mxgraph.flowchart.process': ('200', '100'),
        'mxgraph.flowchart.decision': ('100', '100'),
        'mxgraph.flowchart.data': ('200', '100'),  
        'mxgraph.flowchart.predefined_process': ('200', '100'),
        'mxgraph.flowchart.terminator': ('100', '50'),
        'mxgraph.flowchart.document': ('200', '100'),
        'mxgraph.flowchart.or': ('100', '100'),
        'mxgraph.flowchart.summing_function': ('100', '100'),
        'mxgraph.flowchart.start': ('100', '100'),
    })
    xl_to_drawio_shape_mapping: dict = field(default_factory=lambda: {
        'process': 'mxgraph.flowchart.process',
        'decision': 'mxgraph.flowchart.decision',
        'data': 'mxgraph.flowchart.data',
        'document': 'mxgraph.flowchart.document',
        'subprocess': 'mxgraph.flowchart.predefined_process',
        'start': 'mxgraph.flowchart.start_1',
        'end': 'mxgraph.flowchart.terminator',
        'custom 1': 'mxgraph.flowchart.summing_function',
        'custom 2': 'mxgraph.flowchart.or',
    })
    drawio_to_xl_shape_mapping: dict = field(default_factory=lambda: {
        'mxgraph.flowchart.process': 'process',
        'mxgraph.flowchart.decision': 'decision',
        'mxgraph.flowchart.data': 'data',
        'mxgraph.flowchart.document': 'document',
        'mxgraph.flowchart.predefined_process': 'subprocess',
        'mxgraph.flowchart.start_1': 'start',
        'mxgraph.flowchart.terminator': 'end',
        'mxgraph.flowchart.summing_function': 'custom 1',
        'mxgraph.flowchart.or': 'custom 2',
    })