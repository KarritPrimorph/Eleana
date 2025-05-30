from assets.LoadSave import Load, Save
from pathlib import Path
import tkinter as tk
import customtkinter as ctk
import pickle
from subprogs.preferences.preferences import PreferencesApp

class Init:
    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.app = self.main_menu.app
        self.eleana = self.app.eleana
        self.grapher = self.app.grapher
     
    def main_window(self):
        '''This method sets properties of the main window'''

        width = self.app.mainwindow.winfo_screenwidth()  # Get screen width
        height = self.app.mainwindow.winfo_screenheight()  # Get screen height
        self.app.mainwindow.geometry('800x800')
        self.app.mainwindow.geometry(str(width) + 'x' + str(height) + "+0+0")  # Set geometry to max

        # Add icon to the top window bar form pixmaps folder
        top_window_icon = Path(self.eleana.paths['pixmaps'], "eleana_top_window.png")
        main_icon = tk.PhotoImage(file=top_window_icon)
        self.app.mainwindow.iconphoto(True, main_icon)
        self.app.mainwindow.title('new project - Eleana')

        # Set color modes for GUI
        settings = Load.load_preferences(self.eleana)
        if not settings:
            self.app.color_theme = 'dark-blue'
            self.app.gui_appearence = 'dark'
            preferences = PreferencesApp(self.app)
            preferences.ok()
            Save.save_preferences(self.eleana, self.app, self.grapher)
        else:
            mode = settings.gui_appearence
            ctk.set_appearance_mode(mode)
            self.app.gui_appearence = mode
            color = settings.color_theme
            ctk.set_default_color_theme(color)
            self.app.color_theme = color

        # ---------------------- Set default values in GUI -------
        self.app.sel_group.configure(values=['All'])
        self.app.sel_group.set('All')
        self.app.sel_first.configure(values=['None'])
        self.app.sel_first.set('None')
        self.app.sel_second.configure(values=['None'])
        self.app.sel_second.set('None')
        self.app.sel_result.configure(values=['None', 'yes'])
        self.app.sel_result.set('None')
        self.app.mainwindow.protocol('WM_DELETE_WINDOW', self.app.close_application)


    def folders(self):
        '''This method creates standard Eleana folder in user directory.
            If the folder does not exist it will be created.'''

        home_dir = self.eleana.paths['home_dir']
        eleana_user_dir = Path(home_dir, '.EleanaPy' )
        if not eleana_user_dir.exists():
            try:
                eleana_user_dir.mkdir()
            except:
                return {"Error": True, 'desc': f"Cannot create working Eleana folder in your home directory."}

    def paths(self, update):
        try:
            filename = Path(self.eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')
            # Read paths.pic
            file_to_read = open(filename, "rb")
            paths = pickle.load(file_to_read)
            self.eleana.paths['last_import_dir'] = paths['last_import_dir']
            self.eleana.paths['last_project_dir'] = paths['last_project_dir']
            self.eleana.paths['last_projects'] = paths['last_projects']
            self.eleana.paths['last_export_dir'] = paths['last_export']
            file_to_read.close()
            # Create last project list in the main menu
            last_projects = self.eleana.paths['last_projects']
            last_projects = [element for i, element in enumerate(last_projects) if i <= 10]
            # Write the list to eleana.paths
            self.eleana.paths['last_projects'] = last_projects
            # Perform update to place the item into menu
            update.last_projects_menu()
        except:
            pass

    def eleana_variables(self):
        self.eleana.selections = {'group': 'All',
                      'first': -1, 'second': -1, 'result': -1,
                      'f_cpl': 're', 's_cpl': 're', 'r_cpl': 're',
                      'f_stk': 0, 's_stk': 0, 'r_stk': 0,
                      'f_dsp': True, 's_dsp': True, 'r_dsp': True
                      }
        self.eleana.notes = {"content": "",
                 "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [],
                          "largest size": [],
                          "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],
                          "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}
        self.eleana.dataset = []
        self.eleana.results_dataset = []
        self.eleana.assignmentToGroups = self.assignmentToGroups = {'<group-list/>': ['All']}
        self.eleana.groupsHierarchy = {}

    def graph(self):
        # Bind keyboard Navbar events to function
        self.grapher.canvas.mpl_connect("key_press_event", lambda event: self.grapher.on_key_press_on_graph(event))

        # Set variables for Graph buttons
        self.app.firstComplex.set(value="re")
        self.app.secondComplex.set(value="re")
        self.app.resultComplex.set(value="re")
        self.app.check_first_show.select()
        self.app.check_second_show.select()
        self.app.check_result_show.select()
        self.app.check_autoscale_x.select()
        self.app.check_autoscale_y.select()
        self.app.check_log_x.deselect()
        self.app.check_log_y.deselect()
        self.app.check_indexed_x.deselect()