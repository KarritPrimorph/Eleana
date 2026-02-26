from assets.Dropfiles import FileDropWindow
from assets.Error import Error
from assets.Callbacks import main_menubar_callbacks
from modules.CTkMessagebox import CTkMessagebox
from subprogs.table.table import CreateFromTable
from subprogs.select_data.select_items import SelectItems
from subprogs.select_data.select_data import SelectData
from tkinter import filedialog

from pathlib import Path
import pandas
import csv

class MenuFileMixin:
    def load_project(self, event=None, recent=None, filename = None):

        ''' Load project '''

        if filename:
            recent = filename
        if recent is not None and filename is None:
            try:
                recent = self.eleana.paths['last_projects'][recent]
            except IndexError:
                Error.show(title = 'Error', info = "The project could not be found on list.")
        project = self.load.load_project(recent)
        self.main_menubar.create_showplots_menu()
        if not project:
            return
        self.eleana.create_missing_id()
        self.update.dataset_list()
        self.update.groups()
        self.update.all_lists()
        path_to_file = Path(self.eleana.paths['last_projects'][0])
        name = path_to_file.name
        name = name.replace('.ele', '')
        self.mainwindow.title(name + ' - Eleana')
        self.eleana.paths['last_project_dir'] = str(Path(path_to_file).parent)
        self.main_menubar.last_projects_menu()
        self.main_menubar.create_showplots_menu()

        # Set Selections according eleana.selections
        self.gui_to_selections()

        # Add custom annotations to graph
        if self.eleana.settings.grapher['custom_annotations']:
            try:
                cursor_mode = self.eleana.settings.grapher['custom_annotations'][0]['mode']
            except KeyError:
                cursor_mode = 'Free select'
            self.sel_graph_cursor(value=cursor_mode, clear_annotations=False)
            self.grapher.updateAnnotationList()
            self.sel_cursor_mode.set(cursor_mode)



    def load_recent(self, selected_value_text):

        """ Recent project """

        index = selected_value_text.split('. ')
        index = int(index[0])
        index = index - 1
        recent = self.eleana.paths['last_projects'][index]
        self.load_project(recent=recent)
        self.eleana.paths['last_project_dir'] = Path(recent).parent
        self.grapher.plot_graph()


    def save_as(self, filename = None):
        ''' Save as '''
        file_saved = self.eleana.save_project(filename)
        if not file_saved:
            return
        else:
            # Perform update to place the item into menu
            self.main_menubar.last_projects_menu()
            self.mainwindow.title(Path(file_saved).name[:-9] + ' - Eleana')

    def save_current(self, event=None):

        ''' Save '''

        win_title = self.mainwindow.title()
        if win_title == 'new project - Eleana':
            self.save_as(filename = None)
        else:
            file = win_title[:-9].strip()
            file = file
            if '.ele' not in file:
                file = file + '.ele'
            filename = Path(self.eleana.paths['last_project_dir'], file)
            self.save_as(filename)







    ''' 
        >>>>> ---------------------------------------------------------------
        >>>>>  IMPORT
        >>>>> ---------------------------------------------------------------
    '''

    def import_elexsys(self, filename = None):

        ''' Bruker Elexsys '''

        try:
            self.load.loadElexsys(filename = filename)
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            last_in_list = self.sel_first._values
            self.first_selected(last_in_list[-1])
        except Exception as e:
            Error.show(title = "Error loading Elexsys file.", info = e)


    def import_EMX(self, filename = None):

        ''' Bruker EMX '''

        try:
            self.load.loadEMX(filename = filename)
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading EMX file.", info=e)

    def import_adani_dat(self):

        ''' Adani Dat'''

        try:
            self.load.loadAdaniDat()
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading Adani dat file.", info=e)


    def import_magnettech1(self, filename = None):

        ''' Magnetech 1'''

        try:
            self.load.loadMagnettech(mscope = 1, filename = filename)
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading Magnettech file.", info=e)


    def import_magnettech2(self):

        ''' Magnetech 2 '''

        try:
            self.load.loadMagnettech(mscope = 2)
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading Magnettech file.", info=e)


    def import_biokine(self, filename = None, skip_messeges = False):

        ''' Biokine'''

        self.mainwindow.config(cursor = "watch")
        try:
            self.load.loadbiokine(filename = filename, skip_messeges = skip_messeges)
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            last_in_list = self.sel_first._values
            self.first_selected(last_in_list[-1])
            self.mainwindow.config(cursor="arrow")
        except Exception as e:
            self.mainwindow.config(cursor="arrow")
            Error.show(title="Error loading BioKine file.", info=e)


    def import_shimadzu_spc(self, filename = None):

        ''' Shimadzu '''

        try:
            self.load.loadShimadzuSPC(filenames = [filename])
            self.update.dataset_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading Shimadzu spc file.", info=e)


    def import_ascii(self, clipboard=None, filename = None, auto = False):

        ''' ASCII '''

        try:
            self.load.loadAscii(master = self.mainwindow, clipboard = clipboard, filename = filename, auto = auto)
            self.update.dataset_list()
            self.update.group_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading Ascii file.", info=e)

    def import_excel(self, filename = None):

        ''' Excel'''

        try:
            x = [['', ''], ['', '']]
            headers = ['A', 'B']
            empty = pandas.DataFrame(x, columns=headers)
            table = CreateFromTable(eleana=self.eleana, master=self.mainwindow, df=empty, loadOnStart='excel', excelfile = filename)
            response = table.get()
            self.update.dataset_list()
            self.update.group_list()
            self.update.all_lists()
            self.eleana.save_paths()
            self.first_selected(self.sel_first._values[-1])
        except Exception as e:
            Error.show(title="Error loading Excel file.", info=e)

    def import_more_formats(self, filename = None, type = None):

        ''' More formats '''

        if type is None:
            items = ['1. Flasher UJ (*.ele)',
                     #'2. Low-temperature UV spectrophotometer UJ',
                     #'3. SR curve (Pulse Spectrometer UJ)',
                     #'4. Low-temperature UV spectrophotometer UJ',
                     ]
            dialog = SelectItems(master = self.mainwindow,
                                 title = "Select appropriate file format",
                                 items = items, multiple_selections=False )
            response = dialog.get()
            response = response.split('.')[0]
        if response == '1':
            type = 'flasher'
        else:
            Error.show(master = self.mainwindow, info = 'Not implemented yet')
            return

        self.load.loadOther(filename=filename, type = type)
        self.update.dataset_list()
        self.update.all_lists()
        self.eleana.save_paths()
        last_in_list = self.sel_first._values
        self.first_selected(last_in_list[-1])


    def drag_and_drop_files(self):

        ''' Drag and Drop '''

        files = FileDropWindow(master = self.mainwindow, callbacks = main_menubar_callbacks(self))

    def export_first(self):

        ''' Export: Export First '''

        self.export.csv('first')

    def export_group(self):

        ''' Export: Export Group to folder'''

        self.export.group_csv(self.eleana.selections['group'])

    def export_spreadsheet(self, group = True, clipboard = False):

        ''' Export: Export Spreadsheet to folder
                  : Export Selected to Spreadsheet'''

        if group:
            current_group = self.sel_group.get()
            if current_group == 'All':
                indexes_to_export = list(range(len(self.eleana.dataset)))
            else:
                indexes_to_export = self.eleana.assignmentToGroups.get(current_group)
        else:
            av_data = self.sel_first._values
            av_data.pop(0)
            # Open dialog if index_to_delete was not set
            select_data = SelectData(master=self.mainwindow, title='Select data',
                                     group=self.eleana.selections['group'],
                                     items=av_data)
            response = select_data.get()
            if response == None:
                return
            indexes_to_export = self.get_indexes_by_name(response)

        if not indexes_to_export:
            return

        full_table = []
        for index in indexes_to_export:
            data = self.eleana.dataset[index]
            col_x = None
            col_y = None
            col_z = None
            is_2D = False
            # Single spectrum
            if data.type == 'single 2D' and not data.complex:
                col_x = [data.name + ' [X]'] + data.x.tolist()
                col_y = [data.name + ' [Y]'] + data.y.tolist()
            elif data.type == 'single 2D' and data.complex:
                col_x = [data.name + ' [X]'] + list(data.x)
                col_rey = [data.name + ' [Re Y]'] + data.y.real.tolist()
                col_imy = [data.name + ' [Im Y]'] + data.y.imag.tolist()
                col_y = [col_rey, col_imy]
                is_2D = True
            elif data.type == 'stack 2D' and not data.complex:
                col_x = [data.name + ' [X]'] + list(data.x)
                col_y = []
                i = 0
                for stk_name in data.stk_names:
                    col_y_single = [data.name + ':' + stk_name + ' [Y]'] + data.y[i].tolist()
                    col_y.append(col_y_single)
                    i += 1

                col_z = [data.name + ' [Z]'] + data.z.tolist()
                col_y.append(col_z)
                is_2D = True
            elif data.type == 'stack 2D' and data.complex:
                col_x = [data.name + ' [X]'] + list(data.x)
                col_y = []
                i = 0
                for stk_name in data.stk_names:
                    col_y_single_re = [data.name + ':' + stk_name + ' [Re Y]'] + data.y[i].real.tolist()
                    col_y_single_im = [data.name + ':' + stk_name + ' [Im Y]'] + data.y[i].imag.tolist()
                    col_y.append(col_y_single_re)
                    col_y.append(col_y_single_im)
                    i += 1
                col_z = [data.name + ' [Z]'] + data.z.tolist()
                col_y.append(col_z)
                is_2D = True

            else:
                Error.show(title = 'Export spreadsheet CVS', info = 'Data not supported yet.')
                return
            # Add columns
            if col_x:
                full_table.append(col_x)
            if col_y:
                if is_2D:
                    full_table.extend(col_y)
                else:
                    full_table.append(col_y)

            max_len = max(len(r) for r in full_table)
            filled_rows = [r + [""] * (max_len - len(r)) for r in full_table]
            transposed = list(map(list, zip(*filled_rows)))

        if clipboard:
            text_output = "\n".join("\t".join(str(item) for item in row) for row in transposed)
            self.mainwindow.clipboard_clear()
            self.mainwindow.clipboard_append(text_output)
            self.mainwindow.update()
        else:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save spreadsheet CSV"
            )

            if filename:  # If canceled
                try:
                    with open(filename, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerows(transposed)
                        self.eleana.paths['last_export_dir'] = filename
                        self.eleana.save_paths()
                except Exception as e:
                    Error.show(title='Export Spreadsheet', info = 'Error while saving csv speadsheet.', details = e)

    def close_application(self, event=None):

        ''' Quit '''

        quit_dialog = CTkMessagebox(master=self.mainwindow, title="Quit",
                                    message="Do you want to close the program?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            # # Save current settings:
            self.eleana.save_paths()
            self.eleana.save_settings()
            # self.mainwindow.iconify()
            # Close all static_plot windows from self.eleana.active_static_windows
            if self.eleana.storage.static_plots:
                for window_nr in self.eleana.storage.static_plots:
                    close_cmd = "self.grapher.static_plot_" + str(window_nr) + ".cancel()"
                    try:
                        exec(close_cmd)
                    except:
                        print("Error: " + close_cmd)
            self.mainwindow.destroy()
            if self.root is not None:
                self.root.destroy()
