import itertools
from abc import ABCMeta, abstractmethod


class Sudoku(metaclass=ABCMeta):
    '''TODO: Refactor to subclass list?'''

    def __init__(self):
        self._iteration_index = 0
        self.cells = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._iteration_index == self.NUM_CELLS:
            raise StopIteration

        next_cell = self.cells[self._iteration_index]
        self._iteration_index += 1

        return next_cell

    @property
    @abstractmethod
    def NUM_CELLS(self):
        pass


class StandardSudoku(Sudoku):

    @property
    def NUM_CELLS(self):
        return 81

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
        pass

    def solve(self):
        elimination_methods = itertools.cycle([
            self.eliminate_column_values,
            self.eliminate_row_values,
            self.eliminate_box_values
        ])

        while(not self.solved):
            next(elimination_methods)()
            self.fill_singles()

    @property
    def solved(self):
        return len(self.filter_filled_cells()) == 0

    def eliminate_column_values(self):
        empty_cells = self.filter_filled_cells()
        for cell in empty_cells:
            cell_index = self.get_cell_index(cell)
            column_index = self.get_column_index(cell_index)
            column_cells = self.get_cells_in_column(column_index)

            for column_cell in column_cells:
                if column_cell.value:
                    cell.viable_values.remove(column_cell.value)

    def fill_singles(self):
        empty_cells = self.filter_filled_cells()
        for cell in empty_cells:
            if len(cell.viable_values) == 1:
                cell.value = cell.viable_values[0]

    def get_cells_in_row(self, row_index):
        return list(filter(lambda cell: cell.row == row_index, self.cells))

    def get_cells_in_column(self, column_index):
        return list(filter(lambda cell: cell.column == column_index, self.cells))

    def get_cells_in_box(self, box_index):
        return list(filter(lambda cell: cell.box == box_index, self.cells))

    def filter_filled_cells(self):
        return list(filter(lambda cell: cell.value is None, self))

    def get_cell_index(self, cell):
        return self.cells.index(cell)


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
