import json
from pathlib import Path
import tkinter as tk
import customtkinter as ctk
from json import loads, dumps

class Init():
    def main_window(self, app, eleana):
        '''This method sets properties of the main window'''

        width = app.mainwindow.winfo_screenwidth()  # Get screen width
        height = app.mainwindow.winfo_screenheight()  # Get screen height
        app.mainwindow.geometry(str(width) + 'x' + str(height) + "+0+0")  # Set geometry to max


        # Add icon to the top window bar form pixmaps folder
        top_window_icon = Path(eleana.paths['pixmaps'], "eleana_top_window.png")
        main_icon = tk.PhotoImage(file=top_window_icon)
        app.mainwindow.iconphoto(True, main_icon)
        app.mainwindow.title('Eleana')
        # Set color motive for GUI
        ctk.set_default_color_theme("dark-blue")

        # ---------------------- Set default values in GUI -------
        app.sel_group.configure(values=['All'])
        app.sel_group.set('All')
        app.sel_first.configure(values=['None'])
        app.sel_first.set('None')
        app.sel_second.configure(values=['None'])
        app.sel_second.set('None')
        app.sel_result.configure(values=['None', 'yes'])
        app.sel_result.set('None')

        app.mainwindow.protocol('WM_DELETE_WINDOW', app.close_application)

    def folders(self, eleana):
        '''This method creates standard Eleana folder in user directory.
            If the folder does not exist it will be created.'''

        home_dir = eleana.paths['home_dir']
        eleana_user_dir = Path(home_dir, '.EleanaPy' )
        if not eleana_user_dir.exists():
            try:
                eleana_user_dir.mkdir()
            except:
                return {"Error": True, 'desc': f"Cannot create working Eleana folder in your home directory."}

        print('Plik initialization.py - def folders')
        exit()

        try:
            with open(path_to_file, "w") as file:
                file.write(content)
        except:
            return {"Error": False, 'desc': ""}
