import unittest

from util import read_sudoku_from_file
from sudoku_types import StandardSudoku


TEST_SUDOKU_DATA = read_sudoku_from_file('sudokus_test.json')


class TestStandardSudokuMethods(unittest.TestCase):
    def setUp(self):
        self.standard_soduku_instance = StandardSudoku(TEST_SUDOKU_DATA['sudokus'][0])

    def test_instantiate(self):
        self.assertEqual(list(map(lambda cell: cell.value, self.standard_soduku_instance)), TEST_SUDOKU_DATA['sudokus'][0])

    def test_get_box_index(self):
        test_cases = [
            {
                'cell_index': 0,
                'box_index': 0
            },
            {
                'cell_index': 11,
                'box_index': 0
            },
            {
                'cell_index': 20,
                'box_index': 0
            },
            {
                'cell_index': 3,
                'box_index': 1
            },
            {
                'cell_index': 12,
                'box_index': 1
            },
            {
                'cell_index': 23,
                'box_index': 1
            }
        ]

        for test_case in test_cases:
            # import IPython
            # IPython.embed()
            actual_index = self.standard_soduku_instance.get_box_index(test_case['cell_index'])
            self.assertEqual(actual_index, test_case['box_index'])

    def test_get_cells_in_row(self):
        test_cases = [
            {
                'index': 0,
                'cell_values': [
                    8,
                    None,
                    None,
                    9,
                    3,
                    None,
                    None,
                    None,
                    2
                ]
            }
        ]

        for test_case in test_cases:
            self.check_get(self.standard_soduku_instance.get_cells_in_row, test_case)

    def test_get_cells_in_column(self):
        test_cases = [
            {
                'index': 0,
                'cell_values': [
                    8,
                    None,
                    7,
                    2,
                    None,
                    None,
                    None,
                    None,
                    5
                ]
            }
        ]

        for test_case in test_cases:
            self.check_get(self.standard_soduku_instance.get_cells_in_column, test_case)

    def test_get_cells_in_box(self):
        test_cases = [
            {
                'index': 0,
                'cell_values': [
                    8,
                    None,
                    None,
                    None,
                    None,
                    9,
                    7,
                    None,
                    2
                ]
            }
        ]

        for test_case in test_cases:
            self.check_get(self.standard_soduku_instance.get_cells_in_box, test_case)

    def check_get(self, check_function, data):
        actual_cells = check_function(data['index'])

        self.assertEqual(list(map(lambda cell: cell.value, actual_cells)), data['cell_values'])

    def test_eliminate_column_values(self):
        test_cases = [
            {
                'viable_values': [
                    [],
                    [1, 4, 5, 8, 9],
                    [1, 3, 4, 5, 6, 8],
                    [],
                    [],
                    [1, 3, 4, 5, 7, 9],
                    [1, 2, 3, 6, 7, 8],
                    [1, 2, 3, 5, 8],
                    [],
                    [1, 3, 4, 6, 9],
                    [1, 4, 5, 8, 9],
                    [],
                    [2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 4, 5, 7, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [1, 2, 3, 6, 7, 8],
                    [],
                    [1, 3, 4, 7, 9],
                    [],
                    [1, 4, 5, 8, 9],
                    [],
                    [],
                    [1, 2, 4, 5, 7, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [],
                    [],
                    [1, 3, 4, 7, 9],
                    [],
                    [1, 4, 5, 8, 9],
                    [1, 3, 4, 5, 6, 8],
                    [2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 4, 5, 7, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [1, 2, 3, 6, 7, 8],
                    [],
                    [1, 3, 4, 7, 9],
                    [1, 3, 4, 6, 9],
                    [],
                    [1, 3, 4, 5, 6, 8],
                    [2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 4, 5, 7, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [1, 2, 3, 6, 7, 8],
                    [],
                    [1, 3, 4, 7, 9],
                    [1, 3, 4, 6, 9],
                    [],
                    [1, 3, 4, 5, 6, 8],
                    [2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 4, 5, 7, 8, 9],
                    [],
                    [1, 2, 3, 6, 7, 8],
                    [1, 2, 3, 5, 8],
                    [],
                    [1, 3, 4, 6, 9],
                    [],
                    [],
                    [2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 4, 5, 7, 8, 9],
                    [],
                    [],
                    [1, 2, 3, 5, 8],
                    [],
                    [1, 3, 4, 6, 9],
                    [],
                    [1, 3, 4, 5, 6, 8],
                    [2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 4, 5, 7, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [],
                    [1, 2, 3, 5, 8],
                    [1, 3, 4, 7, 9],
                    [],
                    [1, 4, 5, 8, 9],
                    [1, 3, 4, 5, 6, 8],
                    [2, 3, 4, 5, 6, 7, 8],
                    [],
                    [],
                    [1, 2, 3, 6, 7, 8],
                    [1, 2, 3, 5, 8],
                    []
                ]
            }
        ]
        for test_case in test_cases:
            self.standard_soduku_instance.eliminate_column_values()
            viable_values = list(map(lambda cell: cell.viable_values, self.standard_soduku_instance.cells))
            self.assertEqual(viable_values, test_case['viable_values'])

            # Should not change if run again
            self.standard_soduku_instance.eliminate_column_values()
            self.assertEqual(viable_values, test_case['viable_values'])

    def test_eliminate_row_values(self):
        test_cases = [
            {
                'viable_values': [
                    [],
                    [1, 4, 5, 6, 7],
                    [1, 4, 5, 6, 7],
                    [],
                    [],
                    [1, 4, 5, 6, 7],
                    [1, 4, 5, 6, 7],
                    [1, 4, 5, 6, 7],
                    [],
                    [1, 2, 3, 5, 6, 7, 8],
                    [1, 2, 3, 5, 6, 7, 8],
                    [],
                    [1, 2, 3, 5, 6, 7, 8],
                    [1, 2, 3, 5, 6, 7, 8],
                    [1, 2, 3, 5, 6, 7, 8],
                    [1, 2, 3, 5, 6, 7, 8],
                    [],
                    [1, 2, 3, 5, 6, 7, 8],
                    [],
                    [3, 4, 5, 8],
                    [],
                    [],
                    [3, 4, 5, 8],
                    [3, 4, 5, 8],
                    [],
                    [],
                    [3, 4, 5, 8],
                    [],
                    [1, 3, 4, 5, 6, 7, 8],
                    [1, 3, 4, 5, 6, 7, 8],
                    [1, 3, 4, 5, 6, 7, 8],
                    [1, 3, 4, 5, 6, 7, 8],
                    [1, 3, 4, 5, 6, 7, 8],
                    [1, 3, 4, 5, 6, 7, 8],
                    [],
                    [1, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 8, 9],
                    [],
                    [1, 2, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 8, 9],
                    [],
                    [1, 2, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 8, 9],
                    [],
                    [1, 2, 3, 4, 8, 9],
                    [1, 2, 3, 4, 8, 9],
                    [1, 2, 3, 4, 8, 9],
                    [],
                    [1, 2, 3, 4, 8, 9],
                    [1, 2, 3, 4, 8, 9],
                    [],
                    [1, 3, 5, 9],
                    [],
                    [],
                    [1, 3, 5, 9],
                    [1, 3, 5, 9],
                    [],
                    [],
                    [1, 3, 5, 9],
                    [],
                    [1, 2, 4, 6, 7, 8, 9],
                    [],
                    [1, 2, 4, 6, 7, 8, 9],
                    [1, 2, 4, 6, 7, 8, 9],
                    [1, 2, 4, 6, 7, 8, 9],
                    [1, 2, 4, 6, 7, 8, 9],
                    [],
                    [1, 2, 4, 6, 7, 8, 9],
                    [1, 2, 4, 6, 7, 8, 9],
                    [],
                    [1, 3, 4, 7, 9],
                    [1, 3, 4, 7, 9],
                    [1, 3, 4, 7, 9],
                    [],
                    [],
                    [1, 3, 4, 7, 9],
                    [1, 3, 4, 7, 9],
                    []
                ]
            }
        ]

        for test_case in test_cases:
            self.standard_soduku_instance.eliminate_row_values()
            viable_values = list(map(lambda cell: cell.viable_values, self.standard_soduku_instance.cells))
            self.assertEqual(viable_values, test_case['viable_values'])

            # Should not change if run again
            self.standard_soduku_instance.eliminate_row_values()
            self.assertEqual(viable_values, test_case['viable_values'])

    def test_eliminate_box_values(self):
        test_cases = [
            {
                'viable_values': [
                    [],
                    [1, 3, 4, 5, 6],
                    [1, 3, 4, 5, 6],
                    [],
                    [],
                    [2, 4, 5, 6, 7, 8],
                    [1, 3, 5, 7, 8],
                    [1, 3, 5, 7, 8],
                    [],
                    [1, 3, 4, 5, 6],
                    [1, 3, 4, 5, 6],
                    [],
                    [2, 4, 5, 6, 7, 8],
                    [2, 4, 5, 6, 7, 8],
                    [2, 4, 5, 6, 7, 8],
                    [1, 3, 5, 7, 8],
                    [],
                    [1, 3, 5, 7, 8],
                    [],
                    [1, 3, 4, 5, 6],
                    [],
                    [],
                    [2, 4, 5, 6, 7, 8],
                    [2, 4, 5, 6, 7, 8],
                    [],
                    [],
                    [1, 3, 5, 7, 8],
                    [],
                    [1, 3, 4, 5, 8, 9],
                    [1, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 6, 8],
                    [],
                    [1, 2, 3, 4, 6, 8],
                    [1, 3, 4, 5, 8, 9],
                    [],
                    [1, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 6, 8],
                    [],
                    [1, 2, 3, 4, 6, 8],
                    [1, 3, 4, 5, 8, 9],
                    [],
                    [1, 3, 4, 5, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [1, 2, 3, 4, 5, 7, 8, 9],
                    [],
                    [1, 2, 3, 4, 6, 8],
                    [1, 2, 3, 4, 6, 8],
                    [],
                    [1, 4, 6, 8, 9],
                    [],
                    [],
                    [1, 3, 4, 5, 7, 9],
                    [1, 3, 4, 5, 7, 9],
                    [],
                    [],
                    [1, 2, 3, 7, 9],
                    [],
                    [1, 4, 6, 8, 9],
                    [],
                    [1, 4, 6, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [1, 3, 4, 5, 7, 9],
                    [1, 3, 4, 5, 7, 9],
                    [],
                    [1, 2, 3, 7, 9],
                    [1, 2, 3, 7, 9],
                    [],
                    [1, 4, 6, 8, 9],
                    [1, 4, 6, 8, 9],
                    [1, 3, 4, 5, 7, 9],
                    [],
                    [],
                    [1, 2, 3, 7, 9],
                    [1, 2, 3, 7, 9],
                    []
                ]
            }
        ]

        for test_case in test_cases:
            self.standard_soduku_instance.eliminate_box_values()
            viable_values = list(map(lambda cell: cell.viable_values, self.standard_soduku_instance.cells))
            self.assertEqual(viable_values, test_case['viable_values'])

            # Should not change if run again
            self.standard_soduku_instance.eliminate_box_values()
            self.assertEqual(viable_values, test_case['viable_values'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
