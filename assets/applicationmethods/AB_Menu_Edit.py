from assets.Callbacks import main_menubar_callbacks
from assets.Error import Error
from modules.CTkMessagebox import CTkMessagebox

from subprogs.edit_values_in_table.edit_values_in_table import EditValuesInTable
from subprogs.edit_values_in_table.edit_dataclass_in_table import EditDataclassInTable
from subprogs.table.table import CreateFromTable
from subprogs.edit_parameters.edit_parameters import EditParameters
from subprogs.group_edit.stack_to_group import StackToGroup
from subprogs.select_data.select_items import SelectItems
from subprogs.notepad.notepad import Notepad
from subprogs.preferences.preferences import PreferencesApp
from subprogs.user_input.TwoListSelection import TwoListSelection

import numpy as np
import pandas
import copy
from subprogs.user_input.single_dialog import SingleDialog

class MenuEditMixin:
    def find(self, find_by):
        ''' Find '''
        if find_by == 'id':
            all_ids = []
            all_names = []
            all_names_nr = []
            for each in self.eleana.dataset:
                all_ids.append(each.id.lower())
                # all_names.append(each.name)
                # all_names_nr.append(each.name_nr)
                # all_stknames.append(each.stk_names)
        i = True
        while i:
            dialog = SingleDialog(master = self.mainwindow, title="Search for ID", label = "Enter the ID:")
            search_for_id = dialog.get()
            if search_for_id is None:
                return
            if len(search_for_id) == 18 and all(c in "0123456789abcdefABCDEF" for c in search_for_id):
                if search_for_id.lower() in all_ids:
                    index = all_ids.index(search_for_id.lower())
                    assign = CTkMessagebox(message = "Data found. Do you want to display it as:", option_1 = "Cancel", option_2 = "Second", option_3 = "First")
                    response = assign.get()
                    i = False
                    if response == "First":
                        self.eleana.selections['first'] = index
                        self.eleana.selections['f_dsp'] = True
                        self.gui_to_selections()
                    elif response == "Second":
                        self.eleana.selections['second'] = index
                        self.eleana.selections['s_dsp'] = True
                        self.gui_to_selections()
                else:
                    i = False
            else:
                Error.show(info = "Please enter a valid ID.")


    def edit_values_in_table(self, which ='first'):

        ''' Edit data in table'''

        if which == 'first' or which == 'second':
            index_in_data = self.eleana.selections[which]
        if index_in_data < 0:
            Error.show(info = 'No data selected to edit.')
            return

        data = self.eleana.dataset[index_in_data]
        x_header = f"{data.parameters['name_x']} [{data.parameters['unit_x']}]"
        if data.type == 'single 2D' or data.type == "":
            y_header = f"{data.parameters.get('name_y', '')} [{data.parameters.get('unit_y', '')}]"
            headers = [x_header, y_header]
        elif data.type == 'stack 2D':
            headers = [x_header]
            headers.extend(data.stk_names)
        else:
            Error.show(info = "Data type not specified. Expected 'single 2D' or 'stack 2D'")
            return

        # table = EditValuesInTable(eleana_app=self.eleana,
        #                         master=self.mainwindow,
        #                         x = data.x,
        #                         y = data.y,
        #                         #name = data.name,
        #                         #window_title = f"Edit {data.name}",
        #                         column_names = headers,
        #                         complex = data.complex
        #                         )

        table = EditDataclassInTable(eleana_app=self.eleana,
                                  master=self.mainwindow,
                                  grapher = self.grapher,
                                  )


        # response = table.get()
        # if response is None:
        #     return
        # data.x = response[0]
        # data.y = response[1]
        # self.update.dataset_list()
        # self.update.group_list()
        # self.update.all_lists()
        # self.grapher.plot_graph()

    def create_from_table(self):

        ''' Create data from table'''

        length_of_data = len(self.eleana.dataset)
        headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        value = ""
        cols = 10
        rows = 100
        # Generate empty table
        data = [[value for _ in range(cols)] for _ in range(rows)]

        df = pandas.DataFrame(columns=headers, data=data)
        name = 'new'
        spreadsheet = CreateFromTable(eleana = self.eleana,
                                      master = self.mainwindow,
                                      df = df,
                                      name = name,
                                      group = self.eleana.selections['group'])
        response = spreadsheet.get()
        self.update.group_list()
        self.update.dataset_list()
        self.update.all_lists()
        after_addition = len(self.eleana.dataset)
        if after_addition > length_of_data:
            self.eleana.selections['first'] = after_addition -1
            self.gui_to_selections()


    def edit_parameters(self, which='first'):

        ''' Edit parameters'''

        idx = self.eleana.selections.get(which, - 1)
        if idx < 0:
            return
        par_to_edit = self.eleana.dataset[idx].parameters
        name_nr = self.eleana.dataset[idx].name_nr
        edit_par = EditParameters(master = self.mainwindow, parameters = par_to_edit, name = name_nr)
        response = edit_par.get()

        if response:
            self.eleana.dataset[idx].parameters = response
            self.grapher.plot_graph()
        else:
            return

    def transpose_stack(self):

        ''' Transpose stack '''

        selected = self.eleana.selections['first']
        if selected < 0:
            selected = self.eleana.selections['second']
        if selected < 0:
            return

        data = self.eleana.dataset[selected]
        if data.type != 'stack 2D':
            Error.show(title = 'Transpose stack', info='The selected data is not a stack.' )
            return

        self.mainwindow.config(cursor="watch")
        # Transpose y and change axes
        y_axis = data.y.T
        x_axis = data.z
        z_axis = data.x

        # Swap names and units
        name_x = data.parameters.get('name_z', '')
        name_z = data.parameters.get('name_x', '')
        unit_x = data.parameters.get('unit_z', '')
        unit_z = data.parameters.get('unit_z', '')

        stk_names = []
        for i in z_axis:
            name = name_z + ' ' + str(i) + ' ' + unit_z
            stk_names.append(name)

        data.x = x_axis
        data.y = y_axis
        data.z = z_axis
        data.parameters['name_x'] = name_x
        data.parameters['name_z'] = name_z
        data.parameters['unit_x'] = unit_x
        data.parameters['unit_z'] = unit_z
        data.stk_names = stk_names

        self.update.dataset_list()
        self.update.group_list()
        self.update.all_lists()
        self.grapher.plot_graph()
        self.mainwindow.config(cursor="arrow")

    def average_stack(self):

        ''' Create averaged stack '''

        selected = self.eleana.selections['first']
        if selected < 0:
            selected = self.eleana.selections['second']
        if selected < 0:
            return

        data = copy.deepcopy(self.eleana.dataset[selected])
        if data.type != 'stack 2D':
            Error.show(title='Average stack', info='The selected data is not a stack.')
            return

        self.mainwindow.config(cursor="watch")
        # Transpose y and change axes
        data.y = np.mean(data.y, axis=0)
        data.z = None

        # Swap names and units
        data.parameters.pop('name_z', None)
        data.parameters.pop('unit_z', None)

        data.type = 'single 2D'
        data.stk_names = []

        data.name = data.name + ':AVG'
        self.eleana.results_dataset.append(data)

        self.update.dataset_list()
        self.update.group_list()
        self.update.all_lists()
        positions = self.sel_result._values
        self.result_selected(positions[-1])
        self.sel_result.set(positions[-1])
        self.mainwindow.config(cursor="arrow")

    def stack_to_group(self, which):

        ''' Convert stack to group '''

        if which == 'any':
            index = self.eleana.selections['first']
            if index < 0:
                index = self.eleana.selections['second']
                if index < 0:
                    return
        else:
            index = self.eleana.selections[which]
        if index < 0:
            return
        data = copy.deepcopy(self.eleana.dataset[index])
        if not data.type == 'stack 2D':
            CTkMessagebox(master = self.mainwindow, title="Conversion to group", message="The data you selected is not a 2D stack")
        else:
            convert_stack_to_group = StackToGroup(master = self.mainwindow, eleana = self.eleana, index = index)
            response = convert_stack_to_group.get()
            if response == None:
                 return
            self.update.dataset_list()
            self.update.group_list()
            self.update.all_lists()


    def extract_from_stack(self, which = None):
        if which is None:
            index = self.eleana.selections['first']
            if index < 0:
                index = self.eleana.selections['second']
                if index < 0:
                    return

        data = self.eleana.dataset[index]
        if data.type != "stack 2D":
            return

        av_data = data.stk_names
        select_data = SelectItems(master=self.mainwindow, title='Select data',
                                 items=av_data)
        response = select_data.get()
        if response:
            dialog = CTkMessagebox(title ='', message = "Delete selected data or extract", option_1 = 'Extract', option_2 = "Delete")
            oper = dialog.get()
            idxs = []
            for i in response:
                if i in av_data:
                    index = av_data.index(i)
                    idxs.append(index)
            idxs.sort(reverse=True)
            extracted = copy.deepcopy(data)
            if oper == 'Delete':
                # Delete
               for i in idxs:
                    extracted.y = np.delete(extracted.y, i, axis = 0)
                    extracted.stk_names.pop(i)

            else:
                # Extract
                extracted.y = extracted.y[idxs]
                stk_names = []
                for i in idxs:
                    stk_names.append(extracted.stk_names[i])
                extracted.stk_names = stk_names
                if len(extracted.stk_names) == 1:
                    extracted.name = extracted.name + '/' + stk_names[0]
                    extracted.stk_names = []
                    extracted.type = 'single 2D'
                    extracted.y = extracted.y.ravel()

            self.eleana.results_dataset.append(extracted)
            self.update.list_in_combobox('sel_result')
            self.update.list_in_combobox('r_stk')
            # Set the position to the last added item
            list_of_results = self.sel_result._values
            position = list_of_results[-1]
            self.sel_result.set(position)
            self.result_selected(position)

    def quick_copy(self, event = None):

        ''' Copy '''

        curves = self.grapher.ax.get_lines()
        the_longest = 0
        collected_list = []

        for curve in curves:
            label = curve.get_label()
            x_data = [str(element) for element in curve.get_xdata()]
            if x_data:
                x_data.insert(0, f'{label} [X]')
                collected_list.append(x_data)
                y_data = [str(element) for element in curve.get_ydata()]
                y_data.insert(0, f'{label} [Y]')
                collected_list.append(y_data)
                length = len(x_data)

                if length > the_longest:
                    the_longest = length

        # Replenish shorter lists with empty strings
        even_collected_list = []
        for row in collected_list:
            row_length = len(row)
            diff = the_longest - row_length
            if diff > 0:
                row.extend([""] * diff)
            even_collected_list.append(row)

        # Transpose list
        transposed_data = list(map(list, zip(*even_collected_list)))
        text_output = "\n".join("\t".join(row) for row in transposed_data)
        self.mainwindow.clipboard_clear()
        self.mainwindow.clipboard_append(text_output)
        self.mainwindow.update()

    def quick_paste(self, event=None):

        ''' Paste '''

        try:
            text = self.mainwindow.clipboard_get()
            self.import_ascii(text)
        except Exception as e:
            Error.show(title="Paste from clipboard", info = "Cannot paste from clipboard", details=e)

    def notes(self):

        ''' Notes '''

        notepad = Notepad(master=self.mainwindow, title="Edit notes", text=self.eleana.notes)
        response = notepad.get()
        if response == None:
            return
        else:
            self.eleana.notes = response


    def clear_dataset(self, dialog = True):

        ''' Clear dataset '''

        if dialog:
            quit_dialog = CTkMessagebox(master = self.mainwindow, title="Clear dataset",
                                    message="Are you sure you want to clear the entire dataset?",
                                    icon="warning", option_1="No", option_2="Yes")
            response = quit_dialog.get()
        else:
            response = 'Yes'

        if response == "Yes":
            self.resultFrame.grid_remove()
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()
            self.eleana.dataset.clear()
            self.eleana.results_dataset.clear()

            self.eleana.selections = {'group':'All',
                      'first':-1, 'second':-1, 'result':-1,
                      'f_cpl':'re','s_cpl':'re', 'r_cpl':'re',
                      'f_stk':0, 's_stk':0, 'r_stk':0,
                      'f_dsp':True, 's_dsp':True ,'r_dsp':True
                      }
            self.update.dataset_list()
            self.update.group_list()
            self.update.all_lists()
            self.update.gui_widgets()
            self.gui_to_selections()

            self.sel_graph_cursor(value = 'None', clear_annotations = True)

    def first_to_group(self):

        ''' Assign first to group '''

        if self.eleana.selections['first'] < 0:
            return
        groups = copy.copy(self.eleana.assignmentToGroups.get('<group-list/>', None))
        if not groups:
            Error.show(title = 'Error in groups', info = "def first_to_groups: groups not found")

        groups.remove('All')
        dialog = TwoListSelection(left_label="Available groups",
                                    master = self.mainwindow,
                                    right_label="Assigned to groups",
                                  items = groups,
                                  disable_new = False
                                  )
        selected = dialog.get()
        if not selected:
            return

        selected.insert(0, 'All')
        first = self.eleana.dataset[self.eleana.selections['first']]
        #group_assign = Groupassign(master=self.mainwindow, eleana = self.eleana, which='first')
        #response = group_assign.get()
        first.groups = selected

        self.update.group_list()
        self.update.all_lists()

    def second_to_group(self):

        ''' Assign second to group '''

        if self.eleana.selections['second'] < 0:
            return
        #group_assign = Groupassign(master=app, which='second')
        #response = group_assign.get()

        groups = copy.copy(self.eleana.assignmentToGroups.get('<group-list/>', None))
        if not groups:
            Error.show(title='Error in groups', info="def first_to_groups: groups not found")

        groups.remove('All')
        dialog = TwoListSelection(left_label="Available groups",
                                  master=self.mainwindow,
                                  right_label="Assigned to groups",
                                  items=groups,
                                  disable_new=False
                                  )
        selected = dialog.get()
        if not selected:
            return

        selected.insert(0, 'All')
        second = self.eleana.dataset[self.eleana.selections['second']]
        second.groups = selected

        self.update.group_list()
        self.update.all_lists()

    def preferences(self):

        ''' Preferences '''

        preferences = PreferencesApp(master = self.mainwindow, eleana = self.eleana, grapher = self.grapher)
        response = preferences.get()

    def rescan_dataset(self, show_errors = True):

        ''' Rescan and fixed '''

        try:
            self.update.dataset_list()
        except:
            pass
        try:
            self.update.groups()
        except:
            self.update.all_lists()
        try:
            self.gui_to_selections()
        except:
            pass
        try:
            self.eleana.busy = False
        except:
            pass

