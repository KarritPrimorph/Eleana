#!/usr/bin/python3
if __name__ == "__main__":
    from IntegrateRegionui import IntegrateRegionUI as WindowGUI
    import numpy as np
else:

    from integrate_region.IntegrateRegionui import IntegrateRegionUI as WindowGUI

from scipy.integrate import cumulative_trapezoid, trapezoid
from assets.SubprogMethods import SubMethods

'''
##################################
#     SUBPROG SETTINGS           #
##################################'''

# General
TITLE = 'Integrate region'  # <--- TITLE OF THE WINDOW
WORK_ON_START = False  # <--- IF TRUE THEN CALCULATION ON CURRENT SELECTED DATA IS PERFORMED UPON OPENING OF THE SUBPROG
ON_TOP = True  # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
REGIONS = True  # <--- IF TRUE THE DATA WILL BE EXTRACTED FROM REGIONS IN SELF.ELEANA.COLOR_SPAN
TWO_SETS = False  # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE FOR CALCULATIONS
STACK_SEP = True  # <--- IF TRUE THEN EACH DATA IN A STACK WILL BE CALCULATED SEPARATELY
#      WHEN FALSE THEN YOU MUST CREATE A METHOD THAT CALCS OF THE WHOLE STACK
DATA_LABEL_WIDGET = 'data_label'  # <--- ID OF THE LABEL WIDGET WHERE NAME OF CURRENTLY SELECTED DATA WILL APPEAR.
#      THE LABEL WIDGET OF THE SAME ID NAME MUST EXIST IN THE GUI. IF NOT USED SET THIS TO NONE
# Report settings
REPORT = True  # <--- IF TRUE THEN REPORT WILL BE CREATED AFTER CALCULATIONS
REPORT_HEADERS = ['Nr', 'Name', 'Parameter values \n for consecutive data in stack',
                  'Integral Value']  # <--- Define names of columns in the Report
REPORT_DEFAULT_X = 0  # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT X IN THE REPORT
REPORT_DEFAULT_Y = 3  # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT Y IN THE REPORT
REPORT_NAME_X = 'Data Number'  # <--- NAME OF X AXIS IN THE REPORT
REPORT_NAME_Y = 'Integral Value'  # <--- NAME OF Y AXIS IN THE REPORT
REPORT_UNIT_X = ''  # <--- NAME OF X UNIT IN THE CREATED REPORT
REPORT_UNIT_Y = ''  # <--- NAME OF Y UNIT IN THE CREATED REPORT

'''
##################################
#    END OF SUBPROG SETTINGS     #
##################################'''


class IntegrateRegion(SubMethods, WindowGUI):
    ''' THIS IS STANDARD CONSTRUCTOR THAT SHOULD NOT BE MODIFIED '''

    def __init__(self, app=None, which='first', batch_mode=False):
        if app and not batch_mode:
            # Initialize window if app is defined and not batch mode is set
            WindowGUI.__init__(self, app.mainwindow)
        self.get_from_region = REGIONS
        self.create_report = REPORT
        self.collected_reports = {'headers': REPORT_HEADERS, 'rows': [], 'x_name': REPORT_NAME_X,
                                  'y_name': REPORT_NAME_Y, 'default_x': REPORT_HEADERS[REPORT_DEFAULT_X],
                                  'default_y': REPORT_HEADERS[REPORT_DEFAULT_Y], 'x_unit': REPORT_UNIT_X,
                                  'y_unit': REPORT_UNIT_Y}
        # Use second data
        self.use_second = TWO_SETS
        SubMethods.__init__(self, app=app, which=which, use_second=self.use_second, stack_sep=STACK_SEP,
                            data_label=DATA_LABEL_WIDGET, work_on_start=WORK_ON_START, window_title=TITLE,
                            on_top=ON_TOP)

    def configure_window(self):
        # HERE DEFINE ADDITIONAL WINDOW CONFIGURATION
        # self.mainwindow =

        # HERE DEFINE YOUR REFERENCES TO WIDGETS
        self.check_double_integration = self.builder.get_object('check_double', self.mainwindow)

        # AND CONFIGURE CUSTOM WIDGETS
        self.field_value = self.builder.get_object('field_value', self.mainwindow)

    # STANDARD METHODS FOR BUTTON EVENTS ON CLICK
    def ok_clicked(self):
        ''' [-OK-] button
            This is standard function in SubprogMethods '''
        self.perform_single_calculations()

    def process_group_clicked(self):
        ''' [-Process Group-] button
            This is standard function in SubprogMethods '''
        self.perform_group_calculations()

    def show_report_clicked(self):
        ''' [-Show Report-] button
            This is standard function in SubprogMethods '''
        self.show_report()

    def clear_report_clicked(self):
        ''' [-Show Report-] button
            This is standard function in SubprogMethods '''
        self.clear_report()

        # DEFINE YOUR CUSTOM METHODS FOR THIS ROUTINE

    # ----------------------------------------------
    def set_double_integration(self):
        self.perform_single_calculations()  # <-- This is custom button

    def calculate_stack(self, x, y, name, z=None, stk_index=None):
        ''' If STAC_SEP is False it means that data in stack should
            not be treated as separate data but are calculcated as whole
            '''
        print('Stack calculations')
        print('Not used for intergation')

    def calculate(self, dataset=None, name=None, stk_index=None, y=None, x=None, z=None, cmd=False,
                  double=None
                  ):
        ''' Your algorithm to perform calculations on single x,y,z data. Do not modify line below '''
        x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal = self.prep_calc_data(dataset, x, y, z, name)

        ''' HERE STARTS YOUR CODE 
        --------------------------
        Use:
            x_data:  contains original data for x axis
            y_data:  contains original data for y axis (can be complex)
            z_data:  contains original data for z axis if there is a stack
        After calculation put calculated data:
            y_cal:  the results of calculations on y_data
            x_cal:  the result of calculations on x_data
            z_cal:  the result of calculations on z_data
            result: the value of resulted calculations 
        '''

        if double is None:
            double = self.check_double_integration.get()
        y_cal = cumulative_trapezoid(y_data, x_data, initial=0)
        integral = trapezoid(y_data, x_data)
        if double:
            y_cal2 = cumulative_trapezoid(y_cal, x_data, initial=0)
            integral = trapezoid(y_cal, x_data)
            y_cal = y_cal2

        result = integral  # <--- Put the result value to 'result' variable

        # ------- AFTER CALCULATIONS ---------
        # Update Window Widgets
        if not self.batch:
            self.field_value.delete(0, 'end')
            self.field_value.insert(0, str(result))  # <--- Put 'result' to the widget
        # Construct line for the report
        if not self.batch:
            to_result_row = [self.consecutive_number, name_cal, z_cal,
                             result]  # <--- Create report row according to REPORT_HEADERS
            # Update results of the calculations
            self.update_result_data(y=y_cal, x=x_cal)
            return to_result_row
        else:
            return result  # <-- Return this if executed command line


# THIS IS FOR TESTING COMMAND LINE
if __name__ == "__main__":
    ir = IntegrateRegion()
    x_data = np.array([1, 2, 3, 4, 5, 6])
    y_data = np.array([4, 3, 5, 3, 5, 6])
    double = False
    integral = ir.calculate(x=x_data, y=y_data, double=double)
    print(integral)

