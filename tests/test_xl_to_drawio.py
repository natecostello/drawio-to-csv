import unittest
import io
import csv
import os
from xml.etree import ElementTree as ET
import subprocess
from tests.testing_support import normalize_xml
from tests.testing_support import TEST_DRAWIO_FILE_DATA
from tests.testing_support import TEST_DRAWIO_CSV_FILE_DATA
from tests.testing_support import TEST_XL_FILE_DATA


from drawio_xl.utils import get_max_decision_count_from_headers, get_connect_frontmatter, get_ignore_frontmatter
from drawio_xl.config import Config


from drawio_xl.xl_to_drawio import rename_headers
from drawio_xl.xl_to_drawio import lower_shape_case
from drawio_xl.xl_to_drawio import lower_status_case
from drawio_xl.xl_to_drawio import replace_newlines
from drawio_xl.xl_to_drawio import save_id
from drawio_xl.xl_to_drawio import rename_shapes
from drawio_xl.xl_to_drawio import insert_height_width
from drawio_xl.xl_to_drawio import parse_decisions
from drawio_xl.xl_to_drawio import add_frontmatter
from drawio_xl.xl_to_drawio import csv_to_drawio
from drawio_xl.xl_to_drawio import xl_to_drawio
from drawio_xl.xl_to_drawio import add_frontmatter


