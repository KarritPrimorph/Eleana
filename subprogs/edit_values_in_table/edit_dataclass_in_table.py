#!/usr/bin/python3
import pathlib
import customtkinter as ctk
import numpy as np
import pygubu
import string
from modules.tksheet import Sheet
from assets.Error import Error
from assets.Observer import Observer
import copy
from modules.CTkMessagebox import CTkMessagebox

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "edit_dataset_in_table.ui"

class EditDataclassInTable:
    def __init__(self, eleana_app, master, grapher,
                    x = None,               # X array as 1D of np.array type
                    y = None,               # Y array as 1D or 2D np.array type
                    column_names = None,    # The column headers if None will be default
                    window_title = None,    # The title of the window. If none it will be default
                    complex = None,         # Are the data complex? If None, it will be determined automatically
                    spreadsheet = None,     # Data ready to display in tksheet
                 ):

        self.master = master
        self.eleana = eleana_app
        self.builder = builder = pygubu.Builder()
        self.grapher = grapher
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Register Observer
        self.observer = Observer(self.eleana, self)
        self.eleana.notify_on = True

        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        self.mainwindow.geometry("800x900")
        builder.connect_callbacks(self)
        if not window_title:
            window_title = 'Edit data in table'

        # References
        self.tableFrame = builder.get_object("tableFrame", master)
        self.mainwindow.title(window_title)

        ''' SWITCHING OFF THE FRAMES WITH FIELDS '''
        self.frame_1 = builder.get_object('ctkframe8', master)
        self.frame_2 = builder.get_object('ctkframe12', master)
        self.frame_3 = builder.get_object('ctkframe4', master)
        self.frame_1.grid_remove()
        self.frame_2.grid_remove()
        self.frame_3.grid_remove()

        self.response = None
        self.mainwindow.bind("<Escape>", self.cancel)
        self.mainwindow.attributes('-topmost', True)

        self.table = None

        self.get_dataset_for_table(which = 'first')

        self.modifications = False

    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event = None):
        self.eleana.dataset[self.original_index] = copy.deepcopy(self.original_copy)
        self.grapher.plot_graph(switch_cursors=False)


        self.response = None

        # Unregister observer
        self.mainwindow.protocol('WM_DELETE_WINDOW', lambda: None)
        self.eleana.detach(self.observer)
        self.observer = None

        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()

    def ok(self):
        # self.response = self.prepare_results()
        # if self.response is None:
        #     return
        # Unregister observer
        self.mainwindow.protocol('WM_DELETE_WINDOW', lambda: None)
        self.eleana.detach(self.observer)
        self.observer = None

        self.mainwindow.destroy()

    def prepare_results(self):
        row_counts = self.table.get_total_rows(include_index=False)
        column_counts = self.table.get_total_columns(include_header=False)
        data = []
        for n in range(row_counts):
            row_data = []
            for m in range(column_counts):
                cell_value = self.table.get_cell_data(n, m)
                try:
                    # Check if values for y are complex
                    if isinstance(cell_value, complex):
                        row_data.append(cell_value)
                    else:
                        # The value is not complex
                        row_data.append(float(cell_value))
                except ValueError:
                    continue

            data.append(row_data)
        x_axis = [row.pop(0) for row in data]
        x = np.array(x_axis)
        if self.column_counts == 2:
            data = [value[0] for value in data]
        y = np.array(data).T
        return [x, y]

    def generate_table(self, headers, list2D):
        if self.table is not None:
            self.table.destroy()
        self.table = Sheet(self.tableFrame)
        self.table.set_sheet_data(list2D)
        self.table.headers(headers)
        self.table.grid(row=0, column=0, sticky="nswe")
        self.table.change_theme(ctk.get_appearance_mode())
        self.table.enable_bindings("ctrl_select", "all", "right_click_popup_menu")
        self.table.extra_bindings("sheetmodified", self.on_cell_change)

    def get_data_from_column(self, column_name):
        index = self.sel_x_axis._values.index(column_name)
        if index < 0:
            return
        column_data = self.table.get_column_data(index - 1)
        return column_data

    def paste_event(self, event):
        data = self.mainwindow.clipboard_get()
        rows = data.split('\n')
        nrows = len(rows)
        ncols = max(len(row.split('\t')) for row in rows)
        self.table.set_sheet_data([[None] * ncols] * nrows)

    def data_changed(self, variable, value):
        if variable != "grapher_action":
            if self.modifications:
                dialog = CTkMessagebox(message = "The data has been modified. Do you want to accept the changes?", option_1 = "Decline", option_2 = "Accept")
                response = dialog.get()
                if response == 'Decline':
                    self.eleana.dataset[self.original_index] = self.original_copy
                    self.modifications = False

        if variable == "first":
            self.get_dataset_for_table(which = 'first')
            self.modifications = False
        else:
            return

    def get_dataset_for_table(self, which):
        ''' Get current data for table'''
        index_in_data = self.eleana.selections[which]
        data = self.eleana.dataset[index_in_data]

        # Create copy of original data and position in dataset
        self.original_copy = copy.deepcopy(data)
        self.original_index = index_in_data

        # Prepare values for cells
        x_header = f"{data.parameters['name_x']} [{data.parameters['unit_x']}]"
        if data.type == 'single 2D' or data.type == "":
            y_header = f"{data.parameters.get('name_y', '')} [{data.parameters.get('unit_y', '')}]"
            headers = [x_header, y_header]
        elif data.type == 'stack 2D':
            headers = [x_header]
            headers.extend(data.stk_names)
        list2D = self.create_data_for_table(data.x, data.y, complex_ = data.complex, column_names=headers)

        self.generate_table(headers = headers, list2D = list2D)
        self.mainwindow.title(data.name_nr)

    def create_data_for_table(self, x, y, complex_, column_names):
        self.row_counts = len(x)
        x_data = np.atleast_1d(x)
        shape = y.shape
        if len(shape) == 2:
            self.column_counts = shape[0] + 1
        else:
            self.column_counts = 2
        y_data = np.atleast_2d(y).T

        if complex_ is None:
            self.complex = np.iscomplexobj(y_data)
        else:
            self.complex = complex_
        list2D = [[x_data[i], *y_data[i]] for i in range(0, len(x_data))]
        if not column_names:
            column_names = []
            n = len(list2D[0])
            for i in range(0, n):
                label = ""
                while i >= 0:
                    label = string.ascii_uppercase[i % 26] + label
                    i = i // 26 - 1
                column_names.append(label)
        return list2D


    def on_cell_change(self, event):
        col = event.column
        row = event.row
        text = event.text
        try:
            value = float(text)
        except:
            Error.show(info = "Could not convert value to float. See column {col}.")
            return

        if col == 0:
            data = self.eleana.dataset[self.original_index].x
        elif col == 1:
            data = self.eleana.dataset[self.original_index].y

        data[row] = value
        self.modifications = True

        self.grapher.plot_graph(switch_cursors=False)

        return event.text

    def reset_changes(self):
        self.eleana.dataset[self.original_index] = self.original_copy
        self.modifications = False
        self.get_dataset_for_table(which = 'first')
        self.grapher.plot_graph(switch_cursors=False)

if __name__ == "__main__":
    app = CreateFromTable()
    app.run()
