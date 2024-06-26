import unittest
import io
import subprocess
import os
import csv
from tests.testing_support import normalize_csv
from tests.testing_support import TEST_DRAWIO_FILE_DATA
from tests.testing_support import TEST_DRAWIO_CSV_FILE_DATA
from tests.testing_support import TEST_XL_FILE_DATA

from drawio_xl.drawio_to_xl import convert_to_csv  
from drawio_xl.drawio_to_xl import strip_front_matter  
from drawio_xl.drawio_to_xl import delete_height_width
from drawio_xl.drawio_to_xl import replace_ids_with_xl_ids  
from drawio_xl.drawio_to_xl import delete_xl_ids  
from drawio_xl.drawio_to_xl import rename_shapes
from drawio_xl.drawio_to_xl import parse_decisions
from drawio_xl.drawio_to_xl import insert_newlines
from drawio_xl.drawio_to_xl import rename_headers
from drawio_xl.drawio_to_xl import reorder_headers
from drawio_xl.drawio_to_xl import drawio_to_xl

class TestConvertToCSV(unittest.TestCase):    
    def test_convert_to_csv(self):
        # Remove the limit on the length of the diff message
        self.maxDiff = None

        # create the input stream and output stream from the test data
        input_stream = io.StringIO(TEST_DRAWIO_FILE_DATA)
        actual_output_stream = convert_to_csv(input_stream)
        actual_output = actual_output_stream.read()
        
        expected_output = TEST_DRAWIO_CSV_FILE_DATA
        
        # Check that the actual output matches the expected output
        self.assertEqual(normalize_csv(actual_output), normalize_csv(expected_output))
        
class TestStripFrontMatter(unittest.TestCase):
    def test_strip_front_matter(self):
        input_data = io.StringIO("# This is a comment\nThis is not a comment\n# Another comment")
        expected_output = "This is not a comment\n"
        actual_output_stream = strip_front_matter(input_data)
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output)

class TestDeleteHeightWidth(unittest.TestCase):
    def test_delete_height_width(self):
        csv_content = io.StringIO("name,age,height,width\nAlice,20,160,60\nBob,25,175,75\n")
        expected_output = "name,age\nAlice,20\nBob,25\n"
        actual_output_stream = delete_height_width(csv_content)
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output)

class TestReplaceIdsWithXlId(unittest.TestCase):  
    def test_replace_ids_with_xl_ids(self):  
        csv_content = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n1,100,"2,3",3,4,5\n2,200,1,3,4,5\n3,300,1,2,4,5\n4,400,1,2,3,5\n5,500,1,2,3,4\n'
        input_stream = io.StringIO(csv_content)
        expected_output = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n100,100,"200,300",300,400,500\n200,200,100,300,400,500\n300,300,100,200,400,500\n400,400,100,200,300,500\n500,500,100,200,300,400\n'
        actual_output_stream = replace_ids_with_xl_ids(input_stream)
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output) 
    
    def test_replace_ids_with_xl_ids_empty_xl_id(self):
        csv_content = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n1,,2,3,4,5\n2,200,1,3,4,5\n3,300,1,2,4,5\n4,400,1,2,3,5\n5,500,1,2,3,4\n'
        input_stream = io.StringIO(csv_content)
        expected_output = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n1,,2,3,4,5\n2,200,1,3,4,5\n3,300,1,2,4,5\n4,400,1,2,3,5\n5,500,1,2,3,4\n'
        actual_output_stream = replace_ids_with_xl_ids(input_stream)
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output)

class TestDeleteXlIds(unittest.TestCase):
    def test_delete_xl_ids(self):
        csv_content = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n100,100,"200,300",300,400,500\n200,200,100,300,400,500\n300,300,100,200,400,500\n400,400,100,200,300,500\n500,500,100,200,300,400\n'
        input_stream = io.StringIO(csv_content)
        expected_output = 'id,next_step_id,decision0_id,decision1_id,decision2_id\n100,"200,300",300,400,500\n200,100,300,400,500\n300,100,200,400,500\n400,100,200,300,500\n500,100,200,300,400\n'
        actual_output_stream = delete_xl_ids(input_stream)
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output)

