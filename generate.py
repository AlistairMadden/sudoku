from abc import ABCMeta, abstractmethod


class Sudoku(metaclass=ABCMeta):

    def __init__(self):
        self._iteration_index = 0
        self.cells = [None]*self.NUM_CELLS

    def __iter__(self):
        return self

    def __next__(self):
        if self._iter_index == self.NUM_CELLS:
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


class SudokuGenerator:
    pass


if __name__ == '__main__':
    import IPython
    IPython.embed()
