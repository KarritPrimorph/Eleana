#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
import customtkinter as ctk
from widgets.CTkSpinbox import CTkSpinbox
import numpy as np
import importlib
import weakref
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator, BarycentricInterpolator
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from modules.CTkListbox.ctk_listbox import CTkListbox
from subprogs.curve_fit.built_in_functions import BuiltInFunctions, Function
import copy
from assets.Error import Error

''' GENERAL SETTINGS '''
# If True all active subprog windows will be closed on start this subprog
CLOSE_SUBPROGS: bool = False

# Folder name containing THIS file
SUBPROG_FOLDER: str = 'curve_fit'

# Name of GUI python file created by pygubu-designer. Usually with ...ui.py endings
GUI_FILE: str = 'curve_fitui.py'

# Name of class in GUI_FILE used to create the window
GUI_CLASS: str = 'Curve_fitUI'

# Title of the window that shown in the main bar
TITLE: str = 'Curve Fit'

# If True, this window will be always on top
# self.subprog_settings['on_top']
ON_TOP : bool = True

# If True then values for selected elements will be stored after close
# and restored automatically when subprog is started again.
# This works only until Eleana is closed
RESTORE_SETTINGS = True

# ID name of a CTkLabel widget where the name of current data is displayed.
# CTkLabel with the same ID name must exist in the GUI.
# If not used set this to None
# self.subprog_settings['data_label']
DATA_LABEL: str = None

# The suffix that will be added to the name of processed data.
# For example if "Spectrum" is processed and NAME_SUFFIX = "_MODIFIED"
# you will get "Spectrum_MODIFIED" name in result
# self.subprog_settings['name_suffix']
NAME_SUFFIX: str = '_BASELINE'

# If true, calculations are done automatically upon selection of data in the main GUI
# self.subprog_settings['auto_calculate']
AUTO_CALCULATE: bool = False

''' INPUT DATA CONFIGURATION '''
# Define if data for calculations should be extracted.
# self.regions['from']
#REGIONS_FROM: str = 'none'        # 'none' - do not extract
REGIONS_FROM: str = 'selection'    # 'selection' - take data only from selected range on graph (Range selection)
#REGIONS_FROM: str = 'scale'       # ' scale' - take data from current x scale

# Define if original, not extracted data are added to self.data_for_calculations in indexes +1
# For example. If set True then: self.data_for_calculations[0] = extracted data
#                                self.data_for_calculations[1] = original, not extracted data
# When USE_SECOND is set True then Second data extracted is in [2] and original in [3].
# This is very useful if something must be calculated on selected fragments and then used he results on original data.
# self.regions['orig_in_odd_idx'] <-- this will keep 0 or 1
ORIG_IN_ODD_IDX: bool = True

# If both First and Second data are needed set this True
# self.use_second
USE_SECOND: bool = False

# If First and Second data have different dimensions, the error will be shown.
# if you want to override checking if the dimensions are the same set this parameter True
IGNORE_DIMENSIONS: bool = True

# If each subspectrum in a Stack 2D can be processed separately set this to True
# When the calculations requires all data fro the stack in x and y set this  to False
# If False then the method 'calculate_stack must contain appropriate method
# self.stack_sep
STACK_SEP: bool = True

# If this is True, data containing the parameter 'origin':@result
# will be ignored for calculations.
# This is useful, if 'Group' is set to 'All' and summary data from table
# are added to the dataset. THis prevents taking summary for further calculations.
# self.subprog_settings['result_ignore']
RESULT_IGNORE: bool = True

''' RESULT DATA CONFIGURATION '''
# Define if processed data should be created, added or replaced
# self.subprog_settings['result']
#RESULT_CREATE: str = ''          # Do not create any result dataset
#RESULT_CREATE: str = 'add'      # Add created results to the result_dataset
RESULT_CREATE: str = 'replace'  # Replace the data in result with new results

