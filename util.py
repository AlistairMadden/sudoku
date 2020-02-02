import json


def read_sudoku_from_file(file):
    with open(file) as file_handle:
        sudoku_data = json.load(file_handle)

    return sudoku_data