class TestRenameHeaders(unittest.TestCase):
    def test_rename_headers(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("Process Step ID,Shape Type,Connector Label,Next Step ID,Some Other Header\n1,Rectangle,Label,2,Other Value")

        # Call the function
        output_stream = rename_headers(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "id,shape,connector_label,next_step_id,some_other_header\n1,Rectangle,Label,2,Other Value\n")

class TestFixShapeCase(unittest.TestCase):
    def test_lower_shape_case(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("id,shape,connector_label,next_step_id\n1,Rectangle,Label,2")

        # Call the function
        output_stream = lower_shape_case(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "id,shape,connector_label,next_step_id\n1,rectangle,Label,2\n")

class TestLowerStatusCase(unittest.TestCase):
    def test_lower_status_case(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("id,shape,connector_label,next_step_id,status\n1,Rectangle,Label,2,ACTIVE")

        # Call the function
        output_stream = lower_status_case(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "id,shape,connector_label,next_step_id,status\n1,Rectangle,Label,2,active\n")

class TestReplaceNewlines(unittest.TestCase):
    def test_replace_newlines(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO('id,shape,connector_label,next_step_id,status\n1,Rectangle,"Label\nLabel2",2,ACTIVE')

        # Call the function
        output_stream = replace_newlines(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), 'id,shape,connector_label,next_step_id,status\n1,Rectangle,Label<br>Label2,2,ACTIVE\n')

class TestSaveId(unittest.TestCase):
    def test_save_id(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("id,shape,connector_label,next_step_id,status\n1,Rectangle,Label,2,ACTIVE")

        # Call the function
        output_stream = save_id(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "id,shape,connector_label,next_step_id,status,xl_id\n1,Rectangle,Label,2,ACTIVE,1\n")

class TestRenameShapes(unittest.TestCase):
    def test_rename_shapes(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("shape\nstart\ncustom 1\ncustom 2\nend")

        # Call the function
        output_stream = rename_shapes(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "shape\nmxgraph.flowchart.start_1\nmxgraph.flowchart.summing_function\nmxgraph.flowchart.or\nmxgraph.flowchart.terminator\n")
        
    def test_rename_shapes_no_renaming(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("shape\nmxgraph.flowchart.rectangle\nmxgraph.flowchart.circle")

        # Call the function
        output_stream = rename_shapes(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "shape\nmxgraph.flowchart.rectangle\nmxgraph.flowchart.circle\n")
        
    def test_rename_shapes_empty_input(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("shape\n")

        # Call the function
        output_stream = rename_shapes(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "shape\n")

class TestInsertHeightWidth(unittest.TestCase):
    def test_insert_height_width(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("shape\nmxgraph.flowchart.process\nmxgraph.flowchart.or\nmxgraph.flowchart.start_1\nmxgraph.flowchart.terminator")

        # Call the function
        output_stream = insert_height_width(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "shape,width,height\nmxgraph.flowchart.process,200,100\nmxgraph.flowchart.or,100,100\nmxgraph.flowchart.start_1,100,100\nmxgraph.flowchart.terminator,100,50\n")

class TestParseDecisions(unittest.TestCase):
    def test_parse_decisions(self):
        # Prepare the input
        input_data = 'shape,next_step_id,connector_label\n' \
                     'mxgraph.flowchart.decision,"1,2,3","option1,option2,option3"\n' \
                     'mxgraph.flowchart.process,4,\n'
        input_stream = io.StringIO(input_data)

        # Call the function
        output_stream = parse_decisions(input_stream)

        # Check the output
        output_data = output_stream.getvalue()
        expected_output_data = 'shape,next_step_id,decision0_id,decision0_label,decision1_id,decision1_label,decision2_id,decision2_label\n' \
                               'mxgraph.flowchart.decision,,1,option1,2,option2,3,option3\n' \
                               'mxgraph.flowchart.process,4,,,,,,\n'
        self.assertEqual(output_data, expected_output_data)

class TestAddFrontmatter(unittest.TestCase):
    def test_add_frontmatter(self):
        # Create a sample input stream
        input_data = "header1,header2,header3,decision0_id,decision0_label,decision1_id,decision1_label\nrow1,row2,row3,0_id,0_label,1_id,1_label\n"
        input_stream = io.StringIO(input_data)

        # Create a Config instance
        config_instance = Config()

        # Calculate the expected max_decision_count and frontmatter_content
        reader = csv.reader(io.StringIO(input_data))
        headers = next(reader)
        expected_max_decision_count = get_max_decision_count_from_headers(headers)
        expected_frontmatter_content = config_instance.static_frontmatter + \
                                       get_connect_frontmatter(expected_max_decision_count, config_instance.connector_style) + \
                                       get_ignore_frontmatter(expected_max_decision_count)

        # Call the add_frontmatter function
        output_stream = add_frontmatter(input_stream)

        # Read the output stream
        output_data = output_stream.read()
        
        # Check that the output data starts with the expected frontmatter content
        self.assertTrue(output_data.startswith(expected_frontmatter_content))

        # Check that the output data ends with the input stream data
        self.assertTrue(output_data.endswith(input_data))

class TestCsvToDrawio(unittest.TestCase):
    def test_csv_to_drawio(self):
        self.maxDiff = None
        
        # Set up the input stream
        input_stream = io.StringIO(TEST_DRAWIO_CSV_FILE_DATA)
        # Add the frontmatter to the input stream
        input_stream = add_frontmatter(input_stream)

        # Call the csv_to_drawio function
        output_stream = csv_to_drawio(input_stream)
        
        # Setup the expected output
        expected_output = TEST_DRAWIO_FILE_DATA

        # Compare the output to the expected output (only look inside root node)
        self.assertEqual(normalize_xml(output_stream.getvalue()), normalize_xml(expected_output))

class TestXlToDrawio(unittest.TestCase):
    def test_xl_to_drawio(self):
        self.maxDiff = None
        
        input_stream = io.StringIO(TEST_XL_FILE_DATA)

        output_stream = xl_to_drawio(input_stream)

        expected_output = TEST_DRAWIO_FILE_DATA

        # Compare the output to the expected output
        self.assertEqual(normalize_xml(output_stream.getvalue()), normalize_xml(expected_output))

class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        self.output_file = 'tests/test_output.drawio'

        # write the test input file from TEST_XL_FILE_DATA
        with open('tests/test_input.csv', 'w') as f:
            f.write(TEST_XL_FILE_DATA)
        self.input_file = 'tests/test_input.csv'

    def test_xl_to_drawio(self):
        self.maxDiff = None

        # Call the script with the input and output files
        result = subprocess.run(['python3', 'drawio_xl/xl_to_drawio.py', self.input_file, self.output_file], capture_output=True)
        
        # Check if the script exited without errors
        self.assertEqual(result.returncode, 0)

        # Check if the output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Read the output file and the expected output file
        with open(self.output_file, 'r') as f:
            output = f.read()
        expected_output = TEST_DRAWIO_FILE_DATA

        # Check if the output matches the expected output
        self.assertEqual(normalize_xml(output), normalize_xml(expected_output))

    def tearDown(self):
        # Delete the output file
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        # Delete the input file
        if os.path.exists(self.input_file):
            os.remove(self.input_file)

if __name__ == '__main__':
    unittest.main()