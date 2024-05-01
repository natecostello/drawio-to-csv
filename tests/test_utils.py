import unittest
import io

from drawio_xl.utils import delete_column
from drawio_xl.utils import delete_non_utf8
from drawio_xl.utils import delete_empty_cols
from drawio_xl.utils import delete_empty_rows


class TestDeleteColumn(unittest.TestCase):
    def test_delete_column(self):
        csv_content = io.StringIO("name,age,height\nAlice,20,160\nBob,25,175\n")
        expected_output = "name,age\nAlice,20\nBob,25\n"
        actual_output_stream = delete_column(csv_content, "height")
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output)

    def test_delete_nonexistent_column(self):
        csv_content = io.StringIO("name,age,height\nAlice,20,160\nBob,25,175\n")
        expected_output = "name,age,height\nAlice,20,160\nBob,25,175\n"
        actual_output_stream = delete_column(csv_content, "weight")
        actual_output = actual_output_stream.read()
        self.assertEqual(actual_output, expected_output)

class TestDeleteNonUTF8(unittest.TestCase):
    def test_delete_non_utf8(self):
        # Create a BytesIO object with some non-UTF-8 bytes
        input_stream = io.BytesIO(b'Hello, world!\x80\x81\x82')

        # Call the function
        output_stream = delete_non_utf8(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), 'Hello, world!')

class TestDeleteEmptyCols(unittest.TestCase):
    def test_delete_empty_cols(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("header1,,header3\nvalue1,,value3,,,")

        # Call the function
        output_stream = delete_empty_cols(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "header1,header3\nvalue1,value3\n")

class TestDeleteEmptyRows(unittest.TestCase):
    def test_delete_empty_rows(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("header1,header2,header3\nvalue1,value2,value3\n,,\nvalue4,value5,value6")

        # Call the function
        output_stream = delete_empty_rows(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "header1,header2,header3\nvalue1,value2,value3\nvalue4,value5,value6\n")

if __name__ == '__main__':
    unittest.main()