''' REPORT SETTINGS '''
# Define if a report should be created. Reports contain summary of calculations, values etc.
# self.report['create']
REPORT_CREATE: bool = False

# Results of Stack data usually requires separate calculations for each data in the stack.
# Hence this often requires summary of calculation as a Table.
# If set to True, the summary table will not be shown.
# self.report['report_skip_for_stk']
REPORT_SKIP_FOR_STK: bool = False

# The name of the window containg the reported results.
# self.report['report_window_title']
REPORT_WINDOW_TITLE: str = 'Results of distance measurements'

# Report headers is the list of srtings that contains HEADERS of the table
# in which the results of calculations are shown.
# self.report['headers']
# Here is an example:
REPORT_HEADERS: list = ['Nr',
                  'Name',
                  'X1',
                  'X2',
                  'dX',
                  'Y1',
                  'Y2',
                  'dY']

# Index in REPORT_HEADERS that defines a column to create default X axis.
# This can be manually changed when the report is displayed.
# self.report['default_x']
# Example: 2 means that column 'X1' is taken as default X
REPORT_DEFAULT_X: int = 2

# The same as X but for Y axis.
# self.report['default_y']
# Example: 7 - dY column is set as default Y
REPORT_DEFAULT_Y: int = 7

# The default name of data, that will be used after Add to dataset.
# self.report['report_name']
REPORT_NAME: str = "Distance measurements"

# Default name of X axis for report data
# self.report['x_name']
REPORT_NAME_X: str =  'Data Number'

# Default name of Y axis for report data
# self.report['y_name']
REPORT_NAME_Y: str =  'dY Value'

# Default unit name of values in the X axis
# self.report['x_unit']
REPORT_UNIT_X: str = ''

# Default unit name of values in the Y axis
# self.report['y_unit']
REPORT_UNIT_Y: str = ''

# Default name of Group to which the report data are assigned.
# If not existing, the appropriate group is created
# self.report['to_group']
REPORT_TO_GROUP: str = 'RESULT Distance'

''' CURSOR SETTINGS '''
# If False, the manual changing of cursor type in the main GUI Window is disabled.
# self.subprog_cursor['changing']
CURSOR_CHANGING: bool = True

# Name of the cursor that is automatically switched on when the subprog window is opened.
# Possible values: 'None', 'Continuous read XY', 'Selection of points with labels'
#                  'Selection of points', 'Numbered selections', 'Free select', 'Crosshair', 'Range select'
# self.subprog_cursor['type']
CURSOR_TYPE: str = 'Free select'

# Set the maximum number of annotations that can be added to the graph.
# Set to 0 for no limit
# self.subprog_cursor['limit']
CURSOR_LIMIT: int = 0

# If True the any added cursors in the graph will be removed
# self.subprog_cursor['clear_on_start']
CURSOR_CLEAR_ON_START: bool = True

# Minimum number of cursor annotations needed for calculations.
# Set 0 for no checking
# self.subprog_cursor['cursor_required']
CURSOR_REQUIRED: int = 2

# A text string to show in a pop up window if number of cursors is less than required for calculations
# Leve this empty if no error should be displayed
# self.subprog_cursor['cursor_req_text']
CURSOR_REQ_TEXT: str = 'Please select at least two points.'

# Enable checking if all cursor annotations are between Xmin and Xmax of data_dor_calculations
# self.subprog_cursor['cursor_outside_x']
CURSOR_OUTSIDE_X: bool = False

# The same as for X but for Ymin and Ymax
# self.subprog_cursor['cursor_outside_y']
CURSOR_OUTSIDE_Y: bool = False

# Text to display if any cursor is outside Xmin, Xmax or Ymin, Ymax
# self.subprog_cursor['cursor_outside_text']
CURSOR_OUTSIDE_TEXT: str = 'One or more selected points are outside the (x, y) range of data.'


