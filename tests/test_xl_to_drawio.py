import unittest
import io
import csv

from drawio_xl.xl_to_drawio import delete_non_utf8
from drawio_xl.xl_to_drawio import delete_empty_cols
from drawio_xl.xl_to_drawio import delete_empty_rows
from drawio_xl.xl_to_drawio import rename_headers

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

class TestRenameHeaders(unittest.TestCase):
    def test_rename_headers(self):
        # Create a StringIO object with some CSV data
        input_stream = io.StringIO("Process Step ID,Shape Type,Connector Label,Next Step ID,Some Other Header\n1,Rectangle,Label,2,Other Value")

        # Call the function
        output_stream = rename_headers(input_stream)

        # Check that the output is as expected
        self.assertEqual(output_stream.getvalue(), "id,shape,connector_label,next_step_id,some_other_header\n1,Rectangle,Label,2,Other Value\n")


if __name__ == '__main__':
    unittest.main()