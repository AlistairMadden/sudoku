import json
import unittest

import util


class TestReadSudokuFromFile(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_file(self):
        expected_output = {
            "sudokus": [
                [
                    8,
                    None,
                    None,
                    9,
                    3,
                    None,
                    None,
                    None,
                    2,
                    None,
                    None,
                    9,
                    None,
                    None,
                    None,
                    None,
                    4,
                    None,
                    7,
                    None,
                    2,
                    1,
                    None,
                    None,
                    9,
                    6,
                    None,
                    2,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    9,
                    None,
                    None,
                    6,
                    None,
                    None,
                    None,
                    None,
                    None,
                    7,
                    None,
                    None,
                    7,
                    None,
                    None,
                    None,
                    6,
                    None,
                    None,
                    5,
                    None,
                    2,
                    7,
                    None,
                    None,
                    8,
                    4,
                    None,
                    6,
                    None,
                    3,
                    None,
                    None,
                    None,
                    None,
                    5,
                    None,
                    None,
                    5,
                    None,
                    None,
                    None,
                    6,
                    2,
                    None,
                    None,
                    8
                ]
            ]
        }

        actual_output = util.read_sudoku_from_file('sudokus_test_util.json')

        self.assertEqual(actual_output, expected_output)

    def test_invalid_file(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            util.read_sudoku_from_file(__file__)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            util.read_sudoku_from_file('notafile')
