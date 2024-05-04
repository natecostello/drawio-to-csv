import xml.etree.ElementTree as ET
import io
import csv

# Define your large strings here
TEST_DRAWIO_FILE_DATA = """
<mxfile host="Electron" modified="2024-05-02T01:37:06.710Z" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/23.0.2 Chrome/120.0.6099.109 Electron/28.1.0 Safari/537.36" version="23.0.2" etag="9RgxjAd1FdjPu928ed5j">
  <diagram id="PrHAqnK2EjatVVtQv7mB" name="pageWithNumber">
    <mxGraphModel dx="-994" dy="-177" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="0" page="0" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="nate" description="This is a long task description like we would expect" status="todo" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="2" placeholders="1" id="2">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.process;html=1;" parent="1" vertex="1">
            <mxGeometry x="20" y="270" width="200" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="alan" description="Cell B" status="done" function="mechanical" phase="detail design" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="3" placeholders="1" id="3">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.decision;fillColor=#d5e8d4;strokeColor=#82b366;html=1;" parent="1" vertex="1">
            <mxGeometry x="470" y="70" width="100" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="Cell C" status="doing" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="4" placeholders="1" id="4">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.decision;fillColor=#fff2cc;strokeColor=#d6b656;html=1;" parent="1" vertex="1">
            <mxGeometry x="820" y="120" width="100" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="alan" description="Cell D - I would like to see what a long description on a predefined process looks like" status="waiting" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="5" placeholders="1" id="5">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.predefined_process;fillColor=#f5f5f5;strokeColor=#666666;html=1;" parent="1" vertex="1">
            <mxGeometry x="1120" y="270" width="200" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="Cell E" status="stop" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="6" placeholders="1" id="6">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.data;fillColor=#f8cecc;strokeColor=#b85450;html=1;" parent="1" vertex="1">
            <mxGeometry x="1120" y="70" width="200" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="" status="waiting" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="7" placeholders="1" id="7">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.summing_function;fillColor=#f5f5f5;strokeColor=#666666;html=1;" parent="1" vertex="1">
            <mxGeometry x="1520" y="270" width="100" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="Done" status="" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="8" placeholders="1" id="8">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.terminator;html=1;" parent="1" vertex="1">
            <mxGeometry x="1820" y="295" width="100" height="50" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="Repo" status="" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="9" placeholders="1" id="9">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.document;html=1;" parent="1" vertex="1">
            <mxGeometry x="420" y="470" width="200" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="" status="" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="10" placeholders="1" id="10">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.or;html=1;" parent="1" vertex="1">
            <mxGeometry x="1170" y="470" width="100" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="%description%&lt;br&gt;&lt;b&gt;%xl_id%&lt;/b&gt; - &lt;i&gt;%owner%&lt;/i&gt;&lt;br&gt;%estimated_completion_date%" owner="" description="start" status="" function="" phase="" estimated_duration="" estimated_completion_date="" notes="" wbs="" oqe="" xl_id="11" placeholders="1" id="11">
          <mxCell style="whiteSpace=wrap;shape=mxgraph.flowchart.start_1;html=1;" parent="1" vertex="1">
            <mxGeometry x="820" y="520" width="100" height="100" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="12" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="2" target="3" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="232" y="286.25" />
              <mxPoint x="408" y="120" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="13" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="2" target="4" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="234" y="308.75" />
              <mxPoint x="320" y="270" />
              <mxPoint x="720" y="270" />
              <mxPoint x="808" y="192.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="14" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="2" target="5" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="234" y="331.25" />
              <mxPoint x="320" y="370" />
              <mxPoint x="720" y="370" />
              <mxPoint x="720" y="320" />
              <mxPoint x="1020" y="320" />
              <mxPoint x="1108" y="342.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="15" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="2" target="9" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="232" y="353.75" />
              <mxPoint x="408" y="520" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="16" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="5" target="7" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1332" y="320" />
              <mxPoint x="1506" y="320" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="17" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="6" target="7" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1332" y="120" />
              <mxPoint x="1508" y="290" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="18" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="7" target="8" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1632" y="320" />
              <mxPoint x="1808" y="320" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="19" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="9" target="10" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="632" y="520" />
              <mxPoint x="720" y="420" />
              <mxPoint x="1020" y="420" />
              <mxPoint x="1108" y="497.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="20" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="10" target="7" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1332" y="520" />
              <mxPoint x="1508" y="350" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="21" value="" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="11" target="10" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="932" y="570" />
              <mxPoint x="1108" y="542.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="22" value="Yes" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="3" target="4" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="632" y="142.5" />
              <mxPoint x="808" y="147.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="23" value="Pass" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="4" target="6" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="932" y="147.5" />
              <mxPoint x="1108" y="142.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="24" value="No" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="3" target="6" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="632" y="97.5" />
              <mxPoint x="720" y="20" />
              <mxPoint x="1020" y="20" />
              <mxPoint x="1108" y="97.5" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="25" value="Fail" style="endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;" parent="1" source="4" target="5" edge="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="932" y="192.5" />
              <mxPoint x="1108" y="297.5" />
            </Array>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

TEST_DRAWIO_CSV_FILE_DATA = """id,owner,description,status,function,phase,estimated_duration,estimated_completion_date,notes,wbs,oqe,next_step_id,shape,xl_id,width,height,decision0_id,decision0_label,decision1_id,decision1_label
2,nate,This is a long task description like we would expect,todo,,,,,,,,"3,4,5,9",process,2,200,100,,,,
3,alan,Cell B,done,mechanical,detail design,,,,,,,decision,3,100,100,4,Yes,6,No
4,,Cell C,doing,,,,,,,,,decision,4,100,100,6,Pass,5,Fail
5,alan,Cell D - I would like to see what a long description on a predefined process looks like,waiting,,,,,,,,7,predefined_process,5,200,100,,,,
6,,Cell E,stop,,,,,,,,7,data,6,200,100,,,,
7,,,waiting,,,,,,,,8,summing_function,7,100,100,,,,
8,,Done,,,,,,,,,,terminator,8,100,50,,,,
9,,Repo,,,,,,,,,10,document,9,200,100,,,,
10,,,,,,,,,,,7,or,10,100,100,,,,
11,,start,,,,,,,,,10,start_1,11,100,100,,,,
"""

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
    line = next(reader, None)  # Return None if reader has no more items
    if line and line[0].startswith('#'):
        while line and line[0].startswith('#'):
            frontmatter.append(line)
            line = next(reader, None)  # Return None if reader has no more items
    
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