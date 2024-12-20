#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
import numpy as np

# General setting of the application. Here is an example
# File/Path/Class settings
SUBPROG_FOLDER = 'distance_read'        # <--- SUBFOLDER IN SUBPROGS CONTAINING THIS FILE
GUI_FILE = 'DistanceReadui.py'          # <--- PYTHON FILE GENERATED BY PYGUBU-DESIGNER CONTAINING GUI
GUI_CLASS = 'DistanceReadUI'            # <--- CLASS NAME IN GUI_FILE THAT BUILDS THE WINDOW

# Window settings
TITLE = 'Calculate XY Distance'         # <--- TITLE OF THE WINDOW
ON_TOP = True                           # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
DATA_LABEL = 'data_label'               # <--- ID OF THE LABEL WIDGET WHERE NAME OF CURRENTLY SELECTED DATA WILL APPEAR.
                                        #      THE LABEL WIDGET OF THE SAME ID NAME MUST EXIST IN THE GUI. IF NOT USED SET THIS TO NONE
NAME_SUFFIX = ''                        # <--- DEFINES THE SUFFIX THAT WILL BE ADDED TO NAME OF PROCESSED DATA
AUTO_CALCULATE = True                   # <--- DEFINES IF CALCULATION IS AUTOMATICALLY PERFORMED UPON DATA CHANGE IN GUI
# Data settings
#REGIONS_FROM = 'scale'                  # <--- DEFINES IF DATA WILL BE EXTRACTED:
REGIONS_FROM = 'selection'             # 'none' - DO NOT EXTRACT
                                        # 'scale' - EXTRACT DATA BETWEEN X MIN X MAX
                                        # 'sel' - EXTRACT DATA FROM SELECTED RANGE

USE_SECOND = False                      # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE FOR CALCULATIONS
STACK_SEP = True                        # <--- IF TRUE THEN EACH DATA IN A STACK WILL BE CALCULATED SEPARATELY
                                        #      WHEN FALSE THEN YOU MUST CREATE A METHOD THAT CALCS OF THE WHOLE STACK

# Report settings
REPORT_CREATE = True                    # <--- IF TRUE THEN REPORT WILL BE CREATED AFTER CALCULATIONS
REPORT_HEADERS = ['Nr', 'Name', 'X1', 'X2', 'dX', 'Y1', 'Y2', 'dY'] # <--- Define names of columns in the Report
REPORT_DEFAULT_X = 0                    # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT X IN THE REPORT
REPORT_DEFAULT_Y = 7                    # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT Y IN THE REPORT
REPORT_NAME_X =  'Data Number'          # <--- NAME OF X AXIS IN THE REPORT
REPORT_NAME_Y =  'dY Value'             # <--- NAME OF Y AXIS IN THE REPORT
REPORT_UNIT_X = ''                      # <--- NAME OF X UNIT IN THE CREATED REPORT
REPORT_UNIT_Y = ''                      # <--- NAME OF Y UNIT IN THE CREATED REPORT
REPORT_TO_GROUP = 'RESULT:distance'     # <--- DEFAULT GROUP NAME TO WHICH REPORT WILL BE ADDED

# Cursors on graph
CURSOR_CHANGING = True                  # <--- IF TRUE THEN CURSOR SELECTION IN MAIN GUI WILL BE DISABLED
CURSOR_TYPE = 'Crosshair'               # <--- USE CURSORS: 'None', 'Continuous read XY', 'Selection of points with labels'
                                        #       'Selection of points', 'Numbered selections', 'Free select', 'Crosshair', 'Range select'
CURSOR_LIMIT = 2                        # <--- SET THE MAXIMUM NUMBER OF CURSORS THAT CAN BE SELECTED. FOR NO LIMIT SET 0
# ----------------------------------------------------------------------------------------------------
#   -- Here starts obligatory part of the application                                               #|
#   -- In general it should not be modified                                                         #|
#                                                                                                   #|
cmd_to_import = GUI_FILE[:-3] + ' import ' + GUI_CLASS + ' as WindowGUI'                            #|
if __name__ == "__main__":                                                                          #|
    cmd_to_import = 'from ' + cmd_to_import                                                         #|
else:                                                                                               #|
    cmd_to_import = 'from ' + SUBPROG_FOLDER + '.' + cmd_to_import                                  #|
