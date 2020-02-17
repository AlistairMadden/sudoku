import unittest

from util import read_sudoku_from_file
from sudoku_types import StandardSudoku, Cell, CellSubset


TEST_SUDOKU_DATA = read_sudoku_from_file('sudokus_test.json')


class TestCellSubset(unittest.TestCase):
    def setUp(self):
        cell_values = [None, 1, 5, None, 2, None, None, 7, None]
        self.row_instance = CellSubset()

        for cell_index, cell_value in enumerate(cell_values):
            self.row_instance.append(Cell(cell_value, index=cell_index, row=0, column=cell_index, box=cell_index/3))

    def test_fill_only_options(self):
        # In this instance, the cell at index 3 should be updated with value 3, and the cell at index 5 updated with the value 9
        self.row_instance[0].viable_values = [4, 6]
        self.row_instance[3].viable_values = [3, 6]
        self.row_instance[5].viable_values = [4, 6, 9]
        self.row_instance[6].viable_values = [4, 6, 8]
        self.row_instance[8].viable_values = [4, 8]

        self.row_instance.fill_only_options()

        self.assertEqual([cell.value for cell in self.row_instance], [None, 1, 5, 3, 2, 9, None, 7, None])


class TestStandardSudokuMethods(unittest.TestCase):
    def setUp(self):
        self.standard_sudoku_instance = StandardSudoku(TEST_SUDOKU_DATA['sudokus'][0])

    def test_instantiate(self):
        self.assertEqual(list(map(lambda cell: cell.value, self.standard_sudoku_instance)), TEST_SUDOKU_DATA['sudokus'][0])

    def test_iteration(self):

        iterator = iter(self.standard_sudoku_instance)

        for test_sudoku_value in TEST_SUDOKU_DATA['sudokus'][0]:
            self.assertEqual(next(iterator).value, test_sudoku_value)

        with self.assertRaises(StopIteration):
            next(iterator)

    def test_equality(self):
        self.assertTrue(self.standard_sudoku_instance == self.standard_sudoku_instance)

        second_sudoku_instance = StandardSudoku(TEST_SUDOKU_DATA['sudokus'][0])
        self.assertTrue(self.standard_sudoku_instance == second_sudoku_instance)

        third_sudoku_instance = StandardSudoku(TEST_SUDOKU_DATA['sudokus'][0])
        second_sudoku_instance.cells[0].value = 1
        third_sudoku_instance.cells[0].value = 1
        self.assertTrue(second_sudoku_instance == third_sudoku_instance)

        third_sudoku_instance.cells[0].value = 2
        self.assertFalse(second_sudoku_instance == third_sudoku_instance)

        self.assertFalse([] == second_sudoku_instance)

        self.assertFalse(3 == second_sudoku_instance)

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
            actual_index = self.standard_sudoku_instance.get_box_index(test_case['cell_index'])
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
            self.check_get(self.standard_sudoku_instance.get_cells_in_row, test_case)

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
            self.check_get(self.standard_sudoku_instance.get_cells_in_column, test_case)

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
            self.check_get(self.standard_sudoku_instance.get_cells_in_box, test_case)

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
            self.standard_sudoku_instance.eliminate_column_values()
            viable_values = list(map(lambda cell: cell.viable_values, self.standard_sudoku_instance.cells))
            self.assertEqual(viable_values, test_case['viable_values'])

            # Should not change if run again
            self.standard_sudoku_instance.eliminate_column_values()
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
            self.standard_sudoku_instance.eliminate_row_values()
            viable_values = list(map(lambda cell: cell.viable_values, self.standard_sudoku_instance.cells))
            self.assertEqual(viable_values, test_case['viable_values'])

            # Should not change if run again
            self.standard_sudoku_instance.eliminate_row_values()
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
            self.standard_sudoku_instance.eliminate_box_values()
            viable_values = list(map(lambda cell: cell.viable_values, self.standard_sudoku_instance.cells))
            self.assertEqual(viable_values, test_case['viable_values'])

            # Should not change if run again
            self.standard_sudoku_instance.eliminate_box_values()
            self.assertEqual(viable_values, test_case['viable_values'])

    def test_fill_singles(self):
        for cell in self.standard_sudoku_instance.empty_cells:
            cell.viable_values = [1]

        self.standard_sudoku_instance.fill_singles()

        expected_sudoku_data = TEST_SUDOKU_DATA['sudokus'][0]
        expected_sudoku_data = [value if value else 1 for value in expected_sudoku_data]
        expected_sudoku = StandardSudoku(expected_sudoku_data)

        self.assertEqual(self.standard_sudoku_instance, expected_sudoku)

    def test_num_cells(self):
        self.assertEqual(StandardSudoku.NUM_CELLS, 81)

    def test_generate(self):
        with self.assertRaises(NotImplementedError):
            self.standard_sudoku_instance.generate()

    def test_solved_property(self):

        self.assertFalse(self.standard_sudoku_instance.solved)

        for cell in self.standard_sudoku_instance:
            cell.value = 1

        self.assertTrue(self.standard_sudoku_instance.solved)

    def test_str_representation(self):

        expected_str_representation = (
            '8 0 0 9 3 0 0 0 2\n'
            '0 0 9 0 0 0 0 4 0\n'
            '7 0 2 1 0 0 9 6 0\n'
            '2 0 0 0 0 0 0 9 0\n'
            '0 6 0 0 0 0 0 7 0\n'
            '0 7 0 0 0 6 0 0 5\n'
            '0 2 7 0 0 8 4 0 6\n'
            '0 3 0 0 0 0 5 0 0\n'
            '5 0 0 0 6 2 0 0 8\n'
        )

        self.assertEqual(self.standard_sudoku_instance.__str__(), expected_str_representation)

    def test_fill_only_row_options(self):
        standard_sudoku_instance = StandardSudoku(TEST_SUDOKU_DATA['sudokus'][1])
        standard_sudoku_instance.eliminate_values()
        standard_sudoku_instance.fill_only_row_options()

        expected_cell_values = TEST_SUDOKU_DATA['sudokus'][1].copy()

        expected_cell_values[0] = 1

        self.assertEqual([cell.value for cell in standard_sudoku_instance.cells], expected_cell_values)

    def test_fill_only_column_options(self):
        standard_sudoku_instance = StandardSudoku(TEST_SUDOKU_DATA['sudokus'][1])
        standard_sudoku_instance.eliminate_values()
        standard_sudoku_instance.fill_only_column_options()

        expected_cell_values = TEST_SUDOKU_DATA['sudokus'][1].copy()

        expected_cell_values[0] = 1

        self.assertEqual([cell.value for cell in standard_sudoku_instance.cells], expected_cell_values)