class TestRenameShapes(unittest.TestCase):
    def test_rename_shapes(self):
        input_data = """id,shape,next_step_id,decision0_id,decision1_id,decision2_id
100,mxgraph.flowchart.start_1,"200,300",300,400,500
200,mxgraph.flowchart.terminator,100,300,400,500
300,mxgraph.flowchart.summing_function,100,200,400,500
400,mxgraph.flowchart.or,100,200,300,500
500,mxgraph.flowchart.Ellipse,100,200,300,400
"""
        expected_output = """id,shape,next_step_id,decision0_id,decision1_id,decision2_id
100,start,"200,300",300,400,500
200,end,100,300,400,500
300,custom 1,100,200,400,500
400,custom 2,100,200,300,500
500,mxgraph.flowchart.Ellipse,100,200,300,400
"""
        input_stream = io.StringIO(input_data)
        expected_output_stream = io.StringIO(expected_output)

        actual_output_stream = rename_shapes(input_stream)

        self.assertEqual(actual_output_stream.getvalue(), expected_output_stream.getvalue())

class TestParseDecisions(unittest.TestCase):
    def test_parse_decisions(self):
        self.maxDiff = None
        input_data = """shape,next_step_id,decision0_id,decision0_label,decision1_id,decision1_label,decision2_id,decision2_label
mxgraph.flowchart.decision,,id0,label0,id1,label1,id2,label2
other,step_id,,,,,,
mxgraph.flowchart.decision,,id3,label3,id4,label4,id5,label5
"""
        expected_output = """shape,next_step_id,connector_label
mxgraph.flowchart.decision,"id0, id1, id2","label0, label1, label2"
other,step_id,
mxgraph.flowchart.decision,"id3, id4, id5","label3, label4, label5"
"""
        input_stream = io.StringIO(input_data)
        output_stream = parse_decisions(input_stream)
        self.assertEqual(expected_output, output_stream.getvalue())

class TestInsertNewlines(unittest.TestCase):
    def test_insert_newlines(self):
        self.maxDiff = None
        input_data = """shape,next_step_id,decision
decision,,id0<br>id1<br>id2
other,step_id,
decision,,id3<br>id4<br>id5
"""
        expected_output = """shape,next_step_id,decision
decision,,"id0
id1
id2"
other,step_id,
decision,,"id3
id4
id5"
"""
        input_stream = io.StringIO(input_data)
        output_stream = insert_newlines(input_stream)
        self.assertEqual(expected_output, output_stream.getvalue())


class TestRenameHeaders(unittest.TestCase):
    def test_rename_headers(self):
        input_data = """id,shape,connector_label,next_step_id,other_header
1,decision,label1,2,other_value
"""
        expected_output = """Process Step ID,Shape Type,Connector Label,Next Step ID,Other Header
1,decision,label1,2,other_value
"""
        input_stream = io.StringIO(input_data)
        output_stream = rename_headers(input_stream)
        self.assertEqual(expected_output, output_stream.getvalue())

class TestReorderHeaders(unittest.TestCase):
    def test_reorder_headers(self):
        input_data = """Description,Owner,Process Step ID,Notes,Status
desc1,owner1,1,note1,status1
desc2,owner2,2,note2,status2
"""
        expected_output = """Process Step ID,Owner,Description,Status,Notes
1,owner1,desc1,status1,note1
2,owner2,desc2,status2,note2
"""
        input_stream = io.StringIO(input_data)
        output_stream = reorder_headers(input_stream)
        self.assertEqual(expected_output, output_stream.getvalue())

class TestDrawioToXl(unittest.TestCase):
    def test_drawio_to_xl(self):
        self.maxDiff = None
        
        input_stream = io.StringIO(TEST_DRAWIO_FILE_DATA)

        expected_output = TEST_XL_FILE_DATA

        # Call the function and get the actual output
        output_stream = drawio_to_xl(input_stream)
        actual_output = output_stream.getvalue()

        # Compare the actual output with the expected output
        self.assertEqual(expected_output, actual_output)


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        self.output_file = 'tests/test_output.csv'
        # write the test input file from TEST_DRAWIO_FILE_DATA
        with open('tests/test_input.drawio', 'w') as f:
            f.write(TEST_DRAWIO_FILE_DATA)
        self.input_file = 'tests/test_input.drawio'

    def test_drawio_to_xl(self):
        self.maxDiff = None
        # Call the script with the input and output files
        result = subprocess.run(['python3', 'drawio_xl/drawio_to_xl.py', self.input_file, self.output_file], capture_output=True)

        # Check if the script exited without errors
        self.assertEqual(result.returncode, 0)

        # Check if the output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Read the output file and the expected output file
        with open(self.output_file, 'r') as f:
            output = f.read()
        
        expected_output = TEST_XL_FILE_DATA

        # Check if the output matches the expected output
        self.assertEqual(output, expected_output)

    def tearDown(self):
        # Delete the output file
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        # Delete the input file
        if os.path.exists(self.input_file):
            os.remove(self.input_file)

if __name__ == '__main__':
    unittest.main()