'''**************************************************************************************************
*                      THE DEFAULT CONSTRUCTOR (LINES BETWEEN **)                                   * 
**************************************************************************************************'''
if __name__ == "__main__":
    module_path = f"subprogs.{SUBPROG_FOLDER}.{GUI_FILE[:-3]}"
    class_name = GUI_CLASS
    from assets.Eleana import Eleana
else:
    module_path = f"{SUBPROG_FOLDER}.{GUI_FILE[:-3]}"
    class_name = GUI_CLASS
mod = importlib.import_module(module_path)
WindowGUI = getattr(mod, class_name)

from subprogs.general_methods.SubprogMethods5 import SubMethods_05 as Methods
class CurveFit(Methods, WindowGUI):
    def __init__(self, app=None, which='first', commandline=False):
        self.__app = weakref.ref(app)
        if app and not commandline:                                                                 #|
            # Initialize window if app is defined and not commandline                               #|
            WindowGUI.__init__(self, self.__app().mainwindow)
            #|
        # Create settings for the subprog                                                           #|
        self.subprog_settings = {'folder':SUBPROG_FOLDER, 'title': TITLE, 'on_top': ON_TOP, 'data_label': DATA_LABEL, 'name_suffix': NAME_SUFFIX,
                                 'restore':RESTORE_SETTINGS, 'auto_calculate': AUTO_CALCULATE, 'result': RESULT_CREATE, 'result_ignore':RESULT_IGNORE,
                                 'ignore_dimensions':IGNORE_DIMENSIONS}
        self.regions = {'from': REGIONS_FROM, 'orig_in_odd_idx':int(ORIG_IN_ODD_IDX)}
        self.report = {'nr': 1, 'create': REPORT_CREATE, 'headers': REPORT_HEADERS, 'rows': [], 'x_name': REPORT_NAME_X, 'y_name': REPORT_NAME_Y, 'default_x': REPORT_HEADERS[REPORT_DEFAULT_X], 'default_y': REPORT_HEADERS[REPORT_DEFAULT_Y],
                       'x_unit': REPORT_UNIT_X, 'y_unit': REPORT_UNIT_Y, 'to_group': REPORT_TO_GROUP, 'report_skip_for_stk': REPORT_SKIP_FOR_STK, 'report_window_title': REPORT_WINDOW_TITLE, 'report_name': REPORT_NAME}
        self.subprog_cursor = {'type': CURSOR_TYPE, 'changing': CURSOR_CHANGING, 'limit': CURSOR_LIMIT, 'clear_on_start': CURSOR_CLEAR_ON_START, 'cursor_required': CURSOR_REQUIRED, 'cursor_req_text':CURSOR_REQ_TEXT,
                               'cursor_outside_x':CURSOR_OUTSIDE_X, 'cursor_outside_y':CURSOR_OUTSIDE_Y, 'cursor_outside_text':CURSOR_OUTSIDE_TEXT}
        self.use_second = USE_SECOND                                                                #|
        self.stack_sep = STACK_SEP
        Methods.__init__(self, app_weak=self.__app, which=which, commandline=commandline, close_subprogs=CLOSE_SUBPROGS)
        self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)


    # PRE-DEFINED FUNCTIONS TO EXECUTE AT DIFFERENT STAGES OF SUBPROG METHODS
    # Unused definitions can be deleted

    def graph_action(self, variable=None, value=None):
        ''' Do something when cursor action on is triggered. '''

    def after_data_changed(self, variable, value):
        ''' This method is called after data changing by clicking in the Main GUI. '''

    def after_calculations(self):
        ''' This method is called after single calculations
            and just before showing the report. '''

    def after_result_show_on_graph(self):
        ''' This method is called immediately when results
            for graph are ready but grapher canva has not been refreshed yet. '''

    def after_ok_clicked(self):
        ''' This method is called when all functions are
            finished after clicking 'Calculate' button. '''

    def after_process_group_clicked(self):
        ''' This method is called when all functions are
             finished after clicking 'Process group' button. '''

    def after_graph_plot(self):
        ''' This method is called when the main application refreshes Graph canva content.
            For example, after changing First data, the graph is reploted and then
            this function is run.
            DO NOT USE FUNCTIONS USING GRAPHER METHODS HERE!'''

    def finish_action(self, by_method):
        ''' This method is called when all calculations are finished and main window
            awaits for action. This is useful if you need to put annotations to the graph etc.
            by_method - the name of a method that triggered the action.
        '''


    # DEFINE YOUR CUSTOM METHODS FOR THIS ROUTINE
    # ----------------------------------------------
    def configure_window(self):
        # HERE DEFINE ADDITIONAL MAIN WINDOW CONFIGURATION
        #self.mainwindow =


        # Function definition:
        self.built_in_functions = BuiltInFunctions()
        self.function_definition =Function()

        # References to widgets
        self.graphFrame = self.builder.get_object('graphFrame', self.master)
        self.categoryFrame = self.builder.get_object('categoryFrame', self.master)
        self.functionFrame = self.builder.get_object('functionFrame', self.master)
        self.widget_equation = self.builder.get_object('widget_equation', self.master)

        # Create CTkListbox for Categories and Functions
        self.list_category = self.custom_widget(CTkListbox(master = self.categoryFrame, command = self.category_selected))
        self.list_category.grid(row = 1, column = 0, sticky="nsew")
        self.list_function = self.custom_widget(CTkListbox(master=self.functionFrame, command = self.function_selected))
        self.list_function.grid(row=1, column=0, sticky="nsew")

        self.widget_name = self.builder.get_object('widget_name', self.master)
        self.widget_parameters = self.builder.get_object('widget_parameters', self.master)
        self.widget_indep_var = self.builder.get_object('widget_indep_var', self.master)
        self.widget_function_edit = self.builder.get_object('widget_function_edit', self.master)

        self.button_validate = self.builder.get_object('button_validate', self.master)

        #
        # TAB: FIT
        #
        self.widget_function_to_fit = self.builder.get_object('widget_function_to_fit', self.master)

        # Table Frames
        self.tableFrames = {'parameter': self.builder.get_object('tableFrame_Parameter', self.master),
                            'value': self.builder.get_object('tableFrame_Value', self.master),
                            'const': self.builder.get_object('tableFrame_Const', self.master),
                            'min': self.builder.get_object('tableFrame_Min', self.master),
                            'max': self.builder.get_object('tableFrame_Max', self.master),
                            'non-negative': self.builder.get_object('tableFrame_Nonnegative', self.master),
                            }
        self.table_widgets = {'parameter':[],
                              'value': [],
                              'const': [],
                              'min':[],
                              'max': [],
                              'non-negative': []
                              }

        # Populate lists
        self.populate_category_and_functions()

        # Create Graph
        self.plt = plt
        self.graphFrame = self.builder.get_object("graphFrame", self.mainwindow)
        self.fig = Figure(figsize=(8,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.graphFrame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.draw()

    #
    # CATEGORY AND FUNCTIONS WIDGETS
    #
    def populate_category_and_functions(self):
        ''' Create list of function categories and the categories '''
        self.list_category.insert(0, 'User defined')
        self.list_category.insert(1, 'Built-in functions')

    def category_selected(self, category):
        ''' Create list of functions when category is selected '''
        if category == "Built-in functions":
            lsf = self.built_in_functions.get_list()
            i = 0
            for name in lsf:
                self.list_function.insert(i, name)
                i+= 1
        elif category == "User defined":
            print('Category selected: User defined')

    # Handle selected from list
    def function_selected(self, value):
        ''' If you select a function from the list this is executed'''
        category = self.list_category.get()
        if category == 'Built-in functions':
            functions_container = self.built_in_functions
        elif category == 'User defined':
            functions_container = "User defined"

        self.function_definition = copy.deepcopy(functions_container.get_by_name(value))
        if not self.function_definition:
            return

        # (1) Print Equation text in "Equation" textbox and Function to fit
        self.widget_equation.configure(state='normal')
        self.widget_equation.delete("0.0", "end")
        self.widget_equation.insert("0.0", self.function_definition.equation_text)
        self.widget_equation.configure(state="disabled")
            # Display function that will be fitted
        self.widget_function_to_fit.configure(state='normal')
        self.widget_function_to_fit.delete("0.0", "end")
        function = str(f'f({self.function_definition.variable})={self.function_definition.equation_text}')
        self.widget_function_to_fit.insert("0.0", function)
        self.widget_function_to_fit.configure(state='disabled')

        # (2) Print function name in "Name" Entrybox
        self.widget_name.delete(0, "end")
        self.widget_name.insert(0, value)

        # (3) Check if parameters are defined. If not find them in the equation
        if self.function_definition.parameters == []:
            self.function_definition.find_parameters()

        # (4) Display parameters in the "Parameters" Entrybox
        self.widget_parameters.delete(0, "end")
        param_text = ", ".join(self.function_definition.parameters)
        self.widget_parameters.insert(0, param_text)

        # (5) Display the Function in the "Function" CTkTextbox
        self.widget_function_edit.configure(state="normal")
        self.widget_function_edit.delete('0.0', "end")
        self.widget_function_edit.insert('0.0', self.function_definition.equation_text)

        if self.function_definition.validated:
            self.create_initial_guesses_list()


    def validate_function(self):
        ''' After clicking Validate button the equation is taken from the widgets
            and entered to the function and it is checked
        '''
        if not self.widget_name.get().strip():
            Error.show(title="Curve fit", info = 'Field Name should not be empty')
            return
        self.function_definition.name = self.widget_name.get()
        if not self.widget_function_edit.get("1.0", "end").strip():
            Error.show(title="Curve fit", info = 'Define a function to fit.')
            return

        self.function_definition.equation_text = self.widget_function_edit.get("1.0","end").strip()
        self.function_definition.variable = self.widget_indep_var.get().strip()
        self.function_definition.prepare_equation()
        self.function_definition.find_parameters()
        self.function_definition.sort_parameters()

        # Detect parameters automatically
        self.widget_parameters.delete(0, "end")
        param_text = ", ".join(self.function_definition.parameters)
        self.widget_parameters.insert(0, param_text)

        # Create the table for initail guesses
        self.create_initial_guesses_list()

        # Display function that will be fitted
        self.widget_function_to_fit.configure(state = 'normal')
        self.widget_function_to_fit.delete("0.0", "end")
        function = str(f'f({self.function_definition.variable})={self.function_definition.equation_text}' )
        self.widget_function_to_fit.insert("0.0",  function)
        self.widget_function_to_fit.configure(state='disabled')

    def create_initial_guesses_list(self):
        ''' Create table for initial guesses and displays it in the Tab
        '''

        # FRAME PARAMETERS
        if self.table_widgets['parameter']:
            for widget in self.tableFrames['parameter'].winfo_children():
                widget.destroy()
        self.table_widgets['parameter'].clear()
        # Create entries
        for i, param in enumerate(self.function_definition.parameters):
            entry = ctk.CTkEntry(master = self.tableFrames['parameter'], justify = 'right', width = 40, height = 30)
            entry.insert(0, param)
            entry.grid(row=i, column=0, padx=2, pady=2, sticky="")
            entry.configure(state='disabled')
            self.table_widgets['parameter'].append(entry)


        # FRAME VALUES
        try:
            for widget in self.tableFrames['value'].winfo_children():
                widget.destroy()
        except:
            pass
        self.table_widgets['value'].clear()

        # Create entries
        for i, param in enumerate(self.function_definition.parameters):
            entry = CTkSpinbox(master = self.tableFrames['value'],
                               width = 200,
                               height = 34,
                               command = lambda p=param: self.table_changed(widget = 'value', parameter = p))
            value = self.function_definition.initial_values.get(param, 1)
            entry.set(value)
            entry.grid(row=i, column=0, padx=2, pady=0, sticky="we")
            self.table_widgets['value'].append(entry)


        # FRAME CONSTANT
        try:
            for widget in self.tableFrames['const'].winfo_children():
                widget.destroy()
        except:
            pass
        self.table_widgets['const'].clear()
        # Create entries
        for i, param in enumerate(self.function_definition.parameters):
            entry = ctk.CTkCheckBox(master=self.tableFrames['const'],
                                    width=40,
                                    height=34,
                                    text="",
                                    command = lambda p=param: self.table_changed(widget = 'const', parameter = p))
            value = self.function_definition.fit_parameters.get(param, False)
            if value:
                entry.select()
            else:
                entry.deselect()
            entry.grid(row=i, column=0, padx=2, pady=0, sticky="we")
            self.table_widgets['const'].append(entry)

        # FRAME MINIMUM/MAXIMUM
        try:
            for widget in self.tableFrames['min'].winfo_children():
                widget.destroy()
        except:
            pass
        self.table_widgets['min'].clear()
        for widget in self.tableFrames['max'].winfo_children():
            widget.destroy()
        # Create entries
        for i, param in enumerate(self.function_definition.parameters):
            entry_min = ctk.CTkEntry(master=self.tableFrames['min'],
                               width=100,
                               height=30,
                                     )#command = lambda p=param: self.table_changed(widget = 'min', parameter = p))
            entry_max = ctk.CTkEntry(master=self.tableFrames['max'],
                                     width=100,
                                     height=30,
                                     )#command = lambda p=param: self.table_changed(widget = 'max', parameter = p))
            value_min = self.function_definition.minimum.get(param, float("-inf"))
            entry_min.delete(0, "end")
            entry_min.insert(0, value_min)
            entry_min.grid(row=i, column=0, padx=2, pady=2, sticky="we")
            self.table_widgets['min'].append(entry_min)

            value_max = self.function_definition.minimum.get(param, float("inf"))
            entry_max.delete(0, "end")
            entry_max.insert(0, value_max)
            entry_max.grid(row=i, column=0, padx=2, pady=2, sticky="we")
            self.table_widgets['max'].append(entry_max)

        # FRAME NON-NEGATIVE VALUES
        try:
            for widget in self.tableFrames['non-negative'].winfo_children():
                widget.destroy()
        except:
            pass
        self.table_widgets['non-negative'].clear()
        # Create entries
        for i, param in enumerate(self.function_definition.parameters):
            entry = ctk.CTkCheckBox(master=self.tableFrames['non-negative'],
                    width = 80,
                    height = 34,
                    text = "",
                    command = lambda p =param: self.table_changed(widget='non-negative', parameter=p))
            value = self.function_definition.fit_parameters.get(param, False)
            if value:
                entry.select()
            else:
                entry.deselect()
            entry.grid(row=i, column=0, padx=2, pady=0, sticky="we")
            self.table_widgets['non-negative'].append(entry)

    def table_changed(self, widget, parameter):
        print('widget:',widget)
        print('parameter:',parameter)

    def calculate_stack(self, commandline = False):
        ''' If STACK_SEP is False it means that data in stack should
            not be treated as separate data but are calculated as whole

            DO NOT USE FUNCTION REQUIRED GUI UPDATE HERE
            '''

        # AVAILABLE DATA. REMOVE UNNECESSARY
        # EACH X,Y,Z IS NP.ARRAY
        # X, Z is 1D, Y is 2D
        # -----------------------------------------
        sft = +self.regions['orig_in_odd_idx']
        x1 = self.data_for_calculations[0]['x']
        y1 = self.data_for_calculations[0]['y']
        z1 = self.data_for_calculations[0]['z']
        name1 = self.data_for_calculations[0]['name']
        stk_value1 = self.data_for_calculations[0]['stk_value']
        complex1 = self.data_for_calculations[0]['complex']
        type1 = self.data_for_calculations[0]['type']
        origin1 = self.data_for_calculations[0]['origin']
        comment1 = self.data_for_calculations[0]['comment']
        parameters1 = self.data_for_calculations[0]['parameters']
        if self.use_second:
            x2 = self.data_for_calculations[1]['x']
            y2 = self.data_for_calculations[1]['y']
            z2 = self.data_for_calculations[1]['z']
            name2 = self.data_for_calculations[1]['name']
            stk_value2 = self.data_for_calculations[1]['stk_value']
            complex2 = self.data_for_calculations[1]['complex']
            type2 = self.data_for_calculations[1]['type']
            origin2 = self.data_for_calculations[1]['origin']
            comment2 = self.data_for_calculations[1]['comment']
            parameters2 = self.data_for_calculations[1]['parameters']
        # ------------------------------------------

    def calculate(self, commandline = False):
        ''' The algorithm for calculations on single x,y,z data.

        Usage:
            x1, y1, z1: contain the prepared x, y, z data for calculations
            x2, y2, z2: contain the reference data to use for example to subtract from data1
        After calculation put calculated data to:
            x1, y1 and z1 etc.
            result: the value of resulted calculations

            DO NOT USE FUNCTION REQUIRED GUI UPDATE HERE
        '''

        # AVAILABLE DATA. REMOVE UNNECESSARY
        # EACH X,Y,Z IS NP.ARRAY OF ONE DIMENSION
        # -----------------------------------------
        sft = +self.regions['orig_in_odd_idx']
        x1 = self.data_for_calculations[0]['x']
        y1 = self.data_for_calculations[0]['y']
        z1 = self.data_for_calculations[0]['z']
        name1 = self.data_for_calculations[0]['name']
        stk_value1 = self.data_for_calculations[0]['stk_value']
        complex1 = self.data_for_calculations[0]['complex']
        type1 = self.data_for_calculations[0]['type']
        origin1 = self.data_for_calculations[0]['origin']
        comment1 = self.data_for_calculations[0]['comment']
        parameters1 = self.data_for_calculations[0]['parameters']
        if self.use_second:
            x2 = self.data_for_calculations[1+sft]['x']
            y2 = self.data_for_calculations[1+sft]['y']
            z2 = self.data_for_calculations[1]+sft['z']
            name2 = self.data_for_calculations[1+sft]['name']
            stk_value2 = self.data_for_calculations[1+sft]['stk_value']
            complex2 = self.data_for_calculations[1+sft]['complex']
            type2 = self.data_for_calculations[1+sft]['type']
            origin2 = self.data_for_calculations[1+sft]['origin']
            comment2 = self.data_for_calculations[1+sft]['comment']
            parameters2 = self.data_for_calculations[1+sft]['parameters']
        cursor_positions = self.grapher.cursor_annotations
        # ------------------------------------------


        # Add to additional plots
        #self.clear_additional_plots()
        #self.add_to_additional_plots(x = x1_orig, y = poly_curve, clear=True)

        # Send calculated values to result (if needed). This will be sent to command line
        result = None # <--- HERE IS THE RESULT TO SEND TO COMMAND LINE

        # Create summary row to add to the report. The values must match the column names in REPORT_HEADERS
        row_to_report = None

        return row_to_report

    def save_settings(self):
        ''' Stores required values to self.eleana.subprog_storage
            This is stored in memory only, not in disk
            define each list element as:
            {'key_for_storage' : function_for_getting_value()}
        '''
        return  [
            {},
                ]

    def restore_settings(self):
        pass

if __name__ == "__main__":
    tester = TemplateClass()
    pass