exec(cmd_to_import)                                                                                 #|
from assets.Error import Error                                                                      #|
from assets.SubprogMethods2 import SubMethods_02                                                    #|
class DistanceRead(SubMethods_02, WindowGUI):                                                       #|
    ''' THIS IS STANDARD CONSTRUCTOR THAT SHOULD NOT BE MODIFIED '''                                #|
    def __init__(self, app=None, which='first', commandline=False):                                 #|
        if app and not commandline:                                                                  #|
            # Initialize window if app is defined and not commandline                               #|
            WindowGUI.__init__(self, app.mainwindow)                                                #|
        # Create settings for the subprog                                                           #|
        self.subwindow_settings = {'title':TITLE, 'on_top':ON_TOP,'data_label':DATA_LABEL,
                                   'name_suffix':NAME_SUFFIX, 'auto_calculate':AUTO_CALCULATE
                                   }                                                                #|
        self.regions = {'from':REGIONS_FROM}                                                        #|
        self.report = {'nr':1,                                                                      #|
                       'create': REPORT_CREATE,                                                     #|
                       'headers':REPORT_HEADERS,                                                    #|
                       'rows':[],                                                                   #|
                       'x_name':REPORT_NAME_X,                                                      #|
                       'y_name':REPORT_NAME_Y,                                                      #|
                       'default_x':REPORT_HEADERS[REPORT_DEFAULT_X],                                #|
                       'default_y':REPORT_HEADERS[REPORT_DEFAULT_Y],                                #|
                       'x_unit':REPORT_UNIT_X,                                                      #|
                       'y_unit':REPORT_UNIT_Y,                                                      #|
                       'to_group':REPORT_TO_GROUP                                                   #|
                       }                                                                            #|
        self.subprog_cursor = {'type':CURSOR_TYPE, 'changing':CURSOR_CHANGING, 'limit':CURSOR_LIMIT,#|
                           'x':[], 'y':[], 'z':[] }                                                 #|
        # Use second data                                                                           #|
        self.use_second = USE_SECOND
        # Treat each data in stack separately
        self.stack_sep = STACK_SEP                                                                  #|
        SubMethods_02.__init__(self, app=app, which=which, commandline=commandline)                                                                       #|
                                                                                                    #|
    # STANDARD METHODS FOR BUTTON EVENTS ON CLICK                                                   #|
    def ok_clicked(self):                                                                           #|
        ''' [-OK-] button                                                                           #|
            This is standard function in SubprogMethods '''                                         #|
        status = self.get_data()
        if status:
            self.perform_single_calculations()                                                      #|
            #self.update_after_calc()
                                                                                                    #|
    def process_group_clicked(self):                                                                #|
        ''' [-Process Group-] button                                                                #|
            This is standard function in SubprogMethods '''                                         #|
        self.perform_group_calculations()                                                           #|
                                                                                           #|
    def show_report_clicked(self):                                                                  #|
        ''' [-Show Report-] button                                                                  #|
            This is standard function in SubprogMethods '''                                         #|
        self.show_report()                                                                          #|
                                                                                                    #|
    def clear_report_clicked(self):                                                                 #|
        ''' [-Clear Report-] button                                                                 #|
            This is standard function in SubprogMethods '''                                         #|
        self.clear_report()                                                                         #|
                                                                                                    #|
    #                                                                                               #|
    # Here ends the obligatory part of the application                                              #|
    # Your code starts from here                                                                    #|
    #-------------------------------------------------------------------------------------------------


    def configure_window(self):
        # Define additional window configuration if needed
        #self.mainwindow =

        # Define references to your additional widgets and configuration
        self.x1_entry = self.builder.get_object('x1_entry', self.mainwindow)
        self.x2_entry = self.builder.get_object('x2_entry', self.mainwindow)
        self.dx_entry = self.builder.get_object('dx_entry', self.mainwindow)
        self.y1_entry = self.builder.get_object('y1_entry', self.mainwindow)
        self.y2_entry = self.builder.get_object('y2_entry', self.mainwindow)
        self.dy_entry = self.builder.get_object('dy_entry', self.mainwindow)
        self.check_keep_track = self.builder.get_object('check_track_minmax', self.mainwindow)
        self.keep_track = False

        # Define list of CTkEntries that should be validated for floats
        self.set_validation_for_ctkentries([
                self.x1_entry,
                self.x2_entry,
                self.y1_entry,
                self.y2_entry
                ])

        # Set disabled field
        self.dx_entry.configure(state='disabled')
        self.dy_entry.configure(state='disabled')

    def graph_action(self, variable=None, value=None):
        ''' Do something when cursor action on graph was done '''


    def find_minmax_clicked(self):
        x_data, y_data = self.grapher.get_graph_line(index = 0)
        index_min_y = np.argmin(y_data)
        min_x = x_data[index_min_y]
        index_max_y = np.argmax(y_data)
        max_x = x_data[index_max_y]
        self.grapher.clear_all_annotations()
        self.place_annotation(x = min_x)
        self.place_annotation(x = max_x)

    def track_minmax_clicked(self):
        self.keep_track = self.check_keep_track.get()
        if self.keep_track:
            self.find_minmax_clicked()

    def calculate_stack(self, x, y, name, z = None, stk_index = None):
        ''' If STACK_SEP is False it means that data in stack should
            not be treated as separate data but are calculated as whole
            If not used, leave it as it is
        '''
        info__ = 'There is no method defined for Stack calculations'
        if self.app is not None:
            Error.show(info=info__)
        else:
            print(info__)

    # Here starts your main algorithm that performs a calculations
    # On a single data
    def calculate(self, name=None, stk_index=None, y=None, x=None, z=None, region=None,
                  # DEFINE YOUR OWN ARGUMENTS HERE
                  track=None
                  ):
        #----------------------------------------------------------------------------------------------------------|
        # Leave the lines below unchanged                                                                        # |
        self.eleana.cmd_error = ''                                                                               # |
        x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal = self.prep_calc_data(x, y, z, name, region) # |
        if self.eleana.cmd_error:                                                                                # |
            return                                                                                               # |
        #-----------------------------------------------------------------------------------------------------------


        ''' 
        Your code starts here 
        ---------------------
        Use:
            x_data:  contains original data for x axis as np.array
            y_data:  contains original data for y axis (can be complex) as np.array
            z_data:  contains original data for z axis if there is a stack as np.array
        After calculation put calculated data to:
            y_cal:  the results of calculations on y_data as np.array
            x_cal:  the result of calculations on x_data as np.array
            z_cal:  the result of calculations on z_data as np.array
            result: the value of resulted calculations 
        '''

        if track or self.keep_track:
            # Auto detect maximum and minimum using numpy
            min_y = np.min(y_data)
            index_min_y = np.argmin(y_data)
            min_x = x_data[index_min_y]
            max_y = np.max(y_data)
            index_max_y = np.argmax(y_data)
            max_x = x_data[index_max_y]
            minimum = [min_x, min_y]
            maximum = [max_x, max_y]
        else:
            # Do not detect where maximum and minimum are
            try:
                p1 = self.grapher.cursor_annotations[0]
                p2 = self.grapher.cursor_annotations[1]
            except:
                return
            minimum = ([p1['point'][0], p1['point'][1]])
            maximum = ([p2['point'][0], p2['point'][1]])

        # Get x1 and x2
        x1 = minimum[0]
        x2 = maximum[0]

        # Find index in x_data which is closest to x1 or x2
        index_x1 = np.abs(x_data - x1).argmin()
        index_x2 = np.abs(x_data - x2).argmin()

        # Get data from x_data and y_data using the indexes for x1 and x2, respectively
        x1 = x_data[index_x1]
        x2 = x_data[index_x2]
        y1 = y_data[index_x1]
        y2 = y_data[index_x2]

        # Calculate differences
        dx = x2 - x1
        dy = y2 - y1

        # Send calculated values to result (if needed). This will be sent to command line
        result = [dx, dy] # <--- HERE IS THE RESULT TO SEND TO COMMAND LINE

        # Create summary row to add to the report. The values must match the column names in REPORT_HEADERS
        to_result_row = [self.consecutive_number, name, x1, x2, dx, y1, y2, dy]

        # Update Window Widgets
        #----------------------------------------------------------------------------------------------
        if not self.batch:                                                                           #|
        # ---------------------------------------------------------------------------------------------
            # Put values to the entries
            self.set_entry_value(self.x1_entry, x1)
            self.set_entry_value(self.x2_entry, x2)
            self.set_entry_value(self.y1_entry, y1)
            self.set_entry_value(self.y2_entry, y2)
            self.set_entry_value(self.dx_entry, dx)
            self.set_entry_value(self.dy_entry, dy)
            pass
        #---------------------------------------------------------------------------------------------
        # Construct line for the report if needed                                                   #|
        # This is obligatory part of the function                                                   #|
        if not self.batch:                                                                          #|
            # Update results of the calculations                                                    #|
            self.update_result_data(y=y_cal, x=x_cal, z=z_cal)                                      #|
            return to_result_row # <--- Return this if report is going to be                        #|
        else:                                                                                       #|
            return result # <-- Return this to command line                                         #|
        #---------------------------------------------------------------------------------------------

# THIS IS FOR TESTING COMMAND LINE
if __name__ == "__main__":
    ir = IntegrateRegion()
    x_data = np.array([1,2,3,4,5,6])
    y_data = np.array([4,3,5,3,5,6])
    double = False
    integral = ir.calculate(x=x_data, y=y_data, double = double)
    print(integral)

