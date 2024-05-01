import unittest
import io
import csv
import os

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
        input_stream = io.StringIO("shape,description\nprocess,AND\nprocess,OR\nend,\nstart,")

        # Call the function
        output_stream = rename_shapes(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "shape,description\nor,\nsumming_function,\nterminator,\nstart_1,\n")

class TestInsertHeightWidth(unittest.TestCase):
    def test_insert_height_width(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("shape\nprocess\nor\nstart_1\nterminator")

        # Call the function
        output_stream = insert_height_width(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "shape,width,height\nprocess,200,100\nor,100,100\nstart_1,100,100\nterminator,100,50\n")

class TestParseDecisions(unittest.TestCase):
    def test_parse_decisions(self):
        # Prepare the input
        input_data = 'shape,next_step_id,connector_label\n' \
                     'decision,"1,2,3","option1,option2,option3"\n' \
                     'process,4,\n'
        input_stream = io.StringIO(input_data)

        # Call the function
        output_stream = parse_decisions(input_stream)

        # Check the output
        output_data = output_stream.getvalue()
        expected_output_data = 'shape,next_step_id,decision0_id,decision0_label,decision1_id,decision1_label,decision2_id,decision2_label\n' \
                               'decision,,1,option1,2,option2,3,option3\n' \
                               'process,4,,,,,,\n'
        self.assertEqual(output_data, expected_output_data)

class TestAddFrontmatter(unittest.TestCase):
    def setUp(self):
        # Create a dummy frontmatter file
        with open('tests/frontmatter.txt', 'w') as f:
            f.write('This is the frontmatter\n')
        print('file created')
        # Create a dummy input stream
        self.input_stream = io.StringIO('This is the main content\n')

    def test_add_frontmatter(self):
        # Call the function
        output_stream = add_frontmatter(self.input_stream, 'tests/frontmatter.txt')

        # Check the output
        self.assertEqual(output_stream.read(), 'This is the frontmatter\nThis is the main content\n')

    def tearDown(self):
        # Clean up the dummy frontmatter file
        os.remove('tests/frontmatter.txt')

class TestCsvToDrawio(unittest.TestCase):
    def test_csv_to_drawio(self):
        self.maxDiff = None
        # Read the test_drawio.csv file into a string stream
        with open('tests/test_drawio.csv', 'r') as file:
            input_stream = io.StringIO(file.read())

        # Call the csv_to_drawio function
        output_stream = csv_to_drawio(input_stream)

        # Read the test_drawio.drawio file
        with open('tests/test_drawio.drawio', 'r') as file:
            expected_output = file.read()

        # Compare the output to the expected output
        self.assertEqual(output_stream.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()