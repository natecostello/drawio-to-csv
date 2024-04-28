import unittest
import io
from drawio_xl.drawio_to_xl import convert_to_csv  
from drawio_xl.drawio_to_xl import strip_front_matter  
from drawio_xl.drawio_to_xl import delete_column
from drawio_xl.drawio_to_xl import delete_height_width
from drawio_xl.drawio_to_xl import replace_ids_with_xl_ids  # replace with your function name


class TestConvertToCSV(unittest.TestCase):
    def test_convert_to_csv(self):
        # Remove the limit on the length of the diff message
        self.maxDiff = None

        # Specify the paths to the input, frontmatter, and expected output files
        input_file = 'tests/test_drawio.drawio'
        frontmatter_file = 'tests/test_frontmatter.txt'
        expected_output_file = 'tests/test_drawio.csv'

        # Open the input file and call the function
        with open(input_file, 'r') as input_stream:
            actual_output = convert_to_csv(input_stream, frontmatter_file)

        # Open the expected output file and read its contents
        with open(expected_output_file, 'r') as f:
            expected_output = f.read()

        # Check that the actual output matches the expected output
        self.assertEqual(actual_output.strip(), expected_output.strip())

class TestStripFrontMatter(unittest.TestCase):
    def test_strip_front_matter(self):
        input_data = io.StringIO("# This is a comment\nThis is not a comment\n# Another comment")
        expected_output = "This is not a comment\n"
        actual_output = strip_front_matter(input_data)
        self.assertEqual(actual_output, expected_output)

class TestDeleteColumn(unittest.TestCase):
    def test_delete_column(self):
        csv_content = "name,age,height\nAlice,20,160\nBob,25,175\n"
        expected_output = "name,age\nAlice,20\nBob,25\n"
        self.assertEqual(delete_column(csv_content, "height"), expected_output)

    def test_delete_nonexistent_column(self):
        csv_content = "name,age,height\nAlice,20,160\nBob,25,175\n"
        expected_output = csv_content  # The output should be unchanged
        self.assertEqual(delete_column(csv_content, "weight"), expected_output)

class TestDeleteHeightWidth(unittest.TestCase):
    def test_delete_height_width(self):
        csv_content = "name,age,height,width\nAlice,20,160,60\nBob,25,175,75\n"
        input_stream = io.StringIO(csv_content)
        expected_output = "name,age\nAlice,20\nBob,25\n"
        self.assertEqual(delete_height_width(input_stream), expected_output)

class TestReplaceIdsWithXlIdsYourFunction(unittest.TestCase):  
    def test_replace_ids_with_xl_ids(self):  
        csv_content = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n1,100,"2,3",3,4,5\n2,200,1,3,4,5\n3,300,1,2,4,5\n4,400,1,2,3,5\n5,500,1,2,3,4\n'
        input_stream = io.StringIO(csv_content)
        expected_output = 'id,xl_id,next_step_id,decision0_id,decision1_id,decision2_id\n100,100,"200,300",300,400,500\n200,200,100,300,400,500\n300,300,100,200,400,500\n400,400,100,200,300,500\n500,500,100,200,300,400\n'
        self.assertEqual(replace_ids_with_xl_ids(input_stream), expected_output) 

if __name__ == '__main__':
    unittest.main()