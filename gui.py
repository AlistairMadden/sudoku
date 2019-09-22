import json
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.cells = [None]*81
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                self.cells[i*9+j] = tk.Text(self.master, height=2, width=4)
                self.cells[i*9+j].grid(row=i, column=j)

        self.submit = tk.Button(self.master, text="Submit", fg="green", command=self.on_submit)
        self.submit.grid(row=9, column=4)

    def on_submit(self):
        self.add_sudoku_data_to_json(self.create_sudoku_data())

    def create_sudoku_data(self):
        data = []
        for cell in self.cells:
            try:
                cell_value = int(cell.get("1.0", 'end-1c'))
            except ValueError:
                cell_value = None

            data.append(cell_value)
        return data

    def add_sudoku_data_to_json(self, data):
        file_path = 'sudokus.json'
        sudoku_data = read_sudoku_from_file(file_path)
        sudoku_data['sudokus'].append(data)
        with open(file_path, 'w') as file_handle:
            json.dump(sudoku_data, file_handle, indent=2)


def read_sudoku_from_file(file):
    try:
        with open(file) as file_handle:
            sudoku_data = json.load(file_handle)
    except FileNotFoundError:
        sudoku_data = {'sudokus': []}

    return sudoku_data


root = tk.Tk()
app = Application(master=root)


import IPython  # noqa
IPython.embed()
