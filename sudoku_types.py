import copy

from abc import ABCMeta


class Sudoku(metaclass=ABCMeta):
    '''TODO: Refactor to subclass list?'''

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

        for cell_index, value in enumerate(data):
            self.cells.append(
                Cell(
                    value,
                    cell_index,
                    self.get_column_index(cell_index),
                    self.get_row_index(cell_index),
                    self.get_box_index(cell_index)
                )
            )

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

    def solve(self):
        elimination_methods = [
            self.eliminate_column_values,
            self.eliminate_row_values,
            self.eliminate_box_values
        ]

        current_state = copy.deepcopy(self)

        while(not self.solved):
            for elimination_method in elimination_methods:
                elimination_method()
            self.fill_singles()

            if current_state == self:
                print('Puzzle could not be solved.')
                break
            else:
                current_state = copy.deepcopy(self)

    @property
    def solved(self):
        return len(self.filter_filled_cells()) == 0

    def eliminate_column_values(self):
        for cell in self.empty_cells:
            cell_index = self.get_cell_index(cell)
            column_index = self.get_column_index(cell_index)
            column_cells = self.get_cells_in_column(column_index)

            for column_cell in column_cells:
                if column_cell.value:
                    try:
                        cell.viable_values.remove(column_cell.value)
                    except ValueError:
                        # Removing value not in viable_values. This is fine.
                        pass

    def eliminate_row_values(self):
        for cell in self.empty_cells:
            cell_index = self.get_cell_index(cell)
            row_index = self.get_row_index(cell_index)
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
            cell_index = self.get_cell_index(cell)
            box_index = self.get_box_index(cell_index)
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

    def get_cell_index(self, cell):
        return self.cells.index(cell)

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


class Box:
    def __init__(self, rows, columns, cells):
        self.rows = rows
        self.columns = columns
        self.cells = cells if cells else []
    cells = []


class Cell:
    POSSIBLE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, value, index, column, row, box):
        self.viable_values = [] if value else self.POSSIBLE_VALUES.copy()
        self.value = value
        self.index = index
        self.column = column
        self.row = row
        self.box = box
