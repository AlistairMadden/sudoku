import json


def read_sudoku_from_file(file):
    try:
        with open(file) as file_handle:
            sudoku_data = json.load(file_handle)
    except FileNotFoundError:
        sudoku_data = {'sudokus': []}

    return sudoku_data
