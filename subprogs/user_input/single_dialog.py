#!/usr/bin/python3
import pathlib
from faulthandler import enable

import pygubu
import tkinter as tk
import re
from modules.CTkMessagebox import CTkMessagebox
from tkinter import ttk
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "single_dialog.ui"

class SingleDialog:
    def __init__(self, master=None, title='', label='', text='', enable_dot=False, disable_edit = False):
        self.enable_dot = enable_dot
        self.master = master
        # Pygubu part below:
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.disable_edit = disable_edit
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)
        # -------------------

        # Set modal
        try:
            self.mainwindow.grab_set()  # Set as modal
        except:
            pass
        self.mainwindow.attributes('-topmost', True)  # Always on top
        self.mainwindow.title(title)

        # Set label
        self.label = builder.get_object("label1", self.mainwindow)
        self.label.configure(text=label)

        # Set textbox
        self.textbox = builder.get_object("textbox", self.mainwindow)
        self.textbox.delete(0, tk.END)
        self.textbox.insert(0, text)
        self.textbox.focus_set()
        if self.disable_edit:
            self.make_readonly(self.textbox)

        # Set return
        self.response = None

        # Bindings
        self.mainwindow.bind('<Escape>', self.cancel)
        self.mainwindow.bind('<Return>', self.ok)

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''

    def make_readonly(self, textbox):

        def block_event(event):
            if (event.state & 0x4) and event.keysym.lower() == "c":
                return
            return "break"

        for seq in [
            "<Key>", "<BackSpace>", "<Delete>", "<Return>",
            "<Control-v>", "<Control-x>"]:
            self.textbox.bind(seq, block_event)

    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()

    def cancel(self, event = None):
        self.mainwindow.destroy()
    ''' END OF MANDATORY METHODS '''

    def ok(self, event = None):
        pattern = r"\.\s"
        text = self.textbox.get()
        if re.search(pattern, text) and not self.enable_dot:
            CTkMessagebox(title="Name check", message="The name cannot contain a dot followed by a space.")
            return
        self.response = text
        self.mainwindow.destroy()

if __name__ == "__main__":
    app = SingleDialogApp()
    app.run()
