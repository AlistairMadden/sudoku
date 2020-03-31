import collections
import copy
import random

from abc import ABCMeta


class Sudoku(metaclass=ABCMeta):

    def __init__(self):
        self.cells = []

    def __iter__(self):
        return iter(self.cells)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return all(self_cell.value == other_cell.value for self_cell, other_cell in zip(self, other))

    NUM_CELLS = None


class StandardSudoku(Sudoku):

    NUM_CELLS = 81

    def __init__(self, data):
        super().__init__()

        self.rows = [CellSubset(sudoku=self, row=i) for i in range(9)]
        self.columns = [CellSubset(sudoku=self, column=i) for i in range(9)]
        self.boxes = [CellSubset(sudoku=self, box=i) for i in range(9)]

        for cell_index, value in enumerate(data):
            cell = Cell(
                value,
                cell_index,
                self.get_column_index(cell_index),
                self.get_row_index(cell_index),
                self.get_box_index(cell_index)
            )

            self.cells.append(cell)
            self.rows[cell.row].append(cell)
            self.columns[cell.column].append(cell)
            self.boxes[cell.box].append(cell)

    def get_row_index(self, cell_index):
        return cell_index // 9

    def get_column_index(self, cell_index):
        return cell_index % 9

    def get_box_index(self, cell_index):
        '''Column index = "x", row index = "y"'''
        return (self.get_row_index(cell_index)//3) * 3 + (self.get_column_index(cell_index)//3)

    def generate(self):
        # Pick a random number to start
        # Set cell at random index with random number from viable numbers
        # Compute viable numbers for all cells
        # While at least one cell is empty
        #   Examine cell at next random index
        #   Choose a number at random from viable numbers
        #   If all remaining cells have viable numbers, continue
        #   Else pick a different number
        raise NotImplementedError

    def get_shuffled_cell_indices(self):
        cell_indices = list(range(self.NUM_CELLS))
        random.shuffle(cell_indices)
        return cell_indices

    def solve(self):

        current_state = copy.deepcopy(self)

        while(not self.solved):
            self.eliminate_and_fill(self.fill_singles)
            self.eliminate_and_fill(self.fill_only_row_options)
            self.eliminate_and_fill(self.fill_only_column_options)
            self.eliminate_and_fill(self.fill_only_box_options)

            if current_state == self:
                print('Puzzle could not be solved.')
                break
            else:
                current_state = copy.deepcopy(self)

    def eliminate_and_fill(self, fill_function):
        self.eliminate_values()
        fill_function()

    def eliminate_values(self):
        self.eliminate_column_values()
        self.eliminate_row_values()
        self.eliminate_box_values()

    @property
    def solved(self):
        return len(self.filter_filled_cells()) == 0

    def eliminate_column_values(self):
        for cell in self.empty_cells:
            column_index = cell.column
            column_cells = self.get_cells_in_column(column_index)

            for column_cell in column_cells:
                column_cell_value = column_cell.value
                if column_cell_value:
                    try:
                        cell.viable_values.remove(column_cell_value)
                    except ValueError:
                        # Removing value not in viable_values. This is fine.
                        pass

    def eliminate_row_values(self):
        for cell in self.empty_cells:
            row_index = cell.row
            row_cells = self.get_cells_in_row(row_index)

            for row_cell in row_cells:
                row_cell_value = row_cell.value
                if row_cell_value:
                    try:
                        cell.viable_values.remove(row_cell_value)
                    except ValueError:
                        # Removing value not in viable_values. This is fine.
                        pass

    def eliminate_box_values(self):
        for cell in self.empty_cells:
            box_index = cell.box
            box_cells = self.get_cells_in_box(box_index)

            for box_cell in box_cells:
                box_cell_value = box_cell.value
                if box_cell_value:
                    try:
                        cell.viable_values.remove(box_cell_value)
                    except ValueError:
                        # Removing value not in viable_values. This is fine.
                        pass

    def fill_singles(self):
        for cell in self.empty_cells:
            if len(cell.viable_values) == 1:
                cell.value = cell.viable_values[0]
                cell.viable_values = []

    def fill_only_column_options(self):
        for column in self.columns:
            column.fill_only_options()

    def fill_only_row_options(self):
        for row in self.rows:
            row.fill_only_options()

    def fill_only_box_options(self):
        for box in self.boxes:
            box.fill_only_options()

    @property
    def empty_cells(self):
        return self.filter_filled_cells()

    def get_cells_in_row(self, row_index):
        return [cell for cell in self if cell.row == row_index]

    def get_cells_in_column(self, column_index):
        return [cell for cell in self if cell.column == column_index]

    def get_cells_in_box(self, box_index):
        return [cell for cell in self if cell.box == box_index]

    def filter_filled_cells(self):
        return [cell for cell in self if cell.value is None]

    def __str__(self):
        pretty_string = ''
        for i in range(9):
            for j in range(9):
                value = self.cells[i*9 + j].value
                pretty_string += str(value if value is not None else 0)
                if j != 8:
                    pretty_string += ' '
            pretty_string += '\n'

        return pretty_string


class CellSubset(list):

    def __init__(self, iterable=(), sudoku=None, row=None, column=None, box=None, *args, **kwargs):
        super().__init__(iterable, *args, **kwargs)
        self.sudoku = sudoku
        self.row = row
        self.column = column
        self.box = box

    @property
    def empty_cells(self):
        return (cell for cell in self if cell.value is None)

    def fill_only_options(self):

        viable_value_cell_mapping = collections.defaultdict(list)

        for cell in self.empty_cells:
            for viable_value in cell.viable_values:
                viable_value_cell_mapping[viable_value].append(cell)

        for value, cell_list in viable_value_cell_mapping.items():
            if len(cell_list) == 1:
                cell_list[0].value = value
                cell_list[0].viable_values = []


class Cell:
    POSSIBLE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, value, index, column, row, box):
        self.viable_values = [] if value else self.POSSIBLE_VALUES.copy()
        self.value = value
        self.index = index
        self.column = column
        self.row = row
        self.box = box
