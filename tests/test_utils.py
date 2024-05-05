import unittest
import io

from drawio_xl.utils import delete_column
from drawio_xl.utils import delete_non_utf8
from drawio_xl.utils import delete_empty_cols
from drawio_xl.utils import delete_empty_rows
from drawio_xl.utils import get_max_decision_count_from_headers
from drawio_xl.utils import get_max_decision_count_from_rows
from drawio_xl.utils import get_connect_frontmatter
from drawio_xl.utils import get_ignore_frontmatter


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


class TestGetMaxDecisionCountFromRows(unittest.TestCase):
    def test_get_max_decision_count_from_rows(self):
        headers = ['shape', 'next_step_id', 'connector_label']
        rows = [
            ['decision', '1,2,3', 'label1'],
            ['decision', '4,5', 'label2'],
            ['action', '6,7,8,9', 'label3'],
            ['decision', '10,11,12,13,14', 'label4'],
            ['action', '15', 'label5']
        ]
        result = get_max_decision_count_from_rows(rows, headers)
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()

class TestGetMaxDecisionCountFromHeaders(unittest.TestCase):
    def test_get_max_decision_count_from_headers(self):
        headers = ['decision1_id', 'decision1_label', 'decision2_id', 'decision2_label', 'decision3_id', 'decision3_label']
        self.assertEqual(get_max_decision_count_from_headers(headers), 4)

        headers = ['decision0_id', 'decision0_label']
        self.assertEqual(get_max_decision_count_from_headers(headers), 1)

        headers = ['id', 'label']
        self.assertEqual(get_max_decision_count_from_headers(headers), 0)

class TestGetConnectFrontmatter(unittest.TestCase):
    def test_get_connect_frontmatter(self):
        connector_style = "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"
        expected_output = '# connect: {"from": "next_step_id", "to": "id", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}\n' \
                          '# connect: {"from": "decision0_id", "to": "id", "fromlabel": "decision0_label", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}\n' \
                          '# connect: {"from": "decision1_id", "to": "id", "fromlabel": "decision1_label", "style": "endArrow=blockThin;endFill=1;fontSize=11;edgeStyle=orthogonalEdgeStyle;"}\n'
        self.assertEqual(get_connect_frontmatter(2, connector_style), expected_output)

class TestGetIgnoreFrontmatter(unittest.TestCase):
    def test_get_ignore_frontmatter(self):
        expected_output = '# ignore: id, next_step_id, shape, width, height, decision0_id, decision0_label, decision1_id, decision1_label, decision2_id, decision2_label\n'
        self.assertEqual(get_ignore_frontmatter(3), expected_output)

        expected_output = '# ignore: id, next_step_id, shape, width, height\n'
        self.assertEqual(get_ignore_frontmatter(0), expected_output)

if __name__ == '__main__':
    unittest.main()